# -*- coding: utf-8 -*-
"""
math functions and fitting
(a half-decent language would have those functions already). Python is worth what it costs.
"""
#%% imports
#
import numpy
from scipy import stats # linear regression
from scipy.optimize import curve_fit # non-linear fit
import math
import scipy
import matplotlib
import matplotlib.pyplot
#
#
#
#%% straight line function
def linear_fun(X, slope, intercept):
    '''straight line function'''
    return intercept + (slope*X)
#
def linear_fit(X,Y):
    '''fit linear'''
    slopefit, interceptfit, r_val, p_val, std_err= stats.linregress(X, Y) 
    return (slopefit, interceptfit)
#
def linear_fit_R2(X,Y):
    '''R^2 quality of fit linear'''
    slopefit, interceptfit, r_val, p_val, std_err= stats.linregress(X, Y) 
    R2=r_val**2
    return (R2)
#
def plot_1Dx3_andfit_samecanva(arrayX1,arrayY1,legend1, arrayX2,arrayY2,legend2, arrayX3,arrayY3,legend3, label_x,label_y, label_title):
    """ 3x 1D scatter plot in the same canva """ 
    fig = matplotlib.pyplot.figure()
    #
    if len(arrayX1)>0: 
        matplotlib.pyplot.plot(arrayX1, arrayY1, 'ob', fillstyle='none', label=legend1)
        (fit_slope1,fit_offset1)=       linear_fit(arrayX1,arrayY1)
        matplotlib.pyplot.plot(arrayX1, linear_fun(arrayX1, fit_slope1,fit_offset1), '--b', label='fit')
    #
    if len(arrayX2)>0: 
        matplotlib.pyplot.plot(arrayX2, arrayY2, 'xg', fillstyle='none', label=legend2)
        (fit_slope2,fit_offset2)=       linear_fit(arrayX2,arrayY2)    
        matplotlib.pyplot.plot(arrayX2, linear_fun(arrayX2, fit_slope2,fit_offset2), '--g', label='fit')
    #
    if len(arrayX3)>0: 
        matplotlib.pyplot.plot(arrayX3, arrayY3, '^r', fillstyle='none', label=legend3)
        (fit_slope3,fit_offset3)=       linear_fit(arrayX3,arrayY3)    
        matplotlib.pyplot.plot(arrayX3, linear_fun(arrayX3, fit_slope3,fit_offset3), '--r', label='fit')
    #
    matplotlib.pyplot.legend(loc='best')
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title) 
    matplotlib.pyplot.show(block=False)
    return (fig)
# ---
#
#
#
#%% 1D gaussian function
def gauss_fun(X, A, mu, sigma):
    '''gaussian function'''
    return A*numpy.exp(-(X-mu)**2/(2.*sigma**2))
#
def gauss_fit(X,Y, A0,mu0,sigma0):
    '''fit gaussian'''
    p0= [A0,mu0,sigma0] # initial guess for the fitting coefficients
    #coeff, var_matrix = curve_fit(gauss_fun, X, Y, p0=p0, maxfev = 100000)
    coeff, var_matrix = curve_fit(gauss_fun, X, Y, p0=p0)
    Afit= coeff[0]
    mufit= coeff[1]
    sigmafit= coeff[2]
    return (Afit,mufit,sigmafit)
# ---
#
#%% 1D log(gaussian function)
def gausslog_fun(X, A,mu,sigma):
    '''log of a gaussian function'''
    #return numpy.log( A*numpy.exp(-(X-mu)**2/(2.*sigma**2)) )
    return numpy.log(A) + -(X-mu)**2/(2.*sigma**2)
#
def gausslog_fit(X,Y, A0,mu0,sigma0):
    '''fit gaussian'''
    X2fit=[]
    Ylog2fit=[]
    for index in range(len(Y)):
        if Y[index] > 0:
            X2fit += [X[index]]
            Ylog2fit += [numpy.log(Y[index])]
    #    
    p0= [A0,mu0,sigma0] # initial guess for the fitting coefficients
    coeff, var_matrix = curve_fit(gausslog_fun, X2fit,Ylog2fit, p0=p0)
    Afit= coeff[0]
    mufit= coeff[1]
    sigmafit= coeff[2]
    return (Afit,mufit,sigmafit)    
