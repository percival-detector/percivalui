""" This is an adaptation of the live_view_adapter in odin_data.
It overrides render_image with percival-specific code, and offers
three images on the urls coarse, fine and gain. Also they are shrunk.
There is some tidying yet to be done: removing old code and
colouring of text. There are some changes to the LiveViewAdapter
in odin-data pending and we are going to wait for them.
"""

import logging
import re
from collections import OrderedDict
import numpy as np
import cv2
import time;
from tornado.escape import json_decode

from odin_data.ipc_tornado_channel import IpcTornadoChannel
from odin_data.ipc_channel import IpcChannelException
from odin.adapters.adapter import ApiAdapter, ApiAdapterResponse, response_types
from odin.adapters.parameter_tree import ParameterTree, ParameterTreeError
from odin.util import convert_unicode_to_string

ENDPOINTS_CONFIG_NAME = 'live_view_endpoints'
COLORMAP_CONFIG_NAME = 'default_colormap'

DEFAULT_ENDPOINT = 'tcp://127.0.0.1:5020'
DEFAULT_COLORMAP = "Jet"


class LiveViewAdapter(ApiAdapter):
    """Live view adapter class.

    This class implements the live view adapter for odin-control.
    """

    def __init__(self, **kwargs):
        """
        Initialise the adapter.

        Creates a LiveViewer Object that handles the major logic of the adapter.

        :param kwargs: Key Word arguments given from the configuration file,
        which is copied into the options dictionary.
        """
        logging.debug("Live View Adapter init called")
        super(LiveViewAdapter, self).__init__(**kwargs)

        if self.options.get(ENDPOINTS_CONFIG_NAME, False):
            endpoints = [x.strip() for x in self.options.get(ENDPOINTS_CONFIG_NAME, "").split(',')]
        else:
            logging.debug("Setting default endpoint of '%s'", DEFAULT_ENDPOINT)
            endpoints = [DEFAULT_ENDPOINT]

        if self.options.get(COLORMAP_CONFIG_NAME, False):
            default_colormap = self.options.get(COLORMAP_CONFIG_NAME, "")
        else:
            default_colormap = "Jet"

        self.live_viewer = LiveViewer(endpoints, default_colormap)

    @response_types('application/json', 'image/*', 'image/webp', 'text/plain', default='application/json')
    def get(self, path, request):
        """
        Handle a HTTP GET request from a client, passing this to the Live Viewer object.

        :param path: The path to the resource requested by the GET request
        :param request: Additional request parameters
        :return: The requested resource, or an error message and code if the request was invalid.
        """
        try:
            response, content_type, status = self.live_viewer.get(path, request)
        except ParameterTreeError as param_error:
            response = {'response': 'LiveViewAdapter GET error: {}'.format(param_error)}
            content_type = 'application/json'
            status = 400

        return ApiAdapterResponse(response, content_type=content_type, status_code=status)

    @response_types('application/json', default='application/json')
    def put(self, path, request):
        """
        Handle a HTTP PUT request from a client, passing it to the Live Viewer Object.

        :param path: path to the resource
        :param request: request object containing data to PUT to the resource
        :return: the requested resource after changing, or an error message and code if invalid
        """
        logging.debug("REQUEST: %s", request.body)
        try:
            data = json_decode(request.body)
            self.live_viewer.set(path, data)
            response, content_type, status = self.live_viewer.get(path)

        except ParameterTreeError as param_error:
            response = {'response': 'LiveViewAdapter PUT error: {}'.format(param_error)}
            content_type = 'application/json'
            status = 400

        return ApiAdapterResponse(response, content_type=content_type, status_code=status)

    def cleanup(self):
        """Clean up the adapter on shutdown. Calls the Live View object's cleanup method."""
        self.live_viewer.cleanup()

# the output from this function prob needs to be int to allow for scaling.
def splitGFC(pval):
    imgGn = pval >> 13;
    imgFn = (pval >> 5) & 0xff;
    imgCrs= pval & 0x1f;

 #   imgGn = imgGn.astype("uint8");
 #   imgFn = imgFn.astype("uint8");
 #   imgCrs = imgCrs.astype("uint8");

    return imgGn, imgFn, imgCrs;

