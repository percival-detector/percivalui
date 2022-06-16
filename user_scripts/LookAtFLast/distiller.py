#!/usr/bin/env python3


"""
This version of the file
P2M_ADCcorr_01nd2nd3_distiller.py
was cobbled together by WN. It has several changes from the original,
and is designed to run without any GUI or user input. You must alter the
parameters yourself below before running it. It takes ~4 hours to run
on 600 acquisitions.
"""

#%% imports and useful constants
from APy3_auxINIT import *
#
GUIflag= False
#
#iGn=APy3_P2Mfuns.iGn; iCrs=APy3_P2Mfuns.iCrs; iFn=APy3_P2Mfuns.iFn; NGnCrsFn==APy3_P2Mfuns.NGnCrsFn # 0 1 2 3
#iSmpl=APy3_P2Mfuns.iSmpl; iRst=APy3_P2Mfuns.iRst; NSmplRst=APy3_P2Mfuns.NSmplRst # 0 1 2
#
NRow= APy3_P2Mfuns.NRow
NCol= APy3_P2Mfuns.NCol
NCol = 1408;
#
ERRint16=APy3_P2Mfuns.ERRint16 #-256 # negative value usable to track Gn/Crs/Fn from missing pack 
ERRBlw=APy3_P2Mfuns.ERRBlw #-0.1
ERRDLSraw=APy3_P2Mfuns.ERRDLSraw #65535 # forbidden uint16, usable to track "pixel" from missing pack
# ---
#
#%% functions
def write_ADCcor_h5(fileNamePath,
                    ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset, ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset,
                    ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset,  ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset
                    ):
    my5hfile= h5py.File(fileNamePath, 'w')
    my5hfile.create_dataset('sample/coarse/slope',  data=ADCparam_Smpl_crs_slope) #
    my5hfile.create_dataset('sample/coarse/offset', data=ADCparam_Smpl_crs_offset) #
    my5hfile.create_dataset('sample/fine/slope',   data=ADCparam_Smpl_fn_slope) #
    my5hfile.create_dataset('sample/fine/offset',  data=ADCparam_Smpl_fn_offset) #
    my5hfile.create_dataset('reset/coarse/slope',   data=ADCparam_Rst_crs_slope) #
    my5hfile.create_dataset('reset/coarse/offset',  data=ADCparam_Rst_crs_offset) #
    my5hfile.create_dataset('reset/fine/slope',    data=ADCparam_Rst_fn_slope) #
    my5hfile.create_dataset('reset/fine/offset',   data=ADCparam_Rst_fn_offset) #
    my5hfile.close()

def plot_2x2D(array1,array2, logScaleFlag, label_x,label_y, label_title1,label_title2, invertx_flag):
    ''' 2x2D image''' 
    cmap = matplotlib.pyplot.cm.jet
    fig = matplotlib.pyplot.figure()
    #
    matplotlib.pyplot.subplot(1,2,1)
    if logScaleFlag: matplotlib.pyplot.imshow(array1, norm=matplotlib.colors.LogNorm(), interpolation='none', cmap=cmap)
    else: matplotlib.pyplot.imshow(array1, interpolation='none', cmap=cmap)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title1)    
    matplotlib.pyplot.colorbar()
    if (invertx_flag==True): matplotlib.pyplot.gca().invert_xaxis(); 
    #
    matplotlib.pyplot.subplot(1,2,2)
    if logScaleFlag: matplotlib.pyplot.imshow(array2, norm=matplotlib.colors.LogNorm(), interpolation='none', cmap=cmap)
    else: matplotlib.pyplot.imshow(array2, interpolation='none', cmap=cmap)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title2)    
    matplotlib.pyplot.colorbar()
    if (invertx_flag==True): matplotlib.pyplot.gca().invert_xaxis();
    matplotlib.pyplot.show(block=False)
    return (fig)
# ---
#
#%% start
APy3_GENfuns.clean()
APy3_GENfuns.printcol("--------------",'blue')
timeId= APy3_GENfuns.whatTimeIsIt()
APy3_GENfuns.printcol("script beginning at "+timeId,'blue')
APy3_GENfuns.printcol("--  --  --  --",'blue')
# ---
#
#%% defaults for GUI window
#
#
#
#
#'''
########################################### SET YOUR PREFERENCES HERE ######################################################
# VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
dflt_folder_data2process= '/dls/detectors/Percival/captures/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_indexFileName='index.dat'
dflt_inputFileSuffix=''
#
#dflt_Row2proc='0:1483' # means: [all]
#dflt_Cols2proc='32:1439' # means: [all]  
dflt_Row2proc='350:356' # a few, just to test
dflt_Cols2proc='1000:1001' # a few, just to test
dflt_Row2proc='all'
dflt_Cols2proc='all'

