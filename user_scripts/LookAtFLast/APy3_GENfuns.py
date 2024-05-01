# -*- coding: utf-8 -*-
"""
general functions and fitting
(a half-decent language would have those functions already). Python is worth what it costs.
"""
#%% imports
#
import sys # command line argument, print w/o newline, version
import time # to have time
import numpy
from scipy import stats # linear regression
from scipy.optimize import curve_fit # non-linear fit
import math
import scipy
import matplotlib
import matplotlib.pyplot
matplotlib.pyplot.rcParams['image.cmap'] = 'jet'
import os # list files in a folder
import glob # to find last file
import re # to sort naturally
import h5py # deal with HDF5
import tkinter
#
import ast # execute command
import collections # len(collections.Counter(A).keys()) n of distinct
#
from mpl_toolkits.mplot3d import Axes3D
#
#
#
#%% constant
VERYBIGNUMBER= 1e18
NOlist= ["","none","None","NONE","no","No","NO"]
ALLlist= ["all","All","ALL",":","*","-1"]
INTERACTLVElist= ['i','I','interactive','Interactive','INTERACTIVE']
#
#%% things that should heve been in numpy
def numpy_NaNs(dims):
    """ like numpy.zeros, only filled with nans """
    out_NaNs= numpy.zeros((dims))*numpy.NaN
    return out_NaNs
def numpy_NaNs_like(otherArray):
    """ like numpy.zeros_like, only filled with nans """
    out_NaNs= numpy.zeros_like(otherArray)*numpy.NaN
    return out_NaNs
#
def count_distinct_elements(Ar):
    """ 
    returns the number of distinct elements in an array
    [5.5,  7.1, 7.1, 5.5, 2.0, 5.5]: 3 distinct elements 
    useful to count how nay steps in a X-list with several Ys for each step 
    """
    NdistinctElements= len(collections.Counter(Ar).keys()) 
    return NdistinctElements
#
def str2list(str_in):
    ''' string_of_a_list:'["a","b","c"]' => list:["a","b","c"] '''
    return ast.literal_eval(str_in)
# ---
#
#%% numeric formats
def convert_uint_2_bits_Ar(in_intAr,Nbits):
    ''' convert (numpyarray of uint => array of Nbits bits) for many bits in parallel '''
    inSize_T= in_intAr.shape
    in_intAr_flat=in_intAr.flatten()
    out_NbitAr= numpy.zeros((len(in_intAr_flat),Nbits), dtype=bool)
    for iBits in range(Nbits):
        out_NbitAr[:,iBits]= (in_intAr_flat>>iBits)&1
    out_NbitAr= out_NbitAr.reshape(inSize_T+(Nbits,))
    return out_NbitAr  
#
def convert_bits_2_int_Ar(bitarray):
    """ Convert (numpyarray of [... , ... , n_bits] => array of [... , ... ](int) """
    shape = bitarray.shape
    n_bits = shape[-1]
    out = numpy.zeros(shape[:-1], dtype=int)
    for ibit in range(n_bits):
        out = (out << 1) | bitarray[...,n_bits-ibit-1]
    return out
#
def convert_bits_2_uint8_Ar(bitarray):
    """ Convert (numpyarray of [... , ... , n_bits] => array of [... , ... ](int) """
    shape = bitarray.shape
    n_bits = shape[-1]
    out = numpy.zeros(shape[:-1], dtype='uint8')
    for ibit in range(n_bits):
        out = (out << 1) | bitarray[...,n_bits-ibit-1]
    return out
#
def convert_bits_2_uint16_Ar(bitarray):
    """ Convert (numpyarray of [... , ... , n_bits] => array of [... , ... ](int) """
    shape = bitarray.shape
    n_bits = shape[-1]
    out = numpy.zeros(shape[:-1], dtype='uint16')
    for ibit in range(n_bits):
        out = (out << 1) | bitarray[...,n_bits-ibit-1]
    return out
#
def convert_britishBits_Ar(BritishBitArray):
    " 0=>1 , 1=>0 "
    HumanReadableBitArray=1-BritishBitArray
    return HumanReadableBitArray
#
def convert_int_2_2xuint8(int2convert):
    ''' 259 => (1,3) '''
    out_uint8_MSB= int2convert//256
    out_uint8_LSB= int2convert%256
    return (out_uint8_MSB, out_uint8_LSB)
#
def convert_2xuint8_2_int(MSByte,LSByte):
    ''' 259 <= (1,3) '''
    out_int= (256*MSByte)+LSByte
    return (out_int)
#
def convert_int_2_4xuint8(int2convert):
    ''' 259 => (0,0,1,3) '''
    aux_int2convert=int2convert
    out_MSB= int2convert//(2**24)
    if aux_int2convert>=(2**24): aux_int2convert=aux_int2convert-(2**24)
    out_mid2SByte= int2convert//(2**16)
    if aux_int2convert>=(2**16): aux_int2convert=aux_int2convert-(2**16)
    out_mid1SByte= int2convert//(2**8)
    if aux_int2convert>=(2**8): aux_int2convert=aux_int2convert-(2**8)
    out_LSB= aux_int2convert
    return(out_MSB, out_mid2SByte, out_mid1SByte, out_LSB)
#
def convert_4xuint8_2_int(MSByte,mid2SByte,mid1SByte,LSByte):
    ''' 259 <= (0,0,1,3) '''
    out_int= ((2**24)*MSByte)+ ((2**16)*mid2SByte)+ ((2**8)*mid1SByte)+ LSByte
    return (out_int)
