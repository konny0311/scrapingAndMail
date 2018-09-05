from getInfo import getFromYFUSScraping, getFromNikkeiScraping
import MongoDBManager
import datetime

def generateText() -> str:
    '''get stock price info from usStockHistory and japanStockHistory.
    And create a text of an email'''
    manager = MongoDBManager.MongoDBManager()
    stockDB = manager.getDB('stock')
    usCompanyList = getCompanyList(manager, 'us')
    usSentences = getLatestMarketHistoryAndCreateSentences(manager, 'usStockHistory', usCompanyList)
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
    marketHistory = manager.getCollection(marketHistory)
    today = datetime.datetime.today()
    weekday = today.weekday()
    if marketHistory is 'japanStockHistory' and weekday is 0:
        queryDate = today - datetime.timedelta(days=3) #get info of Friday when querying on Monday
    elif marketHistory is 'usStockHistory' and weekday is 0:
        queryDate = today - datetime.timedelta(days=2) #get info of Saturday when querying on Monday
    else:
        queryDate = today - datetime.timedelta(days=1)
    stocks = manager.getSpecificDocs({'date':{'$gte':queryDate}})
    sentences = ''
    for each in stocks:
        # print(each.get('code')) #debug
        s = '{:>14}:{:>8},{:>16}\n'.format(companyList.get(each.get('symbol')),each.get('price') , each.get('comparison'))
        sentences += s
    return sentences

# TODO: summarize current ave price
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
    print(dictToReturn) #debug
    return dictToReturn
