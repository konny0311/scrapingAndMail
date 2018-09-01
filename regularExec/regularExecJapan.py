import sys
sys.path.append('../')
from mainProcess import *

#This code is executed to get stock info everyday.
#exec this code every 15:30pm Japan time
manager = MongoDBManager.MongoDBManager()
stockDB = manager.getDB("stock")
japanCompanyList = getCompanyList(manager, 'japan')
if japanCompanyList is not None:
    getFromNikkeiScraping(japanCompanyList)
