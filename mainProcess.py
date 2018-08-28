from getInfo import getFromYFUSScraping, getFromNikkeiScraping
import MongoDBManager
import datetime

def generateText():
    manager = MongoDBManager.MongoDBManager()
    stockDB = manager.getDB('stock')
    us = manager.getCollection('us')
    tickers = manager.getAllDocs()
    usTickers = {}
    for t in tickers:
        usTickers[t.get('ticker')] = t.get('company')
    print(usTickers)
    usHisotry = manager.getCollection('usStockHistory')
    today = datetime.datetime.today()
    queryDate = today - datetime.timedelta(days=2)
    print(queryDate)
    usStocks = manager.getSpecificDocs({'date':{'$gte':queryDate}})
    print(usStocks)
    uslines = ''
    for each in usStocks:
        print(each.get('ticker'))
        s = '{:>14}:{:>8},{:>16}\n'.format(each.get('ticker'),each.get('price') , each.get('comparison'))

    # us = manager.getCollection('usStockHistory')
    # res = manager.getAllDocs()
    # usStocks = {}
    # for info in res:
    #     print(info)
    #     usStocks[info.get('company')] = info.get('ticker')
    # print(usStocks)
    # text = getFromYFUSScraping(usStocks)
    # text += '------------------------\n'
    # japan = manager.getCollection('japan')
    # res = manager.getAllDocs()
    # japanStocks = {}
    # for info in res:
    #     japanStocks[info.get('company')] = info.get('code')
    # # print(usStocks)
    # text += getFromNikkeiScraping(japanStocks)
    # print(text)
    # return text

generateText()
