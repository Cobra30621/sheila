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
        img = interSoup.find_all('img', re.compile('align'))
        image = img[1]['src']   
        
        card = {'title':title,
                    'link':link,
                    'summary': text,
                    'img':image
                    }
        cards.append(card)
 
    
    return cards

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
                        'img':image
                        }
        cards.append(card)

    return cards



def fb():
    '''
    搜尋關鍵評論網（theNewLens）的科學文章，做成字卡
    '''
    url = 'https://www.facebook.com/chasedrea?__tn__=%2CdC-R-R&eid=ARDnjjnJesfZGk4eRSXvv3mzSi9A3t5sZ3KokokeDUJH-COyd6dwjMdjxYTfsMjVQ3GygfVOZrgr54r-&hc_ref=ARRXWEZo5GRi3kCiaSIvgsDW0gdAdO5hexa2T6cM3rpCfCRPAtEiepFoBKhi_kNLLT8&fref=nf'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    atags = soup.find_all('div', re.compile('_26ni hidden_elem img'))

    
    cards = []
    for index in range(3):
        #文章標題
        title = atags2[index].a['title']
        
        #文章連結
        link = atags2[index].a['href']
        
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