#
def convert_hex_byteSwap_Ar(data2convert_Ar):
    ''' interpret the ints in an array as 16 bits. byte-swap them: (byte0,byte1) => (byte1,byte0) '''
    aux_bitted= convert_uint_2_bits_Ar(data2convert_Ar,16) #.astype('uint8')
    aux_byteinverted= numpy.zeros_like(aux_bitted, dtype='uint8')
    #
    aux_byteinverted[...,0:8]= aux_bitted[...,8:16]
    aux_byteinverted[...,8:16]= aux_bitted[...,0:8]
    data_ByteSwapped_Ar=convert_bits_2_int_Ar(aux_byteinverted)
    return (data_ByteSwapped_Ar)

def convert_hex_byteSwap_2nd(data2convert_Ar):
    ''' interpret the ints in an array as 16 bits. byte-swap them: (byte0,byte1) => (byte1,byte0) '''
    by0= numpy.mod(data2convert_Ar, 2**8).astype('uint16')
    by1= data2convert_Ar//(2**8); by1=by1.astype('uint16')
    data_ByteSwapped_Ar= (by0 * (2**8)) + by1
    data_ByteSwapped_Ar= data_ByteSwapped_Ar.astype('uint16')
    return (data_ByteSwapped_Ar)
#
# ---
#
#%% print and getchar
def press_any_key():
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
#
def printcol(string,colour):
    ''' write in colour (red/green/orange/blue/purple) '''
    white  = '\033[0m'  # white (normal)
    if (colour=='black'): outColor  = '\033[30m' # black
    elif (colour=='red'): outColor= '\033[31m' # red
    elif (colour=='green'): outColor  = '\033[32m' # green
    elif (colour=='orange'): outColor  = '\033[33m' # orange
    elif (colour=='blue'): outColor  = '\033[34m' # blue
    elif (colour=='purple'): outColor  = '\033[35m' # purple
    else: outColor  = '\033[30m'
    print(outColor+string+white)
    sys.stdout.flush()
    
def printErr(string):
    printcol("ERROR: "+string,'red')
    sys.exit()
def printERR(string):
    printcol("ERROR: "+string,'red')
    sys.exit()
#
def dot():
    '''print a dot '''
    sys.stdout.write(".")
    sys.stdout.flush() # print it now

def dot_every10th(thisImg,NImg):
        if (thisImg+1)%10==0: dot()
        if (thisImg+1)%1000==0: printcol(" {0}".format(thisImg),'blue')
        if (thisImg+1)==NImg: printcol("",'blue')  
#
#%% yes, no, and general things
def isitYes(string):
    ''' recognize a yes '''
    YESarray=['y','Y','yes','YES','Yes','si','SI','Si','ja','JA','Ja','true','TRUE','True']  
    isitYes= False
    if string in YESarray:
        isitYes=True
    return(isitYes)
#
def isitNo(string):
    ''' recognize a no '''
    NOarray=['n','N','no','NO','No','over my dead body','forget about it','nope','nein','NEIN','Nein','false','FALSE','False']  
    isitNO= False
    if string in NOarray:
        isitNO=True
    return(isitNO)
#
def isitfloat(value):
    ''' recognize a float in a string (like string.isdigit() only for float) '''
    try:
      float(value)
      return True
    except ValueError:
      return False
#
def whatTimeIsIt():
    aux_timeId = time.strftime("%Y_%m_%d__%H:%M:%S")
    return(aux_timeId)
#
def notFound(thispath):
    ''' return True if the path (folder or file) is not valid '''
    isIsNotThere= os.path.exists(thispath)==False
    return(isIsNotThere)
#
def argmax_xD(array2scan):
    ''' coordinates of max for xD array'''
    coord_max= numpy.unravel_index(array2scan.argmax(), array2scan.shape)
    return coord_max

def argmin_xD(array2scan):
    ''' coordinates of min for xD array'''
    coord_max= numpy.unravel_index(array2scan.argmin(), array2scan.shape)
    return coord_max
#
#
#%% matlab-like function
def clean():
    ''' close all figures '''   
    matplotlib.pyplot.close('all')
#    
#def find_2D(Xin,Yin,conditionList):
#    ''' 
#    emulate matlab 'find' (as much as possible in the python nonsense)
#    returns arrays X[i],Y[i] only if conditions[i]==True
#    note that conditions is a list of booleans (created with a statement like "Xin>a_number")
#    '''
#    Xout=[]; Yout=[]
#    for i in range(len(Xin)):
#        if (conditionList[i]==True):
#            Xout+= [Xin[i]]
#            Yout+= [Yin[i]]
#    Xout= numpy.array(Xout)
#    Yout= numpy.array(Yout)
#    return (Xout, Yout)
#
def matlabLike_range(matlabstring):
    '''
    use the sensible matlab syntax to make incremental array, instead of the python nonsense
    'xx:yy'    means:    [xx,xx+1,xx+2,...,yy-1,yy] (numpy array)
    equivalent to numpy.arange(xx,yy+1)
    '''  
    from_str= matlabstring.partition(':')[0]
    to_str= matlabstring.partition(':')[-1]
    #
    out_python_range=numpy.array([]) # default
    if (from_str.isdigit())&(to_str.isdigit()):
        if (int(from_str)<=int(to_str)):
            from_int= int(from_str);  to_int= int(to_str); 
            out_python_range= numpy.arange(from_int, to_int+1)
        else: 
            print("UNABLE TO RECOGNIZE MATLAB-LIKE RANGE, WILL USE NONE []")            
    else:
        print("UNABLE TO RECOGNIZE MATLAB-LIKE RANGE, WILL USE NONE []") # yes, also this is needed
    return(out_python_range)
