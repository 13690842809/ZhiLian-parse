import redis
from bs4 import BeautifulSoup
import urllib.request as ur
import re
r=redis.Redis(host='xxx.xxx.xxx.xxx',port=6379)  #连接主机redis数据库

#---------下方注释掉的位抓取(城市-职位)链接的代码---------

# def parseCityJob():
#     # 存进redis 4554条  城市+职位
#     url = 'http://jobs.zhaopin.com/all'
#     html = ur.urlopen(url).read().decode('utf-8')
#     soup = BeautifulSoup(html, 'lxml')
#     # 获得城市连接
#     city_div = soup.select('div[class="content-list"]')[0].select('div')[1].select('a')
#     city_url = []
#     for i in city_div:
#         city_url.append(i.attrs['href'])
#
#     # 获得职位分类
#     job_classfic_div = soup.select('div[class="content-list"]')[1].select('div')[1].select('a')
#     job_classfic_url = []
#     for i in job_classfic_div:
#         job_classfic_url.append(re.sub(r'http:\/\/jobs.zhaopin.com(.*?)\/', '', i.attrs['href']))
#     for i in city_url:
#         for j in job_classfic_url:
#             r.sadd('url1', i + j)   #存进redis数据库



#-----------通过(城市-职位)链接爬取对应页面的招聘信息链接(含换页)  -------

def get_content(uuu):
    html=ur.urlopen(uuu).read().decode('utf-8')
    soup=BeautifulSoup(html,'lxml')
    span=soup.select('span[class="post"] a') #内容标签
    page_span=soup.select('div[class="searchlist_page"] span')#换页标签

    #获取第一页内容
    for i in span:
        r.sadd('url_all', i.attrs['href'])


    #判断有无下一页
    if(page_span==[]):
        return

    # 获取页数 构造链接
    else:
        page_num=0
        for i in range(len(page_span)):
            if(page_span[i].get_text()=='下一页'):
                page_num=int(page_span[i-1].get_text())
                break
        for i in range(2,page_num+1):
            print(uuu+'p'+str(i)+'/')
            try:
                html = ur.urlopen(uuu + 'p' + str(i)).read().decode('utf-8')
            except:
                continue
            soup = BeautifulSoup(html, 'lxml')
            span = soup.select('span[class="post"] a')  # 内容标签
            for i in span:
                # print(i.attrs['href'])
                r.sadd('url_all',i.attrs['href'])

# get_content('http://jobs.zhaopin.com/fuzhou/bj300200/')
while(True):
    try:
        one_url=r.spop('url1').decode()
    except:
        break
    print('############################'+one_url)
    get_content(one_url)




