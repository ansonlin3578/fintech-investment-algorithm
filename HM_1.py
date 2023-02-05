import code
from email import message
import json
import statistics
from unittest import result
from pandas import DataFrame
import pandas as pd
import requests
import yfinance as yf
from matplotlib import pyplot as plt
import statistics
import math


total_oriented = [ # 力道
  'value',  # 價值
  'trend',  # 趨勢
  'swing',  # 波段
  'chip',  # 籌碼
  'dividend' # 股利
]
value_indicators = {
    '營收年增率': 'REVENUE-YOY',
    '營業現金流對稅後淨利比': 'NCFO-NETINC',
    '本益比河流圖': 'PE-RATIO'
}
trend_indicators = ['surfing-trend', 'power-squeeze', 'power-squeeze-momentum']
chip_indicators = {
    '機構持有率': 'inst-ownship',
    '持有機構數': 'inst-count'
}

api_key = 'tv-ffb6c7b0-b70d-480f-b074-e3290cc29287'
url_head = 'https://api.tradingvalley.com/public'

session = requests.Session()
session.headers.update({'X-API-KEY': api_key})

#////////////////////////////get url 目的地網址////////////////////////////////////
api_url = {
    'symbol_rating': lambda oriented, symbol: f'{url_head}/historical/rating/{oriented}/{symbol}?start_at=2022-01-01&end_at=2022-09-30',
    'symbol_score_rating': lambda oriented, symbol, score: f'{url_head}/historical/rating/{oriented}/{symbol}/{score}?start_at=2022-01-01&end_at=2022-09-30', 
    'symbol_indicators': lambda oriented, symbol, indicator: f'{url_head}/historical/{oriented}/{symbol}/{indicator}?start_at=2022-01-01&end_at=2022-09-30',
    'vix': f'{url_head}/historical/stock/vix'
} #形成可使用之 url

#///////////////////////////////////////////////HM1///////////////////////////////////////////////
#選擇三個標的>>1.APPL(apple) 2.TSLA(tesla) 3.NVDA(nvidia)
#選擇score >>> trend
#投資比重分配 : 1.apple(40000) 2.tesla(30000) 3.nvidia(30000)
#///////////////////////////////////////////AAPL//////////////////////////////////////
apple_fund = 40000
stock_numbers = 0
df = yf.download("AAPL", start = "2018-01-01" , end = "2022-09-30") #download the price in interval
# print(df.head())
# print(df.loc['2021-09-01']['Close'])
apple_fund_per_day = []

url = api_url['symbol_indicators']('trend', 'AAPL', 'surfing-trend')#apple趨勢因子
# print(f'將呼叫 {url}')
response = session.get(url)
surfing_trend_data = response.json()
# print(pandas.DataFrame(json.loads(response.text)['data']))
value_length = len(surfing_trend_data['data'])
# print(surfing_trend_data['data'][value_length - 1])
upper_count = 0
down_count = 0
stock_hold = False
for i in reversed(range(1 , value_length)):
    if upper_count >= 5 and not stock_hold:   #如果連續5次趨勢上升 買入，連五次趨勢下降及賣出
        upper_count = 0
        stock_hold = True
        print('buy stock!' , surfing_trend_data['data'][i]["date"])
        apple_stockprice_buyin = df.loc[surfing_trend_data['data'][i]["date"]]['Close']
        stock_numbers = apple_fund % apple_stockprice_buyin
        apple_fund = apple_fund - (apple_stockprice_buyin * stock_numbers)
        pass    #bull market , buy the stock
    elif down_count >= 5 and stock_hold:
        down_count = 0
        stock_hold = False
        apple_stockprice_sellout = df.loc[surfing_trend_data['data'][i]["date"]]['Close']
        apple_fund = apple_fund + (apple_stockprice_sellout * stock_numbers)
        stock_numbers = 0
        print('sell stock!' , surfing_trend_data['data'][i]["date"])
        pass    #bear market , sell the stock
    if surfing_trend_data['data'][i]["value"] <= surfing_trend_data['data'][i - 1]["value"]:
        upper_count += 1
        down_count = 0
    else:
        down_count += 1
        upper_count = 0
    # print(surfing_trend_data['data'][i]["value"] , surfing_trend_data['data'][i]["date"])
    current_fund = apple_fund + stock_numbers * df.loc[surfing_trend_data['data'][i]["date"]]['Close']
    apple_fund_per_day.append(current_fund)
