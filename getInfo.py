import urllib3
from bs4 import BeautifulSoup
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
import datetime
#日本株は日経スクレイピング
#東急reit: https://www.nikkei.com/nkd/company/?scode=8957
#福岡reit: https://www.nikkei.com/nkd/company/?scode=8968
#楽天: https://www.nikkei.com/nkd/company/?scode=4755
def getFromScraping(JapaneseStocks):
    http = urllib3.PoolManager()
    print(JapaneseStocks.keys())
    text = 'JPN stocks\n'
    for key in JapaneseStocks.keys():
        name = key
        code = JapaneseStocks[key]
        url = 'https://www.nikkei.com/nkd/company/?scode=' + code
        response = http.request('GET', url)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        comparedToYesterday = ''
        presentPrice = soup.find(class_='m-stockPriceElm_value now').text
        presentPrice = presentPrice.replace(' 円', '')
        PlusComparedToYesterday = soup.find(class_='m-stockPriceElm_value comparison plus')
        MinusComparedToYesterday = soup.find(class_='m-stockPriceElm_value comparison minus')
        if MinusComparedToYesterday:
            comparedToYesterday = MinusComparedToYesterday.text
        if PlusComparedToYesterday:
            comparedToYesterday = PlusComparedToYesterday.text
        # TODO: 日本語で出力すると2bit使うのでバラバラになる
        s = '{:>12}:{:>10},{:>16}\n'.format(name, presentPrice, comparedToYesterday)
        print(s)
        text += s
    return text

#米国株はpandas_datareader
#結果に対する細かいメソッド見る
#tickers={'AAPL':200}
def getFromIEX(tickers):
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    start = today - datetime.timedelta(days=4) #週末や連休挟んでもエラー吐かないよう四日分データ取る
    # start = datetime(2018,8,9)
    # end = datetime(2018,8,9)
    results = web.DataReader(tickers, 'iex', start, yesterday)
    print(results.keys())
    text = 'US stocks\n'
    for key in results.keys():
        # text += key + results.get(key)
        print(results[key])
        # print(type(results[key]))
        print('--------------')
        latest = results[key].open[-1]
        print(latest) #株価取得
        dayBefore = results[key].open[-2]
        ratio = round(((latest / dayBefore) - 1)* 100, 2)
        diff = round((latest - dayBefore), 2)
        print(str(ratio) + '%')
        print(str(diff))
        # print(type(results[key].open[0]))
        print('--------------')
        text += '{:>6}:{:>7}, {:>6}%, {:>6}\n'.format(key, str(latest), str(ratio), str(diff))
    print(text)
    return text
