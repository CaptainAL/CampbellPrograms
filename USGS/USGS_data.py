# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 12:38:24 2017

@author: alex.messina
"""




import datetime as dt
import pandas as pd
from tsgettoolbox import tsgettoolbox

def nwis_heat_map(site_name,data):
    from scipy.interpolate import griddata
    import matplotlib.cm as cm
    import matplotlib as mpl
    
    meth = 'linear'  # 'nearest'

    if isinstance(data.index, pd.core.index.MultiIndex):
        data.index = data.index.droplevel(0)

    x = data.index.dayofyear
    y = data.index.year
    z = data.values.ravel()

    xi = np.linspace(x.min(), x.max(), 1000)
    yi = np.linspace(y.min(), y.max(), 1000)
    zi = griddata((x, y), z, (xi[None, :], yi[:, None]), method=meth)

    cmap = plt.cm.get_cmap('RdYlBu')
    norm = mpl.colors.Normalize(vmin=min(z), vmax=max(z))
    norm = mpl.colors.LogNorm(vmin=0.1, vmax=100000)
    m = cm.ScalarMappable(norm=norm, cmap=cmap)
    m.set_array(z)

    fig, ax = plt.subplots(1,1,figsize=(10,9))
    br = plt.contourf(xi, yi, zi, color=m.to_rgba(z), cmap=cmap)
    # setup the colorbar
    cbar = plt.colorbar(m)
    cbar.set_label('Discharge (cfs)')

    plt.xlabel('Month')
    plt.ylabel('Year')
    plt.yticks(range(y.min(), y.max()))

    mons = {'Apr': 90.25, 'Aug': 212.25, 'Dec': 334.25, 'Feb': 31, 'Jan': 1, 'Jul': 181.25, 'Jun': 151.25,
            'Mar': 59.25, 'May': 120.25,
            'Nov': 304.25, 'Oct': 273.25, 'Sep': 243.25}
    monnms = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    plt.title(site_name)
    tickplc = []
    plt.xticks([mons[i] for i in monnms], monnms)
    plt.grid()
    
    return

def get_nwis(service='dv',sites=''):
    df = tsgettoolbox.nwis(database=service,sites=sites,startDT='1900-01-01',endDT='2017-03-22',parameterCd='00060')
    df.index = pd.to_datetime(df.index,utc=True).tz_localize(None)
    return df

SDR_FashionValley = get_nwis('dv','11023000')
## Heat map
nwis_heat_map('SDR Fashion Valley',SDR_FashionValley)
## Timeseries
#SDR_FashionValley.plot()


#SDR_MastRoad = get_nwis('dv','11022480')
### Heat map
#nwis_heat_map('SDR Mast Road',SDR_MastRoad)
### Timeseries
#SDR_MastRoad.plot()



LoganRiver = get_nwis('dv','10109000')
## Heat map
nwis_heat_map('Logan River, UT',LoganRiver)
## Timeseries
#LoganRiver.plot()



# ex. Logan river
#q = wa.nwis('dv','10109000','sites')

## ALL Local USGS sites
#import wellapplication as wa
#q = wa.nwis('dv','18070304','huc')
#site_info = q.get_info()
#site_info = site_info[site_info['data_type_cd'].isin(['ST','ST-CA', 'ST-DCH'])]
### drop duplicates
#site_info = site_info.drop_duplicates(subset='station_nm',keep='first')





