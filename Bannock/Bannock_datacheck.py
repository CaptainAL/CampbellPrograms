# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 10:27:51 2017

@author: alex.messina
"""

import pandas as pd
import datetime as dt
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

## Set Pandas display options
pd.set_option('display.large_repr', 'truncate')
pd.set_option('display.width', 120)
pd.set_option('display.max_rows', 30)
pd.set_option('display.max_columns', 6)



## CampbellSci Data INFLUENT (with Velocity)
filename = 'Bannock_INF_minute_v2.dat'
CS_dir = 'C:/Campbellsci/LoggerNet/'
## Import data
inf = pd.DataFrame.from_csv(CS_dir+filename, header=1,parse_dates=True)[2:]
## Fmt index to datetime
inf.index = pd.to_datetime(inf.index)
## Fmt data as float
for col in inf.columns:
    inf[col] = inf[col].astype('float')
    
inf['Level_filter'] = inf['Level_950'][inf['Level_950'] < 11.]
inf['Level_filter'] = inf['Level_filter'].interpolate(method='linear')

fig, (ax1,ax2) = plt.subplots(2,1,figsize=(16,8),sharex=True)
fig.suptitle(filename,fontsize=18)
# LEVEL AND VELOCITY
ax1.plot_date(inf.index,inf['Level_950'],marker='None',ls='-',c='g')
ax1.plot_date(inf.index,inf['Battery_950'],marker='None',ls='-',c='r',label='950 voltage')
ax1.plot_date(inf.index,inf['Level_filter'],marker='None',ls='-',c='b',label='interpolated Level')
ax1.set_ylabel('Level_950 (inches)',fontsize=16,color='g')
ax1.set_ylim(0,14)

ax1_1 = ax1.twinx()
#ax1_1.plot_date(inf.index,inf['Velocity_950'],marker='None',ls='-',c='r')
#ax1_1.set_ylabel('Velocity (fps)',fontsize=16,color='r')
ax1.grid(True)
ax1.legend(loc='upper left'), ax1_1.legend()

# FLOW
ax2.plot_date(inf.index,inf['Flow_950'],marker='None',ls='-',c='b')
ax2.set_ylabel('Flow_950 (gpm)',fontsize=16,color='b')

ax2_2 = ax2.twinx()
ax2_2.plot_date(inf.index,inf['rain_950'],marker='None',ls='steps-pre',c='k')
ax2_2.set_ylim(0)
#ax2_2.set_ylabel('Rain_950 (inches/min)',fontsize=16,color='k')
ax2.grid(True)
ax2.legend(), ax2_2.legend()


#%%

### CampbellSci Data EFFLUENT 1
filename = 'Bannock_EFF1_minute.dat'
CS_dir = 'C:/Campbellsci/LoggerNet/'
## Import data
eff1 = pd.DataFrame.from_csv(CS_dir+filename, header=1,parse_dates=True)[2:]
## Fmt index to datetime
eff1.index = pd.to_datetime(eff1.index)
## Fmt data as float
for col in eff1.columns:
    eff1[col] = eff1[col].astype('float')

fig, (ax1,ax2) = plt.subplots(2,1,figsize=(16,8),sharex=True)
fig.suptitle(filename,fontsize=18)
# LEVEL 
ax1.plot_date(eff1.index,eff1['Level_950'],marker='None',ls='-',c='g')
ax1.set_ylabel('Level_950 (inches)',fontsize=16,color='g')
ax1.grid(True)
# FLOW
ax2.plot_date(eff1.index,eff1['Flow_950'],marker='None',ls='-',c='b')
ax2.set_ylabel('Flow_950 (gpm)',fontsize=16,color='b')

ax2_2 = ax2.twinx()
ax2_2.plot_date(eff1.index,eff1['rain_950'],marker='None',ls='steps-pre',c='k')
ax2_2.set_ylim(0)
ax2_2.set_ylabel('Rain_950 (inches/min)',fontsize=16,color='k')
ax2.grid(True)
ax2.legend(), ax2_2.legend()


#%%
#
### CampbellSci Data EFFLUENT 2
#filename = 'Bannock_EFF2_minute_v2.dat'
#CS_dir = 'C:/Campbellsci/LoggerNet/'
### Import data
#eff2 = pd.DataFrame.from_csv(CS_dir+filename, header=1,parse_dates=True)[2:]
### Fmt index to datetime
#eff2.index = pd.to_datetime(eff2.index)
### Fmt data as float
#for col in eff2.columns:
#    eff2[col] = eff2[col].astype('float')
#
#fig, (ax1,ax2) = plt.subplots(2,1,figsize=(16,8),sharex=True)
#fig.suptitle(filename,fontsize=18)
## LEVEL 
#ax1.plot_date(eff2.index,eff2['Level_950'],marker='None',ls='-',c='g')
#ax1.set_ylabel('Level_950 (inches)',fontsize=16,color='g')
#ax1.grid(True)
## FLOW
#ax2.plot_date(eff2.index,eff2['Flow_950'],marker='None',ls='-',c='b')
#ax2.set_ylabel('Flow_950 (gpm)',fontsize=16,color='b')
#
#ax2_2 = ax2.twinx()
#ax2_2.plot_date(eff2.index,eff2['rain_950'],marker='None',ls='steps-pre',c='k')
#ax2_2.set_ylim(0)
#ax2_2.set_ylabel('Rain_950 (inches/min)',fontsize=16,color='k')
#ax2.grid(True)
#ax2.legend(), ax2_2.legend()
#
#
#
