美元投資型保單新契約保費收入與各項變數之關係  
==========================================================================================
## 1.相關變數儀表板  
![image](https://github.com/Suweihsiang/USDUL/blob/main/image/Dashboard.png)  
(相關程式碼請見：[ui_MainWindow.py](https://github.com/Suweihsiang/USDUL/blob/main/ui_MainWindow.py)、[myMainWindow.py](https://github.com/Suweihsiang/USDUL/blob/main/myMainWindow.py)、[main.py](https://github.com/Suweihsiang/USDUL/blob/main/main.py))  
(1)儀表板左上方可以選擇資料起始及終止日，點擊即可以日曆選擇，若選擇之起始日晚於終止日或是選擇之終止日早於起始日，則同步更新終止日或起始日於選擇之日期。  
(2)儀表板展示五張圖表，分別為美元兌台幣匯率、MSCI世界指數、摩根全球政府債券指數、美國十年期公債殖利率以及美股四大指數，在線條上方盤旋會顯示該點之日期與對應之數值。  
  
## 2.投資型保險商品新契約保費收入影響變數分析  
(相關程式碼請見：(網路爬蟲)[America_Stock_db.py](https://github.com/Suweihsiang/USDUL/blob/main/America_Stock_db.py)、[US10Y_db.py](https://github.com/Suweihsiang/USDUL/blob/main/US10Y_db.py)、[USDTWD_db.py](https://github.com/Suweihsiang/USDUL/blob/main/USDTWD_db.py)、[morgan_bond.py](https://github.com/Suweihsiang/USDUL/blob/main/morgan_bond.py)、[msci.py](https://github.com/Suweihsiang/USDUL/blob/main/msci.py) (數據分析)[analysis.ipynb
](https://github.com/Suweihsiang/USDUL/blob/main/analysis.ipynb))  
現在外幣投資型保險商品新契約保費收入，以美元為大宗，因此美元商品之銷售情形足以影響整體外幣投資型保單之保費收入。而在每月撰寫新契約保費收入變動分析之同時，曾經經歷過熱銷的時期，也曾經經歷過衰退之時期。因此，對於影響新契約保費收入之因子，我先蒐集了美元兌台幣匯率、美股四大指數、MSCI全球指數、摩根全球政府債券指數、美元十年期公債殖利率之數據，試圖尋找其中之關鍵因素。  
首先，我先將透過爬蟲程式取得之美元兌台幣匯率、美股四大指數及美元十年期公債殖利率存入SQL的資料庫中，並下載MSCI全球指數及摩根全球政府債券指數之檔案。由於保險局每月公布當月之美元投資型保單新契約保費收入，因此各項變數資料都須以月為單位，故將上述資料皆以月為群組取平均數作為當月之數值。  
而後再進行資料清理後，繪製各變數與美元投資型保單新契約保費收入(USUL FYP)之相關係數矩陣圖以及散點圖，可以輕易地發現美元兌台幣匯率、美元十年期公債殖利率(Yield)對於保費收入明顯呈現負相關之影響，摩根全球政府債券指數則是呈現正相關之影響。  
![image](https://github.com/Suweihsiang/USDUL/blob/main/image/corr.png)  
![image](https://github.com/Suweihsiang/USDUL/blob/main/image/scatter_plot.png)  
接著在經過資料標準化後，透過Lasso及隨機森林迴歸試圖篩選出重要之特徵，在使用Lasso時，先設定從0.0001到10共400個之alpha參數，並觀察每個特徵係數收斂至0之情形，可以看出美元兌台幣匯率最後收斂至0，可以得知此項變數對於新契約保費收入相當重要。  
![image](https://github.com/Suweihsiang/USDUL/blob/main/image/Lasso_coef.png)  
再透過Lasso之最小角演算法向前選取特徵建立模型，並使用BIC作為衡量模型之標準，最後以BIC最小值篩選出最佳模型，其所對應之alpha為0.01，篩選出之特徵為美元兌台幣匯率、那斯達克綜合指數以及摩根全球政府債券指數，其中以美元兌台幣匯率之重要程度最高，且呈現負相關之影響，其餘兩者則重現正相關之影響。而模型之均方差為0.14661，R2為0.8534。  
![image](https://github.com/Suweihsiang/USDUL/blob/main/image/Alpha_BIC.png)  
![image](https://github.com/Suweihsiang/USDUL/blob/main/image/Lasso_predicted_line.png)  
另一方面，再使用隨機森林迴歸，透過向前選取特徵之方式，並藉由R2作為選取最佳特徵組合之指標，選擇出美元兌台幣匯率、道瓊指數、美國十年期公債殖利率以及MSCI全球指數為最重要特徵組合。藉由篩選出之四項特徵建立隨機森林迴歸模型，其均方差為0.021，R2為0.9786，擬合程度明顯比Lasso模型好。而篩選出的四項特徵中，仍以美元兌台幣匯率之重要程度最高，其次為美元十年期公債殖利率。  
![image](https://github.com/Suweihsiang/USDUL/blob/main/image/RandomForestRegressor.png)  
由此可知，當美元兌台幣匯率高時，美元保單變得更貴，對於保戶之購買可能產生阻力。而另一方面，在2024年上半年時，市場預期美國聯準會將於下半年展開降息，屆時美債殖利率走跌，美債將變得更值錢，因此市場資金湧入美債，美國十年期公債殖利率走升，美元投資型保單相較之下則非市場進行美元資產配置之首選，故其新契約保費收入相形失色。而當市場狀況佳時，較能吸引保戶購買投資型保單，欲藉由投資收益為保險保障加碼，因此，當美國股市表現好時，對於美元投資型保單之銷售將產生助力。