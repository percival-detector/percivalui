"""
Created on 22nd July 2016

:author: Alan Greer
"""
import logging
import time
from odin.adapters.adapter import ApiAdapter, ApiAdapterResponse, request_types, response_types
from percival.detector.detector import PercivalDetector
from concurrent import futures
from tornado.ioloop import IOLoop
from tornado.concurrent import run_on_executor


class PercivalAdapter(ApiAdapter):
    """
    PercivalAdapter class

    This class provides the adapter interface between the ODIN server and the PERCIVAL detector system,
    transforming the REST-like API HTTP verbs into the appropriate EXCALIBUR detector control actions
    """

    # Thread executor used for background tasks
    executor = futures.ThreadPoolExecutor(max_workers=1)

    def __init__(self, **kwargs):
        """
        Initialise the PercivalAdapter object

        :param kwargs:
        """
        super(PercivalAdapter, self).__init__(**kwargs)

        self._detector = PercivalDetector(False,False)
        self._detector.set_global_monitoring(True)
        self._auto_read = True
        self.status_update(0.1)

    @run_on_executor
    def status_update(self, task_interval):
        if self._detector:
            if self._auto_read:
                self._detector.update_status()
        time.sleep(task_interval)
        IOLoop.instance().add_callback(self.status_update, task_interval)

    @request_types('application/json')
    @response_types('application/json', default='application/json')
    def get(self, path, request):

        """
        Implementation of the HTTP GET verb for ExcaliburAdapter

        :param path: URI path of the GET request
        :param request: Tornado HTTP request object
        :return: ApiAdapterResponse object to be returned to the client
        """

        logging.debug("%s", request)

        # Split the path by /
        options = path.split("/")
        # Pass the option to the detector to obtain the parameter
        response = self._detector.read(options[0])
        # If the driver status has been requested append the auto_read status
        if options[0] in "driver":
            response["auto_read"] = self._auto_read

        status_code = 200
        logging.debug(response)

        return ApiAdapterResponse(response, status_code=status_code)

    @request_types('application/json')
    @response_types('application/json', default='application/json')
    def put(self, path, request):  # pylint: disable=W0613

        """
        Implementation of the HTTP PUT verb for ExcaliburAdapter

        :param path: URI path of the PUT request
        :param request: Tornado HTTP request object
        :return: ApiAdapterResponse object to be returned to the client
        """

        logging.debug("%s", request)

        # Split the path by /
        options = path.split("/")
        logging.debug("%s", options)
        # Database reconnection
        if options[0] in "influxdb" and options[1] in "connect":
            self._detector.setup_db()
        elif options[0] in "auto_read":
            # Global monitoring has either been requested to start or stop
            if options[1] in "start":
                self._auto_read = True
            else:
                self._auto_read = False
        else:
            # Pass the option to the detector to obtain the parameter
            self._detector.set_value(options[0], int(options[1]))

        response = {'response': '{}: PUT on path {}'.format(self.name, path)}
        status_code = 200

        logging.debug(response)

        return ApiAdapterResponse(response, status_code=status_code)

    @request_types('application/json')
    @response_types('application/json', default='application/json')
    def delete(self, path, request):  # pylint: disable=W0613
        """
        Implementation of the HTTP DELETE verb for ExcaliburAdapter

        :param path: URI path of the DELETE request
        :param request: Tornado HTTP request object
        :return: ApiAdapterResponse object to be returned to the client
        """
        response = {'response': '{}: DELETE on path {}'.format(self.name, path)}
        status_code = 200

        logging.debug(response)

        return ApiAdapterResponse(response, status_code=status_code)
