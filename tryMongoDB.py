import MongoDBManager
from getInfo import getFromNikkeiScraping, getFromYFUSScraping
from mainProcess import *

manager = MongoDBManager.MongoDBManager()
stockDB = manager.getDB("stock")
usCompanyList = getCompanyList(manager, 'us')
result = getLatestMarketHistoryAndCreateSentences(manager, 'usStockHistory', usCompanyList)
print(result)
