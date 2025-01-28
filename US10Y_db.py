from curl_cffi.requests import impersonate
from curl_cffi import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import sqlite3,os
from pandas.io.sql import table_exists

url = 'https://www.macromicro.me/charts/75/10-year-bond-yield-us-mid14'
url2 = 'https://www.macromicro.me/charts/data/75'

req = requests.get(url=url,impersonate='chrome101')                                             #in order the get cookie
soup = bs(req.text,'lxml')
ptag = soup.select('.sosume p')[0]
data_stk = ptag['data-stk']
cookie_dict = req.cookies.get_dict()
cookie = 'PHPSESSID' + "=" + cookie_dict['PHPSESSID']

headers = {'Authorization':'Bearer '+data_stk,'Cookie':cookie,'referer':url}                    #add cookie to header
res = requests.get(url2,headers=headers,impersonate='chrome101')
res_json = res.json()

df = pd.DataFrame(res_json['data']['c:75']['series'][0],columns=['Date','US10Y_Treasury_Yield'])#US-10years-treasury-bond yield
df.set_index(['Date'],inplace=True)

conn = sqlite3.connect('US10Y.db')                                                              #connect to database
cursor = conn.cursor()
if (table_exists('US10Y',conn) != 1):                                                           #create table if not exist
    sql = 'CREATE TABLE US10Y(Date date PRIMARY KEY,US10Y_Treasury_Yield float)'
    cursor.execute(sql)
    conn.commit()
    df.to_sql('US10Y',conn,if_exists='append',index=True)

if os.path.isfile('US10Y.db'):
    last_day = pd.read_sql('SELECT * FROM US10Y ORDER BY Date DESC LIMIT 1',conn)['Date'][0]
    if max(df.index) > str(last_day) :                                                          #check if there is new data should be updated
        df.sort_index(ascending=False,inplace=True)
        i = 0
        for d in df.index :
            if d == str(last_day) : break
            i += 1
        df = df[0:i].sort_index()
        df.to_sql('US10Y',conn,if_exists='append',index=True)

print(pd.read_sql('SELECT * FROM US10Y',conn))                                                  #check if every data update successfully

cursor.close()
conn.close()                                                                                    #close the database