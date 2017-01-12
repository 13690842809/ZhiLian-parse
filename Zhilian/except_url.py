from bs4 import BeautifulSoup
import urllib.request as ur

from pymongo import MongoClient
import re
import redis

r=redis.Redis(host='192.168.90.225',port=6379)
# conn = MongoClient('mongodb://192.168.90.225:27017')
# db = conn.zhilian
while(r.scard('except_url')!=0):
    one_url=r.spop('except_url').decode()
    try:
        html=ur.urlopen(one_url).read().decode('utf-8')
    except :
        r.sadd('except_url',one_url)
        continue
    soup = BeautifulSoup(html, 'lxml')
    employment_info = soup.select('div[class="terminalpage-left"] ul li[class="outmoded_container_img"]')
    if(employment_info!=[]):
        r.sadd('out_job_url',one_url)
        print(one_url)
        continue
    else:
        r.sadd('url_all',one_url)

