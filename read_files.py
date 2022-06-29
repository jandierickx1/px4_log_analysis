#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  6 11:45:57 2022

@author: Jan Dierickx
"""

from functools import reduce
import os
import pandas as pd


def read_log_file(filename, parameters):
    
    os.system('mkdir temp')
    os.chdir('temp')
    try:
        os.system('cp ../' + filename + ' .')
        os.system('ulog2csv ' + filename)
        data_frames = []
        for ii in range(len(parameters)):
            data_frames.append(pd.read_csv(filename[:-4] + '_' + parameters[ii] + '.csv'))
            data_frames[ii].timestamp = pd.to_datetime(data_frames[ii]['timestamp'], unit='us')
            #data_frames[ii].timestamp = pd.Series([val.time() for val in data_frames[ii].timestamp])
     
    finally:
        os.chdir('..')
        os.system('rm -r temp')
    
    
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['timestamp'],
                                            how='outer'), data_frames)
    df_merged = df_merged.set_index('timestamp')
    
    df_merged.sort_index(inplace=True)
    df_merged.interpolate(inplace=True)
    
    return df_merged
