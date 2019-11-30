
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[1]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[56]:

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
get_ipython().magic('matplotlib notebook')


df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')


mintem = []
maxtem = []
# 去掉02-29日期的数据
df = df[~(df['Date'].str.endswith(r'02-29'))]
# 将date列的str转换为datetime64[ns]类型
times1 = pd.DatetimeIndex(df['Date'])

# 生成新的不包括2015年数据的dataframe
df1 = df[times1.year != 2015]
# 将date列的str转换为datetime64[ns]类型
times = pd.DatetimeIndex(df1['Date'])
# !!!重要！！！
for j in df1.groupby([times.month, times.day]):
    mintem.append(min(j[1]['Data_Value']))
    maxtem.append(max(j[1]['Data_Value']))

# 生成2015年的数据集
df2015 = df[times1.year == 2015]
# 将date列的str转换为datetime64[ns]类型
times2015 = pd.DatetimeIndex(df2015['Date'])

mintem2015 = []
maxtem2015 = []
for j in df2015.groupby([times2015.month, times2015.day]):
    mintem2015.append(min(j[1]['Data_Value']))
    maxtem2015.append(max(j[1]['Data_Value']))
    
minaxis = []
maxaxis = []
minvals = []
maxvals = []
for i in range(len(mintem)):
    if((mintem[i] - mintem2015[i]) > 0):
        minaxis.append(i)
        minvals.append(mintem2015[i])
    if((maxtem[i] - maxtem2015[i]) < 0):
        maxaxis.append(i)
        maxvals.append(maxtem2015[i])
    
plt.figure()
colors = ['steelblue','indinared']
plt.plot(mintem, color='steelblue', alpha=0.5, label='Minimum temperature between 2005-2014')
plt.plot(maxtem, color='indianred', alpha=0.5, label='Maximum temperature between 2005-2014')
plt.scatter(minaxis, minvals, s = 5, c = 'red', alpha = 0.8, label = '2015 Break the Minimum Record')
plt.scatter(maxaxis, maxvals, s = 5, c = 'blue', alpha = 0.8, label = '2015 Break the Maximum Record')
plt.gca().fill_between(range(len(mintem)), 
                       mintem, maxtem, 
                       facecolor='gray', 
                       alpha=0.2)


plt.ylim(-400, 500)
plt.legend(loc = 8, frameon=False, fontsize=6)
plt.xticks( np.linspace(15,15 + 30*11 , num = 12), (r'Jan', r'Feb', r'Mar', r'Apr', r'May', r'Jun', r'Jul', r'Aug', r'Sep', r'Oct', r'Nov', r'Dec') )
plt.xlabel('Month')
plt.ylabel('Temperature (tenths of degrees C)')
plt.title(r'Extreme temperature by months')

plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)

    
plt.show()



# In[ ]:



