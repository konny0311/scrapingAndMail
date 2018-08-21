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

# 購入した株を登録する
@app.route('/buy/stocks', methods=['POST'])
def updatePurchaseRecord():
    # query parameter取得
    company = request.args.get('company')
    unitPrice = request.args.get('price')
    units = request.args.get('units')

    # TODO:mongoDB叩く

@app.route('/sell/stocks', methods=['POST'])
def updateSellRecord():
    company = request.args.get('company')
    unitPrice = request.args.get('price')
    units = request.args.get('units')

    # TODO:mongoDB叩く
    
