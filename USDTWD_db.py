from curl_cffi.requests import impersonate
from curl_cffi import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import sqlite3,os
from pandas.io.sql import table_exists

url = 'https://www.macromicro.me/charts/76510/USD-TWD-CNY'
url2 = 'https://www.macromicro.me/charts/data/76510'

req = requests.get(url=url,impersonate='chrome101')                                             #in order the get cookie
soup = bs(req.text,'lxml')
ptag = soup.select('.sosume p')[0]
data_stk = ptag['data-stk']
cookie_dict = req.cookies.get_dict()
cookie = 'PHPSESSID' + "=" + cookie_dict['PHPSESSID']

headers = {'Authorization':'Bearer '+data_stk,'Cookie':cookie,'referer':url}                    #add cookie to header
res = requests.get(url2,headers=headers,impersonate='chrome101')
res_json = res.json()

df = pd.DataFrame(res_json['data']['c:76510']['series'][1],columns=['Date','USDTWD'])           #USDTWD
df.set_index(['Date'],inplace=True)

conn = sqlite3.connect('USDTWD.db')                                                             #connect to database
cursor = conn.cursor()
if (table_exists('USDTWD',conn) != 1):                                                          #create table if not exist
    sql = 'CREATE TABLE USDTWD(Date date PRIMARY KEY,USDTWD float)'
    cursor.execute(sql)
    conn.commit()
    df.to_sql('USDTWD',conn,if_exists='append',index=True)

if os.path.isfile('USDTWD.db'):
    last_day = pd.read_sql('SELECT * FROM USDTWD ORDER BY Date DESC LIMIT 1',conn)['Date'][0]
    if  max(df.index) > str(last_day) :                                                         #check if there is new data should be updated
        df.sort_index(ascending=False,inplace=True)
        i = 0
        for d in df.index :
            if d == str(last_day) : break
            i += 1
        df = df[0:i].sort_index()
        df.to_sql('USDTWD',conn,if_exists='append',index=True)

print(pd.read_sql('SELECT * FROM USDTWD',conn))                                                 #check if every data update successfully

cursor.close()
conn.close()                                                                                    #close the database