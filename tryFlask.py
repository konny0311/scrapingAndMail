#flask:http://flask.pocoo.org/docs/1.0/
#set exporting the FLASK_APP="this file name" in your terminal environment.
#then command "flask run". A server starts.
from flask import Flask
import os
from mainProcess import generateText

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
    company = request.args.get('company')
    unitPrice = request.args.get('price')
    units = request.args.get('units')

    # TODO:mongoDB叩く
    #http://api.mongodb.com/python/current/tutorial.html

@app.route('/sell/stocks', methods=['POST'])
def updateSellRecord():
    company = request.args.get('company')
    unitPrice = request.args.get('price')
    units = request.args.get('units')

    # TODO:mongoDB叩く
