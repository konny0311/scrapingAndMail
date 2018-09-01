import MongoDBManager
from getInfo import getFromNikkeiScraping, getFromYFUSScraping
from mainProcess import getCompanyList

manager = MongoDBManager.MongoDBManager()
stockDB = manager.getDB("stock")
usCompanyList = getCompanyList(manager, 'us')
getFromYFUSScraping(usCompanyList)