#
def matlabLike_range2(matlabstring,specList,specRange, verboseFlag):
    '''
    use the sensible matlab syntax to make incremental array, instead of the python nonsense
    'xx:yy'    means:    [xx,xx+1,xx+2,...,yy-1,yy] (numpy array)
    equivalent to numpy.arange(xx,yy+1)
    xx means [xx]
    specialList (['!','#','xxx', ...]) means specRange
    '''  
    out_python_range=numpy.array([]) # default
    #
    if matlabstring in specList: out_python_range= specRange
    elif matlabstring.isdigit(): out_python_range= numpy.arange(int(matlabstring),int(matlabstring)+1)
    else:
        from_str= matlabstring.partition(':')[0]
        to_str= matlabstring.partition(':')[-1]
        #  
        if (from_str.isdigit())&(to_str.isdigit()):
            if (int(from_str)<=int(to_str)):
                from_int= int(from_str);  to_int= int(to_str); 
                out_python_range= numpy.arange(from_int, to_int+1)
            elif verboseFlag: printcol("UNABLE TO RECOGNIZE MATLAB-LIKE RANGE, WILL USE NONE []",'orange')            
        elif verboseFlag: printcol("UNABLE TO RECOGNIZE MATLAB-LIKE RANGE, WILL USE NONE []",'orange') # yes, also this is needed
    return(out_python_range)
#
#%% sorting list in natural form
''' natural sorting of a list of strings with numbers ['a0','a1','a2',...,'a10','a11',...] '''
def atoi(text):
    return int(text) if text.isdigit() else text
#
def natural_keys(text):
    ''' thisIsaList.sort(key=natural_keys)'''
    return [atoi(c) for c in re.split('(\d+)', text)]
def sort_nicely(myList):
    ''' natural sorting of a list of strings with numbers ['a0','a1','a2',...,'a10','a11',...] '''
    myList.sort(key=natural_keys)
#
#
def avgY_of_sameX_1D(arrayX,arrayY):
    """ for each unique val of arrayX, avg the Ys that correspond to thet value => array_of_uniqueX,array_of_avgY, array_of_stdY """
    if arrayX.shape != arrayY.shape: printErr('avgY_of_sameX_1D(arrayX,arrayY): arrayX.shape {0} != arrayY.shape {1}'.format(arrayX.shape,arrayY.shape))
    array_uniqueX= numpy.unique(arrayX)
    array_avgY= numpy_NaNs_like(array_uniqueX)
    array_stdY= numpy_NaNs_like(array_uniqueX)
    for i_X,this_X in enumerate(array_uniqueX):
        aux_map= arrayX==this_X
        array_avgY[i_X]= numpy.nanmean(arrayY[aux_map])
        array_stdY[i_X]= numpy.nanstd(arrayY[aux_map])
        del aux_map
    return(array_uniqueX,array_avgY,array_stdY)
# ---
#
#%% indexing functions
#
# indices in the form (row, col) => pointTuple[Trow]= pointTuple[0]= row
#Trow=0
#Tcol=1
#
def indices_rectangle(Rows2look,Cols2look):
    ''' list of tuples covering the rectangle [Rows2look,Cols2look]'''
    indices=[]
    #
    for iRow in Rows2look:
        for iCol in Cols2look:
            indices += [(iRow,iCol)]
    return indices
#
#def my_indices_cuboid(Imgs2look,Rows2look,Cols2look):
#    indices=[]
#    #
#    for iImg in Imgs2look:    
#        for iRow in Rows2look:
#            for iCol in Cols2look:
#                indices += [(iImg,iRow,iCol)]
#    return indices
# 
#def my_indices_circle(centerT, radius, inROITArray): 
#    indices=[]
#    radius= radius+0.0
#    #
#    for thispointT in inROITArray:
#        thisDistance = (centerT[Trow] - thispointT[Trow])**2 +0.0
#        thisDistance += (centerT[Tcol] - thispointT[Tcol])**2 +0.0
#        thisDistance= numpy.sqrt(thisDistance)
#        if (thisDistance <= radius):
#           indices += [thispointT] 
#    return indices  
#   
#%% file functions
#
def read_csv(filenamepath):
    ''' read numerical data from csv '''
    my_data= numpy.genfromtxt(filenamepath, delimiter= ',')
    return my_data
# 
def write_csv(filenamepath, data):
    ''' write numerical data from csv '''
    numpy.savetxt(filenamepath, data, fmt='%f', delimiter=",")
#
def read_tst(filenamepath):
    ''' read text from tab-separated-texts file '''
    #my_data= numpy.genfromtxt(filenamepath, delimiter= '\t', dtype='string')
    my_data= numpy.genfromtxt(filenamepath, dtype=str)
    return my_data
#
def write_tst(filenamepath, data):
    ''' write text in tab-separated-texts file '''
    numpy.savetxt(filenamepath, data, delimiter= '\t', fmt='%s')
#
def read_bin_uint8(filenamepath):
    ''' read uint8 data from binary file '''
    with open(filenamepath) as thisfile:
        fileContent=numpy.fromfile(thisfile, dtype=numpy.uint8)
        thisfile.close()
    return fileContent
#
#def read_bin_uint8(filenamepath):
#    ''' read uint8 data from binary file '''
#    thisfile= open(filenamepath, 'r')
#    fileContent=numpy.fromfile(thisfile, dtype=numpy.uint8); 
#    thisfile.close()
#    return fileContent
#
def read_1xh5(filenamepath, path_2read):
    ''' read h5 file: data in path_2read '''
    my5hfile= h5py.File(filenamepath, 'r')
    myh5dataset=my5hfile[path_2read]
    my_data_2D= numpy.array(myh5dataset)
    my5hfile.close()
    return my_data_2D
#
def write_1xh5(filenamepath, data2write, path_2write):
    ''' write h5 file: data in path_2write '''
    my5hfile= h5py.File(filenamepath, 'w')
    my5hfile.create_dataset(path_2write, data=data2write) 
    my5hfile.close()
#
def size_1xh5(filenamepath, path_2read):
    ''' estimate shape of h5 file: data in path_2read '''
    my5hfile= h5py.File(filenamepath, 'r')
    myh5dataset=my5hfile[path_2read]
    out_shape= myh5dataset.shape
    my5hfile.close()
    return out_shape
