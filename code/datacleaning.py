# %%
# -*- coding: utf-8 -*-
'''
functions related with the gathering, merging and data cleansing
@author: Gerson Colorado github@gucoloradoc
'''
import numpy as np
import pandas as pd
from datetime import timedelta
from os import path

def dfretrival(datapath, sheetpath):
    '''
    Extracts the data in excel worksheets. Very specific for the Monterrey data.
    '''
    fullsheetpath= path.join(datapath,sheetpath)
    dframe= pd.read_excel(fullsheetpath, index_col=[0,1], header=[0,1])
    dframe.index.names=['FECHA', 'HORA']
    dframe=dframe.reset_index()
    if type(dframe.HORA[0]).__name__=='time':
        timedvec=np.vectorize(lambda x: timedelta(hours=float(x.hour)))
    else:
        timedvec=np.vectorize(lambda x: timedelta(hours=float(x)))
    dframe.iloc[:,0]=dframe.iloc[:,0]+pd.Series(timedvec(dframe.iloc[:,1]))
    dframe=dframe.set_index('FECHA')
    #Reshaping to have station as value
    dframe=dframe.drop('HORA', axis=1)
    dframe.columns.names=['ESTACION', 'MEDIDA']
    return dframe

