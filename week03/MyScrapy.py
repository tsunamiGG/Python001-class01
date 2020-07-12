import requests
from lxml import etree
from queue import Queue
import threading
import json
import  re
from DB import  ConnDB

dataQueue = Queue() # 存放解析数据的queue
flag = False

class CrawlThread(threading.Thread):
    # 这是爬虫
    def __init__(self,thread_id,queue):
        super().__init__()
        self.thread_id = thread_id
        self.queue = queue

    def run(self) :
        # 重写run
        print(f'启动线程:{self.thread_id}')
        self.scheduler()
        print(f'线程结束:{self.thread_id}')

    def crawler(self,city,pn):
        url = 'https://www.lagou.com/jobs/positionAjax.json'

        headers = {
            'authority': 'www.lagou.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-anit-forge-code': '0',
            'x-requested-with': 'XMLHttpRequest',
            'x-anit-forge-token': 'None',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.lagou.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.lagou.com/jobs/list_python%E5%B7%A5%E7%A8%8B%E5%B8%88/p-city_2?px=default',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
            'cookie': 'LG_HAS_LOGIN=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216876807%22%2C%22%24device_id%22%3A%22171e535602925b-03f36512d927e4-c373667-1327104-171e535602aa12%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2281.0.4044.129%22%7D%2C%22first_id%22%3A%22171e535602925b-03f36512d927e4-c373667-1327104-171e535602aa12%22%7D; RECOMMEND_TIP=true; user_trace_token=20200709084501-a334cce3-b74d-4c13-9856-57373246c5bd; LGUID=20200709084501-842fab3b-6e46-40c2-bd0c-b0e79567f09d; _ga=GA1.2.757311201.1594255501; _gid=GA1.2.1440719219.1594255501; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=ABAAAECABIEACCAC386051FE769090280D45EF2B16F0E99; WEBTJ-ID=20200709153735-17332821f1015f-08f9652f1509b-4353760-1327104-17332821f116ea; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1594255501,1594280256; LGSID=20200709163341-1c6f64f7-699a-4209-b447-cb090ec67775; gate_login_token=1d818623c711792e4afc35a33d306f53fa640fdbf13a8f490843cc5bf89bab4d; LG_LOGIN_USER_ID=6762d50d934b71c54003c05a64389a05a1a90ec2289ccf28fa5fc74661fdd0ec; _putrc=F85F9D15977A87B8123F89F2B170EADC; login=true; unick=%E7%94%A8%E6%88%B74875; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; privacyPolicyPopup=false; X_MIDDLE_TOKEN=3746f4671fb9dbcff4e9d46386b88448; TG-TRACK-CODE=search_code; _gat=1; X_HTTP_TOKEN=9f80c832783ff9c844378249518748716c27d45dcb; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1594287345; LGRID=20200709173545-47fa47b2-ef28-400d-a02e-7abf5cc53829; SEARCH_ID=10c00bb20d374ea4842ebcbf46a9b48f'
        }

        param = {
            'px': 'default',
            'city': city,
            'needAddtionalResult': 'false'
        }

        data = {
            'first': 'false',
            'pn': pn,
            'kd': 'python工程师'
        }

        res = requests.post(url=url , headers=headers , params=param , data=data )

        return res.json()

    # 调度器
    def scheduler(self):
        while True:
            if self.queue.empty():  # 若爬取队列为空
                break
            else:
                city , pn = self.queue.get()
                print(f'下载线程为:{self.thread_id},下载页面:https://www.lagou.com/jobs/positionAjax.json?px=default&city={city}&needAddtionalResult=false')

            try:
                # 下载器
                response = self.crawler(city,pn)
                dataQueue.put(response)
            except Exception as e :
                print('下载出现异常',e)

class ParserThread(threading.Thread):
    # 解析页面内容

    def __init__(self,thread_id,queue):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.queue = queue
        self.dbInfo = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'db': 'python_salary'
        }

    # 重写run
    def run(self) :
        print(f'启动处理线程:{self.thread_id}')
        while not  flag:
            try:
                item = self.queue.get(False)   #队列为空时抛出异常
                if not item:
                    pass
                self.parse_data(item)
                self.queue.task_done()  # get之后检测是否会阻塞

            except Exception as e:
                pass
        print(f'结束线程:{self.thread_id}')

    def parse_data(self,item):
        # 解析数据
        try:
            results = item['content']['positionResult']['result']
            for result in results:
                job = result['positionName']
                low_salary = re.findall(r'(\d+)k',result['salary'])[0]
                high_salary = re.findall(r'(\d+)k',result['salary'])[1]
                city = result['city']
                sql = [f"insert into lagou(job , city ,low_salary , high_salary) values ('{job}','{city}','{low_salary}','{high_salary}');"]
                db = ConnDB(self.dbInfo, sql)
                db.run()

        except Exception as e:
            print('json error:',e)

if __name__ == '__main__':

    param_Queue = Queue(50)
    city_list = ['北京','上海','广州','深圳']

    # 任务队列
    for pn in range(10):
        for city in city_list:
            param_Queue.put((city,pn))

    crawl_threds = []
    crawl_name_list = ['crawl_1','crawl_2','crawl_3']

    # 爬虫进程
    for thread_id in crawl_name_list:
        thread = CrawlThread(thread_id,param_Queue)
        thread.start()
        crawl_threds.append(thread)

    # 解析进程
    parse_threads = []
    parse_name_list = ['parse_1','parse_2','parse_3']
    for thread_id in parse_name_list:
        thread = ParserThread(thread_id , dataQueue )
        thread.start()
        parse_threads.append(thread)

    # 结束crawl线程
    for t in crawl_threds:
        t.join()

    # 结束parse线程
    flag = True
    for t in parse_threads:
        t.join()

    print('退出主线程')








