from editText import appendInText
from getInfo import getFromIEX, getFromScraping

def generateText():

    USStocks = ["AAPL"]
    text = getFromIEX(USStocks)
    JapaneseStocks = {"Rakuten": "4755", "Tokyu": "8957", "Fukuoka": "8968"}
    text += "------------------------\n"
    text += getFromScraping(JapaneseStocks)
    return text