class LiveViewer(object):
    """
    Live viewer main class.

    This class handles the major logic of the adapter, including generation of the images from data.
    """

    def __init__(self, endpoints, default_colormap):
        """
        Initialise the LiveViewer object.

        This method creates the IPC channel used to receive images from odin-data and
        assigns a callback method that is called when data arrives at the channel.
        It also initialises the Parameter tree used for HTTP GET and SET requests.
        :param endpoints: the endpoint address that the IPC channel subscribes to.
        """
        logging.debug("Initialising LiveViewer")

        self.img_data = np.zeros( (1400, 1400), dtype=np.uint16 );
        # we choose to drop 6/7 rows because a rowgroup is 7 rows.
        self.shrink_ratio = 7;
        self.clip_min = None
        self.clip_max = None
        self.header = {}
        self.endpoints = endpoints
        self.ipc_channels = []
        self.frame_num = -1;
        for endpoint in self.endpoints:
            endpoint = "tcp://" + endpoint;
            try:
                tmp_channel = SubSocket(self, endpoint)
                self.ipc_channels.append(tmp_channel)
                logging.info("Subscribed to endpoint: %s", tmp_channel.endpoint)
            except IpcChannelException as chan_error:
                logging.warning("Unable to subscribe to %s: %s", endpoint, chan_error)

        logging.debug("Connected to %d endpoints", len(self.ipc_channels))

        if not self.ipc_channels:
            logging.warning(
                "Warning: No subscriptions made. Check the configuration file for valid endpoints")

        # Define a list of available cv2 colormaps
        self.cv2_colormaps = {
            "Autumn": cv2.COLORMAP_AUTUMN,
            "Bone": cv2.COLORMAP_BONE,
            "Jet": cv2.COLORMAP_JET,
            "Winter": cv2.COLORMAP_WINTER,
            "Rainbow": cv2.COLORMAP_RAINBOW,
            "Ocean": cv2.COLORMAP_OCEAN,
            "Summer": cv2.COLORMAP_SUMMER,
            "Spring": cv2.COLORMAP_SPRING,
            "Cool": cv2.COLORMAP_COOL,
            "HSV": cv2.COLORMAP_HSV,
            "Pink": cv2.COLORMAP_PINK,
            "Hot": cv2.COLORMAP_HOT,
            "Parula": cv2.COLORMAP_PARULA
        }

        # Build a sorted list of colormap options mapping readable name to lowercase option
        self.colormap_options = OrderedDict()
        for colormap_name in sorted(self.cv2_colormaps.keys()):
            self.colormap_options[colormap_name.lower()] = colormap_name

        # Set the selected colormap to the default
        if default_colormap.lower() in self.colormap_options:
            self.selected_colormap = default_colormap.lower()
        else:
            self.selected_colormap = "jet"

        self.render_image()

        self.param_tree = ParameterTree({
            "name": "Live View Adapter",
            "endpoints": (self.get_channel_endpoints, None),
            "frame": (lambda: self.header, None),
            "colormap_options": self.colormap_options,
            "colormap_selected": (self.get_selected_colormap, self.set_selected_colormap),
            "data_min_max": (lambda: [int(self.img_data.min()), int(self.img_data.max())], None),
            "frame_counts": (self.get_channel_counts, self.set_channel_counts),
            "clip_range": (lambda: [self.clip_min, self.clip_max], self.set_clip)
        })

    def get(self, path, _request=None):
        """
        Handle a HTTP get request.

        Checks if the request is for the image or another resource, and responds accordingly.
        :param path: the URI path to the resource requested
        :param request: Additional request parameters.
        :return: the requested resource,or an error message and code, if the request is invalid.
        """
        path_elems = re.split('[/&?#]', path);

        if path_elems[0] == 'coarse':
            if self.img_crs:
                response = self.img_crs
                content_type = 'image/png'
                status = 200
            else:
                response = {"response": "LiveViewAdapter: No Image Available"}
                content_type = 'application/json'
                status = 400

        elif path_elems[0] == 'fine':
            response = self.img_fn
            content_type = 'image/png'
            status = 200
        elif path_elems[0] == 'gain':
            response = self.img_gn
            content_type = 'image/png'
            status = 200
        elif path_elems[0] == 'shrinkratio':
            response = str(self.shrink_ratio);
            content_type = 'text/plain'
            status = 200
        else:
            response = self.param_tree.get(path)
            content_type = 'application/json'
            status = 200

        return response, content_type, status

    def set(self, path, data):
        """
        Handle a HTTP PUT i.e. set request.

        :param path: the URI path to the resource
        :param data: the data to PUT to the resource
        """
        self.param_tree.set(path, data)

    def create_image_from_socket(self, msg):
        """
        Create an image from data received on the socket.

        This callback function is called when data is ready on the IPC channel. It creates
        the image data array from the raw data sent by the Odin Data Plugin, reshaping
        it to a multi dimensional array matching the image dimensions.
        :param msg: a multipart message containing the image header, and raw image data.
        """
        # Message should be a list from multi part message.
        # First part will be the json header from the live view, second part is the raw image data
        header = json_decode(msg[0])

        # json_decode returns dictionary encoded in unicode. Convert to normal strings if necessary.
        header = convert_unicode_to_string(header)
        logging.debug("Got image with header: %s", header)

        self.frame_num = header['frame_num'];
        # Extract the type of the image data from the header. If the type is float, coerce to
        # float32 since the native float in HDF5 is 32-bit vs 64-bit in python and numpy.
        dtype = header['dtype']
        if dtype == 'float':
            dtype = 'float32'

        # this line belongs in the FP plugins, but since there are 3 of them, we'll put it here temporarily
        dtype = "uint16";
        # create a np array of the image data, of type specified in the frame header
        img_data = np.fromstring(msg[1], dtype=np.dtype(dtype))

        self.img_data = img_data.reshape([int(header["shape"][0]), int(header["shape"][1])])
        self.header = header

        self.render_image();

    def render_image(self):
        # we choose to show row 1 and drop the others because in no-crosstalk mode of the detector, only
        # rows 1,3,5 are active.
        first_row_to_show = 1;
        img_shrunk = self.img_data[first_row_to_show::self.shrink_ratio,::self.shrink_ratio];
        img_gn, img_fn, img_crs = splitGFC(img_shrunk);

        max_gn = 3;
        max_fn = 255;
        max_crs = 31;

        img_gn = self.scale_array(img_gn, 0, max_gn);
        img_fn = self.scale_array(img_fn, 0, max_fn);
        img_crs = self.scale_array(img_crs, 0, max_crs);

        img_gn = self.add_key(img_gn, str(max_gn));
        img_fn = self.add_key(img_fn, str(max_fn));
        img_crs = self.add_key(img_crs, str(max_crs));

        # Scale to 0-255 for colormap
     #   img_scaled = self.scale_array(img_clipped, 0, 255).astype(dtype=np.uint8)

        # Apply colormap to create an ndarray of BGR.
        cv2_colormap = self.cv2_colormaps[self.colormap_options[self.selected_colormap]]
        gn_colormapped = cv2.applyColorMap(img_gn, cv2_colormap);
        crs_colormapped = cv2.applyColorMap(img_crs, cv2_colormap);
        fn_colormapped = cv2.applyColorMap(img_fn, cv2_colormap);

        font = cv2.FONT_HERSHEY_SIMPLEX;
        # this seems to be col, row, and row increases downwards
        # this is 20 pixels in from the bottom left corner
        org = (20, img_shrunk.shape[0]-20);
        fontScale = 2;
        tcolor = (100,200,100);
        thickness = 5;
        # this is a test to see if the data came from the Fp, or if it's our default pic.
        if -1==self.frame_num:
          cv2.putText(crs_colormapped, "None", org, font, 
                           fontScale, tcolor, thickness);
          cv2.putText(fn_colormapped, "None", org, font, 
                           fontScale, tcolor, thickness);
          cv2.putText(gn_colormapped, "None", org, font, 
                           fontScale, tcolor, thickness);


        fontScale = 0.5;
        thickness = 1;
        # this is in the key area, 15 pixels down from the top
        org = (img_shrunk.shape[1], 15);
     #   org= ();
        # %Y-%m-%d 
        strtime = time.strftime("%H:%M:%Shrs", time.localtime());
        cv2.putText(gn_colormapped, strtime, org, font, 
                         fontScale, tcolor, thickness);
        org = (img_shrunk.shape[1],35);
        if 0<=self.frame_num:
          strframe = "frame:{:04d}".format(self.frame_num % 10000);
          cv2.putText(gn_colormapped, strframe, org, font, 
                           fontScale, tcolor, thickness);

        # Most time consuming step, depending on image size and the type of image
        fn_encode = cv2.imencode('.png', fn_colormapped, params=[cv2.IMWRITE_PNG_COMPRESSION, 0])[1];
        gn_encode = cv2.imencode('.png', gn_colormapped, params=[cv2.IMWRITE_PNG_COMPRESSION, 0])[1];
        crs_encode = cv2.imencode('.png', crs_colormapped, params=[cv2.IMWRITE_PNG_COMPRESSION, 0])[1];

        self.img_fn = fn_encode.tostring();
        self.img_crs = crs_encode.tostring();
        self.img_gn = gn_encode.tostring();


    @staticmethod
    def scale_array(src, srcmin, srcmax):
        """
        This function maps the src array into the range 0,255 and type uint8.

        :param src: the source array to rescale
        :param srcmin: this value in the src image (and below) maps to zero in the output. Must be in 0,255
        :param srcmin: this value in the src image (and above) maps to 255 in the output. Must be in 0,255
        :return: an array of the same dimensions as the source, but with the data in the range 0,255.
        """
       # smin, smax = src.min(), src.max()

        ret = np.maximum(src, srcmin);        
        ret = ret - srcmin;

        # we expect ret.dtype == uint16 here.
        ret = (ret * 255) / (srcmax-srcmin);
        ret = np.minimum(ret, 255);

        return ret.astype("uint8");

    # Do I want to call this before or after the scaling? after.
    # pixelmax the value mapping to the top of the colorMap.
    # img_in the pixels in this image must be uint8s in the range 0,255
    @staticmethod
    def add_key(img_in, pixelmax = "high"):
      keywidth = 100;
      keymargintop = 50;
      keymarginbot = 10;
      keymarginleft = 10;
      keymarginright = 10;
      rows, cols = img_in.shape;
      key = np.ones( (rows, keywidth), dtype=np.uint8 ) * 50;

      for r in range(keymarginbot, rows-keymargintop):
        key[rows - r, keymarginleft : keywidth-60] = (r-keymarginbot)*255.0 / (rows-keymarginbot-keymargintop);

      font = cv2.FONT_HERSHEY_SIMPLEX;
      # this seems to be col, row
      org = (50, 25);
      fontScale = 0.7;
      tcolor = (100);
      thickness = 2;

      cv2.putText(key, str(pixelmax), (50,keymargintop+20), font, 
                       fontScale, tcolor, thickness)
      image = cv2.putText(key, "0", (50,rows-keymarginbot), font,
                       fontScale, tcolor, thickness, cv2.LINE_AA)

      image = np.hstack((img_in, key));

    #  img_color = cv2.applyColorMap(image, cv2.COLORMAP_JET);
      return image;

    def cleanup(self):
        """Close the IPC channels ready for shutdown."""
        for channel in self.ipc_channels:
            channel.cleanup()

    def get_selected_colormap(self):
        """
        Get the default colormap for the adapter.

        :return: the default colormap for the adapter
        """
        return self.selected_colormap

    def set_selected_colormap(self, colormap):
        """
        Set the selected colormap for the adapter.

        :param colormap: colormap to select
        """
        if colormap.lower() in self.colormap_options:
            self.selected_colormap = colormap.lower()

    def set_clip(self, clip_array):
        """
        Set the image clipping, i.e. max and min values to render.

        :param clip_array: array of min and max values to clip
        """
        if (clip_array[0] is None) or isinstance(clip_array[0], int):
            self.clip_min = clip_array[0]

        if (clip_array[1] is None) or isinstance(clip_array[1], int):
            self.clip_max = clip_array[1]

    def get_channel_endpoints(self):
        """
        Get the list of endpoints this adapter is subscribed to.

        :return: a list of endpoints
        """
        endpoints = []
        for channel in self.ipc_channels:
            endpoints.append(channel.endpoint)

        return endpoints

    def get_channel_counts(self):
        """
        Get a dict of the endpoints and the count of how many frames came from that endpoint.

        :return: A dict, with the endpoint as a key, and the number of images from that endpoint
        as the value
        """
        counts = {}
        for channel in self.ipc_channels:
            counts[channel.endpoint] = channel.frame_count

        return counts

    def set_channel_counts(self, data):
        """
        Set the channel frame counts.

        This method is used to reset the channel frame counts to known values.
        :param data: channel frame count data to set
        """
        data = self.convert_to_string(data)
        logging.debug("Data Type: %s", type(data).__name__)
        for channel in self.ipc_channels:
            if channel.endpoint in data:
                logging.debug("Endpoint %s in request", channel.endpoint)
                channel.frame_count = data[channel.endpoint]


