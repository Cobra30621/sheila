# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 00:17:32 2018

@author: linzino
"""
import requests #引入函式庫
from bs4 import BeautifulSoup
import re
import json
import feedparser


def udn_news():
    '''
    抓最新前三篇新聞
    
    回傳是一個dict
    '''
    rss_url = 'https://udn.com/rssfeed/news/2/6638?ch=news'
 
    # 抓取資料
    rss = feedparser.parse(rss_url)
    
    cards = []    
    for index in range(0,3):
        # 抓文章標題
        title = rss['entries'][index]['title']
        # 抓文章連結
        link = rss['entries'][index]['link']
        # 處理摘要格式
        summary =  rss['entries'][index]['summary']
        
        if 'img' in summary:
            soup = BeautifulSoup(summary, 'html.parser')
            p_list = soup.find_all('p')
            # 抓文章摘要 限制只有60個字
            text = p_list[1].getText()[:50]
            # 抓文章圖片
            image = p_list[0].img['src']
        else:
            # 沒有圖片
            text = summary[:50]
            image = 'https://i.imgur.com/vkqbLnz.png'
        
        card = {'title':title,
                'link':link,
                'summary': text,
                'img':image
                }
        cards.append(card)
        
    return cards



def google():
    '''
    抓到最新google map資料
    '''
    pretext = ')]}\''
    
    # 爬下com
    url = 'https://www.google.com.tw/maps/preview/reviews?authuser=0&hl=zh-TW&gl=tw&pb=!1s0x3442abcfe9e7617d%3A0x496596e7748a5757!2i0!3i10!4e3!7m4!2b1!3b1!5b1!6b1'
    resp = requests.get(url)
    text = resp.text.replace(pretext,'')
    soup = json.loads(text)
    
    # 抓第一篇
    first = soup[0][0]
    # 整理資料 
    username = first[0][1]
    time = first[1]
    mesg = first[3]
    star = first[4]
    
    string = '%s \n於 %s 將您評為 %s顆星 \n留言：%s' % (username, time,star,mesg)
    
    return string

def techorangeAi():
    '''
    在techorangeAi 上某個關鍵字最新的文章
    '''
    url = 'https://buzzorange.com/techorange/?s=ai'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    atags = soup.find_all('h4', re.compile('entry-title'))

    cards = []
    for index in range(3):    
        #文章標題

        findtitle = atags[index].a['onclick'].split(',')
        title = findtitle[4].replace('\'', '')
        
        #文章內文
        interUrl = atags[index].a['href']
        resp = requests.get(interUrl)
        soup = BeautifulSoup(resp.text, 'html.parser')
        interAtags = soup.find_all('div', re.compile('entry-content'))
        
        if 'blockquote' in str(interAtags[0]):
            text = str(interAtags[0].blockquote.p)[:50]
            text = text.replace('<p>', ' ')
        else:
            text = interAtags[0].find_all('p',{'class':'p1'})


        '''tmp = interAtags[0].find_all('p',{'class':'p1'})
        tmp[1]'''
        #文章連結
        link = interUrl
        
        #圖片
        img = soup.find_all('img', re.compile('align'))
        image = img[1]['src']   
        
        card = {'title':title,
                    'link':link,
                    'summary': text,
                    'img':image
                    }
        cards.append(card)
 
    
    return cards
    
    
'''    string = '最新4篇techorange貼文：\n'
    for  item in range(3):
        string += atags[item].a['href'] +'\n'
    return string        
    '''

def theNewLens():
    '''
    搜尋關鍵評論網（theNewLens）的科學文章，做成字卡
    '''
    url = 'https://www.thenewslens.com/category/science'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    atags = soup.find_all('div', re.compile('info-box'))
    atags2 = soup.find_all('div', re.compile('img-box'))
    
    cards = []
    for index in range(3):
        #文章標題
        title = atags2[index].a['title']
        
        #文章連結
        link = atags[index].a['href']
        
        #文章內文
        textlist = atags[index].find_all('div', re.compile('description'))
        text = str(textlist[0])
        text = text.replace('<div class="description"> ', '')[:50] 
        
        #圖片
        
        imglist = str(atags2[index].a.div.img).split(',')
        imglist = imglist[2].split(' ')
        image = imglist[1]
        
        
        card = {'title':title,
                        'link':link,
                        'summary': text,
                        'img':image
                        }
        cards.append(card)

    return cards
