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
from oandapyV20.contrib.requests import MarketOrderRequest
from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails
import oandapyV20.endpoints.orders as orders
from datetime import datetime

bot = Bot(cache_path=True, console_qr=True)

f1 = bot.friends().search('先知')[0]
f2 = bot.friends().search('Commander')[0]
mp = bot.mps().search('度一咨询')[0]
foreteller = [f1, f2, mp]

reg1 = r'度一多空平(火星系统)'
reg_red = r'明日股市预测:   <font size="+2" color="red">'
reg_green = r'明日股市预测:   <font size="+2" color="green">'
reg_black = r'明日股市预测:   <font size="+2" color="black">'

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
        if tradelist == []:
            print('下单做多')
            f1.send_msg('下单做多')
            marketOrder(units1)
        else:
            for trade in tradelist:
                if int(trade['units']) < 0:
                    print('平空单')
                    f1.send_msg('平空单')
                    tradeClose(trade['id'])
                    print('下单做多')
                    f1.send_msg('下单做多')
                    marketOrder(units1)
                else:
                    print('已存在多单')
                    f1.send_msg('已存在多单')
    elif signal == '平仓':
        tradelist = tradeList()
        if tradelist != []:
            for trade in tradelist:
                print('平仓')
                f1.send_msg('平仓')
                tradeClose(trade['id'])
        print('没有持仓')
        f1.send_msg('没有持仓')
    elif signal == '做空':
        tradelist = tradeList()
        if tradelist == []:
            print('下单做空')
            f1.send_msg('下单做空')
            marketOrder(-units1)
        else:
            for trade in tradelist:
                if int(trade['units']) > 0:
                    print('平多单')
                    f1.send_msg('平多单')
                    tradeClose(trade['id'])
                    print('下单做空')
                    f1.send_msg('下单做空')
                    marketOrder(-units1)
                else:
                    print('已存在空单')
                    f1.send_msg('已存在空单')
    else:
        print('指令无效')
        f1.send_msg('指令无效')
        
def tradeList():
    # request trades list
    print('查询订单')
    r = trades.TradesList(accountID)
    rv = client.request(r)
    tradelist = []
    print('rv:',rv)
    if rv['trades'] != []:
        for dict in rv['trades']:
            if dict['instrument'] == instrument1:
                tradelist.append({'id':dict['id'],'units':dict['currentUnits']})
    print('查询到的订单：',tradelist)
    return tradelist
def marketOrder(units):
    print('执行下单')
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
        print('下单中。。。')
        rv = client.request(r)
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
    rv = client.request(r)
    print('平仓')
    f1.send_msg('平仓'+'\n'+json.dumps(rv, indent=2))

@bot.register(foreteller)
def command(msg):
    print(msg)
    f1.send_msg(msg)
    if msg.sender in foreteller and msg.url is not None:
        print(msg.url)
        f1.send_msg(msg.url)
        str1 = msg.text
        print(msg.text)
        f1.send_msg(msg.text)
        m = str1.find(reg1)
        print('reg1',m)
        f1.send_msg(m)
        if m != -1:
            date = str1[m+11:m+21]
            print(date)
            f1.send_msg(date)
            y = datetime.strptime(date, '%Y-%m-%d')
            z = datetime.now()
            diff = y - z
            if diff.days >= 0:
                print('get article')
                res = requests.get(msg.url).text
                if res.find(reg_red) != -1:
                    n = res.find(reg_red)
                    print('reg_red',n)
                    f1.send_msg(n)
                    print(n)
                    signal = res[n+38:n+40]
                    print(signal)
                    f1.send_msg(signal)
                    trade(signal)
                elif res.find(reg_green) != -1:
                    n = res.find(reg_green)
                    print('reg_green',n)
                    f1.send_msg(n)
                    print(n)
                    signal = res[n+40:n+42]
                    print(signal)
                    f1.send_msg(signal)
                    trade(signal)
                elif res.find(reg_black) != -1:
                    n = res.find(reg_black)
                    print('reg_black',n)
                    f1.send_msg(n)
                    print(n)
                    signal = res[n+40:n+42]
                    print(signal)
                    f1.send_msg(signal)
                    trade(signal)
    elif msg.sender in [f1,f2]:
        signal = msg.text
        print(signal)
        f1.send_msg(signal)
        trade(signal)
    
embed()