#
def read_warn_1xh5(filenamepath, path_2read):
    if notFound(filenamepath): printErr("not found: "+filenamepath)
    dataout= read_1xh5(filenamepath, path_2read)
    return dataout
#
def read_2xh5(filenamepath, path1_2read, path2_2read):
    ''' read 2xXD h5 file (paths_2read: '/data','/reset' ) '''
    my5hfile= h5py.File(filenamepath, 'r')
    myh5dataset=my5hfile[path1_2read]
    my_data1= numpy.array(myh5dataset)
    myh5dataset=my5hfile[path2_2read]
    my_data2= numpy.array(myh5dataset)
    my5hfile.close()
    return (my_data1,my_data2)
#
def read_partial_2xh5(filenamepath, path1_2read, path2_2read, fromImg, toImg):
    ''' read 2xXD h5 file (paths_2read: '/data','/reset' ) '''
    my5hfile= h5py.File(filenamepath, 'r')
    myh5dataset=my5hfile[path1_2read]
    if myh5dataset.shape[0] <= toImg: my5hfile.close(); printErr('only {0} img in file (path1)'.format(myh5dataset.shape[0]))
    my_data1= numpy.array(myh5dataset[fromImg:toImg+1,...])
    myh5dataset=my5hfile[path2_2read]
    if myh5dataset.shape[0] <= toImg: my5hfile.close(); printErr('only {0} img in file (path2)'.format(myh5dataset.shape[0]))
    my_data2= numpy.array(myh5dataset[fromImg:toImg+1,...])
    my5hfile.close()
    return (my_data1,my_data2)
#
def write_2xh5(filenamepath, 
               data1_2write, path1_2write, 
               data2_2write, path2_2write):
    ''' write 2xXD h5 file (paths_2write: '/data','/reset' ) '''
    my5hfile= h5py.File(filenamepath, 'w')
    my5hfile.create_dataset(path1_2write, data=data1_2write) #
    my5hfile.create_dataset(path2_2write, data=data2_2write) #
    my5hfile.close()
#
def list_files(folderpath, expectedPrefix, expectedSuffix):
    ''' look for files in directory having the expected prefix and suffix ('*' to have any) '''
    anyfix='*'
    allFileNameList=os.listdir(folderpath)
    dataFileNameList=[]
    for thisFile in allFileNameList:
        if (expectedPrefix==anyfix)&(expectedSuffix==anyfix):
            dataFileNameList.append(thisFile)
        elif (expectedPrefix==anyfix)&(expectedSuffix!=anyfix)&(thisFile.endswith(expectedSuffix)):
            dataFileNameList.append(thisFile)
        elif (expectedPrefix!=anyfix)&(expectedSuffix==anyfix)&(thisFile.startswith(expectedPrefix)):
            dataFileNameList.append(thisFile)
        elif (expectedPrefix!=anyfix)&(expectedSuffix!=anyfix)& \
                (thisFile.endswith(expectedSuffix))&(thisFile.startswith(expectedPrefix)):
            dataFileNameList.append(thisFile)
    sort_nicely(dataFileNameList) # natural sorting
    return dataFileNameList

def last_file(folderpath,expectedSuffix):
    ''' look for last files in directory having the expected suffix (just '*' to have any) '''
    fileList=glob.glob(folderpath+expectedSuffix)
    latestFile= max(fileList, key= os.path.getctime)
    return latestFile
#    
#
#
#%% GUI
def my_GUIwin_bring2front(win):
    ''' bring the GUI window to the foreground '''
    win.lift()
    win.attributes('-topmost', True)
    win.attributes('-topmost', False)
#    
def my_GUIwin_text(arguments):
    '''
    create a GUI window
    arguments should  be label0, default_val0, label1, default_val1,  ...
    label and default_val are strings
    '''
    #    
    win=tkinter.Tk()
    my_GUIwin_bring2front(win)    
    #
    Nargs= len(arguments)//2
    VariableList=[]
    #
    for iitem in range(Nargs):
        ilabel= 2*iitem
        idefault= 1+2*iitem
        #
        thisLabel=tkinter.Label(win, text=arguments[ilabel])
        thisLabel.grid(row=iitem, column=0)
        #
        thisVariable=tkinter.StringVar()
        thisVariable.set(arguments[idefault])
        thisField= tkinter.Entry(win, textvariable=thisVariable, width=100)
        VariableList += [thisVariable]                
        thisField.grid(row=iitem, column=1)
    #
    execButton= tkinter.Button(win, text="execute")
    execButton.grid(row=Nargs, column=1)
    #
    ValuesList= []
    #
    def my_GUIexec():
        ''' GUI exec button: saves variable values and close window '''
        for iitem in range(Nargs):
            ValuesList.append( VariableList[iitem].get() )
        win.destroy()
    #
    execButton.configure(command= my_GUIexec)
    #
    win.mainloop()
    return(ValuesList)
#
#
#
#%% plots
def maximize_plot():
    figManager = matplotlib.pyplot.get_current_fig_manager()
    figManager.window.showMaximized()
    
def color_y_axis(ax, color):
    '''Color your axes '''
    for t in ax.get_yticklabels():
        t.set_color(color)
    return None
#
def plot_1D(arrayX, arrayY, label_x,label_y,label_title):
    ''' 1D scatter plot ''' 
    fig = matplotlib.pyplot.figure()
    matplotlib.pyplot.plot(arrayX, arrayY, 'o', fillstyle='none')
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title)    
    matplotlib.pyplot.show(block=False)
    return (fig)