#
dflt_Img2proc='2:9'#
dflt_fit_crsRange='5:29'
dflt_fit_minNpoints=4
dflt_fit_minR2=0.9
#dflt_fit_minR2=0.85 # use the lesser restriction if there are a lot of failures
#'''
#
dflt_saveFlag= 'Y'; # if you want to save the params to file (will overwrite!) 
dflt_outFolder= dflt_folder_data2process;
dflt_outFileprefix= 'example_'
#
dflt_highMemFlag='Y' 
dflt_verboseFlag='N'
#
dflt_showFlag='Y'; dflt_showFlag='N'
#
#AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
# ---
#
#
#
#
if GUIflag:
  pass;
else: 
    #%% NO GUI window
    folder_data2process= dflt_folder_data2process
    indexFileName= dflt_indexFileName
    #
    Cols2proc_mtlb= dflt_Cols2proc
    if Cols2proc_mtlb in ['all','All','ALL',':','*','-1']: Cols2proc= numpy.arange(NCol)
    else: Cols2proc=APy3_GENfuns.matlabLike_range(Cols2proc_mtlb)
    #
    Rows2proc_mtlb= dflt_Row2proc
    if Rows2proc_mtlb in ['all','All','ALL',':','*','-1']: Rows2proc= numpy.arange(NRow)
    else: Rows2proc=APy3_GENfuns.matlabLike_range(Rows2proc_mtlb) 
    #
    Img2proc_mtlb= dflt_Img2proc
    if Img2proc_mtlb in ['all','All','ALL',':','*','-1']: APy3_GENfuns.printERR('you need to give an explicit range to the process data: using images [from:to]')
    else: Img2proc=APy3_GENfuns.matlabLike_range(Img2proc_mtlb); NImg2procxFile=len(Img2proc)
    #
    fit_crsRange_mtlb= dflt_fit_crsRange
    if fit_crsRange_mtlb in ['all','All','ALL',':','*','-1']: fit_crsRange= numpy.arange(32)
    else: fit_crsRange=APy3_GENfuns.matlabLike_range(fit_crsRange_mtlb)
    #
    fit_minNpoints= int(dflt_fit_minNpoints); 
    fit_minR2= float(dflt_fit_minR2);
    #
    highMemFlag=APy3_GENfuns.isitYes(str(dflt_highMemFlag))
    #
    saveFlag=APy3_GENfuns.isitYes(str(dflt_saveFlag));
    outFolder=dflt_outFolder
    outFileprefix=dflt_outFileprefix
    #
    showFlag=APy3_GENfuns.isitYes(str(dflt_showFlag))
    verboseFlag=APy3_GENfuns.isitYes(str(dflt_verboseFlag))
    # ---
# ---

