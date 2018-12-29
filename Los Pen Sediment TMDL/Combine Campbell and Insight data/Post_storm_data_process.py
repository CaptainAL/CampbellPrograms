# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 12:42:36 2016

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


## HACH Flowmeter Data from Insight export
filename = 'CCC-00000003.000-01-04-2017-for Campbell.txt'
## Directory
Hach_dir = 'C:/Program Files (x86)/Hach/Insight/DATA/TEXT/'
## Import flowmeter Level data  
flowfile = pd.read_csv(Hach_dir+filename, header=1, skiprows=[0,2,3], delim_whitespace=True)
flowfile.columns = ['Date','Time','Level','Flow1']
flowfile.index = pd.to_datetime(flowfile['Date']+' '+flowfile['Time'])

## CampbellSci Sample History
filename = 'Carroll Canyon_Sample_History.dat'
CS_dir = 'C:/Campbellsci/LoggerNet/'
## Import Sample History data
sample_history = pd.DataFrame.from_csv(CS_dir+filename, header=1,parse_dates=True)[2:]
sample_history.index = pd.to_datetime(sample_history.index)
## Make float...which is lame should be automatic
sample_history['pulses_sent_to_sampler'] = sample_history['pulses_sent_to_sampler'].astype('float')
sample_history['Success_Max'] = sample_history['Success_Max'].astype('float')
sample_history['Bottle_Max'] = sample_history['Bottle_Max'].astype('float')
## Make datetimes and round to minutes to match up with flowmeter data
sample_history['pulses_sent_to_sampler_TMx'] = pd.to_datetime(sample_history['pulses_sent_to_sampler_TMx']).values.astype('<M8[m]')
sample_history['Bottle_TMx'] = pd.to_datetime(sample_history['Bottle_TMx']).values.astype('<M8[m]')
sample_history['Success_TMx'] = pd.to_datetime(sample_history['Success_TMx']).values.astype('<M8[m]')

## Cut out samples where Success was 0
sample_history = sample_history[sample_history['Success_Max']>0]

## Add Level data to Sample times
samples_level = pd.DataFrame(flowfile['Level'].ix[sample_history['pulses_sent_to_sampler_TMx'].values].dropna())
## Add sample number
samples_level['Sample_Num'] = sample_history['pulses_sent_to_sampler'].astype('int').values 


#%%

## Plot Flowmeter LEVEL
fig, ax = plt.subplots(1,1,figsize=(14,6))
ax.plot_date(flowfile.index,flowfile['Level'],ls='-',marker='None',label='Flowmeter')
## Plot Sample Times
ax.plot_date(samples_level.index,samples_level['Level'],c='r',marker='o',markersize=12,label='SSC grab')
## Label Sample #
for label, x, y in zip(samples_level['Sample_Num'].values, samples_level.index.values, samples_level['Level'].values):
    print label, pd.Timestamp(x), y
    ax.annotate(label, xy = (mdates.date2num(pd.Timestamp(x)), y),xytext=(-8, 30),textcoords='offset points', arrowprops=dict(facecolor='black',arrowstyle='-|>'))
# FMT
ax.set_ylabel('Level (inches)',fontsize=14)
plt.title('Level and Sample Collection Times for CCC 12/15-16/2016')
ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%m/%d %H:%M'))

#%%


def plot_level_and_samples(name,flowdata,samplehistory):
    ## HACH Flowmeter Data from Insight export
    filename = flowdata
    ## Directory
    Hach_dir = 'C:/Program Files (x86)/Hach/Insight/DATA/TEXT/'
    ## Import flowmeter Level data  
    flowfile = pd.read_csv(Hach_dir+filename, header=1, skiprows=[0,2,3], delim_whitespace=True)
    try:
        flowfile.columns = ['Date','Time','Level','Flow1']
    except:
        flowfile.columns = ['Date','Time','Level']
    flowfile.index = pd.to_datetime(flowfile['Date']+' '+flowfile['Time'])
    
    ## CampbellSci Sample History
    filename = samplehistory
    CS_dir = 'C:/Campbellsci/LoggerNet/'
    ## Import Sample History data
    sample_history = pd.DataFrame.from_csv(CS_dir+filename, header=1,parse_dates=True)[2:]
    sample_history.index = pd.to_datetime(sample_history.index)
    ## Make float...which is lame should be automatic
    sample_history['pulses_sent_to_sampler'] = sample_history['pulses_sent_to_sampler'].astype('float')
    sample_history['Success_Max'] = sample_history['Success_Max'].astype('float')
    sample_history['Bottle_Max'] = sample_history['Bottle_Max'].astype('float')
    ## Make datetimes and round to minutes to match up with flowmeter data
    sample_history['pulses_sent_to_sampler_TMx'] = pd.to_datetime(sample_history['pulses_sent_to_sampler_TMx']).values.astype('<M8[m]')
    sample_history['Bottle_TMx'] = pd.to_datetime(sample_history['Bottle_TMx']).values.astype('<M8[m]')
    sample_history['Success_TMx'] = pd.to_datetime(sample_history['Success_TMx']).values.astype('<M8[m]')
    ## Cut out samples where Success was 0
    sample_history = sample_history[sample_history['Success_Max']>0]
    ## Add Level data to Sample times
    samples_level = pd.DataFrame(flowfile['Level'].ix[sample_history['pulses_sent_to_sampler_TMx'].values].dropna())
    ## Add sample number
    samples_level['Sample_Num'] = sample_history['pulses_sent_to_sampler'].astype('int').values 
    
    ## Plot Flowmeter LEVEL
    fig, ax = plt.subplots(1,1,figsize=(14,6))
    ax.plot_date(flowfile.index,flowfile['Level'],ls='-',marker='None',label='Flowmeter')
    ## Plot Sample Times
    ax.plot_date(samples_level.index,samples_level['Level'],c='r',marker='o',markersize=12,label='SSC grab')
    ## Label Sample #
    for label, x, y in zip(samples_level['Sample_Num'].values, samples_level.index.values, samples_level['Level'].values):
        print label, pd.Timestamp(x), y
        ax.annotate(label, xy = (mdates.date2num(pd.Timestamp(x)), y),xytext=(-8, 30),textcoords='offset points', arrowprops=dict(facecolor='black',arrowstyle='-|>'))
    # FMT
    ax.set_ylabel('Level (inches)',fontsize=14)
    plt.title('Level and Sample Collection Times for '+name)
    ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%m/%d %H:%M'))
    return 

plot_level_and_samples('Carroll Canyon','CCC-00000003.000-01-04-2017-for Campbell.txt','Carroll Canyon_Sample_History.dat')


