#
def plot_1D_errbar(arrayX1,arrayY1,errbarY1, label_x,label_y, label_title, loglogFlag):
    """ scatter plot (+errbars)""" 
    fig = matplotlib.pyplot.figure()
    if loglogFlag:
        matplotlib.pyplot.xscale('log', nonposx='clip')
        matplotlib.pyplot.yscale('log', nonposy='clip')
    matplotlib.pyplot.errorbar(arrayX1, arrayY1,yerr=errbarY1, fmt='ob', fillstyle='none', capsize=5)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title) 
    matplotlib.pyplot.show(block=False)
    return (fig)
#
def plot_1Dx2(arrayX1, arrayY1,label_title1, arrayX2, arrayY2,label_title2, label_x,label_y,label_supertitle):
    """ 2x 1D scatter plot """ 
    fig = matplotlib.pyplot.figure()
    matplotlib.pyplot.subplot(1,2,1)
    matplotlib.pyplot.plot(arrayX1, arrayY1, 'ob', fillstyle='none')
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title1)
    matplotlib.pyplot.subplot(1,2,2)   
    matplotlib.pyplot.plot(arrayX2, arrayY2, 'xg', fillstyle='none')
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title2) 
    #
    fig.suptitle(label_supertitle)
    matplotlib.pyplot.show(block=False)
    return (fig)
#
def plot_multi1D(arrayX, arrayY_2D, infoSets_List, label_x,label_y,label_title, showLineFlag):
    """ plot1D multiple datasets (arrayX[:], arrayY_2D[i,:]) , identified by infoSets_List[i] """
    fig = matplotlib.pyplot.figure()
    (Nsets,Npoints)= arrayY_2D.shape
    for iSet, thisSet in enumerate(infoSets_List):
        if showLineFlag: matplotlib.pyplot.plot(arrayX, arrayY_2D[iSet,:],'o-', fillstyle='none')
        else: matplotlib.pyplot.plot(arrayX, arrayY_2D[iSet,:],'o', fillstyle='none')
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title)   
    matplotlib.pyplot.legend(infoSets_List, loc='upper right')
    matplotlib.pyplot.show(block=False) 
    return fig
#
def plot_1D_2scales(dataX, dataY0, dataY1, labelX, labelY0, labelY1, labelTitle):
    ''' scatter plot dataY0/1 on left/right axes'''
    colY0='blue'
    colY1='red'
    #
    fig, ax1 = matplotlib.pyplot.subplots()
    ax2 = ax1.twinx()
    ax1.plot(dataX, dataY0, 'o', color=colY0, fillstyle='none')
    ax1.set_xlabel(labelX)
    ax1.set_ylabel(labelY0,color=colY0)
    ax2.plot(dataX, dataY1, 'x', color=colY1)
    ax2.set_ylabel(labelY1, color=colY1)
    matplotlib.pyplot.title(labelTitle)
    color_y_axis(ax1, colY0)
    color_y_axis(ax2, colY1)
    matplotlib.pyplot.show(block=False)
    return (fig, ax1, ax2) 
#
def plot_1Dx2_samecanva(arrayX1,arrayY1,legend1, arrayX2,arrayY2,legend2, label_x,label_y, label_title, loglogFlag):
    """ 2x 1D scatter plot in the same canva """ 
    fig = matplotlib.pyplot.figure()
    if loglogFlag: 
        if len(arrayX1)>0: matplotlib.pyplot.loglog(arrayX1, arrayY1, 'ob', fillstyle='none', label=legend1)
        if len(arrayX2)>0: matplotlib.pyplot.loglog(arrayX2, arrayY2, 'xg', fillstyle='none', label=legend2)
    else:
        if len(arrayX1)>0: matplotlib.pyplot.plot(arrayX1, arrayY1, 'ob', fillstyle='none', label=legend1)
        if len(arrayX2)>0: matplotlib.pyplot.plot(arrayX2, arrayY2, 'xg', fillstyle='none', label=legend2)
    matplotlib.pyplot.legend(loc='best')
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title) 
    matplotlib.pyplot.show(block=False)
    return (fig)
#
def plot_1Dx3_samecanva(arrayX1,arrayY1,legend1, arrayX2,arrayY2,legend2, arrayX3,arrayY3,legend3, label_x,label_y, label_title, loglogFlag):
    """ 3x 1D scatter plot in the same canva """ 
    fig = matplotlib.pyplot.figure()
    if loglogFlag: 
        if len(arrayX1)>0: matplotlib.pyplot.loglog(arrayX1, arrayY1, '^r', fillstyle='none', label=legend1)
        if len(arrayX2)>0: matplotlib.pyplot.loglog(arrayX2, arrayY2, 'xb', fillstyle='none', label=legend2)
        if len(arrayX3)>0: matplotlib.pyplot.loglog(arrayX3, arrayY3, 'ok', fillstyle='none', label=legend3)
    else:
        if len(arrayX1)>0: matplotlib.pyplot.plot(arrayX1, arrayY1, '^r', fillstyle='none', label=legend1)
        if len(arrayX2)>0: matplotlib.pyplot.plot(arrayX2, arrayY2, 'xb', fillstyle='none', label=legend2)
        if len(arrayX3)>0: matplotlib.pyplot.plot(arrayX3, arrayY3, 'ok', fillstyle='none', label=legend3)
    matplotlib.pyplot.legend(loc='best')
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title) 
    matplotlib.pyplot.show(block=False)
    return (fig)
#
def plot_errbar_1Dx3_samecanva(arrayX1,arrayY1,errbarY1,legend1, arrayX2,arrayY2,errbarY2,legend2, arrayX3,arrayY3,errbarY3,legend3, label_x,label_y, label_title, loglogFlag):
    """ 3x 1D scatter plot (+errbars) in the same canva """ 
    fig = matplotlib.pyplot.figure()
    if loglogFlag:
        matplotlib.pyplot.xscale('log', nonposx='clip')
        matplotlib.pyplot.yscale('log', nonposy='clip')
    if len(arrayX1)>0: matplotlib.pyplot.errorbar(arrayX1, arrayY1,yerr=errbarY1, fmt='^r', fillstyle='none', capsize=5, label=legend1)
    if len(arrayX2)>0: matplotlib.pyplot.errorbar(arrayX2, arrayY2,yerr=errbarY2, fmt='xb', fillstyle='none', capsize=5, label=legend2)
    if len(arrayX3)>0: matplotlib.pyplot.errorbar(arrayX3, arrayY3,yerr=errbarY3, fmt='ok', fillstyle='none', capsize=5, label=legend3)
    matplotlib.pyplot.legend(loc='best')
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title) 
    matplotlib.pyplot.show(block=False)
    return (fig)
