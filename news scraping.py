#!/usr/bin/env python
# coding: utf-8

# In[1]:


#載入套件
import requests
import re
from bs4 import BeautifulSoup as Soup
import time
import selenium                
from selenium import webdriver#載入selenium套件


# In[2]:


driver=webdriver.Chrome('/Users/alanlin/Desktop/chromedriver')#建立Chromedriver


# In[3]:


driver.get("https://tw.news.yahoo.com/entertainment")#進入yahoo news 娛樂


# In[4]:


html = driver.page_source
soup = Soup(html,'html.parser')#利用bs4獲取網頁html


# In[5]:


#獲取上半部文章url
top_list = []
for story in soup.find_all('a', {'class': 'Pos(a) W(100%) H(100%) Start(0px) Td(n) B(0px) Trstf(l) Trsde(0s) Trsdu(.18s) Trsp(background-color) Bgc(imageCover)'}):
    top = story['href']
    top_list.append(top)
#print(top_list)


# In[6]:


#向下捲動三次獲取下半部文章url
n_scroll=3
bottom_list = []
for i in range (n_scroll):
    scroll = 'window.scrollTo(0,document.body.scrollHeight);'
    driver.execute_script(scroll)
    html = driver.page_source
    soup = Soup(html,'lxml')
    #利用soup抓取文章url
    for url in soup.find_all('a', {'class': 'C($c-fuji-grey-l) Fw(b) Fz(20px) Lh(23px) LineClamp(2,46px) Fz(17px)--sm1024 Lh(19px)--sm1024 LineClamp(2,38px)--sm1024 mega-item-header-link Td(n) C(#0078ff):h C(#000) LineClamp(2,46px) LineClamp(2,38px)--sm1024 not-isInStreamVideoEnabled'}):
        bottom = url['href']
        bottom = "https://tw.news.yahoo.com"+bottom
        bottom_list.append(bottom)
    time.sleep(2)
#print(bottom_list)


# In[7]:


#將上半部url以及下半部（捲動3次）合併
url_list = top_list + bottom_list
print(url_list)


# In[11]:


title_list=[]
yimg_list=[]
content_list=[]
#url迴圈抓取title、yimg、content
for url in url_list:
    driver.get(url)
    html = driver.page_source
    soup = Soup(html,'html.parser')
    text =""
    
    #利用soup抓取文章title
    titles = soup.find("header", class_="caas-title-wrapper")
    #print(titles.string)
    title_list.append(titles.string)

    
    #利用soup抓取文章yimg    
    yimgs = soup.find("img", class_="caas-img has-preview caas-loaded")
    if yimgs != None:
        #print(yimgs['src'])
        yimg_list.append(yimgs['src'])
    else:
        #print("")
        yimg_list.append("")

    #利用soup抓取文章content
    contents = soup.find_all('p')
    for content in contents:
        #print(content.text)
        for i in range(len(content.text)):
            text = text + content.text[i]
    #利用正規表示式去除內文以外的文字
#     re.sub(r'新聞', '報導', text)
#     re.sub(r'文章', '報導', text)
    sub_text = re.sub(r'新聞', '報導', text)
    sub_text2 = re.sub(r'文章', '報導', sub_text)
    regex = r'更多\s*\w*\s*\s*\w*\s*(新聞)?(文章)?報導'
    x = re.search(regex,sub_text2)
    if x ==None:
        continue
    delete_text = x.group(0)
    #print(delete_text)
    rest_text = sub_text2.split(delete_text,1)[0]
    #print(rest_text)
    content_list.append(rest_text)

        
# print(title_list)
# print(url_list)
# print(yimg_list)
print(content_list)


# In[12]:


#載入json套件
import json 
jsonList = []

#利用迴圈將4個list寫入jsonList
for i in range(0,len(title_list)):
    jsonList.append({"title" : title_list[i], "url" : url_list[i],"yimg" : yimg_list[i],"content" : content_list[i]})
#print(json.dumps(jsonList, indent = 1))

#利用json.dumps寫入json格式
x = json.dumps(jsonList,ensure_ascii=False, indent = 1)
print(x)


# In[13]:


#寫入json檔
file = "yahoo-news.json"
with open(file,"w") as f:
    json.dump(jsonList,f,ensure_ascii=False, indent = 1)

