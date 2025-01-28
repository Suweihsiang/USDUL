from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os,time,sys

url = 'https://www.stockq.org/index/BIJPGG.php'
driver = webdriver.Firefox()                                                        #create webbrowser
driver.get(url)

if os.path.isfile('morgan_bond.csv') != 1:                                          #if there is no such file ,download all datas that website have
    try:
        driver.find_element(By.XPATH,'//*[@id="return5y"]').click()
        time.sleep(10)
    except:                                                                         #stop if error occurs
        print("RemoteError has occure")
        driver.close()
        sys.exit()
else:                                                                               #check if there is any data should be update in two years
    try:
        driver.find_element(By.XPATH,'//*[@id="return2y"]').click()
        time.sleep(10)
    except:                                                                         #stop if error occurs
        print("RemoteError has occure")
        driver.close()
        sys.exit()

thead = driver.find_element(By.XPATH,'//*[@id="sma_chart"]/div/div[1]/div/div/table').find_element(By.TAG_NAME,'thead').find_element(By.TAG_NAME,'tr').find_elements(By.TAG_NAME,'th')
th = []                                                                             #columns name list
for i in range(len(thead)):
    th.append(thead[i].get_attribute('textContent'))

table = driver.find_element(By.XPATH,'//*[@id="sma_chart"]/div/div[1]/div/div/table').find_elements(By.TAG_NAME,'tr')
tlist = []                                                                          #data list
for i in range(1,len(table)):
    date = table[i].find_elements(By.TAG_NAME,'td')[0].get_attribute('textContent')
    price = table[i].find_elements(By.TAG_NAME,'td')[1].get_attribute('textContent')
    MA20 = table[i].find_elements(By.TAG_NAME,'td')[2].get_attribute('textContent')
    MA60 = table[i].find_elements(By.TAG_NAME,'td')[3].get_attribute('textContent')
    MA120 = table[i].find_elements(By.TAG_NAME,'td')[4].get_attribute('textContent')
    MA240 = table[i].find_elements(By.TAG_NAME,'td')[5].get_attribute('textContent')
    tlist.append([date,price,MA20,MA60,MA120,MA240])
df = pd.DataFrame(tlist,columns=th).rename(columns={'Time':'Date'})
df['Date'] = pd.to_datetime(df['Date'],format='mixed')
if os.path.isfile('morgan_bond.csv'):                                                #check if this file exist
    data = pd.read_csv('morgan_bond.csv')
    data['Date'] = pd.to_datetime(data['Date'])
    if(data['Date'].iloc[-1] != df['Date'].iloc[-1]) :                               #check if there is new data should be updated
        data = pd.concat([data,df]).dropna(axis=1).drop_duplicates(subset=['Date']).set_index('Date')
        data.to_csv('morgan_bond.csv')
else:                                                                                #create file if not exist
    df.set_index('Date',inplace=True)
    df.to_csv('morgan_bond.csv')
print(pd.read_csv('morgan_bond.csv'))                                                #check if every data update successfully
driver.close()                                                                       #web browser close