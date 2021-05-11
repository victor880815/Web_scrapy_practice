#!/usr/bin/env python
# coding: utf-8

# In[61]:


import urllib.request as req
import bs4
import requests
import json
import time, datetime,os


# In[2]:


url = "https://www.twse.com.tw/zh/page/trading/exchange/STOCK_DAY.html"
request=req.Request(url,headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
})
with req.urlopen(request) as response:
    data=response.read().decode("utf-8")
print(data)


# In[20]:




url ='http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20210301&stockNo=2330&'
res = requests.get(url)

s = json.loads(res.text)
#print(s)


for data in (s['data']):
    print (data)



# In[62]:


now = datetime.datetime.now()
print(now)


# In[63]:


dt = datetime.datetime.now()
#dt.year
#dt.month
#dt.day


# In[64]:


id_list = ['2303','2330','1234','3006','2412'] #inout the stock IDs
now = datetime.datetime.now()
year_list = range (2015,now.year+1) #since 2007 to this year
month_list = range(1,13)  # 12 months


# In[65]:


print(year_list)
print(month_list)


# In[66]:


print("{0:0=2d}".format(month))


# In[67]:


#def get_webmsg (year, month, stock_id):
date = str (year) + "{0:0=2d}".format(month) +'01' ## format is yyyymmdd
sid = str(stock_id)
url_twse = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date='+date+'&stockNo='+sid
res =requests.post(url_twse,)
soup = bs4.BeautifulSoup(res.text , 'html.parser')
smt = json.loads(soup.text) #convert data into json
for data in (smt['data']):
    print (data)
#print(smt)
#print(date)
#print(smt)
#return smt


# In[69]:


for stock_id in id_list:
    for year in year_list:
        for month in month_list:
            if (dt.year == year and month > dt.month) :break  # break loop while month over current month
            sid = str(stock_id)
            yy  = str(year)
            mm  = month
            smt = get_webmsg(year ,month, stock_id)
            for data in (smt['data']):
                print (data)
                                        #put the data into smt 
            time.sleep(2)