# ---
#
"""
#%% 2D-gaussian function
def gauss_2Dsimm_fun( (X,Y), A, muX, muY, sigma):
    '''
    2D (simmetrical) gaussian function
    here is how to use it:
    x = numpy.linspace(0, 200, 201); y = numpy.linspace(0, 200, 201); x, y = numpy.meshgrid(x, y)
    data = MYFITfuns.gauss_2Dsimm_fun((x, y), 3, 100, 150, 20)
    matplotlib.pyplot.figure()
    matplotlib.pyplot.imshow(data.reshape(201, 201))
    matplotlib.pyplot.colorbar()
    matplotlib.pyplot.show()
    '''
    g= A*numpy.exp(-(((X-muX)**2)+((Y-muY)**2))/(2.*sigma**2))
    return g.ravel()
#
def gauss_2Dsimm_fit( (X,Y), Z, A0, muX0, muY0, sigma0):
    '''
    fit of 2D (simmetrical) gaussian function
    use it with:
    x = numpy.linspace(0, 200, 201); y = numpy.linspace(0, 200, 201); x, y = numpy.meshgrid(x, y)
    '''
    initial_guess= [A0,muX0,muY0,sigma0] # initial guess for the fitting coefficients
    coeff, var_matrix = curve_fit(gauss_2Dsimm_fun, (X,Y), Z, p0=initial_guess)
    Afit= coeff[0]
    muXfit= coeff[1]
    muYfit= coeff[2]
    sigmafit= coeff[3]    
    return (Afit,muXfit,muYfit,sigmafit) 
"""
# ---
#
#
#
#%% normalized Edge response function (erf)
def normEdge_fun(X, slope, shift):
    '''function emulating a normalized Edge response'''
    Y=[]    
    for xi in X:
        Y += [(math.erf((xi*slope)-shift) +1)/2]
    Y=numpy.array(Y)
    return Y
#
def normEdge_fit(X,Y,slope0,shift0):
    '''fit normalized Edge response (erf)'''
    p0= [slope0,shift0] # initial guess for the fitting coefficients
    coeff, var_matrix = curve_fit(normEdge_fun, X, Y, p0=p0)
    slopefit= coeff[0]
    shiftfit= coeff[1]
    return (slopefit,shiftfit)
# ---
#
#%% normalized Edge response (erf of 2nd order polinomial) function
def norm2pEdge_fun(X, a0,a1,a2):
    '''normalized Edge response (erf of 2nd order polinomial) function'''
    Y=[]    
    for xi in X:
        Y += [(math.erf(a0 + (a1*xi)+ (a2*xi*xi)) +1)/2]
    Y=numpy.array(Y)
    return Y
#
def norm2pEdge_fun_fit(X,Y,a0_0,a1_0,a2_0):
    '''fit normalized Edge response (erf of 2nd order polinomial)'''
    p0= [a0_0,a1_0,a2_0] # initial guess for the fitting coefficients
    coeff, var_matrix = curve_fit(norm2pEdge_fun, X, Y, p0=p0)
    a0_fit=coeff[0]
    a1_fit=coeff[1]
    a2_fit=coeff[2]
    return (a0_fit,a1_fit,a2_fit)
# ---
#
#%% normalized Edge response (erf of 3rd order polinomial) function
def norm3pEdge_fun(X, a0,a1,a2,a3):
    '''normalized Edge response (erf of 3rd order polinomial) function'''
    Y=[]    
    for xi in X:
        Y += [(math.erf(a0 + (a1*xi)+ (a2*xi*xi)+ (a3*xi*xi*xi)) +1)/2]
    Y=numpy.array(Y)
    return Y
#
def norm3pEdge_fun_fit(X,Y,a0_0,a1_0,a2_0,a3_0):
    '''fit normalized Edge response (erf of 3rd order polinomial)'''
    p0= [a0_0,a1_0,a2_0,a3_0] # initial guess for the fitting coefficients
    coeff, var_matrix = curve_fit(norm3pEdge_fun, X, Y, p0=p0)
    a0_fit=coeff[0]
    a1_fit=coeff[1]
    a2_fit=coeff[2]
    a3_fit=coeff[3]
    return (a0_fit,a1_fit,a2_fit,a3_fit)
