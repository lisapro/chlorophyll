# coding=utf8
'''
Created on 5. mar. 2018

@author: ELP
'''

import matplotlib
import pandas as pd 
import numpy as np
import re
import seaborn as sns
import matplotlib.pyplot as plt 
sns.set()

def get_station(df,name):
    df_st = df.where(df.StationName == name)
    return df_st

def get_station_2names(df,name1,name2):
    df_st = df.loc[(df.StationName == name1)|(df.StationName == name2)].copy()
    return df_st

def filter_by_depth(indf,depth):     
    return indf.loc[indf['Depth1'] == depth] 

def get_year(df,yr):
    # Function choose only one needed year from the dataframe
    #1 convert format of dates column to datetime
    df.toDate = pd.to_datetime(df.toDate, format='%d.%m.%Y %X') 
    #2 choose the year  
    df_year = df.where(df.toDate.dt.year == yr).dropna(how='all')
    #3 set date as index (first) column
    df_year = df_year.set_index('toDate').sort_index()
    #4 interpolate by month and get the max value 
    df_year = df_year.resample('M').max() 
    return df_year

Months = ('Jan', 'Feb', 'Mar', 'Apr', 'May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')
labels = ('2013','2014','2015','2016','2017','2018')
a=1
ind = np.arange(1,14) 
width = 0.1

def plot_station(df,name):
      # Function to plot the bar from dataframe
      # datagrame contains data from one station
      df_2013 = get_year(df,2013)
      df_2014 = get_year(df,2014)
      df_2015 = get_year(df,2015)
      df_2016 = get_year(df,2016)
      df_2017 = get_year(df,2017)
      df_2018 = get_year(df,2018)
      
      # create figure (fig) and subplot (ax)
      fig, ax = plt.subplots(figsize = (11,3))
      
      #loop over files with data from diff years, k,v is key,value 
      for k,v in enumerate([df_2013,df_2014,df_2015,df_2016,df_2017,df_2018],start = 1): #]
            ax.bar(v.index.month.values+0.9*(width*k),v.KrA.values,alpha = a,width =  width,label = labels[k-1])

      ax.set_ylabel(r'$Klorfyll-A\ \mu g L^{-1}$')
      ax.set_xticks(df_2013.index.month.values+0.9*(width*4))
      ax.set_xticklabels(Months)
      ax.legend()
      ax.set_title(name)
      plt.savefig('{}.png'.format(name))
      #plt.show()
      
file = r'klf_vt71_vt72.xlsx'
        
dff = pd.read_excel(file,sheet_name=1,skiprows = 1)

#get only needed columns 
df = dff.iloc[:,[4,5,6,10]]
#rename columns
df.columns = ['StationName','toDate' ,'Depth1','KrA']

df = df.replace({'KrA': r'^< 0.16$'}, {'KrA': '0.1'}, regex=True)
df = df.replace({'KrA': r'^< 0.25$'}, {'KrA': '0.1'}, regex=True)
df.KrA= pd.to_numeric(df.KrA) 
df = df.drop_duplicates()


df_skinn = get_station(df,'Skinnbrokleia')
#df_skinn = df_skinn[df_skinn['Depth1'] == 5].copy()
plot_station(df_skinn,'Skinnbrokleia')
plt.clf()


df_heroy = get_station_2names(df,'Herøyfjorden_SOOP','Herøyfjorden')
#df_heroy= df_heroy[df_heroy['Depth1'] == 4].copy()
plot_station(df_heroy,'Herøyfjorden')