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



##  INFLUENT AVB Primary
filename = 'Bannock_INF_test_AVBprimary.txt'
Hach_dir = ''
## Import data
inf_AVBprim =  pd.read_csv(Hach_dir+filename, header=1, skiprows=[0,2,3], delim_whitespace=True)
## Fmt index to datetime
inf_AVBprim.columns = ['Date','Time','Level','Vel','Flow']
inf_AVBprim.index = pd.to_datetime(inf_AVBprim['Date']+' '+inf_AVBprim['Time'])


##  INFLUENT AVB Secondary
filename = 'Bannock_INF_test_AVBsecondary.txt'
Hach_dir = ''
## Import data
inf_AVBsec =  pd.read_csv(Hach_dir+filename, header=1, skiprows=[0,2,3], delim_whitespace=True)
## Fmt index to datetime
inf_AVBsec.columns = ['Date','Time','Level','Flow']
inf_AVBsec.index = pd.to_datetime(inf_AVBsec['Date']+' '+inf_AVBsec['Time'])


##  INFLUENT AVB Secondary
filename = 'Bannock_INF_test_MetalRing.txt'
Hach_dir = ''
## Import data
inf_MetRing =  pd.read_csv(Hach_dir+filename, header=1, skiprows=[0,2,3], delim_whitespace=True)
## Fmt index to datetime
inf_MetRing.columns = ['Date','Time','Level','Flow']
inf_MetRing.index = pd.to_datetime(inf_MetRing['Date']+' '+inf_MetRing['Time'])


## EFFLUENT 1 - Rain
filename = 'Bannock_EFF1_test.txt'
Hach_dir = ''
## Import data
eff1 =  pd.read_csv(Hach_dir+filename, header=1, skiprows=[0,2,3], delim_whitespace=True)
## Fmt index to datetime
eff1.columns = ['Date','Time','Rain','Level','Flow']
eff1.index = pd.to_datetime(eff1['Date']+' '+eff1['Time'])
eff1['Rain_15'] = eff1['Rain'].resample('15Min',how='sum')


############################
###### PLOT ################
############################
fig, (ax1,ax2,ax3) = plt.subplots(3,1,figsize=(16,8),sharex=True)
#fig.suptitle(filename,fontsize=18)
# LEVEL
ax1.plot_date(inf_AVBprim.index,inf_AVBprim['Level'],marker='None',ls='-',c='g',label='AVB primary')
ax1.plot_date(inf_AVBsec.index,inf_AVBsec['Level'],marker='None',ls='-',c='y',label='AVB secondary')
ax1.plot_date(inf_MetRing.index,inf_MetRing['Level'],marker='None',ls='-',c='r',label='Metal Ring')

# VELOCITY
ax2.plot_date(inf_AVBprim.index,inf_AVBprim['Vel'],marker='None',ls='-',c='r',label='AVB primary')

# FLOW
ax3.plot_date(inf_AVBprim.index,inf_AVBprim['Flow'],marker='None',ls='-',c='g',label='AVB primary')
ax3.plot_date(inf_AVBsec.index,inf_AVBsec['Flow'],marker='None',ls='-',c='y',label='AVB secondary')
ax3.plot_date(inf_MetRing.index,inf_MetRing['Flow'],marker='None',ls='-',c='r',label='Metal Ring')

## FMT
ax1.set_ylabel('Level (inches)',fontsize=16,color='g')
ax2.set_ylabel('Velocity (fps)',fontsize=16,color='r')
ax3.set_ylabel('Flow (gpm)',fontsize=16,color='b')
ax1.grid(True), ax2.grid(True), ax3.grid(True)

## Rain
for ax in fig.axes:
    ax_2 = ax.twinx()
    ax_2.plot_date(eff1['Rain_15'].dropna().index,eff1['Rain_15'].dropna(),marker='None',ls='steps-post',c='b',alpha=0.5,label='rain')
    ax_2.set_ylabel('Rain_950 \n (inches/15min)',fontsize=16,color='b')
    ax.legend(loc='upper right')

plt.tight_layout()