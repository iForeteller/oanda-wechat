# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 19:41:45 2019

@author: Foreteller
"""

from wxpy import *
import requests
import oandapyV20
#from datetime import datetime

bot = Bot(cache_path=True, console_qr=True)

f1 = bot.friends().search('先知')[0]
f2 = bot.friends().search('Commander')[0]
mp = bot.mps().search('度一咨询')[0]
foreteller = [f1, f2, mp]

reg1 = r'度一每日多空平'
reg2 = r'明日股市预测:   <font size="+2" color="black">'

def trade(signal):
    if signal == '做多':
    if signal == '平仓':
        
'''
def order_buy():
def order_sell():
def order_close_buy():
def order_close_sell():
def order_select():
'''
    
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
                    trade(signal)
    else:
        signal = msg.text
        trade(signal)
    
embed()
