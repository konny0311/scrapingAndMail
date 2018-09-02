import sys
sys.path.append('../')
from mainProcess import *
import datetime

#This code is executed to get stock info everyday.
#exec this code every 15:30pm Japan time
dayOfWeek = datetime.datetime.today().weekday()
if 0 <= dayOfWeek and dayOfWeek <= 4: #work in weekdays
    manager = MongoDBManager.MongoDBManager()
    stockDB = manager.getDB("stock")
    japanCompanyList = getCompanyList(manager, 'japan')
    if japanCompanyList is not None:
        getFromNikkeiScraping(japanCompanyList)
