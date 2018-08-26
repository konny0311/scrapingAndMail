from getInfo import getFromYFUSScraping, getFromNikkeiScraping
import MongoDBManager

def generateText():
    manager = MongoDBManager.MongoDBManager()
    stockDB = manager.getDB("stock")
    us = manager.getCollection('us')
    res = manager.getAllDocs()
    usStocks = {}
    for info in res:
        usStocks[info.get('company')] = info.get('ticker')
    # print(usStocks)
    text = getFromYFUSScraping(usStocks)
    text += '------------------------\n'
    japan = manager.getCollection('japan')
    res = manager.getAllDocs()
    japanStocks = {}
    for info in res:
        japanStocks[info.get('company')] = info.get('code')
    # print(usStocks)
    text += getFromNikkeiScraping(japanStocks)
    print(text)
    return text

generateText()