# ---
#
#
#
#%% Airy Disk profile
def AiryDiskProfile_fun(X, Energy_eV, pin_diam,pin_Dist, J0):
    '''Airy Disk profile'''
    # BesselX= ((pi * pin_diam)/lambda)* sin(teta) = ((pi * pin_diam)/lambda)* (x/pin_dist)
    # lambda= hPlank * cLight / Energy
    #
    hPlank= 6.626e-34  # plank
    cLight= 299792458 # speed of light
    qelectron= 1.6e-19 # electron charge
    '''
    cLight= scipy.constants.speed_of_light #6.626e-34  # plank
    hPlank= scipy.constants.Planck #299792458 # speed of light
    qelectron= scipy.constants.elementary_charge #1.6e-19 # electron charge
    '''
    #
    Energy_J= Energy_eV*qelectron
    lambda_m= hPlank * cLight /Energy_J
    auxBesselX= ((math.pi * pin_diam)/lambda_m)* (X/pin_Dist);
    auxBesselY= scipy.special.jv(1,auxBesselX)
    auxAiryY= (J0)*(2*auxBesselY /abs(auxBesselX))**2;
    #
    # set the X=0 to J0
    if numpy.isscalar(X) and (X==0.0): auxAiryY=  J0
    elif numpy.isscalar(X)==False:
        map0 = X==0.0
        auxAiryY[map0]= J0
    return auxAiryY
#
def plot_1D_data_nd_Airy(arrayX,arrayY,
                 pix0,pixPitch,
                 Energy_eV, pin_diam,pin_Dist,J0,
                 label_x,label_y,label_title):
    fig = matplotlib.pyplot.figure()
    matplotlib.pyplot.plot(arrayX, arrayY, 'o')
    arrayAX_SI= (arrayX-pix0)*pixPitch
    arrayAY= AiryDiskProfile_fun(arrayAX_SI, Energy_eV, pin_diam,pin_Dist, J0)
    matplotlib.pyplot.plot(arrayX, arrayAY, '-')
    matplotlib.pyplot.title(label_title)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.show()
    return (fig)
# ---
#
#
#
#%% Spectrum fit
def spectrum2peaks_fun(X, A0,mu0, A1,mu1, sigma):
    '''2-gaussian peaks (same sigma) function'''
    Y= gauss_fun(X, A0,mu0,sigma) + gauss_fun(X, A1,mu1,sigma)
    return Y

def spectrum2peaks_fit(X,Y, A0_h,mu0_h, A1_h,mu1_h, sigma_h):
    '''fit gaussian'''
    p0= [A0_h,mu0_h, A1_h,mu1_h, sigma_h] # initial guess for the fitting coefficients
    coeff, var_matrix = curve_fit(spectrum2peaks_fun, X, Y, p0=p0)
    A0_fit= coeff[0]
    mu0_fit= coeff[1]
    A1_fit= coeff[2]
    mu1_fit= coeff[3]
    sigma_fit= coeff[4]
    return (A0_fit,mu0_fit, A1_fit,mu1_fit, sigma_fit)

def spectrum3peaks_fun(X, A0,mu0, A1,mu1, A2,mu2, sigma):
    '''3-gaussian peaks (same sigma) function'''
    Y= gauss_fun(X, A0,mu0,sigma) + gauss_fun(X, A1,mu1,sigma) + gauss_fun(X, A2,mu2,sigma) 
    return Y

def spectrum3peaks_fit(X,Y, A0_h,mu0_h, A1_h,mu1_h, A2_h,mu2_h, sigma_h):
    '''fit gaussian'''
    p0= [A0_h,mu0_h, A1_h,mu1_h, A2_h,mu2_h, sigma_h] # initial guess for the fitting coefficients
    coeff, var_matrix = curve_fit(spectrum3peaks_fun, X, Y, p0=p0)
    A0_fit= coeff[0]
    mu0_fit= coeff[1]
    A1_fit= coeff[2]
    mu1_fit= coeff[3]
    A2_fit= coeff[4]
    mu2_fit= coeff[5]
    sigma_fit= coeff[6]
    return (A0_fit,mu0_fit, A1_fit,mu1_fit, A2_fit,mu2_fit, sigma_fit)

def spectrum4peaks_fun(X, A0,mu0, A1,mu1, A2,mu2, A3,mu3, sigma):
    '''3-gaussian peaks (same sigma) function'''
    Y= gauss_fun(X, A0,mu0,sigma) + gauss_fun(X, A1,mu1,sigma) + gauss_fun(X, A2,mu2,sigma) + gauss_fun(X, A3,mu3,sigma) 
    return Y

def spectrum4peaks_fit(X,Y, A0_h,mu0_h, A1_h,mu1_h, A2_h,mu2_h, A3_h,mu3_h, sigma_h):
    '''fit gaussian'''
    p0= [A0_h,mu0_h, A1_h,mu1_h, A2_h,mu2_h, A3_h,mu3_h, sigma_h] # initial guess for the fitting coefficients
    coeff, var_matrix = curve_fit(spectrum4peaks_fun, X, Y, p0=p0)
    A0_fit= coeff[0]
    mu0_fit= coeff[1]
    A1_fit= coeff[2]
    mu1_fit= coeff[3]
    A2_fit= coeff[4]
    mu2_fit= coeff[5]
    A3_fit= coeff[6]
    mu3_fit= coeff[7]
    sigma_fit= coeff[8]
    return (A0_fit,mu0_fit, A1_fit,mu1_fit, A2_fit,mu2_fit, A3_fit,mu3_fit, sigma_fit)
