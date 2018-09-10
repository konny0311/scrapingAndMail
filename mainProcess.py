from getInfo import getFromYFUSScraping, getFromNikkeiScraping
import MongoDBManager
import datetime

def generateText() -> str:
    '''get stock price info from usStockHistory and japanStockHistory.
    And create a text of an email'''
    manager = MongoDBManager.MongoDBManager()
    stockDB = manager.getDB('stock')
    #create US stock info
    usCompanyList = getCompanyList(manager, 'us')
    usSentences = getLatestMarketHistoryAndCreateSentences(manager, 'usStockHistory', usCompanyList)

    #create Japan stock info
    japanCompanyList = getCompanyList(manager, 'japan')
    japanSentences = getLatestMarketHistoryAndCreateSentences(manager, 'japanStockHistory', japanCompanyList)
    text = 'US market\n' + usSentences + '---------------\nJapan market\n' + japanSentences
    # print(text) #debug
    return text

def getCompanyList(manager:MongoDBManager, market:str) -> dict:
    '''get {'symbol':'companyName'} dict of the given market.'''
    market = manager.getCollection(market)
    symbols = manager.getAllDocs()
    companyList = {}
    for t in symbols:
        companyList[t.get('symbol')] = t.get('company')
    # print(companyList) #debug
    return companyList

def getLatestMarketHistoryAndCreateSentences(manager:MongoDBManager, marketHistory:str, companyList:dict) -> str:
    '''create sentences to be inserted in an email'''
    portfolio = getPriceAtPurchase(manager, companyList)
    history = manager.getCollection(marketHistory)
    today = datetime.datetime.today()
    weekday = today.weekday()
    # print(weekday) #debug
    if marketHistory == 'japanStockHistory' and weekday == 0:
        queryDate = today - datetime.timedelta(days=3) #get info of Friday when querying on Monday
    elif marketHistory == 'usStockHistory' and weekday == 0:
        queryDate = today - datetime.timedelta(days=10) #get info of Saturday when querying on Monday
    else:
        queryDate = today - datetime.timedelta(days=1)
    stocks = manager.getSpecificDocs({'date':{'$gte':queryDate}})
    sentences = ''
    for each in stocks:
        print(each.get('symbol')) #debug
        symbol = each.get('symbol')
        purchsaeInfo = portfolio.get(symbol)
        print(purchsaeInfo) #debug
        if purchsaeInfo is not None:
            s = '{:>14}:{:>8},{:>16}\n{:>14}\n'.format(companyList.get(symbol),each.get('price') , each.get('comparison'),str(purchsaeInfo[0]) + '/' + str(purchsaeInfo[1]))
            sentences += s
            # print(sentences)
    return sentences

# TODO: what if a company has many purchsae records
def getPriceAtPurchase(manager:MongoDBManager, companyList:dict) -> dict:
    '''get order record from db and calculate stock price when purchasing'''
    '''companyList as dict is like {'symbol':'companyName'}.Returns {'symbol':[price,units] as list} as dict'''
    record = manager.getCollection('orderRecord')
    dictToReturn = {}
    for key in companyList.keys():
        companyOrderRecord = manager.getSpecificDocs({'symbol':key})
        for order in companyOrderRecord:
            if order.get('sold') == 'false':
                purchasePrices = [int(order.get('price')), int(order.get('units'))]
                dictToReturn[key] = purchasePrices
    # print(dictToReturn) #debug
    return dictToReturn