if stock_hold:
    print('sell stock!' , surfing_trend_data['data'][i]["date"])
    apple_stockprice_sellout = df.loc[surfing_trend_data['data'][i]["date"]]['Close']
    apple_fund = apple_fund + (apple_stockprice_sellout * stock_numbers)

# plt.plot(apple_fund_per_day)
# plt.xlabel("Time")
# plt.ylabel("apple_fund")
# plt.show()
print(apple_fund)

# ///////////////////////////////////////////TSLA//////////////////////////////////////
tesla_fund = 30000
stock_numbers = 0
df = yf.download("TSLA", start = "2018-01-01" , end = "2022-09-30") #download the price in interval
tesla_fund_per_day = []

stock_hold = False
url = api_url['symbol_indicators']('trend', 'TSLA', 'power-squeeze')  #tesla趨勢因子
print(f'將呼叫 {url}')
response = session.get(url)
power_squeeze_data = response.json()
# print(pandas.DataFrame(json.loads(response.text)['data']))
# print(power_squeeze_data['data'][0])
for i in reversed(range(1 , value_length)):
    if power_squeeze_data['data'][i]['value'] >= 3 and not stock_hold: #如果價值力道大於等於3買入，小於2賣出
        stock_hold = True
        print('buy stock!' , power_squeeze_data['data'][i]["date"])
        tesla_stockprice_buyin = df.loc[surfing_trend_data['data'][i]["date"]]['Close']
        stock_numbers = tesla_fund % tesla_stockprice_buyin
        tesla_fund = tesla_fund - (tesla_stockprice_buyin * stock_numbers)
        pass    #bull market , buy the stock
    elif power_squeeze_data['data'][i]['value'] < 2 and stock_hold:
        stock_hold = False
        print('sell stock!' , power_squeeze_data['data'][i]["date"])
        tesla_stockprice_sellout = df.loc[surfing_trend_data['data'][i]["date"]]['Close']
        tesla_fund = tesla_fund + (tesla_stockprice_sellout * stock_numbers)
        stock_numbers = 0  
        pass    #bear market , sell the stock
    # print(power_squeeze_data['data'][i]["value"] , power_squeeze_data['data'][i]["date"])
    current_fund = tesla_fund + stock_numbers * df.loc[surfing_trend_data['data'][i]["date"]]['Close']
    tesla_fund_per_day.append(current_fund)
if stock_hold:
    print('sell stock!' , surfing_trend_data['data'][i]["date"])
    tesla_stockprice_sellout = df.loc[surfing_trend_data['data'][i]["date"]]['Close']
    tesla_fund = tesla_fund + (tesla_stockprice_sellout * stock_numbers)
# plt.plot(tesla_fund_per_day)
# plt.xlabel("Time")
# plt.ylabel("tesla_fund")
# plt.show()
print(tesla_fund)
# ///////////////////////////////////////////meta//////////////////////////////////////
meta_fund = 30000
stock_numbers = 0
df = yf.download("META", start = "2018-01-01" , end = "2022-09-30") #download the price in interval
meta_fund_per_day = []

