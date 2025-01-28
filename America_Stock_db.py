import pandas as pd
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import calendar
import requests
import sqlite3,os
from pandas.io.sql import table_exists

date = datetime.today().date() + relativedelta(months=-3)                                                  #this website provide monthly data three months before current month 
year = date.year
month = date.month
day = calendar.monthrange(year,month)[1]
timestamp = pd.to_datetime(str(year)+ '-' + str(month) + '-' + str(day) + ' 16:00:00').timestamp() * 1000  #changed to timestamp
timestamp = str(int(timestamp))

url = 'https://www.wantgoo.com/investrue/dji/historical-monthly-candlesticks?before='+timestamp+'&top=490'  #Dow Jone index
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
          AppleWebKit/537.36 (KHTML, like Gecko)\
          Chrome/108.0.0.0 Safari/537.36',}
html = requests.get(url,headers=headers).json()
data_dj = pd.DataFrame({'Date':datetime.fromtimestamp(html[i]['time']/1000).date().strftime('%Y-%m-%d'),
                     'close_dj':html[i]['close'],
                     'open_dj':html[i]['open'],
                     'high_dj':html[i]['high'],
                     'low_dj':html[i]['low'],
                     'volume_dj':html[i]['volume']
                     } for i in range(len(html)))
data_dj.set_index('Date',inplace=True)
data_dj.sort_index(ascending=True,inplace=True)

url = 'https://www.wantgoo.com/investrue/nas/historical-monthly-candlesticks?before='+timestamp+'&top=490'  #NASDAQ index
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
          AppleWebKit/537.36 (KHTML, like Gecko)\
          Chrome/108.0.0.0 Safari/537.36',}
html = requests.get(url,headers=headers).json()
data_nas = pd.DataFrame({'Date':datetime.fromtimestamp(html[i]['time']/1000).date().strftime('%Y-%m-%d'),
                     'close_nas':html[i]['close'],
                     'open_nas':html[i]['open'],
                     'high_nas':html[i]['high'],
                     'low_nas':html[i]['low'],
                     'volume_nas':html[i]['volume']
                     } for i in range(len(html)))
data_nas.set_index('Date',inplace=True)
data_nas.sort_index(ascending=True,inplace=True)

url = 'https://www.wantgoo.com/investrue/sox/historical-monthly-candlesticks?before='+timestamp+'&top=490'  #SOX index
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
          AppleWebKit/537.36 (KHTML, like Gecko)\
          Chrome/108.0.0.0 Safari/537.36',}
html = requests.get(url,headers=headers).json()
data_sox = pd.DataFrame({'Date':datetime.fromtimestamp(html[i]['time']/1000).date().strftime('%Y-%m-%d'),
                     'close_sox':html[i]['close'],
                     'open_sox':html[i]['open'],
                     'high_sox':html[i]['high'],
                     'low_sox':html[i]['low'],
                     'volume_sox':html[i]['volume']
                     } for i in range(len(html)))
data_sox.set_index('Date',inplace=True)
data_sox.sort_index(ascending=True,inplace=True)

url = 'https://www.wantgoo.com/investrue/sp5/historical-monthly-candlesticks?before='+timestamp+'&top=490'  #SP500 index
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
          AppleWebKit/537.36 (KHTML, like Gecko)\
          Chrome/108.0.0.0 Safari/537.36',}
html = requests.get(url,headers=headers).json()
data_sp5 = pd.DataFrame({'Date':datetime.fromtimestamp(html[i]['time']/1000).date().strftime('%Y-%m-%d'),
                     'close_sp5':html[i]['close'],
                     'open_sp5':html[i]['open'],
                     'high_sp5':html[i]['high'],
                     'low_sp5':html[i]['low'],
                     'volume_sp5':html[i]['volume']
                     } for i in range(len(html)))
data_sp5.set_index('Date',inplace=True)
data_sp5.sort_index(ascending=True,inplace=True)

data=pd.concat([data_dj,data_nas,data_sox,data_sp5],axis=1,join='inner')                                    #concat all index

conn = sqlite3.connect('USStock_index.db')                                                                  #connect to database
cursor = conn.cursor()
if(table_exists('Stock_index',conn) != 1):                                                                  #create table if not exist
    sql = 'CREATE TABLE Stock_index(Date date NOT NULL PRIMARY KEY,close_dj float,open_dj float,high_dj float,low_dj float,volume_dj float,close_nas float,open_nas float,high_nas float,low_nas float,volume_nas float,close_sox float,open_sox float,high_sox float,low_sox float,volume_sox float,close_sp5 float,open_sp5 float,high_sp5 float,low_sp5 float,volume_sp5 float)'
    cursor.execute(sql)
    conn.commit()
    data.to_sql('Stock_index',conn,if_exists='append',index=True)

if os.path.isfile('USStock_index.db'):
    last_day = pd.read_sql("SELECT * FROM Stock_index ORDER BY Date DESC LIMIT 1",conn)['Date'][0]
    if str(max(data.index)) > last_day :                                                                    #check if there is new data should be updated
        data.sort_index(ascending=False,inplace=True)
        i = 0
        for d in data.index :
            if(str(d) == last_day) : break
            i += 1
        data = data[0:i].sort_index()
        data.to_sql('Stock_index',conn,if_exists='append',index=True)

print(pd.read_sql('SELECT * FROM Stock_index',conn))                                                        #check if every data update successfully

cursor.close()
conn.close()                                                                                                #close the database