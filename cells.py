# coding=utf8
'''
Created on 5. mar. 2018

@author: ELP
'''
import pandas as pd 
import numpy as np
import seaborn as sns #sets up styles and gives us more plotting options
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
sns.set()
sns.set_context("paper")
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import matplotlib.ticker as mtick 

a = 1
colors = ['#ee9a55','#4b85af','#BEBEBE']
one = 'kiselalger'
two = 'fureflagellater'
three = 'Andre flagellater og monader'
path = r'K:\Avdeling\214-Oseanografi\DATABASER\OKOKYST_2017\Planktontellinger_2018\NorskehavetNord1,2,3 og Barentshavet'

def plot_station(path_cell,path_carb_bugoynes,path_chla,sheet,stationname,to_title):
    
    
    file = r'{}{}'.format(path,path_cell)
    file2 = r'{}{}'.format(path,path_carb_bugoynes)
    file_klor = r'{}{}'.format(path,path_chla)

    to_names= pd.read_excel(file,nrows = 1,skiprows = 3).values[0]
    to_names[0:3] = ['x','blank','type']
    to_names2= pd.read_excel(file2,nrows = 1,skiprows = 3).values[0]
    to_names2[0:3] = ['x','blank','type']

    #cols_in_file = [0,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    df = pd.read_excel(file,names = to_names)[4:] 
    df2 = pd.read_excel(file2,names = to_names)[4:]          
                                                                    
    df = df.replace({ r'^.$'}, {np.nan}, regex=True)         
    df2 = df2.replace({ r'^.$'}, {np.nan}, regex=True)      

    df3 = pd.read_excel(file_klor,sheet_name = sheet)
    df3 = df3.replace({ r'<17$'}, {0}, regex=True)  
    df3 = df3.replace({ r'< 0.17$'}, {0}, regex=True)         
    df3 = df3.replace({ r'< 0.16$'}, {0}, regex=True)     
    df3 = df3.replace({ r'< 0,16$'}, {0}, regex=True)     
    df3 = df3.replace({ r'< 0,22$'}, {0}, regex=True)   
    df3 = df3.replace({ r'< 0.21$'}, {0}, regex=True)     
    df3 = df3.replace({ r'<*$'}, {0}, regex=True) 
    
    def get_sum(df):
        new_df = pd.DataFrame()
        for n in range(1,4):
            d = df[df['x'] == n]
            d= d.transpose().drop(['x','blank','type'], axis=0)
            d = d.sum(axis = 1)
            new_df[str(n)] = d
        return new_df

    new_df = get_sum(df)
    new_df2 = get_sum(df2)

    fig = plt.figure(figsize=(11, 6))

    ax0 = fig.add_subplot(3, 1, 1) # row-col-num
    ax = fig.add_subplot(3, 1, 2) # row-col-num
    ax1 = fig.add_subplot(3, 1, 3) 
    

    dates = to_names[3:] 
    dates2 = to_names2[3:] 

    try:    
        dates3 = pd.to_datetime(df3['sampledate_{}'.format(stationname)], format='%d.%m.%Y') 
    except ValueError:
        dates3 = pd.to_datetime(df3['sampledate_{}'.format(stationname)], format='%d.%m.%Y %H:%M:%S')   
    except ValueError:
        dates3 = pd.to_datetime(df3['sampledate_{}'.format(stationname)], format='%d-Y-%m-%d')   

    ax0.set_xticks(dates3)
    ax.set_xticks(dates)
    ax1.set_xticks(dates2)  

    for axis in [ax0,ax1,ax]:
        axis.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))
        axis.tick_params(axis='x', rotation=30)
        axis.set_xlim(dates[0],dates[-1])

    df3 = df3.dropna(how = 'all') 

    ax0.plot(dates3 ,df3[stationname])

    ax1.fill_between(dates, 0, new_df['1'],label = one,alpha = a,color = colors[0])
    ax.fill_between(dates2, 0, new_df2['1'],label = one,alpha = a,color = colors[0])

    ax1.fill_between(dates, new_df['1'], new_df['1']+new_df['2'],label = two,alpha = a,color = colors[1])
    ax.fill_between(dates2, new_df2['1'], new_df2['1']+new_df2['2'],label = two,alpha = a,color = colors[1])

    ax1.fill_between(dates, new_df['1']+new_df['2'], new_df['1']+new_df['2']+new_df['3'],label = three,alpha = a,color = colors[2])
    ax.fill_between(dates2, new_df2['1']+new_df2['2'], new_df2['1']+new_df2['2']+new_df2['3'],label = three,alpha = a,color = colors[2])

    ax0.set_ylabel(r'Cellekarbon ($\mu g/L$)')
    ax.set_ylabel( r'Klorofyll a $(\mu g/L)$')
    ax1.set_ylabel(r'Antall celler/L')

    ax0.set_title(r'{}: Klorofyll a $(\mu g/L)$'.format(to_title))        
    ax.set_title( r'{}: Fytoplankton cellekarbon ($\mu g/L$)'.format(to_title))
    ax1.set_title(r'{}: Fytoplankton antall celler'.format(to_title))   

    def fmt(x, pos):
        a, b = '{:.1e}'.format(x).split('e')
        b = int(b)
        return r'${} \times 10^{{{}}}$'.format(a, b)

    ax1.yaxis.set_major_formatter( mtick.FuncFormatter(fmt))

    ax.legend(loc = 'best')
    ax1.legend(loc = 'best')

    fig.tight_layout(pad = 0.3)

    #plt.savefig(r'{}\Plot\{}.png'.format(path,to_title))
    plt.show()
    #print (new_df)

