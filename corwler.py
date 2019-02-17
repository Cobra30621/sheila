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

#科技報橘用請求
def getHTMLText(url):
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding
        return resp.text
    except:
        return ''

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

        title = articleList[index + 1].text.replace('0' + str(index + 1), '')[:40]
        title = title.replace('\n', '')
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



#科技報橘人工智慧
def techorangeAi():

    url = 'https://buzzorange.com/techorange/tag/artificialintelligence/'
    respText = getHTMLText(url)
    soup = BeautifulSoup(respText, 'html.parser')
    atags = soup.select('.entry-title')

    cards = []
    for index in range(3):    
        #文章標題

        title = atags[index].text[:40]
        
        #文章內文
        interUrl = atags[index].a['href']
        interResp = getHTMLText(interUrl)
        interSoup = BeautifulSoup(interResp, 'html.parser')
        interAtags = interSoup.select('.entry-content')
        text = interAtags[0].text.replace(' ', '')
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
 
#科技報橘首頁
def techorange():

    url = 'https://buzzorange.com/techorange/'
    respText = getHTMLText(url)
    soup = BeautifulSoup(respText, 'html.parser')
    atags = soup.find_all('a', {'class':'post-thumbnail'})
        
    cards = []
    for index in range(3):    
        #文章標題
        interUrl = atags[index]['href']
        interResp = requests.get(interUrl)
        interSoup = BeautifulSoup(interResp.text, 'html.parser')
        interAtags = interSoup.select('.entry-content')
        
        titleAtags = interSoup.find_all('header', {'class':'entry-header post-header'})
        title = titleAtags[0].h1.text[:40]
        
        #文章內文

        text = interAtags[0].text.replace('\n', '')
        text = text.replace('【我們為什麼挑選這篇文章】', '')[:50]
        
        #文章連結
        link = interUrl
        
        #圖片
        image = atags[index]['style'].replace('background-image:url(', '')
        image = image.replace(')', '')

        card = {'title':title,
                    'link':link,
                    'summary': text,
                    'img':image
                    }
        cards.append(card)
 
    return cards

#關鍵評論網
def theNewLens(newType):
    '''
    搜尋關鍵評論網（theNewLens）的科學文章，做成字卡
    '''
    newType =  newType
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
        title = titles[index].text.replace(' ', '')[:40]
        
        #文章連結
        link = links[index].a['href']
        
        #文章內文
        text = texts[index].text.replace(' ', '')[:50] 
        
        #圖片
        image = 'https://pansci.asia/wp-content/uploads/2015/09/257f5436a53b89af50469aa6e6c67d7a.png'
        #b = re.findall('350w,[\S]*400w',str(images[0]))
        
        
        
        card = {'title':title,
                        'link':link,
                        'summary': text,
                        'img': image
                        }
        cards.append(card)

    return cards


