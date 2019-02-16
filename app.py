# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 18:12:45 2018

@author: linzino
"""
# server-side
from flask import Flask, request, abort

# line-bot
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

# package
import re
from datetime import datetime 

# customer module
import mongodb
import corwler


app = Flask(__name__)

line_bot_api = LineBotApi('qxQIS8TTitqfZkp4+wuHQCe+pEWKskFrxr/jRB8mRMjaEr5EHgZKKwWC1MX+UUy6sbqD1Gbr299QTpplU3idbEBBTGs/LQZGG6dHCUnvK7Fs8my2hCIwYPlw92p/W+Vs97wZQQASgXsVT6/oADxNNQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('258c64afe44ab5ed8e041a75f88fcf27')

#自動傳訊息
datetime.datetime()

#基本設定
import schedule
import time
from pymongo import MongoClient
import urllib.parse
import datetime

yourID='U952f3be2ef6be155c9b8af9d47aff137'

'''
#執行工作
def job():
    for i in techorangeNew:
        dic = corwler.techorange(i)
        remessage = makeEverydayCard(dic)
        line_bot_api.push_message(yourID, remessage)

second_5_j = schedule.every().day.at('21:25').do(job)

#迴圈
while True: 
    schedule.run_pending()

'''

@app.route("/callback", methods=['POST'])
def callback():

    
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(FollowEvent)
def handle_follow(event):
    '''
    當使用者加入時觸動
    '''
    # 取得使用者資料
    profile = line_bot_api.get_profile(event.source.user_id)
    name = profile.display_name
    uid = profile.user_id
    
    print(name)
    print(uid)
    # Udbddac07bac1811e17ffbbd9db459079
    if mongodb.find_user(uid,'users')<= 0:
        # 整理資料
        dic = {'userid':uid,
               'username':name,
               'creattime':datetime.now(),
               'Note':'user',
               'ready':0}
        
        mongodb.insert_one(dic,'users')

#做卡片
def makeCard(dic, event):
    dic = dic
    columns = []
    for i in range(3):
        carousel = CarouselColumn(
                    thumbnail_image_url = dic[i]['img'],
                    title = dic[i]['title'],
                    text = dic[i]['summary'],
                    actions=[
                        URITemplateAction(
                            label = '點我看新聞',
                            uri = dic[i]['link']
                          )
                        ]
                    )
        columns.append(carousel)
    
    remessage = TemplateSendMessage(
                alt_text='Carousel template',
                template=CarouselTemplate(columns=columns)
                )
    
    
    line_bot_api.reply_message(event.reply_token, remessage)      
        

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    '''
    當收到使用者訊息的時候
    '''
    profile = line_bot_api.get_profile(event.source.user_id)
    name = profile.display_name
    uid = profile.user_id
    message = event.message.text
    print(name)
    print(uid)
    print(message)
    
    dic = {'userid':uid,
       'username':name,
       'creattime':datetime.now(),
       'mess':message}
    mongodb.insert_one(dic,'message')
    

#關鍵評論網
            
    if re.search('theNewLens', event.message.text, re.IGNORECASE):
     
        dic = corwler.theNewLens('science')       
        makeCard(dic, event)

        dic = corwler.theNewLens('business')
        makeCard(dic, event)

        dic = corwler.theNewLens('career')       
        makeCard(dic, event)
        
        return 0 

#科技報橘
        
    if re.search('科技報橘', event.message.text, re.IGNORECASE):
        #人工智慧
        dic = corwler.techorange('artificialintelligence/')
        makeCard(dic, event)    

        #全部
        dic = corwler.techorange2()        
        makeCard(dic, event)
        
#泛科學       
    if re.search('泛科學', event.message.text, re.IGNORECASE):
        dic = corwler.Pansci()
        makeCard(dic, event)    


if __name__ == '__main__':
    app.run(debug=True)