# ---
#
def Spectrum_Noise_1ph_fit(dataX,dataY, thisEnergy, verbose_flag, \
PeakNoise_min,PeakNoise_max , PeakNoise_A0,PeakNoise_mu0,PeakNoise_sig0, fit_Noise_flag,\
Peak1ph_min,Peak1ph_max , Peak1ph_A0,Peak1ph_mu0,Peak1ph_sig0, fit_1ph_flag):
    '''
    Spectrum fit (noise peak and 1-photon peak)
    '''
    #
    PeakNoise_fitA=0; PeakNoise_fitmu=0; PeakNoise_fitsig=0
    Peak1ph_fitA=0; Peak1ph_fitmu=0; Peak1ph_fitsig=0
    #
    if fit_Noise_flag==True:
        PeakNoise_data2fitX=[]; PeakNoise_data2fitY=[]
        for thisindex in range(len(dataX)):
            if (dataX[thisindex]>=PeakNoise_min) and (dataX[thisindex]<=PeakNoise_max):
                PeakNoise_data2fitX += [dataX[thisindex]]
                PeakNoise_data2fitY += [dataY[thisindex]]
        (PeakNoise_fitA,PeakNoise_fitmu,PeakNoise_fitsig)= gausslog_fit(PeakNoise_data2fitX,PeakNoise_data2fitY, PeakNoise_A0,PeakNoise_mu0,PeakNoise_sig0)
    #
    if fit_1ph_flag==True:    
        Peak1ph_data2fitX=[]; Peak1ph_data2fitY=[]
        for thisindex in range(len(dataX)):
            if (dataX[thisindex]>=Peak1ph_min) and (dataX[thisindex]<=Peak1ph_max):
                Peak1ph_data2fitX += [dataX[thisindex]]
                Peak1ph_data2fitY += [dataY[thisindex]]
        Peak1ph_data2fitY= Peak1ph_data2fitY - gauss_fun(Peak1ph_data2fitX , PeakNoise_fitA,PeakNoise_fitmu,PeakNoise_fitsig)
        (Peak1ph_fitA,Peak1ph_fitmu,Peak1ph_fitsig)= gausslog_fit(Peak1ph_data2fitX,Peak1ph_data2fitY, Peak1ph_A0,Peak1ph_mu0,Peak1ph_sig0)
    #
    aux_legend= ["data "+str(thisEnergy)+"eV"]
    if (verbose_flag==True):
        matplotlib.pyplot.figure()
        matplotlib.pyplot.semilogy(dataX,dataY,'o')
        #
        if fit_Noise_flag==True:
            print("Noise Peak best fit: A={0}, mu={1}, sigma={2}".format(PeakNoise_fitA,PeakNoise_fitmu,PeakNoise_fitsig))
            matplotlib.pyplot.semilogy(PeakNoise_data2fitX,gauss_fun(PeakNoise_data2fitX,PeakNoise_fitA,PeakNoise_fitmu,PeakNoise_fitsig),'y-' , linewidth=2)
            aux_string= "Noise Peak: " + str(float(int(PeakNoise_fitmu*100))/100) + "e"           
            aux_legend += [aux_string]
        if fit_1ph_flag==True:
            print("1-photon Peak best fit: A={0}, mu={1}, sigma={2}".format(Peak1ph_fitA,Peak1ph_fitmu,Peak1ph_fitsig))
            matplotlib.pyplot.semilogy(Peak1ph_data2fitX,gauss_fun(Peak1ph_data2fitX,Peak1ph_fitA,Peak1ph_fitmu,Peak1ph_fitsig),'r-' , linewidth=2)
            aux_string= "1-photon Peak: " + str(float(int(Peak1ph_fitmu*100))/100) + "e"
            aux_legend += [aux_string]
        matplotlib.pyplot.legend(aux_legend)
        matplotlib.pyplot.xlabel('Energy [eV]')
        matplotlib.pyplot.ylabel('occurences')
        matplotlib.pyplot.show()
    return (PeakNoise_fitA,PeakNoise_fitmu,PeakNoise_fitsig , Peak1ph_fitA,Peak1ph_fitmu,Peak1ph_fitsig)
#
