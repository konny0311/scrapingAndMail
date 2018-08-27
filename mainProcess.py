from getInfo import getFromYFUSScraping, getFromNikkeiScraping
import MongoDBManager
import datetime

def generateText():
    manager = MongoDBManager.MongoDBManager()
    stockDB = manager.getDB('stock')
    usHisotry = manager.getCollection('usHisotry')
    # us = manager.getCollection('us')
    today = datetime.datetime.today()
    queryDate = today - datetime.timedelta(days=1)
    usStocks = manager.getSpecificDocs({'date':{'gte':queryDate}})
    print(usStocks)
    for each in manager.getAllDocs():
        print(each.get('ticker'))
    # res = manager.getAllDocs()
    # usStocks = {}
    # for info in res:
    #     usStocks[info.get('company')] = info.get('ticker')
    # # print(usStocks)
    # text = getFromYFUSScraping(usStocks)
    # text += '------------------------\n'
    # japan = manager.getCollection('japan')
    # res = manager.getAllDocs()
    # japanStocks = {}
    # for info in res:
    #     japanStocks[info.get('company')] = info.get('code')
    # # print(usStocks)
    # text += getFromNikkeiScraping(japanStocks)
    # print(text)
    # return text

generateText()
