import sys
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QDate, pyqtSlot,QRect
from PyQt5.QtWebEngineWidgets import QWebEngineView

from ui_MainWindow import Ui_MainWindow                             #GUI
import pandas as pd
import sqlite3
import plotly.graph_objects as go
import plotly.offline as offline

class QmyMainWindow(QMainWindow):                                   #this class is inherit from QMainWindow

    def __init__(self,parent=None):
        super().__init__(parent)                                    #use QMainWindow inititialize function 
        self.ui=Ui_MainWindow()                                     #construct GUI
        self.ui.setupUi(self)
        width = QApplication.primaryScreen().size().width()
        height = QApplication.primaryScreen().size().height()
        self.setFixedSize(width,height)
        self.ui.layoutWidget.setGeometry(QRect(10, 20, width, int(height * 0.9)))
        self.ui.centralwidget.setStyleSheet('background:rgb(0,0,0)')
        self.ui.date_Start.setStyleSheet('color:rgb(255,255,255)')
        self.ui.date_End.setStyleSheet('color:rgb(255,255,255)')
        self.ui.label_Start.setStyleSheet('color:rgb(255,255,255)')
        self.ui.label_End.setStyleSheet('color:rgb(255,255,255)')
        self.ui.Enter_Button.setStyleSheet('background:rgb(255,255,255)')

        current_date = QDate.currentDate()
        self.ui.date_Start.setDate(current_date.addYears(-2))
        self.ui.date_End.setDate(current_date)

        self.load_data()
        
        
    
#=====================================由connectSlotByName()自動連結的槽函數===================================================
    @pyqtSlot(QDate)
    def on_date_Start_dateChanged(self,date):                                       #if date_Start > date_End, set them the same
        if(self.ui.date_End.date() < date): self.ui.date_End.setDate(date)

    @pyqtSlot(QDate)
    def on_date_End_dateChanged(self,date):                                         #if date_End < date_Start, set them the same
        if(self.ui.date_Start.date() > date): self.ui.date_Start.setDate(date)

    @pyqtSlot()
    def on_Enter_Button_clicked(self):
        self.draw() 

#============================================自定義槽函數===================================================================


