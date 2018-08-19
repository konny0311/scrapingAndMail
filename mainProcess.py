from getInfo import getFromIEX, getFromScraping

def generateText():

    USStocks = ['AAPL','F']
    text = getFromIEX(USStocks)
    # JapaneseStocks = {'Rakuten': '4755', 'Tokyu': '8957', 'Fukuoka': '8968'}
    # text += '------------------------\n'
    # text += getFromScraping(JapaneseStocks)
    return text

generateText()