'''
def plot_errbar_1Dx3_samecanva(arrayX1,arrayY1,errbarY1,legend1, arrayX2,arrayY2,errbarY2,legend2, arrayX3,arrayY3,errbarY3,legend3, label_x,label_y, label_title):
    """ 3x 1D scatter plot (+errbars) in the same canva """ 
    fig = matplotlib.pyplot.figure()
    if len(arrayX1)>0: matplotlib.pyplot.errorbar(arrayX1, arrayY1,yerr=errbarY1, fmt='ob', fillstyle='none', capsize=5, label=legend1)
    if len(arrayX2)>0: matplotlib.pyplot.errorbar(arrayX2, arrayY2,yerr=errbarY2, fmt='xg', fillstyle='none', capsize=5, label=legend2)
    if len(arrayX3)>0: matplotlib.pyplot.errorbar(arrayX3, arrayY3,yerr=errbarY3, fmt='xg', fillstyle='none', capsize=5, label=legend3)
    matplotlib.pyplot.legend(loc='best')
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title) 
    matplotlib.pyplot.show(block=False)
    return (fig)
'''
#
def plot_2D_all(array2D, logScaleFlag, label_x,label_y,label_title, invertx_flag):
    ''' 2D image''' 
    cmap = matplotlib.pyplot.cm.jet
    fig = matplotlib.pyplot.figure()
    if logScaleFlag: matplotlib.pyplot.imshow(array2D, norm=matplotlib.colors.LogNorm(), interpolation='none', cmap=cmap)
    else: matplotlib.pyplot.imshow(array2D, interpolation='none', cmap=cmap)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title)    
    matplotlib.pyplot.colorbar()
    if (invertx_flag==True): matplotlib.pyplot.gca().invert_xaxis();  
    matplotlib.pyplot.show(block=False)
    return (fig)
#
def plot_2D_map(array2D, goodPixMap, label_x,label_y,label_title, invertx_flag):
    ''' 2D image , mark as error where map ia False''' 
    cmap = matplotlib.pyplot.cm.jet
    fig = matplotlib.pyplot.figure()
    badPixMap= (goodPixMap==False)
    array2D[badPixMap]= numpy.NAN
    matplotlib.pyplot.imshow(array2D, interpolation='none', cmap=cmap)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title)    
    matplotlib.pyplot.colorbar()
    if (invertx_flag==True): matplotlib.pyplot.gca().invert_xaxis();  
    matplotlib.pyplot.show(block=False)
    return (fig)
#
def plot_2D(array2D, label_x,label_y,label_title, invertx_flag, ErrBelow):
    ''' 2D image , mark as error (white) the values << ErrBelow''' 
    cmap = matplotlib.pyplot.cm.jet
    cmap.set_under(color='white')    
    fig = matplotlib.pyplot.figure()
    matplotlib.pyplot.imshow(array2D, interpolation='none', cmap=cmap, vmin=ErrBelow)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title)    
    matplotlib.pyplot.colorbar()
    if (invertx_flag==True): matplotlib.pyplot.gca().invert_xaxis();  
    matplotlib.pyplot.show(block=False)
    return (fig) 
def plot_2D_notBelow(array2D, label_x,label_y,label_title, invertx_flag, ErrBelow):
    fig= plot_2D(array2D, label_x,label_y,label_title, invertx_flag, ErrBelow)
    return (fig) 
#
def plot_2D_stretched(array2D, label_x,label_y,label_title, invertx_flag, ErrBelow):
    ''' 2D image (stretched), mark as error (white) the values << ErrBelow''' 
    cmap = matplotlib.pyplot.cm.jet
    cmap.set_under(color='white')    
    fig = matplotlib.pyplot.figure()
    matplotlib.pyplot.imshow(array2D, interpolation='none', aspect='auto', cmap=cmap, vmin=ErrBelow)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title)    
    matplotlib.pyplot.colorbar()
    if (invertx_flag==True): matplotlib.pyplot.gca().invert_xaxis();  
    matplotlib.pyplot.show(block=False)
    return (fig)    
#
def plot_2x2D(array1,array2, logScaleFlag1,logScaleFlag2, label_x,label_y, label_title1,label_title2, invertx_flag):
    ''' 2x2D image''' 
    cmap = matplotlib.pyplot.cm.jet
    fig = matplotlib.pyplot.figure()
    #
    matplotlib.pyplot.subplot(1,2,1)
    if logScaleFlag1: matplotlib.pyplot.imshow(array1, norm=matplotlib.colors.LogNorm(), interpolation='none', cmap=cmap)
    else: matplotlib.pyplot.imshow(array1, interpolation='none', cmap=cmap)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title1)    
    matplotlib.pyplot.colorbar()
    if (invertx_flag==True): matplotlib.pyplot.gca().invert_xaxis(); 
    #
    matplotlib.pyplot.subplot(1,2,2)
    if logScaleFlag2: matplotlib.pyplot.imshow(array2, norm=matplotlib.colors.LogNorm(), interpolation='none', cmap=cmap)
    else: matplotlib.pyplot.imshow(array2, interpolation='none', cmap=cmap)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title2)    
    matplotlib.pyplot.colorbar()
    if (invertx_flag==True): matplotlib.pyplot.gca().invert_xaxis(); 
    matplotlib.pyplot.show(block=False)
    return (fig)