#==========================================自訂函數========================================================================

    def load_data(self):
        conn = sqlite3.connect('USDTWD.db')
        self.usdtwd = pd.read_sql('SELECT * FROM USDTWD',conn).set_index('Date')
        self.usdtwd.index = self.usdtwd.index.astype("string")
        self.usdtwd.sort_index(ascending=True,inplace=True)

        self.msci = pd.read_csv('MSCI.csv').set_index('Date')
        self.msci.index = self.msci.index.astype("string")
        self.msci.sort_index(ascending=True,inplace=True)

        self.morgan = pd.read_csv('Morgan_bond.csv').set_index('Date')
        self.morgan.index = self.morgan.index.astype("string")
        self.morgan.sort_index(ascending=True,inplace=True)

        conn = sqlite3.connect('US10Y.db')
        self.us10y = pd.read_sql('SELECT * FROM US10Y',conn).set_index('Date')
        self.us10y.index = self.us10y.index.astype("string")
        self.us10y.sort_index(ascending=True,inplace=True)

        conn = sqlite3.connect('USStock_index.db')
        self.usstock = pd.read_sql('SELECT Date, close_dj,close_sp5,close_nas,close_sox FROM Stock_index',conn).set_index('Date')
        self.usstock.index = self.usstock.index.astype("string")
        self.usstock.sort_index(ascending=True,inplace=True)

        self.draw()


    def draw(self):
        start_date = self.ui.date_Start.date().toString("yyyyMMdd")
        end_date = self.ui.date_End.date().toString("yyyyMMdd")

        layout = dict(margin = dict(l = 5, r = 5, b = 10, t = 30),
                      xaxis = dict(title = dict(text = 'Date'), linecolor = 'white', showgrid = False),
                      yaxis = dict(linecolor = 'white', showgrid = False),
                      font = dict(color='white'),
                      plot_bgcolor = 'black', 
                      paper_bgcolor = 'black')

        
        data = self.usdtwd[(self.usdtwd.index >= start_date) & (self.usdtwd.index <= end_date)]
        date = pd.to_datetime(data.index)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = date, y = data['USDTWD'], line_color = "cyan",name = 'USDTWD',hovertemplate = '%{x:%Y%m%d},%{y}'))
        fig.update_layout(title = dict(text = 'USDTWD'), yaxis = dict(title = dict(text = 'USDTWD')))
        fig.update_layout(layout)
        html = offline.plot(fig,output_type='div',include_plotlyjs='cdn')
        view = QWebEngineView()
        view.setHtml(html)
        view.page().setBackgroundColor(QColor(0,0,0))
        self.ui.gridLayout.addWidget(view,0,0)

        data = self.msci[(self.msci.index >= start_date) & (self.msci.index <= end_date)]
        date = pd.to_datetime(data.index)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = date,y = data['Price'], line_color = 'deepskyblue',name = 'MSCI',hovertemplate = '%{x:%Y%m%d},%{y:d}'))
        fig.update_layout(title = 'MSCI World Index', yaxis = dict(title = dict(text = 'Index')))
        fig.update_layout(layout)
        html = offline.plot(fig, output_type = 'div', include_plotlyjs = 'cdn')
        view = QWebEngineView()
        view.setHtml(html)
        view.page().setBackgroundColor(QColor(0,0,0))
        self.ui.gridLayout.addWidget(view,0,1)

        data = self.morgan[(self.morgan.index >= start_date) & (self.morgan.index <= end_date)]
        date = pd.to_datetime(data.index)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = date, y = data['Price'], line_color = 'lightskyblue',name = 'Morgan Bond',hovertemplate = '%{x:%Y%m%d},%{y}'))
        fig.update_layout(title = 'Morgan Bond Index', yaxis = dict(title = dict(text = 'Index')))
        fig.update_layout(layout)
        html = offline.plot(fig,output_type='div',include_plotlyjs='cdn')
        view = QWebEngineView()
        view.setHtml(html)
        view.page().setBackgroundColor(QColor(0,0,0))
        self.ui.gridLayout.addWidget(view,0,2)
        
        data = self.us10y[(self.us10y.index >= start_date) & (self.us10y.index <= end_date)]
        date = pd.to_datetime(data.index)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = date, y = data['US10Y_Treasury_Yield'],name = 'US10Y',hovertemplate = '%{x:%Y%m%d},%{y}'))
        fig.update_layout(title = 'US10Y', yaxis = dict(title = dict(text = 'Treasury Yield')))
        fig.update_layout(layout)
        html = offline.plot(fig, output_type='div', include_plotlyjs='cdn')
        view = QWebEngineView()
        view.setHtml(html)
        view.page().setBackgroundColor(QColor(0,0,0))
        self.ui.gridLayout.addWidget(view,1,0)

        data = self.usstock[(self.usstock.index >= start_date) & (self.usstock.index <= end_date)]
        date = pd.to_datetime(data.index)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = date, y = data['close_dj'], line_color = 'lightcoral', name = 'Dow Jone'))
        fig.add_trace(go.Scatter(x = date, y = data['close_nas'], line_color = 'gold', name = 'NAS'))
        fig.add_trace(go.Scatter(x = date, y = data['close_sp5'], line_color = 'greenyellow', name = 'SP500', yaxis = 'y2'))
        fig.add_trace(go.Scatter(x = date, y = data['close_sox'], line_color = 'lightyellow', name = 'SOX', yaxis = 'y2'))
        fig.update_layout(title = 'US Stock Index')
        fig.update_layout(yaxis = dict(title = dict(text = 'Dow Jone/Nas Index')))
        fig.update_layout(yaxis2 = dict(title = dict(text = 'SP500/SOX Index'), anchor = 'x', overlaying = 'y', side = 'right', showgrid = False))
        fig.update_layout(legend = dict(x = 0.01, y = 0.99))
        fig.update_layout(layout)
        html = offline.plot(fig, output_type='div', include_plotlyjs='cdn')
        view = QWebEngineView()
        view.setHtml(html)
        view.page().setBackgroundColor(QColor(0,0,0))
        self.ui.gridLayout.addWidget(view,1,1)
        
#==========================================表單測試程式=====================================================================
if __name__=="__main__":
    app=QApplication(sys.argv)
    form=QmyMainWindow()
    form.showMaximized()
    sys.exit(app.exec_())