import MongoDBManager
from getInfo import getFromNikkeiScraping, getFromYFUSScraping
from mainProcess import *

manager = MongoDBManager.MongoDBManager()
stockDB = manager.getDB("stock")
usCompanyList = getCompanyList(manager, 'us')
getPriceAtPurchase(manager, usCompanyList)
