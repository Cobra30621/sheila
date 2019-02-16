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



#泛科學
def Pansci():
    '''
    在techorangeAi 上某個關鍵字最新的文章
    '''

    url = 'https://pansci.asia/hots/day' 
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    atags = soup.select('table')
    articleList = atags[0].find_all('tr')
        
    cards = []
    for index in range(3):    
        #文章標題

        title = articleList[index + 1].text[:40]
        
        #文章內文
        interUrl = articleList[index + 1].a['href']
        interResp = requests.get(interUrl)
        interSoup = BeautifulSoup(interResp.text, 'html.parser')
        interAtags = interSoup.find('div', {'class':'Zi_ad_ar_iR'})
        
        textList = interAtags.find_all('p')
        text = textList[0].text[:50]
        
        if text == '':
            text = '爬失敗了'
        #文章連結
        link = interUrl
        
        #圖片
        image = 'https://pansci.asia/wp-content/uploads/2015/09/257f5436a53b89af50469aa6e6c67d7a.png'   
        
        card = {'title':title,
                    'link':link,
                    'summary': text,
                    'img':image
                    }
        cards.append(card) 
    
    return cards

#科技報橘
def techorange(newType):
    '''
    在techorangeAi 上某個關鍵字最新的文章
    '''
    newType = newType
    url = 'https://buzzorange.com/techorange/tag/' + newType
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    atags = soup.select('.entry-title')

    cards = []
    for index in range(3):    
        #文章標題

        title = atags[index].text[:40]
        
        #文章內文
        interUrl = atags[index].a['href']
        interResp = requests.get(interUrl)
        interSoup = BeautifulSoup(interResp.text, 'html.parser')
        interAtags = interSoup.select('.entry-content')
        text = interAtags[0].text.replace('\n', '')
        text = text.replace('【我們為什麼挑選這篇文章】', '')[:50]
        
        #文章連結
        link = interUrl
        
        #圖片
        img = interSoup.find_all('img', re.compile('align'))
        image = img[1]['src']   
        
        card = {'title':title,
                    'link':link,
                    'summary': text,
                    'img':image
                    }
        cards.append(card)
 
    
    return cards
    
def techorange2():
    '''
    在techorangeAi 上某個關鍵字最新的文章
    '''
    url = 'https://buzzorange.com/techorange/'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    atags = soup.select('.entry-title')

    cards = []
    for index in range(3):    
        #文章標題

        title = atags[index].text[:40]
        
        #文章內文
        interUrl = atags[index].a['href']
        interResp = requests.get(interUrl)
        interSoup = BeautifulSoup(interResp.text, 'html.parser')
        interAtags = interSoup.select('.entry-content')
        text = interAtags[0].text.replace('\n', '')
        text = text.replace('【我們為什麼挑選這篇文章】', '')[:50]
        
        #文章連結
        link = interUrl
        
        #圖片
#        img = interSoup.find_all('img', re.compile('align'))
#        image = img[1]['src']   
        img = 'https://i.imgur.com/uM5Xj2W.jpg'
        card = {'title':title,
                    'link':link,
                    'summary': text,
                    'img':img
                    }
        cards.append(card)
 
    return cards

#關鍵評論網
def theNewLens(newType):
    '''
    搜尋關鍵評論網（theNewLens）的科學文章，做成字卡
    '''
    newType =  'science'
    url = 'https://www.thenewslens.com/category/' + newType
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    titles = soup.select('.title')
    texts = soup.select('.description')  
    links = soup.select('.img-box') 
    images = soup.select('.lazy-container') 

    cards = []

    for index in range(3):
        #文章標題
        title = titles[index].text[:40]
        
        #文章連結
        link = links[index].a['href']
        
        #文章內文
        text = texts[index].text[:50] 
        
        #圖片
        image = re.findall(r'(https.*?)\d{3,}w',str(images[index]))[2]
        image = image.replace('?auto=compress&amp;h=240&amp;q=80&amp;w=400', '')
        #b = re.findall('350w,[\S]*400w',str(images[0]))
        
        
        
        card = {'title':title,
                        'link':link,
                        'summary': text,
                        'img':'https://i.imgur.com/uM5Xj2W.jpg'
                        }
        cards.append(card)

    return cards


