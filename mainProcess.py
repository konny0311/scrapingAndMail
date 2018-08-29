from getInfo import getFromYFUSScraping, getFromNikkeiScraping
import MongoDBManager
import datetime

def generateText():
    # stock db取得
    manager = MongoDBManager.MongoDBManager()
    stockDB = manager.getDB('stock')
    # usのcompany-ticker collection取得
    us = manager.getCollection('us')
    tickers = manager.getAllDocs()
    usTickers = {}
    for t in tickers:
        usTickers[t.get('symbol')] = t.get('company')
    # print(usTickers) #debug

    #japanのcompany-code collection取得
    japan = manager.getCollection('japan')
    tickers = manager.getAllDocs()
    japanCodes = {}
    for t in tickers:
        japanCodes[t.get('symbol')] = t.get('company')
    # print(japanCodes) #debug

    #usStockHistoryから直近の記録を抜き出し、tickerをcompanyに入れ替え
    usHisotry = manager.getCollection('usStockHistory')
    today = datetime.datetime.today()
    queryDate = today - datetime.timedelta(days=3) #TODO:実行時はdays=1
    print(queryDate) #debug
    usStocks = manager.getSpecificDocs({'date':{'$gte':queryDate}})
    uslines = ''
    for each in usStocks:
        # print(each.get('ticker')) #debug
        s = '{:>14}:{:>8},{:>16}\n'.format(usTickers.get(each.get('ticker')),each.get('price') , each.get('comparison'))
        uslines += s
    print(uslines)

    #japanStockHistoryから直近の記録を抜き出し、codeをcompanyに入れ替え
    japanStockHistory = manager.getCollection('japanStockHistory')
    japanStocks = manager.getSpecificDocs({'date':{'$gte':queryDate}})
    japanlines = ''
    for each in japanStocks:
        # print(each.get('code')) #debug
        s = '{:>14}:{:>8},{:>16}\n'.format(japanCodes.get(each.get('code')),each.get('price') , each.get('comparison'))
        japanlines += s
    print(japanlines)

def getCompanyList(manager:MongoDBManager, market:str) -> dict:
    '''get {'symbol':'companyName'} dict of the given market.'''
    market = manager.getCollection(market)
    symbols = manager.getAllDocs()
    companyList = {}
    for t in symbols:
        companyList[t.get('symbol')] = t.get('company')
        #TODO: db内でus:ticker, japan:codeとしているところを変更
    return companyList

def getLatestMaretHistoryAndCreateSentences(manager:MongoDBManager, marketHistory:str, companyList:dict) -> str:
    '''create sentences to be inserted in an email'''
    marketHistory = manager.getCollection(marketHistory)
    today = datetime.datetime.today()
    queryDate = today - datetime.timedelta(days=3) #TODO:実行時はdays=1
    stocks = manager.getSpecificDocs({'date':{'$gte':queryDate}})
    sentences = ''
    for each in stocks:
        # print(each.get('code')) #debug
        #TODO: db内でus:ticker, japan:codeとしているところを変更
        s = '{:>14}:{:>8},{:>16}\n'.format(companyList.get(each.get('code')),each.get('price') , each.get('comparison'))
        sentences += s
    print(sentences)
    return sentences

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