path_chla = '\klorofyll Norskehavet 1_3_Barentshavet.xlsx'


path_carb_bugoynes = '\Barentshavet\Bugøynes_karbon_2017_2018.xlsx'
path_cell_bugoynes = '\Barentshavet\Bugøynes_celler.L_2017_2018.xlsx'  


path_carb_langfjordnes = '\Barentshavet\Langfjordnes_karbon_2017_2018.xlsx'
path_cell_langfjordnes = '\Barentshavet\Langfjordnes_celler.L_2017_2018.xlsx'  


path_carb_Tanafjord = '\Barentshavet\Tanafjorden_VR24_Karbon_2018.xlsx'
path_cell_Tanafjord = '\Barentshavet\Tanafjord_VR24_celler.L_2018.xlsx'  

path_carb_kongsbakk = r'\Norskehavet Nord 1\kongsbakk_karbon_2017_2018.xlsx'
path_cell_kongsbakk = r'\Norskehavet Nord 1\kongsbakk_celler.L_2017_2018.xlsx'

path_carb_straumsfj = r'\Norskehavet Nord 1\straumsfj_karbon_2017_2018.xlsx'
path_cell_straumsfj = r'\Norskehavet Nord 1\Straumsfj_celler.L_2017_2018.xlsx'

path_cell_tjukkenes = r'\Norskehavet Nord 1\tjukkenes_celler.L_2017_2018.xlsx'
path_carb_tjukkenes = r'\Norskehavet Nord 1\tjukkenes_karbon_2017_2108.xlsx'

path_cell_alvenes = r'\Norskehavet Nord 2\alvenes_celler.L_2017_2018.xlsx'
path_carb_alvenes = r'\Norskehavet Nord 2\alvenes_karbon_2017_2018.xlsx'

path_cell_Setså = r'\Norskehavet Nord 2\setså_celler.L_2017_2018.xlsx'
path_carb_Setså = r'\Norskehavet Nord 2\setså_karbon_2017_2018.xlsx'

path_cell_Reisafjorden = r'\Norskehavet Nord 3\Reisafj_celler.L_2018.xlsx'
path_carb_Reisafjorden = r'\Norskehavet Nord 3\Reisafj_karbon_2018.xlsx'