upper_count = 0
down_count = 0
stock_hold = False
url = api_url['symbol_indicators']('trend', 'NVDA', 'power-squeeze-momentum') #meta趨勢因子
# print(f'將呼叫 {url}')
response = session.get(url)
power_momentum_data = response.json()
# print(pandas.DataFrame(json.loads(response.text)['data']))
# print(power_momentum_data)
for i in reversed(range(1 , value_length)):
    if upper_count >= 5 and not stock_hold:   #如果連續5次趨勢上升降 買入，連五次趨勢下降及賣出
        upper_count = 0
        stock_hold = True
        print('buy stock!' , power_momentum_data['data'][i]["date"])
        meta_stockprice_buyin = df.loc[surfing_trend_data['data'][i]["date"]]['Close']
        stock_numbers = meta_fund % meta_stockprice_buyin
        meta_fund = meta_fund - (meta_stockprice_buyin * stock_numbers)
        pass    #bull market , buy the stock
    elif down_count >= 5 and stock_hold:
        down_count = 0
        stock_hold = False
        print('sell stock!' , power_momentum_data['data'][i]["date"])
        meta_stockprice_sellout = df.loc[surfing_trend_data['data'][i]["date"]]['Close']
        meta_fund = meta_fund + (meta_stockprice_sellout * stock_numbers)
        stock_numbers = 0  
        pass    #bear market , sell the stock
    if power_momentum_data['data'][i]["value"] <= power_momentum_data['data'][i - 1]["value"]:
        upper_count += 1
        down_count = 0
    else:
        down_count += 1
        upper_count = 0
    current_fund = meta_fund + stock_numbers * df.loc[surfing_trend_data['data'][i]["date"]]['Close']
    meta_fund_per_day.append(current_fund)
    # print(power_momentum_data['data'][i]["value"] , power_momentum_data['data'][i]["date"])
if stock_hold:
    print('sell stock!' , surfing_trend_data['data'][i]["date"])
    meta_stockprice_sellout = df.loc[surfing_trend_data['data'][i]["date"]]['Close']
    meta_fund = meta_fund + (meta_stockprice_sellout * stock_numbers)


fig, ax = plt.subplots()
# plt.plot(apple_fund_per_day)
# plt.plot(tesla_fund_per_day)
plt.plot(apple_fund_per_day, color='b', label='apple')
plt.plot(tesla_fund_per_day, color='tab:orange', label='tesla')
plt.plot(meta_fund_per_day, color='g', label='meta')


leg = ax.legend(loc='center right', shadow=True) 
plt.xlabel("Time")
plt.ylabel("fund_summary")
plt.show()

result_fund = apple_fund + tesla_fund + meta_fund
print("final Total Property :",result_fund)
print("Profit : " , (result_fund - 100000))
print("earning ration : {:.2f}%".format((result_fund - 100000)/1000))

total_fund_per_day = []
pct_change = []
for i in range(len(apple_fund_per_day)):
    total_fund = apple_fund_per_day[i] + tesla_fund_per_day[i] + meta_fund_per_day[i]
    total_fund_per_day.append(total_fund)
earning = 0
for i in range(1 , len(apple_fund_per_day)): #計算每日報酬平均
    pct_change.append((total_fund_per_day[i] - total_fund_per_day[i - 1])/total_fund_per_day[i - 1])
earning = sum(pct_change)
earning_avg = earning / 186
risk_free = statistics.stdev(pct_change)    #無風險利率
sharp_ratio = earning_avg / risk_free * math.sqrt(252) #sharp ratio 公式
print("sharp_ratio:" , sharp_ratio)


# s = pd.Series(total_fund_per_day)         #use pakage to calculate sharp ratio
# pct_change = DataFrame.pct_change(s)
# profit = pct_change.mean()
# risk_free = pct_change.std()
# sharp_ratio = profit / risk_free * (252 ** 0.5)
# print(sharp_ratio)

fig, ax = plt.subplots()
plt.plot(total_fund_per_day, color='k', label='earning')
leg = ax.legend(loc='upper left', shadow=True) 
plt.xlabel("Time")
plt.ylabel("earning")
plt.show()


