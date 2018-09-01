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
    print(text)
    return text

def getCompanyList(manager:MongoDBManager, market:str) -> dict:
    '''get {'symbol':'companyName'} dict of the given market.'''
    market = manager.getCollection(market)
    symbols = manager.getAllDocs()
    companyList = {}
    for t in symbols:
        companyList[t.get('symbol')] = t.get('company')
    print(companyList)
    return companyList

def getLatestMarketHistoryAndCreateSentences(manager:MongoDBManager, marketHistory:str, companyList:dict) -> str:
    '''create sentences to be inserted in an email'''
    marketHistory = manager.getCollection(marketHistory)
    today = datetime.datetime.today()
    queryDate = today - datetime.timedelta(days=7) #TODO:実行時はdays=1
    stocks = manager.getSpecificDocs({'date':{'$gte':queryDate}})
    sentences = ''
    for each in stocks:
        # print(each.get('code')) #debug
        s = '{:>14}:{:>8},{:>16}\n'.format(companyList.get(each.get('symbol')),each.get('price') , each.get('comparison'))
        sentences += s
    return sentences
