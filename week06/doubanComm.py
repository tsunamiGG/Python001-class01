import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
#爬取评论
def getComment(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    req =requests.get(url,headers=headers)
    content = req.content
    bs = BeautifulSoup(content, 'html.parser')
    star_tags = bs.findAll('span',attrs={"class":re.compile(r'^allstar\d{2} rating$')})
    star=[int(re.findall(r'\d', i['class'][0])[0]) for i in star_tags]
    comment_tags = bs.findAll('span', 'short')
    comments = [i.string.replace("\r", "").replace("\n", "") for i in comment_tags]
    print(star,comments)
    return [star,comments]
all_result={'n_star':[],'short':[]}
for page in range(2):  
    url = 'https://movie.douban.com/subject/1292052/comments?start=' + str(20*page) + '&limit=20&sort=new_score&status=P'
    print('第%s页的评论:' % (page+1))
    result = getComment(url)
    all_result['n_star']+=result[0]
    all_result['short']+=result[1]
    print(url + '\n')

#情感分析
df=pd.DataFrame(all_result)
df['id']=df.index
from snownlp import SnowNLP
def _sentiment(text):
    s = SnowNLP(text)
    return s.sentiments
df["sentiment"] = df.short.apply(_sentiment)
#保存到数据库
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR,INT,FLOAT,BIGINT
connect_info = 'mysql+pymysql://root:rootroot@localhost:3306/db1?charset=UTF8MB4'
engine = create_engine(connect_info) 
df.to_sql(name = 'douban_t',con = engine,if_exists = 'replace',index = False,dtype = {'id': BIGINT,'n_star': INT,'short': VARCHAR(length=255),'sentiment':FLOAT(12,10)})