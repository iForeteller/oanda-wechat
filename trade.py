# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 19:41:45 2019

@author: Foreteller
"""

from wxpy import *
import requests
import oandapyV20
import json
from oandapyV20 import API    # the client
import oandapyV20.endpoints.trades as trades
#from oandapyV20.contrib.requests import MarketOrderRequest
#from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails
import oandapyV20.endpoints.orders as orders
#from datetime import datetime

bot = Bot(cache_path=True, console_qr=True)

f1 = bot.friends().search('先知')[0]
f2 = bot.friends().search('Commander')[0]
mp = bot.mps().search('度一咨询')[0]
foreteller = [f1, f2, mp]

reg1 = r'度一每日多空平'
reg2 = r'明日股市预测:   <font size="+2" color="black">'

def exampleAuth():
    accountID, token = None, None
    with open("account.txt") as I:
        accountID = I.read().strip()
    with open("token.txt") as I:
        token = I.read().strip()
    return accountID, token

accountID, access_token = exampleAuth()

instrument1 = 'CN50_USD'
units1 = 1

client = API(access_token=access_token)

def trade(signal):
    print('执行中。。。')
    if signal == '做多':
        tradelist = tradeList()
        if tradelist == None:
            print('下单做多')
            marketOrder(units1)
        else:
            for trade in tradelist:
                if int(trade['units']) < 0:
                    print('平空单')
                    tradeClose(trade['id'])
                    print('下单做多')
                    marketOrder(units1)
    elif signal == '平仓':
        tradelist = tradeList()
        if tradelist != None:
            for trade in tradelist:
                print('平仓')
                tradeClose(trade['id'])
    elif signal == '做空':
        tradelist = tradeList()
        if tradelist == None:
            print('下单做空')
            marketOrder(-units1)
        else:
            for trade in tradelist:
                if int(trade['units']) > 0:
                    print('平多单')
                    tradeClose(trade['id'])
                    print('下单做空')
                    marketOrder(-units1)
    else:
        print('指令无效')
        f1.send_msg('指令无效')
        
def tradeList():
    # request trades list
    print('查询订单')
    r = trades.TradesList(accountID)
    rv = client.request(r)
    tradelist = []
    print('rv.response',rv.response)
    if rv.response['trades'] != []:
        for dict in rv.response['trades']:
            if dict['instrument'] == instrument1:
                tradelist.append({'id':dict['id'],'units':dict['currentUnits']})
    print('查询到的订单：',tradelist)
    return tradelist
def marketOrder(units):
    mktOrder = MarketOrderRequest(
    instrument=instrument1,
    units=units,
    #takeProfitOnFill=TakeProfitDetails(price=EUR_USD_TAKE_PROFIT).data,
    #stopLossOnFill=StopLossDetails(price=EUR_USD_STOP_LOSS).data
    )

    # create the OrderCreate request
    r = orders.OrderCreate(accountID, data=mktOrder.data)
    try:
        # create the OrderCreate request
        rv = api.request(r)
    except oandapyV20.exceptions.V20Error as err:
        print('下单错误')
        f1.send_msg('下单错误'+'\n'+r.status_code +'\n' + err)
    else:
        print('下单成功')
        f1.send_msg('下单成功'+'\n'+json.dumps(rv, indent=2))
def tradeClose(tradeID):
    '''
    data =
        {
          "units": 1
        }
    '''
    r = trades.TradeClose(accountID, tradeID)
    client.request(r)
    print('平仓')
    f1.send_msg('平仓'+'\n'+r.response)

@bot.register(foreteller)
def command(msg):
    if msg.sender == mp and msg.type == SHARING:
        if msg.url is not None:
            str1 = msg.text
            m = str1.find(reg1)
            if m != -1:
                '''
                date = str1[m+7:m+17]
                y = datetime.strptime(date, '%Y-%m-%d')
                z = datetime.now()
                diff = z - y
                if diff.days == 1:
                '''    
                res = str(requests.get(url))
                n = res.find(reg1)
                if n!=i1:
                    signal = res[n+40:n+42]
                    print(signal)
                    trade(signal)
    else:
        signal = msg.text
        print(signal)
        trade(signal)
    
embed()
