# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 10:20:38 2019
https://github.com/yxoos/AccuparLAICalculator
@author: Amirh
"""

# =============================================================================
# Calculate LAI
# =============================================================================


import numpy as np
import glob
import matplotlib.pyplot as plt
import xlrd
import csv
from scipy.io import loadmat,savemat
import datetime
#%%

class LAI():
    """
    This algorithm reads Accupar LP-80 files, calculates per sample LAI, and 
    returns more accurate average LAI measurements. 
    
    NOTE: use raw excel file from the device!
    
    Arguments:
        filepath: the filepath of the excel file. 
    """  
    
    def __init__(self,filepath):
        self.filepath = filepath
    def calculate(self):
        book = xlrd.open_workbook(filepath)
        recordings = book.sheet_by_index(0)    
        # =============================================================================
        # get number of samples per reading
        # =============================================================================
        nrows = recordings.nrows
        means_index = []
        samples_index = []
        la_index = []
        lg_index = []
        chi_index = []
        annot_index = []
        start = 1
        for i in range(nrows):
            cells = recordings.row_slice(rowx=i,start_colx=0,end_colx=20)
            typ = cells[0].value
            if typ == "SUM":
                samples_index.append(np.arange(start,i))
                means_index.append(i)
                start = means_index[-1] + 1
                la_index.append(cells[10].value)
                lg_index.append(cells[11].value)
                chi_index.append(cells[7].value)
                annot_index.append(cells[2].value)
                
        # =============================================================================
        # going through each sample and calculating LAI
        # =============================================================================
    
        directory = filepath[:-filepath[::-1].find('.')-1] + '_CALCULATED.csv'
        with open(directory, 'w', newline='') as csvfile:
            xl_file = csv.writer(csvfile, delimiter=',')
            xl_file.writerow(["Record Type","Date and Time", "Above PAR",	"Below PAR"	,
                              "Tau [T]","Leaf Area Index [LAI]","Leaf Distribution [X]",
                              "beam Fraction [Fb]","Zenith Angle","Latitude","Longitude"])
            for i in range(len(samples_index)):
                lais = []
                for j in samples_index[i]:
                    cells = recordings.row_slice(rowx=j,start_colx=0,end_colx=22)
                    # calculating LAI per segment then averaging
                    lai_sg = []
                    Psi_sg = []
                    tau_sg = []
                    fb_sg = []
                    self.below_PAR_sg = []
                    self.above_PAR_sg = []
                    for par_segments in np.arange(12,20):    
                        self.below_PAR = cells[par_segments].value        
                        self.above_PAR = cells[20].value
                    
                        # getting time information for the sample
                        serial_num = cells[1].value #time in serial number format
                        temp = datetime.datetime(1899, 12, 30)
                        delta = datetime.timedelta(days=serial_num)
                        date = temp + delta
                        time = serial_num - int(serial_num)
                        self.J = date.timetuple().tm_yday
                        
                        loc_time_hour = time*24
                        loc_time_minute = (loc_time_hour - int(loc_time_hour))*60
                        loc_time_second = (loc_time_minute - int(loc_time_minute))*60
                        self.loc_time_hour = np.int(loc_time_hour)
                        self.loc_time_minute = np.int(loc_time_minute)
                        self.loc_time_second = np.int(loc_time_second)
                        
                        self.la = la_index[i]
                        self.lg = lg_index[i]
                        self.chi = chi_index[i]
                        self.zenith_angle()
                        self.beam_fraction()
                        self.lai_calc()
            
                        lai_sg.append(self.LAI)
                        Psi_sg.append(self.Psi)
                        tau_sg.append(self.tau)
                        fb_sg.append(self.fb)
                        self.below_PAR_sg.append(self.below_PAR)
                        self.above_PAR_sg.append(self.above_PAR)
                        
                    lai_sg = np.mean(lai_sg)
                    Psi_sg = np.mean(Psi_sg)
                    tau_sg = np.mean(tau_sg)
                    fb_sg = np.mean(fb_sg)
                    below_PAR_sg = np.mean(self.below_PAR_sg)
                    above_PAR_sg = np.mean(self.above_PAR_sg)
                    lais.append(lai_sg)
                                    
                    xl_file.writerow(["BLW",date.strftime("%m/%d/%Y")+" %d:%d:%d"%(self.loc_time_hour,self.loc_time_minute,self.loc_time_second),
                                      above_PAR_sg,below_PAR_sg,tau_sg,lai_sg,self.chi,fb_sg, Psi_sg*180/np.pi,self.la,self.lg])
            
                xl_file.writerow(["SUM",annot_index[i],"","","",np.mean(lais),"","","","",""])
            
        
    def zenith_angle(self):
    
        LC = (self.lg+75)/15 #longitude correction
        t = self.loc_time_hour - 1 + (self.loc_time_minute + self.loc_time_second/60)/60 #standard time
        
        phi = (279.575 + 0.986*self.J)*np.pi/180
        ET = (-104.7*np.sin(phi)+596.2*np.sin(2*phi)+4.3*np.sin(3*phi)- 
              12.7*np.sin(4*phi)-429.3*np.cos(phi)-2.0*np.cos(2*phi)+
              19.3*np.cos(3*phi))/3600
        t0 = 12 - ET - LC
        D = np.arcsin(0.39785*np.sin(4.869+0.0172*self.J+0.03345*np.sin(6.224+0.0172*self.J)))
        la_rad = self.la*np.pi/180
        self.Psi = np.arccos(np.sin(la_rad)*np.sin(D) + np.cos(la_rad)*np.cos(D)*np.cos(0.2618*(t-t0)))
    
    
    def beam_fraction(self):
        solar_const = 2550
        r = self.above_PAR / (solar_const * np.cos(self.Psi))
        
        if r > 0.82:
            r=0.82
        elif r<0.2:
            r = 0.2
        
        self.fb = 1.395 + r*(-14.43+r*(48.57+r*(-59.024+r*24.835)))
    
    def lai_calc(self):
        
        K = np.sqrt(self.chi**2+np.tan(self.Psi)**2)/(self.chi + 1.744*(self.chi+1.182)**(-0.733))
        a = 0.9
        
        self.tau = self.below_PAR/self.above_PAR  
        
        A = 0.283+0.785*a-0.159*(a**2)
        self.LAI = ((1-1/(2*K))*self.fb -1)*np.log(self.tau)/(A*(1-0.47*self.fb))