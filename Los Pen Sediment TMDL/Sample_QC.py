# -*- coding: utf-8 -*-
"""
Created on Mon Jan 09 09:37:39 2017

@author: alex.messina
"""

import pandas as pd
import datetime as dt
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

## Set Pandas display options
pd.set_option('display.large_repr', 'truncate')
pd.set_option('display.width', 180)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 10)

user_input = raw_input('Type the name of the Excel file, or drag and drop the SWAMP datasheet here: \n Example: C:/Documents/Review.xls \n \n' ).replace("\\", "/").strip('"').strip("r'") # uncomment -.strip("r'")- for use in spyder testing
SWAMP_data = pd.ExcelFile(user_input).parse(sheetname='Results',parse_dates=True,parse_cols='B,F:G,V,Y,Z,AB,AD,AE,AF,AG,AH')

print 
print 
print 'Analysis Method = ' +str(SWAMP_data.ix[1]['MethodName'])
print 'Analyte Name = ' +str(SWAMP_data.ix[1]['AnalyteName'])
print 'Units = '+ str(SWAMP_data.ix[1]['UnitName'])
print 'Method Detection Limit = '+ str(SWAMP_data.ix[1]['MDL'])
print 'Reporting Limit = '+ str(SWAMP_data.ix[1]['RL'])

print 
print

SWAMP_data = SWAMP_data.sort('StationCode')
SWAMP_data.index = range(1,len(SWAMP_data)+1)

SWAMP_data['Collection Datetime'] = pd.to_datetime(SWAMP_data['SampleDate'] +' '+ SWAMP_data['CollectionTime'])

SWAMP_data['Analysis Datetime'] = pd.to_datetime(SWAMP_data['AnalysisDate'])

SWAMP_data['HoldTime'] = SWAMP_data['Analysis Datetime'] - SWAMP_data['Collection Datetime']

print SWAMP_data[['StationCode','Collection Datetime','Analysis Datetime','HoldTime','QACode','ResQualCode','Result']]



for sample in SWAMP_data.iterrows():
    hold_time = np.timedelta64(sample[1]['HoldTime'],'ns').astype('timedelta64[D]')
    if hold_time >= dt.timedelta(days=7):
        print sample[1]['StationCode'] + ' is out of hold time!'
    else:
        pass
        
        
        
        
        
#%%

SWAMP_data = SWAMP_data[SWAMP_data['StationCode'] != 'LABQA']
SWAMP_data.index  = SWAMP_data['Collection Datetime']
SWAMP_data.index  = SWAMP_data.index.to_pydatetime()

fig, ax = plt.subplots(1,1,figsize=(16,6))
ax.plot_date(SWAMP_data.index, SWAMP_data['Result'].values,ls='-')
ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%m/%d %H:%M'))
ax.set_ylabel('SSC (mg/L)')
ax.set_title(user_input.split('/')[-3:])      

ax.text(0.5, 0.9, str(SWAMP_data.ix[1]['StationCode'])[:-3],
        horizontalalignment='right',
        verticalalignment='top',
        transform=ax.transAxes)
        
        
        