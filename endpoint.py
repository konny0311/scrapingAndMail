#flask:http://flask.pocoo.org/docs/1.0/
#set exporting the FLASK_APP="this file name" in your terminal environment.
#then command "flask run". A server starts.
from flask import Flask
import os
from mainProcess import generateText
import MongoDBManager
import datetime

app = Flask(__name__) #__name__ is a name of this file(module) when you declare it in another module.

# 保有する株価情報をJSONで返す
@app.route('/stocks/currentPrice', methods=['GET'])
def checkCurrentPrice():
    text = generateText()
    return text

    #Lineボット実装例 https://developers.line.me/ja/reference/messaging-api/#send-push-message
    # line_bot_api = LineBotApi('<channel access token>')
    #
    # try:
    #     line_bot_api.push_message('<to>', TextSendMessage(text='Hello World!'))
    # except LineBotApiError as e:
    # # error handle

# 購入した株を登録する
@app.route('/buy/stocks', methods=['POST'])
def updatePurchaseRecord():
    # query parameter取得
    market = request.args.get('market') #'us' or 'japan'
    symbol = request.args.get('symbol')
    buyPrice = request.args.get('price')
    exchange = request.args.get('exchange') # '1' if japan
    units = request.args.get('units')
    date = request.args.get('date') # 'yyyyMMdd'
    purchaseDate = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:]))
    doc = {'market':market, 'symbol':symbol, 'buyPrice':buyPrice, 'exchange': exchange, 'units':units, 'sold':"false", 'date':purchaseDate}
    manager = MongoDBManager.MongoDBManager()
    stockDB = manager.getDB('stock')
    record = manager.getCollection('orderRecord')
    id = manager.insertOneDoc(doc)
    print(id)
    return(id)
    #TODO:企業collection(us, japan)に銘柄無い場合は追加

    #http://api.mongodb.com/python/current/tutorial.html

@app.route('/sell/stocks', methods=['POST'])
def updateSellRecord():
    market = request.args.get('market') #'us' or 'japan'
    symbol = request.args.get('symbol')
    buyPrice = request.args.get('price')
    exchange = request.args.get('exchange') # '1' if japan
    units = request.args.get('units')
    date = request.args.get('date') # 'yyyyMMdd'
    sellDate = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:]))
    doc = {'market':market, 'symbol':symbol, 'buyPrice':buyPrice, 'exchange': exchange, 'units':units, 'sold':"true", 'date':sellDate}
    manager = MongoDBManager.MongoDBManager()
    stockDB = manager.getDB('stock')
    record = manager.getCollection('orderRecord')
    id = manager.insertOneDoc(doc)
    print(id)
    return(id)