#
#%% what's up doc
APy3_GENfuns.printcol('will process data from '+folder_data2process,'blue')
APy3_GENfuns.printcol('will use {0} as the index file'.format(indexFileName),'blue')
APy3_GENfuns.printcol('will elaborate Cols {0}, Rows {1}, images {2}'.format(Cols2proc_mtlb,Rows2proc_mtlb, Img2proc_mtlb),'blue')
APy3_GENfuns.printcol('will fit crs {0} (at least {1} points, at least R2={2})'.format(fit_crsRange_mtlb,fit_minNpoints,fit_minR2),'blue')
if saveFlag: APy3_GENfuns.printcol('will write output to: {0}{1}...'.format(outFolder,outFileprefix),'blue')
if (showFlag): APy3_GENfuns.printcol('will show graphs','blue')
if (verboseFlag): APy3_GENfuns.printcol('verbose','blue')
APy3_GENfuns.printcol("--  --  --  --",'blue')
# ---
#
#%% start
startTime = time.time()
if (verboseFlag): APy3_GENfuns.printcol("script operations beginning for real at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')
#
SmplCrs_slope= APy3_GENfuns.numpy_NaNs((NRow,NCol))
SmplCrs_offset= APy3_GENfuns.numpy_NaNs_like(SmplCrs_slope)
SmplFn_slope= APy3_GENfuns.numpy_NaNs_like(SmplCrs_slope)
SmplFn_offset= APy3_GENfuns.numpy_NaNs_like(SmplCrs_slope)
SmplProcessed_Map= numpy.zeros_like(SmplCrs_slope, dtype=bool)
SmplCrs_R2= APy3_GENfuns.numpy_NaNs_like(SmplCrs_slope)
SmplFn_R2= APy3_GENfuns.numpy_NaNs_like(SmplCrs_slope)
#
RstCrs_slope= APy3_GENfuns.numpy_NaNs((NRow,NCol))
RstCrs_offset= APy3_GENfuns.numpy_NaNs_like(SmplCrs_slope)
RstFn_slope= APy3_GENfuns.numpy_NaNs_like(SmplCrs_slope)
RstFn_offset= APy3_GENfuns.numpy_NaNs_like(SmplCrs_slope)
RstProcessed_Map= numpy.zeros_like(SmplCrs_slope, dtype=bool)
RstCrs_R2= APy3_GENfuns.numpy_NaNs_like(SmplCrs_slope)
RstFn_R2= APy3_GENfuns.numpy_NaNs_like(SmplCrs_slope)
#
# ---
#
#%% read files
APy3_GENfuns.printcol('reading metadata file','blue')
indexFileList= APy3_GENfuns.read_tst(folder_data2process+indexFileName)
idCollList=indexFileList[:,0]
CollList=indexFileList[:,1]
NColl= len(CollList)
if (verboseFlag): APy3_GENfuns.printcol('{0} collections detailed in the index file'.format(len(CollList)),'green')
#
dataSmpl2proc= numpy.zeros((NColl,NImg2procxFile,NRow,NCol,NGnCrsFn),dtype='int16') 
dataRst2proc=  numpy.zeros((NColl,NImg2procxFile,NRow,NCol,NGnCrsFn),dtype='int16')
Id_allData= numpy.zeros((NColl,NImg2procxFile)) 
#
for thisColl in range(len(CollList)):
    thisCollFile= folder_data2process+CollList[thisColl]+dflt_inputFileSuffix
    thisCollId_nameFromFile= idCollList[thisColl]
    if (verboseFlag): APy3_GENfuns.printcol('reading file {0}'.format(thisCollFile),'green')
    (thisSmpl,thisRst)= APy3_GENfuns.read_2xh5(thisCollFile, '/data/', '/reset/')
    dataSmpl2proc[thisColl,:,:,:,:]= APy3_P2Mfuns.convert_DLSraw_2_GnCrsFn(thisSmpl,thisRst, ERRDLSraw,ERRint16)[Img2proc,iSmpl,:,:,:] # [coll,Img,row,col,gn/cs/fn] <- [Img,SmplRst,row,col,gn/cs/fn]
    dataRst2proc[thisColl,:,:,:,:] = APy3_P2Mfuns.convert_DLSraw_2_GnCrsFn(thisSmpl,thisRst, ERRDLSraw,ERRint16)[Img2proc,iRst ,:,:,:] # [coll,Img,row,col,gn/cs/fn] <- [Img,SmplRst,row,col,gn/cs/fn]
    Id_allData[thisColl,:]= float(idCollList[thisColl])
    if (verboseFlag== False): APy3_GENfuns.dot_every10th(thisColl,len(CollList))
dataSmpl2proc= dataSmpl2proc.reshape((NColl*NImg2procxFile,NRow,NCol,NGnCrsFn))
dataRst2proc=  dataRst2proc.reshape( (NColl*NImg2procxFile,NRow,NCol,NGnCrsFn))
Id_allData= Id_allData.reshape((NColl*NImg2procxFile))
# ---
#
#%% show pixel evols if needed
if (showFlag): 
    aux_minX= min(Id_allData); aux_maxX= max(Id_allData)
    aux_nbinsX= numpy.linspace(aux_minX,aux_maxX, len(CollList))
    for thisRow in Rows2proc:
        for thisCol in Cols2proc:
            aux_labelX= "VRST [V]"
            aux_title= "pix=({0},{1})".format(thisRow,thisCol)
            APy3_GENfuns.plot_histo2D(Id_allData,dataSmpl2proc[:,thisRow,thisCol,iCrs], aux_nbinsX,numpy.arange(31), aux_labelX,"Crs[ADU]","Smpl,"+aux_title, 0.1)
            APy3_GENfuns.plot_histo2D(Id_allData,dataSmpl2proc[:,thisRow,thisCol,iFn], aux_nbinsX,numpy.arange(255), aux_labelX,"Fn[ADU]", "Smpl,"+aux_title, 0.1)
            APy3_GENfuns.plot_histo2D(Id_allData,dataRst2proc[ :,thisRow,thisCol,iCrs], aux_nbinsX,numpy.arange(31), aux_labelX,"Crs[ADU]","Rst,"+aux_title, 0.1)
            APy3_GENfuns.plot_histo2D(Id_allData,dataRst2proc[ :,thisRow,thisCol,iFn], aux_nbinsX,numpy.arange(255), aux_labelX,"Fn[ADU]", "Rst,"+aux_title, 0.1)
# ---
#
#%% elab data   
startElabTime= time.time() 
APy3_GENfuns.printcol("elaborating data",'blue')
if (verboseFlag): APy3_GENfuns.printcol("start elaborating data at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')
for thisRow in Rows2proc:
    for thisCol in Cols2proc:
        # Smpl
        # elab crs
        validCrsMsk= (dataSmpl2proc[:,thisRow,thisCol,iCrs]>=fit_crsRange[0])&(dataSmpl2proc[:,thisRow,thisCol,iCrs]<=fit_crsRange[-1])
        xCrs2fit= Id_allData[validCrsMsk]
        yCrs2fit= dataSmpl2proc[validCrsMsk,thisRow,thisCol,iCrs]
        #
        if len(xCrs2fit) >= fit_minNpoints:
            (slopefit_crs, interceptfit_crs)= APy3_FITfuns.linear_fit(xCrs2fit,yCrs2fit)
            SmplCrs_slope[thisRow,thisCol]= (-1)*slopefit_crs # weird RAL convention
            SmplCrs_offset[thisRow,thisCol]= interceptfit_crs   
            SmplCrs_R2[thisRow,thisCol]= APy3_FITfuns.linear_fit_R2(xCrs2fit,yCrs2fit)
            #
            if (showFlag):
                fig = matplotlib.pyplot.figure()
                matplotlib.pyplot.plot(xCrs2fit, yCrs2fit, 'o')
                matplotlib.pyplot.plot(xCrs2fit, APy3_FITfuns.linear_fun(xCrs2fit,-SmplCrs_slope[thisRow,thisCol],SmplCrs_offset[thisRow,thisCol]),'-')  
                matplotlib.pyplot.xlabel('Vin'); matplotlib.pyplot.ylabel('Crs'); matplotlib.pyplot.title('({0},{1}), Crs fit'.format(thisRow,thisCol))
                matplotlib.pyplot.show()
            #  
            # find most freq crs
            aux_counts= numpy.bincount(yCrs2fit)
            mostFreqCrs=numpy.argmax(aux_counts)
            VinCorr= (mostFreqCrs+0.5 - interceptfit_crs)/slopefit_crs       
            #  elab fn
            validFnMsk= (dataSmpl2proc[:,thisRow,thisCol,iCrs]==mostFreqCrs)&(dataSmpl2proc[:,thisRow,thisCol,iCrs]>=fit_crsRange[0])&(dataSmpl2proc[:,thisRow,thisCol,iCrs]<=fit_crsRange[-1])
            xFn2fit= Id_allData[validFnMsk] -VinCorr
            yFn2fit= dataSmpl2proc[validFnMsk,thisRow,thisCol,iFn]
            #
            if len(xFn2fit) >= fit_minNpoints:
                (slopefit_fn, interceptfit_fn)= APy3_FITfuns.linear_fit(xFn2fit,yFn2fit)    
                SmplFn_slope[thisRow,thisCol]= slopefit_fn
                SmplFn_offset[thisRow,thisCol]= interceptfit_fn
                SmplFn_R2[thisRow,thisCol]= APy3_FITfuns.linear_fit_R2(xFn2fit,yFn2fit)
                #
                if (showFlag):
                    fig = matplotlib.pyplot.figure()
                    matplotlib.pyplot.plot(xFn2fit, yFn2fit, 'o')
                    matplotlib.pyplot.plot(xFn2fit, APy3_FITfuns.linear_fun(xFn2fit,SmplFn_slope[thisRow,thisCol],SmplFn_offset[thisRow,thisCol]),'-')  
                    matplotlib.pyplot.xlabel('Vin'); matplotlib.pyplot.ylabel('Fn'); matplotlib.pyplot.title('({0},{1}), Smpl,Fn fit'.format(thisRow,thisCol)) 
                    matplotlib.pyplot.show()  
                #
                # mark as processed if R2 good enough
                if ((SmplCrs_R2[thisRow,thisCol]>=fit_minR2)&(SmplFn_R2[thisRow,thisCol]>=fit_minR2)): SmplProcessed_Map[thisRow,thisCol]=True
                else: SmplProcessed_Map[thisRow,thisCol]=False
                #
                # report
                if (verboseFlag):
                    if ((SmplCrs_R2[thisRow,thisCol]<fit_minR2)|(SmplFn_R2[thisRow,thisCol]<fit_minR2)): 
                        SmplCrs_slope[thisRow,thisCol]=numpy.NaN;SmplCrs_offset[thisRow,thisCol]=numpy.NaN; SmplFn_slope[thisRow,thisCol]=numpy.NaN;SmplFn_offset[thisRow,thisCol]=numpy.NaN;
                        APy3_GENfuns.printcol('pix=({0},{1}),Smpl: low R2: Crs_slp={2},Crs_off={3},Crs_R2={4}, Fn_slp={5},Fn_off={6},Fn_R2={7}'.format(thisRow,thisCol, SmplCrs_slope[thisRow,thisCol],SmplCrs_offset[thisRow,thisCol],SmplCrs_R2[thisRow,thisCol], SmplFn_slope[thisRow,thisCol],SmplFn_offset[thisRow,thisCol],SmplFn_R2[thisRow,thisCol]),'red') 
                    else:
                        APy3_GENfuns.printcol('pix=({0},{1}),Smpl: Crs_slp={2},Crs_off={3},Crs_R2={4}, Fn_slp={5},Fn_off={6},Fn_R2={7}'.format(thisRow,thisCol, SmplCrs_slope[thisRow,thisCol],SmplCrs_offset[thisRow,thisCol],SmplCrs_R2[thisRow,thisCol], SmplFn_slope[thisRow,thisCol],SmplFn_offset[thisRow,thisCol],SmplFn_R2[thisRow,thisCol]),'green') 
            else:
                SmplProcessed_Map[thisRow,thisCol]=False    
                SmplCrs_slope[thisRow,thisCol]=numpy.NaN;SmplCrs_offset[thisRow,thisCol]=numpy.NaN;SmplCrs_R2[thisRow,thisCol]=numpy.NaN
                SmplFn_slope[thisRow,thisCol]=numpy.NaN;SmplFn_offset[thisRow,thisCol]=numpy.NaN;SmplFn_R2[thisRow,thisCol]=numpy.NaN
                if (verboseFlag): APy3_GENfuns.printcol('pix=({0},{1}),Smpl: not enough points to properly fn-fit'.format(thisRow,thisCol),'orange') 
        else:
            SmplProcessed_Map[thisRow,thisCol]=False  
            SmplCrs_slope[thisRow,thisCol]=numpy.NaN;SmplCrs_offset[thisRow,thisCol]=numpy.NaN;SmplCrs_R2[thisRow,thisCol]=numpy.NaN
            SmplFn_slope[thisRow,thisCol]=numpy.NaN;SmplFn_offset[thisRow,thisCol]=numpy.NaN;SmplFn_R2[thisRow,thisCol]=numpy.NaN  
            if (verboseFlag): APy3_GENfuns.printcol('pix=({0},{1}),Smpl: not enough points to properly crs-fit'.format(thisRow,thisCol),'orange') 
        # ---
        #
        #%% show if needed
        if (showFlag):
            (NAllvalidImg,ignRow,ignCol,aux_NGnCrsFn)= dataSmpl2proc.shape
            alldata2Show_raw= dataSmpl2proc[:,thisRow,thisCol,:].reshape(NAllvalidImg,1,1,aux_NGnCrsFn)
            alldata2Show_ADCcor= APy3_P2Mfuns.ADCcorr_from0_NoGain(alldata2Show_raw[:,0,0,iCrs],alldata2Show_raw[:,0,0,iFn], 
                                            SmplCrs_slope[thisRow,thisCol], SmplCrs_offset[thisRow,thisCol], 
                                            SmplFn_slope[thisRow,thisCol], SmplFn_offset[thisRow,thisCol], 1, 1)[0,:]
            APy3_GENfuns.plot_1D(Id_allData, alldata2Show_ADCcor,'VRST','ADCcorr [ADU]','({0},{1}), Smpl,ADC corrected values'.format(thisRow,thisCol))
            #
            aux_nbinsX_max= max(Id_allData); aux_nbinsX_min= min(Id_allData); aux_nbinsX_Nsteps= len(Id_allData)
            aux_nbinsX= numpy.linspace(aux_nbinsX_min,aux_nbinsX_max, aux_nbinsX_Nsteps)
            aux_nbinsY_max= max(alldata2Show_ADCcor); aux_nbinsY_min= min(alldata2Show_ADCcor); aux_nbinsY_Nsteps= len(Id_allData)
            aux_nbinsY= numpy.linspace(aux_nbinsY_min,aux_nbinsY_max, aux_nbinsY_Nsteps)     
            aux_labelX= "VRST [V]"; aux_title= "pix=({0},{1})".format(thisRow,thisCol)
            if numpy.isnan(alldata2Show_ADCcor).any()==False: APy3_GENfuns.plot_histo2D(Id_allData,alldata2Show_ADCcor, aux_nbinsX,aux_nbinsY, aux_labelX,"ADCcorr [ADU]","Smpl,"+aux_title, 0.1)  
        # ---
        # Rst
        # elab crs
        validCrsMsk= (dataRst2proc[:,thisRow,thisCol,iCrs]>=fit_crsRange[0])&(dataRst2proc[:,thisRow,thisCol,iCrs]<=fit_crsRange[-1])
        xCrs2fit= Id_allData[validCrsMsk]
        yCrs2fit= dataRst2proc[validCrsMsk,thisRow,thisCol,iCrs]
        #
        if len(xCrs2fit) >= fit_minNpoints:
            (slopefit_crs, interceptfit_crs)= APy3_FITfuns.linear_fit(xCrs2fit,yCrs2fit)
            RstCrs_slope[thisRow,thisCol]= (-1)*slopefit_crs # weird RAL convention
            RstCrs_offset[thisRow,thisCol]= interceptfit_crs   
            RstCrs_R2[thisRow,thisCol]= APy3_FITfuns.linear_fit_R2(xCrs2fit,yCrs2fit)
            #
            if (showFlag):
                fig = matplotlib.pyplot.figure()
                matplotlib.pyplot.plot(xCrs2fit, yCrs2fit, 'o')
                matplotlib.pyplot.plot(xCrs2fit, APy3_FITfuns.linear_fun(xCrs2fit,-RstCrs_slope[thisRow,thisCol],RstCrs_offset[thisRow,thisCol]),'-')  
                matplotlib.pyplot.xlabel('Vin'); matplotlib.pyplot.ylabel('Crs'); matplotlib.pyplot.title('({0},{1}), Crs fit'.format(thisRow,thisCol))
                matplotlib.pyplot.show()
            #  
            # find most freq crs
            aux_counts= numpy.bincount(yCrs2fit)
            mostFreqCrs=numpy.argmax(aux_counts)
            VinCorr= (mostFreqCrs+0.5 - interceptfit_crs)/slopefit_crs       
            #  elab fn
            validFnMsk= (dataRst2proc[:,thisRow,thisCol,iCrs]==mostFreqCrs)&(dataRst2proc[:,thisRow,thisCol,iCrs]>=fit_crsRange[0])&(dataRst2proc[:,thisRow,thisCol,iCrs]<=fit_crsRange[-1])
            xFn2fit= Id_allData[validFnMsk] -VinCorr
            yFn2fit= dataRst2proc[validFnMsk,thisRow,thisCol,iFn]
            #
            if len(xFn2fit) >= fit_minNpoints:
                (slopefit_fn, interceptfit_fn)= APy3_FITfuns.linear_fit(xFn2fit,yFn2fit)    
                RstFn_slope[thisRow,thisCol]= slopefit_fn
                RstFn_offset[thisRow,thisCol]= interceptfit_fn
                RstFn_R2[thisRow,thisCol]= APy3_FITfuns.linear_fit_R2(xFn2fit,yFn2fit)
                #
                if (showFlag):
                    fig = matplotlib.pyplot.figure()
                    matplotlib.pyplot.plot(xFn2fit, yFn2fit, 'o')
                    matplotlib.pyplot.plot(xFn2fit, APy3_FITfuns.linear_fun(xFn2fit,RstFn_slope[thisRow,thisCol],RstFn_offset[thisRow,thisCol]),'-')  
                    matplotlib.pyplot.xlabel('Vin'); matplotlib.pyplot.ylabel('Fn'); matplotlib.pyplot.title('({0},{1}), Rst,Fn fit'.format(thisRow,thisCol)) 
                    matplotlib.pyplot.show()  
                #
                # mark as processed if R2 good enough
                if ((RstCrs_R2[thisRow,thisCol]>=fit_minR2)&(RstFn_R2[thisRow,thisCol]>=fit_minR2)): RstProcessed_Map[thisRow,thisCol]=True
                else: RstProcessed_Map[thisRow,thisCol]=False
                #
                # report
                if (verboseFlag):
                    if ((RstCrs_R2[thisRow,thisCol]<fit_minR2)|(RstFn_R2[thisRow,thisCol]<fit_minR2)): 
                        RstCrs_slope[thisRow,thisCol]=numpy.NaN;RstCrs_offset[thisRow,thisCol]=numpy.NaN; RstFn_slope[thisRow,thisCol]=numpy.NaN;RstFn_offset[thisRow,thisCol]=numpy.NaN;
                        APy3_GENfuns.printcol('pix=({0},{1}),Rst: low R2: Crs_slp={2},Crs_off={3},Crs_R2={4}, Fn_slp={5},Fn_off={6},Fn_R2={7}'.format(thisRow,thisCol, RstCrs_slope[thisRow,thisCol],RstCrs_offset[thisRow,thisCol],RstCrs_R2[thisRow,thisCol], RstFn_slope[thisRow,thisCol],RstFn_offset[thisRow,thisCol],RstFn_R2[thisRow,thisCol]),'red') 
                    else:
                        APy3_GENfuns.printcol('pix=({0},{1}),Rst: Crs_slp={2},Crs_off={3},Crs_R2={4}, Fn_slp={5},Fn_off={6},Fn_R2={7}'.format(thisRow,thisCol, RstCrs_slope[thisRow,thisCol],RstCrs_offset[thisRow,thisCol],RstCrs_R2[thisRow,thisCol], RstFn_slope[thisRow,thisCol],RstFn_offset[thisRow,thisCol],RstFn_R2[thisRow,thisCol]),'green') 
            else:
                RstProcessed_Map[thisRow,thisCol]=False    
                RstCrs_slope[thisRow,thisCol]=numpy.NaN;RstCrs_offset[thisRow,thisCol]=numpy.NaN;RstCrs_R2[thisRow,thisCol]=numpy.NaN
                RstFn_slope[thisRow,thisCol]=numpy.NaN;RstFn_offset[thisRow,thisCol]=numpy.NaN;RstFn_R2[thisRow,thisCol]=numpy.NaN
                if (verboseFlag): APy3_GENfuns.printcol('pix=({0},{1}),Rst: not enough points to properly fn-fit'.format(thisRow,thisCol),'orange') 
        else:
            RstProcessed_Map[thisRow,thisCol]=False  
            RstCrs_slope[thisRow,thisCol]=numpy.NaN;RstCrs_offset[thisRow,thisCol]=numpy.NaN;RstCrs_R2[thisRow,thisCol]=numpy.NaN
            RstFn_slope[thisRow,thisCol]=numpy.NaN;RstFn_offset[thisRow,thisCol]=numpy.NaN;RstFn_R2[thisRow,thisCol]=numpy.NaN  
            if (verboseFlag): APy3_GENfuns.printcol('pix=({0},{1}),Rst: not enough points to properly crs-fit'.format(thisRow,thisCol),'orange') 
        # ---
        #
        #%% show if needed
        if (showFlag):
            (NAllvalidImg,ignRow,ignCol,aux_NGnCrsFn)= dataRst2proc.shape
            alldata2Show_raw= dataRst2proc[:,thisRow,thisCol,:].reshape(NAllvalidImg,1,1,aux_NGnCrsFn)
            alldata2Show_ADCcor= APy3_P2Mfuns.ADCcorr_from0_NoGain(alldata2Show_raw[:,0,0,iCrs],alldata2Show_raw[:,0,0,iFn], 
                                            RstCrs_slope[thisRow,thisCol], RstCrs_offset[thisRow,thisCol], 
                                            RstFn_slope[thisRow,thisCol], RstFn_offset[thisRow,thisCol], 1, 1)[0,:]
            APy3_GENfuns.plot_1D(Id_allData, alldata2Show_ADCcor,'VRST','ADCcorr [ADU]','({0},{1}), Rst,ADC corrected values'.format(thisRow,thisCol))
            #
            aux_nbinsX_max= max(Id_allData); aux_nbinsX_min= min(Id_allData); aux_nbinsX_Nsteps= len(Id_allData)
            aux_nbinsX= numpy.linspace(aux_nbinsX_min,aux_nbinsX_max, aux_nbinsX_Nsteps)
            aux_nbinsY_max= max(alldata2Show_ADCcor); aux_nbinsY_min= min(alldata2Show_ADCcor); aux_nbinsY_Nsteps= len(Id_allData)
            aux_nbinsY= numpy.linspace(aux_nbinsY_min,aux_nbinsY_max, aux_nbinsY_Nsteps)     
            aux_labelX= "VRST [V]"; aux_title= "pix=({0},{1})".format(thisRow,thisCol)
            if numpy.isnan(alldata2Show_ADCcor).any()==False: APy3_GENfuns.plot_histo2D(Id_allData,alldata2Show_ADCcor, aux_nbinsX,aux_nbinsY, aux_labelX,"ADCcorr [ADU]","Rst,"+aux_title, 0.1)  
    if (verboseFlag== False): APy3_GENfuns.dot_every10th(thisRow,len(Rows2proc))

endElabTime= time.time()
# ---
APy3_GENfuns.printcol("it took {0}s to load files".format(startElabTime-startTime),'green')
APy3_GENfuns.printcol("it took {0}s to elaborate files".format(endElabTime-startElabTime),'green')
# ---
#
#%% save data 
if saveFlag: 
    APy3_GENfuns.printcol("saving data:",'blue')
    #%% 8 => 1 file
    out_FileNamePath= outFolder+outFileprefix+'_ADCcor.h5'
    write_ADCcor_h5(out_FileNamePath,
                    SmplCrs_slope,SmplCrs_offset, SmplFn_slope,SmplFn_offset,
                    RstCrs_slope, RstCrs_offset,  RstFn_slope, RstFn_offset
                    )
    APy3_GENfuns.printcol('save to {0}'.format(out_FileNamePath),'green')
    #
    if (verboseFlag):
        # yes, verboseFlag. want to see it even if showFlag==False
        (reread_Smpl_crs_slope,reread_Smpl_crs_offset, reread_Smpl_fn_slope,reread_Smpl_fn_offset, 
         reread_Rst_crs_slope, reread_Rst_crs_offset,  reread_Rst_fn_slope, reread_Rst_fn_offset)= APy3_P2Mfuns.read_ADUh5(out_FileNamePath)
        #
        plot_2x2D(reread_Smpl_crs_slope,reread_Smpl_crs_offset, False, 'row','col', 'Smpl_crs_slope','Smpl_crs_offset', True)
        plot_2x2D(reread_Smpl_fn_slope,reread_Smpl_fn_offset,   False, 'row','col', 'Smpl_fn_slope', 'Smpl_fn_offset', True)
        plot_2x2D(reread_Rst_crs_slope,reread_Rst_crs_offset,   False, 'row','col', 'Rst_crs_slope', 'Rst_crs_offset', True)
        plot_2x2D(reread_Rst_fn_slope,reread_Rst_fn_offset,     False, 'row','col', 'Rst_fn_slope',  'Rst_fn_offset', True)
        plot_2x2D(SmplCrs_R2,SmplFn_R2, False, 'row','col', 'SmplCrs R^2', 'SmplFn R^2', True)
        plot_2x2D(RstCrs_R2, RstFn_R2,  False, 'row','col', 'RstCrs R^2',  'RstFn R^2', True)
        APy3_GENfuns.showIt()
# ---
#
#%% that's all folks
APy3_GENfuns.printcol("done",'blue')
endTime=time.time()
APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')
