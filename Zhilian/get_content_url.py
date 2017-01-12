from bs4 import BeautifulSoup #
import urllib.request as ur #请求网站
from pymongo import MongoClient #mongo数据库
import re #正则表达式
import redis #分布式存储数据库
r=redis.Redis(host='xxx.xxx.xxx.xxx',port=6379) #连接主机redis数据库
conn = MongoClient('mongodb://xxx.xxx.xxx.xxx:27017') #连接主机mongo数据库
db = conn.zhilian #数据库 库名
collect=db.information_1 #数据库 表名

def get_infomation(uuu):

    #异常处理：可能存在404 403  HTTP报错
    try:
        html=ur.urlopen(uuu).read().decode('utf-8') #获取源代码

    #处理方法：收集异常链接后期再处理
    except:
        print('失败'+uuu)
        r.sadd('except_url',uuu) #把异常链接存进redis
        return#异常就跳过此次获取

    soup=BeautifulSoup(html,'lxml')#把源代码解析
    dict_info={}
    try:
        # 网址
        dict_info['url'] = uuu

        # 岗位
        job = soup.select('div[class="fixed-inner-box"] h1')[0].get_text()
        dict_info['岗位'] = job

        # 公司名称
        company_name = soup.select('div[class="fixed-inner-box"] h2')[0].get_text()
        dict_info['公司名称'] = company_name

        # 公司福利
        company_welfare = soup.select('div[class="fixed-inner-box"] div div')[0].get_text()
        dict_info['公司福利'] = company_welfare

        # 招聘信息
        employment_info = soup.select('div[class="terminalpage-left"] ul li')[:8]
        for i in employment_info:
            # print(i.select('span')[0].get_text()[:4]+' '+i.select('strong')[0].get_text())
            dict_info[i.select('span')[0].get_text()[:4]] = i.select('strong')[0].get_text()

        # 职位描述
        job_description = soup.select('div[class="tab-cont-box"]')[0].select('div[class="tab-inner-cont"]')[0].select(
            'p')
        str_p = ""
        for i in job_description:
            str_p = str_p + i.get_text()
        dict_info['职位描述'] = str_p

        # 公司资料
        company_data = soup.select('div[class="company-box"] ul li')
        for i in company_data:
            dict_info[i.select('span')[0].get_text()[:4]] = re.sub(r'\s+', "", i.select('strong')[0].get_text())
    except:
        print('失败'+uuu)
        r.sadd('except_url',uuu)
        return
    collect.insert(dict_info)

# get_infomation('http://jobs.zhaopin.com/232036816250813.htm')

while(r.scard('url_all')!=0):
    one_url=r.spop('url_all').decode()
    if('http://xiaoyuan.zhaopin.com/' in one_url):
        continue
    print(one_url)
    get_infomation(one_url)

