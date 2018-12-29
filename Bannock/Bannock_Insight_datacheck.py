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



##  INFLUENT OLD SITE
filename = 'Bannock_INF_Old.txt'
Hach_dir = 'P:/Projects-South/Environmental - Schaedler/5025-16-6015 TT WO 15 Bannock Monitoring/Data/Test Storm 2_10_2017/'
## Import data
inf_old =  pd.read_csv(Hach_dir+filename, header=1, skiprows=[0,2,3], delim_whitespace=True)
## Fmt index to datetime
inf_old.columns = ['Date','Time','Level','Vel','Flow']
inf_old.index = pd.to_datetime(inf_old['Date']+' '+inf_old['Time'])


##  INFLUENT NEW SITE
filename = 'Bannock_INF_New.txt'
Hach_dir = 'P:/Projects-South/Environmental - Schaedler/5025-16-6015 TT WO 15 Bannock Monitoring/Data/Test Storm 2_10_2017/'
## Import data
inf_new =  pd.read_csv(Hach_dir+filename, header=1, skiprows=[0,2,3], delim_whitespace=True)
## Fmt index to datetime
inf_new.columns = ['Date','Time','Level','Vel','Flow']
inf_new.index = pd.to_datetime(inf_new['Date']+' '+inf_new['Time'])

## CampbellSci Data INFLUENT (with Velocity)
filename = 'Bannock_INF_minute.dat'
CS_dir = 'C:/Campbellsci/LoggerNet/'
## Import data
inf = pd.DataFrame.from_csv(CS_dir+filename, header=1,parse_dates=True)[2:]
## Fmt index to datetime
inf.index = pd.to_datetime(inf.index)
## Fmt data as float
for col in inf.columns:
    inf[col] = inf[col].astype('float').shift(-1) #shift to get times to line up


############################
###### PLOT ################
############################
fig, (ax1,ax2,ax3) = plt.subplots(3,1,figsize=(16,8),sharex=True)
fig.suptitle(filename,fontsize=18)
# LEVEL
ax1.plot_date(inf_old.index,inf_old['Level'],marker='None',ls='-',c='g',label='Lev. old site')
ax1.plot_date(inf_new.index,inf_new['Level'],marker='None',ls='-',c='y',label='Lev. new site')

ax1.plot_date(inf.index,inf['Level_950'],marker='None',ls='--',c='r',label='Lev. Campbell')


# VELOCITY
ax2.plot_date(inf_old.index,inf_old['Vel'],marker='None',ls='-',c='b',label='Vel. old site')
ax2.plot_date(inf_new.index,inf_new['Vel'],marker='None',ls='-',c='r',label='Vel. new site')


# FLOW
ax3.plot_date(inf_old.index,inf_old['Flow'],marker='None',ls='-',c='grey',label='Flow old site')
ax3.plot_date(inf_new.index,inf_new['Flow'],marker='None',ls='-',c='k',label='Flow new site')

## FMT
ax1.set_ylabel('Level (inches)',fontsize=16,color='g')
ax2.set_ylabel('Velocity (fps)',fontsize=16,color='r')
ax3.set_ylabel('Flow (gpm)',fontsize=16,color='b')
ax1.legend(loc='upper right'), ax2.legend(loc='upper right'), ax3.legend(loc='upper right')
ax1.grid(True), ax2.grid(True), ax3.grid(True)


## RAIN
#ax2_2 = ax2.twinx()
#ax2_2.plot_date(inf.index,inf['rain_950'],marker='None',ls='steps-pre',c='k')
#ax2_2.set_ylim(0)
#ax2_2.set_ylabel('Rain_950 (inches/min)',fontsize=16,color='k')
#ax2.grid(True)
#ax2.legend(), ax2_2.legend()


