from getInfo import getFromYFUSScraping, getFromNikkeiScraping

def generateText():

    USStocks = {'Apple':'AAPL', 'AT&T':'T'}
    text = getFromYFUSScraping(USStocks)
    text += '------------------------\n'
    JapaneseStocks = {'Rakuten': '4755', 'Tokyu': '8957'}
    text += getFromNikkeiScraping(JapaneseStocks)
    return text

generateText()
