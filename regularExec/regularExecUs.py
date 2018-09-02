import sys
sys.path.append('../')
from mainProcess import *

#This code is executed to get stock info everyday.
#exec this code every 6:00am Japan time
dayOfWeek = datetime.datetime.today().weekday()
if 1 <= dayOfWeek and dayOfWeek <= 5: #work in weekdays
    manager = MongoDBManager.MongoDBManager()
    stockDB = manager.getDB("stock")
    usCompanyList = getCompanyList(manager, 'us')
    if usCompanyList is not None:
        getFromYFUSScraping(usCompanyList)