#       
#def my_surf(X,Y,Z,label_x,label_y,label_title):
#    '''X,Y,Z (each 1D) => surf plot'''
#    fig = matplotlib.pyplot.figure()
#    ax = fig.add_subplot(111, projection='3d')
#    Axes3D.plot_trisurf(ax,X,Y,Z)
#    matplotlib.pyplot.xlabel(label_x)
#    matplotlib.pyplot.ylabel(label_y)
#    matplotlib.pyplot.title(label_title)
#    matplotlib.pyplot.show()
#    return (fig,ax)
#
#def my_scatter3D(X,Y,Z,label_x,label_y,label_title):
#    '''X,Y,Z (each 1D) => 3D scatter plot'''
#    fig = matplotlib.pyplot.figure()
#    ax = fig.add_subplot(111, projection='3d')
#    Axes3D.scatter(ax, X,Y,Z, zdir='z', s=len(X), c='b', depthshade=True)
#    matplotlib.pyplot.xlabel(label_x)
#    matplotlib.pyplot.ylabel(label_y)
#    matplotlib.pyplot.title(label_title)
#    matplotlib.pyplot.show()
#    return (fig,ax)
#
#
def plot_histo1D(array_2plot, histobins, logScaleFlag, label_x,label_y,label_title):
    """ plot a histogram """
    fig = matplotlib.pyplot.figure()
    matplotlib.pyplot.hist(array_2plot, bins=histobins)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title)
    if logScaleFlag: matplotlib.pyplot.yscale('log', nonposy='clip')
    matplotlib.pyplot.show(block=False)
    return fig

def plot_histo1d(array_2plot, histobins, logScaleFlag, label_x,label_y,label_title):
    """ 1d same as 1D (keep for retrocompatibility) """
    fig = plot_histo1D(array_2plot, histobins, logScaleFlag, label_x,label_y,label_title)
    return fig

def histo1Dx2(Smpl,Rst, histobins, logScaleFlag, label_x1,label_x2, label_y, label_title1,label_title2, label_titleFig):
    """ 2x1d histo """ 
    fig = matplotlib.pyplot.figure()
    fig.canvas.manager.set_window_title(label_titleFig) 
    #
    matplotlib.pyplot.subplot(1,2,1)
    matplotlib.pyplot.hist(Smpl, bins=histobins)
    if logScaleFlag: matplotlib.pyplot.yscale('log', nonposy='clip')
    matplotlib.pyplot.xlabel(label_x1)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title1)
    #
    matplotlib.pyplot.subplot(1,2,2)
    matplotlib.pyplot.hist(Rst, bins=histobins)
    if logScaleFlag: matplotlib.pyplot.yscale('log', nonposy='clip')
    matplotlib.pyplot.xlabel(label_x2)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title2)
    return fig


def plot_histo1D_and_curve(data2histo, histobins, x2plot,y2plot, logScaleFlag, xlabel, ylabel, titlelabel):    
    fig = matplotlib.pyplot.figure()
    matplotlib.pyplot.hist(data2histo, bins=histobins)
    if logScaleFlag: matplotlib.pyplot.yscale('log', nonposy='clip')
    matplotlib.pyplot.plot(x2plot,y2plot)
    matplotlib.pyplot.xlabel(xlabel)
    matplotlib.pyplot.ylabel(ylabel)
    matplotlib.pyplot.title(titlelabel)
    matplotlib.pyplot.show(block=False)
    return fig

def plot_multihisto1D(arrays_2plot_2D, histobins, logScaleFlag, legendList, label_x,label_y,label_title, verboseFlag):
    """ plot multiple histograms """
    fig = matplotlib.pyplot.figure()
    (NImg,Narrays)= arrays_2plot_2D.shape
    for iAr in range(Narrays):
        thisData= arrays_2plot_2D[:,iAr]
        thisLeg= legendList[iAr]
        if ( numpy.isnan(thisData).any() ) : 
            # ignore these data
            if verboseFlag: printcol("{0}: no valid data".format(thisLeg), 'orange')
        else:
            matplotlib.pyplot.hist(thisData, histobins, alpha=0.5, label=thisLeg)
            if logScaleFlag: matplotlib.pyplot.yscale('log', nonposy='clip')
            matplotlib.pyplot.legend(loc='upper right')
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title)
    matplotlib.pyplot.show(block=False)
    return fig

def plot_bar1D(edges, freqvals, logScaleFlag, label_x,label_y,label_title):
    """ plot a barplot - essentially an histogram, but using data from: 
        (freqvals, edges) = numpy.histogram(X,this_histobins) """
    fig = matplotlib.pyplot.figure()
    midpoints= 0.5*(edges[1:]+ edges[:-1])
    matplotlib.pyplot.bar(midpoints, freqvals, width=numpy.diff(edges), align="edge")
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title)
    if logScaleFlag: matplotlib.pyplot.yscale('log', nonposy='clip')
    matplotlib.pyplot.show(block=False)
    return fig
#
def plot_histo2D(X,Y, nbinsX,nbinsY, label_x,label_y,label_title,ErrBelow):
    ''' 2D histogram plot, set to white anything < ErrBelow (e.g. 0.1)'''
    cmap = matplotlib.pyplot.cm.jet
    cmap.set_under(color='white')    
    fig = matplotlib.pyplot.figure()
    matplotlib.pyplot.hist2d(X,Y, bins=[nbinsX,nbinsY], cmap=cmap, vmin=ErrBelow)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title)    
    matplotlib.pyplot.colorbar()
    matplotlib.pyplot.show(block=False)
    return (fig)  

def show_it(): 
    matplotlib.pyplot.show(block=True) 
    return
def showIt(): 
    matplotlib.pyplot.show(block=True) 
    return
