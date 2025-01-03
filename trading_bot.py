
import pandas as pd
from binance.client import Client
import time
import numpy
import matplotlib.pyplot as plt
from datetime import datetime
import requests
from plyer import notification

symbol ='BTCUSDT'
API_KEY = '****'
API_SECRET = '*****'
url= 'https://api.alternative.me/fng/?limit=2'

client = Client(API_KEY,API_SECRET,testnet=True)

excel_data = 'token_price.xlsx'
try:
    sheet = pd.read_excel(excel_data)
except FileNotFoundError:
    columns=['Count','Date','Timestamp','Symbol','Price','100 EMA','200 EMA','Index','12 EMA','26 EMA','MACD','Signal Line','Histogram']
    sheet = pd.DataFrame(columns=columns)

def get_index():
    response = requests.get(url)
    result = response.json()
    value = int(result['data'][0]['value'])
    return value

def fear_or_index(x):
    if x > 50:
        return "Greed"
    elif x > 40:
        return "Neutral"
    else:
        return "Fear"

def get_current_price(symbol):
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker['price'])

def find_9_ema(x,y):
    result = (x-y)*0.2 + y
    return result

def find_12_ema(x,y):
    value = x*0.1538 + y*(1-0.1538)
    return value

def find_26_ema(x,y):
    result = (x-y)*0.07407 + y
    return result

def find_100_ema(x,y):
    result = x*0.0198 + y*(1-0.0198)
    return result

def find_200_ema(x,y):
    result = x*0.00995 + y*(1-0.00995)
    return result

def send_notification():
    notification.notify(title='Crypto Trading Bot',message='This might be the right time to buy the Token.',app_name='Trading Bot')

def read_excel():  

    cp= sheet.loc[sheet['Count'] == 4,'Price'].values[-1]
    e_100= sheet.loc[sheet['Count'] == 4,'100 EMA'].values[-1]
    e_200= sheet.loc[sheet['Count'] == 4,'200 EMA'].values[-1]
    mcd= sheet.loc[sheet['Count'] == 4,'MACD'].values[-1]
    sig= sheet.loc[sheet['Count'] == 4,'Signal Line'].values[-1]
    idx = sheet.loc[sheet['Count'] == 4,'Index'].values[-1]
    
    if cp > e_100 and cp > e_200 and mcd > sig and idx > 40:
        send_notification()
        

def fetch_bot():
    ema_12= 68774.27
    ema_26= 68687.03
    macd_input= 87.25
    signal= 136.67
    ema_100= 68033.24
    ema_200= 66900.39
    
    i=0
    counter = 0

    while True:
        price= get_current_price(symbol)        
        now = datetime.now()
        current_date = now.date()
        current_time = now.strftime("%H:%M:%S")
        histo=macd_input - signal

        if i==4:
            fast_ema_12= find_12_ema(price,ema_12)
            slow_ema_26= find_26_ema(price,ema_26)
            macd_line= fast_ema_12 - slow_ema_26
            signal_line= find_9_ema(macd_line,macd_input)
            histo_value= macd_line - signal_line
            hundered_ema= find_100_ema(price, ema_100)
            two_hundered_ema= find_200_ema(price, ema_200)
            index_value = get_index()
            comment = fear_or_index(index_value)

            row = pd.DataFrame({'Count':[i],'Date':[current_date],'Timestamp':[current_time],'Symbol':[symbol],
               'Price':[price],'100 EMA':[hundered_ema],'200 EMA': [two_hundered_ema],'12 EMA':[fast_ema_12],
               '26 EMA':[slow_ema_26],'MACD':[macd_line],'Signal Line':[signal_line],
               'Histogram':[histo_value],'Index':[index_value],'Fear/ Greed': [comment]})

            global sheet
            sheet = pd.concat([sheet,row], ignore_index=True)
                        

            ema_12 = fast_ema_12
            ema_26 = slow_ema_26
            signal = signal_line
            ema_100 = hundered_ema
            ema_200 = two_hundered_ema
            macd_input = macd_line
            i=0
            counter += 1
            if counter >= 4:
                sheet.to_excel(excel_data, index=False)
                counter = 0
            time.sleep(10)
            read_excel()
            
        else:            
               
            row = pd.DataFrame({'Count':[i],'Date':[current_date],'Timestamp':[current_time],'Symbol':[symbol],
               'Price':[price]})        
            sheet = pd.concat([sheet,row], ignore_index=True)
            sheet.to_excel(excel_data, index=False)
            i+=1 
            time.sleep(900)      
               
   