path_cell_Spilderbu =  r'\Norskehavet Nord 3\Spilderbu_celler.L_2018.xlsx'
path_carb_Spilderbu =  r'\Norskehavet Nord 3\spilderbu_karbon_2018.xlsx'

path_cell_Storbukta =  r'\Norskehavet Nord 3\Storbukta_celler.L_2018.xlsx'
path_carb_Storbukta =  r'\Norskehavet Nord 3\Storbukta_karbon_2018.xlsx'

path_cell_Sørfj =  r'\Norskehavet Nord 3\Sørfj_ytre_celler.L_2018.xlsx'
path_carb_Sørfj =  r'\Norskehavet Nord 3\Sørfj_ytre_karbon_2018.xlsx'

path_cell_Ullsfj =  r'\Norskehavet Nord 3\Ullsfj_celler.L_2918.xlsx'
path_carb_Ullsfj =  r'\Norskehavet Nord 3\Ullsfj_karbon_2018.xlsx'

path_cell_Ytre =  r'\Norskehavet Nord 3\Ytre kvæn_celler.L_2018.xlsx'
path_carb_Ytre =  r'\Norskehavet Nord 3\Ytre kvæn_karbon_2018.xlsx'



'''plot_station(path_cell_bugoynes,     path_carb_bugoynes,    path_chla, sheet = 'Barentshavet', stationname ='Bugøynes',     to_title = 'VT22')    
plot_station(path_cell_langfjordnes, path_carb_langfjordnes,path_chla, sheet = 'Barentshavet', stationname ='langfjordnes', to_title = 'langfjordnes')    
plot_station(path_cell_Tanafjord,    path_carb_Tanafjord,   path_chla, sheet = 'Barentshavet', stationname ='Tanafjorden',  to_title = 'VR24')

plot_station(path_cell_kongsbakk,    path_carb_kongsbakk,   path_chla, sheet = 'Nord1Norskehavet', stationname ='Kongsbakkneset',      to_title = 'Kongsbakkneset')
plot_station(path_cell_straumsfj,    path_carb_straumsfj,   path_chla, sheet = 'Nord1Norskehavet', stationname ='StraumsfjordenVR54',  to_title = 'VR54')
plot_station(path_cell_tjukkenes,    path_carb_tjukkenes,   path_chla, sheet = 'Nord1Norskehavet', stationname ='Tjukkeneset',         to_title = 'Tjukkeneset')

plot_station(path_cell_alvenes,      path_carb_alvenes,     path_chla, sheet = 'Nord2Norskehavet', stationname ='Alvenes',  to_title = 'Alvenes')
plot_station(path_cell_Setså,        path_carb_Setså,       path_chla, sheet = 'Nord2Norskehavet', stationname ='Setså',  to_title = 'Setså')
plot_station(path_cell_Reisafjorden,        path_carb_Reisafjorden,       path_chla, sheet = 'Norskehavet3', stationname ='Reisafjorden',  to_title = 'Reisafjorden')

plot_station(path_cell_Spilderbu,        path_carb_Spilderbu,       path_chla, sheet = 'Norskehavet3', stationname ='Spilderbukta',  to_title = 'Spilderbukta')
plot_station(path_cell_Storbukta,        path_carb_Storbukta,       path_chla, sheet = 'Norskehavet3', stationname ='Storbukta',  to_title = 'Storbukta')
plot_station(path_cell_Sørfj,        path_carb_Sørfj,       path_chla, sheet = 'Norskehavet3', stationname ='SørfjordenYtre',  to_title = 'SørfjordenYtre')
plot_station(path_cell_Ullsfj,        path_carb_Ullsfj,       path_chla, sheet = 'Norskehavet3', stationname ='Ullsfjorden',  to_title = 'Ullsfjorden')'''
plot_station(path_cell_Ytre,        path_carb_Ytre,       path_chla, sheet = 'Norskehavet3', stationname ='YtreKvænangen',  to_title = 'YtreKvænangen')