class SubSocket(object):
    """
    Subscriber Socket class.

    This class implements an IPC channel subcriber socker and sets up a callback function
    for receiving data from that socket that counts how many images it receives during its lifetime.
    """

    def __init__(self, parent, endpoint):
        """
        Initialise IPC channel as a subscriber, and register the callback.

        :param parent: the class that created this object, a LiveViewer, given so that this object
        can reference the method in the parent
        :param endpoint: the URI address of the socket to subscribe to
        """
        self.parent = parent
        self.endpoint = endpoint
        self.frame_count = 0
        self.channel = IpcTornadoChannel(IpcTornadoChannel.CHANNEL_TYPE_SUB, endpoint=endpoint)
        self.channel.subscribe()
        self.channel.connect()
        # register the get_image method to be called when the ZMQ socket receives a message
        self.channel.register_callback(self.callback)

    def callback(self, msg):
        """
        Handle incoming data on the socket.

        This callback method is called whenever data arrives on the IPC channel socket.
        Increments the counter, then passes the message on to the image renderer of the parent.
        :param msg: the multipart message from the IPC channel
        """
        self.frame_count += 1
        self.parent.create_image_from_socket(msg)

    def cleanup(self):
        """Cleanup channel when the server is closed. Closes the IPC channel socket correctly."""
        self.channel.close()
