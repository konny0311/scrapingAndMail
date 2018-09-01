import sys
sys.path.append('../')
from mainProcess import *

#This code is executed to get stock info everyday.
#exec this code every 6:00am Japan time
manager = MongoDBManager.MongoDBManager()
stockDB = manager.getDB("stock")
usCompanyList = getCompanyList(manager, 'us')
if usCompanyList is not None:
    getFromYFUSScraping(usCompanyList)
