#智联爬虫


###项目概述 
  - **官网** ：[智联招聘](http://jobs.zhaopin.com/all/)
  - **更新快** ：职位每天更新
  - **数据丰富** ：智联招聘包含了全国各个城市各种类型的职位
  
  
###实施情况  
- 重要城市:23个
- 职位分类:约130个
- 招聘信息条数:约250万

###项目说明
- Python版本: python 3.5
- 编译环境: PyCharm Community Edition 
- 第三方库的支持: BeautifulSoup4,pymongo,redis
- 本地库的支持: re,urllib

###功能
- 抓取全国主要城市各种职业发布的招聘信息,保存到mongodb数据库。  
  * 信息包括:  网址 岗位 公司名称 公司福利 招聘信息 职位描述 公司资料
  
###实现方式
>----    
1. 将主要城市和职位分类抓取下来,构造(城市-职位)链接   
2. 通过(城市-职位)链接爬取对应页面的招聘信息链接(含换页)   
3. 从招聘信息链接爬取所需要的招聘信息内容
>----

###异常处理
- 使用urllib模块请求网页时有可能返回403.404等错误,所以进行了异常处理。
- 若http请求报错则把错误链接存起来,继续执行下一条链接。
``` python
    #可能存在404 403  HTTP报错
    try:
        html=ur.urlopen(uuu).read().decode('utf-8') #获取源代码

    #处理方法：收集异常链接后期再处理
    except:
        print('失败'+uuu)
        r.sadd('except_url',uuu) #把异常链接存进redis
        return#异常就跳过此次获取
```

###招聘信息获取
- 使用beautifulsoup模块获取指定标签的内容
``` python
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
```

###项目优点
1.本项目使用了(redis)实现分布式爬虫,用了多台电脑开启多个爬虫同时爬取智联招聘,250万条数据折合5天(网速问题)。  
由于智联没有采取反爬虫机制,所以爬取过程还算是稳定。