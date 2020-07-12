import socket
import sys
import os
import threading
from queue import Queue

mutex = threading.Lock()
DataQueue = Queue()

class ScanThread(threading.Thread):
    # 扫描端口

    def __init__(self,thread_id,queue,mode):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.queue = queue
        self.mode = mode

    def run(self) :
        # 重写run
        mutex.acquire()
        print(f'启动线程：{self.thread_id}')
        mutex.release()
        self.scheduler()
        mutex.acquire()
        print(f'结束线程：{self.thread_id}')
        mutex.release()

    # 任务调度
    def scheduler(self):
        while True:
            if self.queue.empty():
                break
            else:
                ip , port = self.queue.get()
                try:
                    if self.mode == 'tcp':
                        mutex.acquire()
                        # print('扫描线程为：', self.thread_id, " 扫描端口:：", port)
                        mutex.release()
                        msg = Tcp(ip,port)
                    else:
                        mutex.acquire()
                        # print('扫描线程为：', self.thread_id, " 扫描IP:", ip)
                        mutex.release()
                        msg = Ping(ip)
                    mutex.acquire()
                    print(msg)
                    mutex.release()
                except Exception as e:
                    print('扫描出现异常:',e)


def Ping(ip):
    code =  os.popen('ping %s' % ip).read()

    if '100% 丢失' in code:
        return (f'ip/domain:{ip} Ping 不通')
    else:
        DataQueue.put(ip)
        return (f'ip/diomain :{ip}  Ping 正常')

def Tcp(ip,port):
    address = (ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(3)
        s.connect(address)
        data = s.recv(512)
        s.send(b'test')
        s.close()
        DataQueue.put(f'{ip}:{port}')
        return (f'{ip}:{port} 已开放')
    except ConnectionRefusedError:
        return (f'{ip}:{port} 未开放')
    except socket.gaierror:
        return (f'IP: {ip} 输入不正确')
    except socket.timeout:
        return (f'TCP连接 {ip}:{port} 超时')

def ScanPort(ip,threading_num,file=None):
    IpQueue = Queue(1024*255)
    ips = []
    ip_list = ip.split('-')
    if len(ip_list) == 1:
        print(Ping(ip))
    else:
        ip_start = ip_list[0].split('.')
        ip_end = ip_list[1].split('.')
        start_num = int(ip_start[3])
        end_num = int(ip_end[3])
        for num in range(start_num,end_num+1):
            ip_start[3] = str(num)
            ip = '.'.join(ip_start)
            ips.append(ip)

    for port in range(1,1025):
        for ip in ips:
            IpQueue.put((ip,port))

    # 扫描线程
    scan_threads = []
    scan_name_list = []
    for num in range(threading_num):
        scan_name_list.append(f'scan_{num+1}')
    for thread_id in scan_name_list:
        thread = ScanThread(thread_id,IpQueue,'tcp')
        thread.start()
        scan_threads.append(thread)

    for t in scan_threads:
        t.join()

    if file != None :
        with open(file,'a',encoding='gbk') as File:
            while not DataQueue.empty():
                ip = DataQueue.get()
                File.write(ip+'\n')

def ScanPing(ip,threading_num,file=None):
    IpQueue = Queue(255)
    ip_list = ip.split('-')
    if len(ip_list) == 1:
        print(Ping(ip))
    else:
        ip_start = ip_list[0].split('.')
        ip_end = ip_list[1].split('.')
        start_num = int(ip_start[3])
        end_num = int(ip_end[3])
        for num in range(start_num,end_num+1):
            ip_start[3] = str(num)
            ip = '.'.join(ip_start)
            IpQueue.put((ip,None))

        # 扫描线程
        scan_threads = []
        scan_name_list = []
        for num in range(threading_num):
            scan_name_list.append(f'scan_{num+1}')
        for thread_id in scan_name_list:
            thread = ScanThread(thread_id,IpQueue,mode='ping')
            thread.start()
            scan_threads.append(thread)

        for t in scan_threads:
            t.join()
    if file != None :
        with open(file,'a',encoding='gbk') as File:
            while not DataQueue.empty():
                ip = DataQueue.get()
                File.write(ip+'\n')
        print(f'结果写入{file}成功')