#
# save as png instead of plotting
def png_1D(arrayX, arrayY, label_x,label_y,label_title, filenamepath):
    ''' 1D scatter plot: save(not show): e.g. filenamepath='/tmp/test0.png' '''
    matplotlib.pyplot.ioff()
    #
    if filenamepath[-4:] in ['.png','.PNG']: filenamepath_out= filenamepath
    else:  filenamepath_out= filenamepath+'.png'
    #
    fig = matplotlib.pyplot.figure()
    matplotlib.pyplot.plot(arrayX, arrayY, 'o', fillstyle='none')
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title)
    matplotlib.pyplot.savefig(filenamepath_out)
    matplotlib.pyplot.close(fig)
    #
    matplotlib.pyplot.ion()
    return

def png_histo1D(array_2plot, histobins, logScaleFlag, label_x,label_y,label_title, filenamepath):
    """ plot a histogram: save(not show) as png """
    matplotlib.pyplot.ioff()
    #
    if filenamepath[-4:] in ['.png','.PNG']: filenamepath_out= filenamepath
    else:  filenamepath_out= filenamepath+'.png'
    #
    fig = matplotlib.pyplot.figure()
    matplotlib.pyplot.hist(array_2plot, bins=histobins)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title)
    if logScaleFlag: matplotlib.pyplot.yscale('log', nonposy='clip')
    matplotlib.pyplot.savefig(filenamepath_out)
    matplotlib.pyplot.close(fig)
    #
    matplotlib.pyplot.ion()
    return

def png_2D_all(array2D, logScaleFlag, label_x,label_y,label_title, invertx_flag, filenamepath):
    ''' 2D image: save(not show) as png'''
    matplotlib.pyplot.ioff()
    #
    if filenamepath[-4:] in ['.png','.PNG']: filenamepath_out= filenamepath
    else:  filenamepath_out= filenamepath+'.png'
    #
    cmap = matplotlib.pyplot.cm.jet
    fig = matplotlib.pyplot.figure()
    if logScaleFlag: matplotlib.pyplot.imshow(array2D, norm=matplotlib.colors.LogNorm(), interpolation='none', cmap=cmap)
    else: matplotlib.pyplot.imshow(array2D, interpolation='none', cmap=cmap)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title)
    matplotlib.pyplot.colorbar()
    if (invertx_flag==True): matplotlib.pyplot.gca().invert_xaxis();
    matplotlib.pyplot.savefig(filenamepath_out)
    matplotlib.pyplot.close(fig)
    #
    matplotlib.pyplot.ion()
    return

#
def png_1Dx3_samecanva(arrayX1,arrayY1,legend1, arrayX2,arrayY2,legend2, arrayX3,arrayY3,legend3, label_x,label_y, label_title, loglogFlag, filenamepath):
    """ 3x 1D scatter plot in the same canva """
    #
    matplotlib.pyplot.ioff()
    #
    if filenamepath[-4:] in ['.png','.PNG']: filenamepath_out= filenamepath
    else:  filenamepath_out= filenamepath+'.png'
    #
    fig = matplotlib.pyplot.figure()
    if loglogFlag:
        if len(arrayX1)>0: matplotlib.pyplot.loglog(arrayX1, arrayY1, '^r', fillstyle='none', label=legend1)
        if len(arrayX2)>0: matplotlib.pyplot.loglog(arrayX2, arrayY2, 'xb', fillstyle='none', label=legend2)
        if len(arrayX3)>0: matplotlib.pyplot.loglog(arrayX3, arrayY3, 'ok', fillstyle='none', label=legend3)
    else:
        if len(arrayX1)>0: matplotlib.pyplot.plot(arrayX1, arrayY1, '^r', fillstyle='none', label=legend1)
        if len(arrayX2)>0: matplotlib.pyplot.plot(arrayX2, arrayY2, 'xb', fillstyle='none', label=legend2)
        if len(arrayX3)>0: matplotlib.pyplot.plot(arrayX3, arrayY3, 'ok', fillstyle='none', label=legend3)
    matplotlib.pyplot.legend(loc='best')
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title)
    matplotlib.pyplot.savefig(filenamepath_out)
    matplotlib.pyplot.close(fig)
    #
    matplotlib.pyplot.ion()
    return

def png_errbar_1Dx3_samecanva(arrayX1,arrayY1,errbarY1,legend1, arrayX2,arrayY2,errbarY2,legend2, arrayX3,arrayY3,errbarY3,legend3, label_x,label_y, label_title, loglogFlag, filenamepath):
    """ 3x 1D scatter plot (+errbars) in the same canva: save to png """
    #
    matplotlib.pyplot.ioff()
    #
    if filenamepath[-4:] in ['.png','.PNG']: filenamepath_out= filenamepath
    else:  filenamepath_out= filenamepath+'.png'
    #
    fig = matplotlib.pyplot.figure()
    if loglogFlag:
        matplotlib.pyplot.xscale('log', nonposx='clip')
        matplotlib.pyplot.yscale('log', nonposy='clip')
    if len(arrayX1)>0: matplotlib.pyplot.errorbar(arrayX1, arrayY1,yerr=errbarY1, fmt='^r', fillstyle='none', capsize=5, label=legend1)
    if len(arrayX2)>0: matplotlib.pyplot.errorbar(arrayX2, arrayY2,yerr=errbarY2, fmt='xb', fillstyle='none', capsize=5, label=legend2)
    if len(arrayX3)>0: matplotlib.pyplot.errorbar(arrayX3, arrayY3,yerr=errbarY3, fmt='ok', fillstyle='none', capsize=5, label=legend3)
    matplotlib.pyplot.legend(loc='best')
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title)
    matplotlib.pyplot.savefig(filenamepath_out)
    matplotlib.pyplot.close(fig)
    #
    matplotlib.pyplot.ion()
    return



#
#
