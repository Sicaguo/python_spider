# -*- coding: utf-8 -*-
# @Author: Teiei
# @Date:   2017-11-27 17:57:11
# @Last Modified by:   Teiei
# @Last Modified time: 2017-11-28 15:45:51
import urllib.request
from bs4 import BeautifulSoup
import re
import time
import random



# -------------------------------------------------------公用方法----------------------------------------------------
class CommanCalss:
    def __init__(self):
        self.header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'}
        #self.testurl="www.baidu.com"
        self.url="http://blog.csdn.net"

    def getresponse(self,url):
        req = urllib.request.Request(url, headers=self.header)
        resp = urllib.request.urlopen(req, timeout=5)
        content = resp.read()
        return content

    def _is_alive(self,proxy):
        try:
            resp=0
            for i in range(1):   ### 每一个IP都要经过三次考验，如果中间任意一次出错，就将得到except
            	print('### is_alive proxy = ',proxy)
            	proxy_support = urllib.request.ProxyHandler({"http": proxy})
            	opener = urllib.request.build_opener(proxy_support)
            	urllib.request.install_opener(opener)
            	req = urllib.request.Request(self.url, headers=self.header)
            	time.sleep(3)
            	resp = urllib.request.urlopen(req, timeout=5)
            	print('### is alive resp2 = ',resp)
            	code = resp.getcode()
            	print('respense.getcode() = %s\n\n'%code)
            	print(type(code))
            if code == 200 :
            	print('### return ture ')
            	return True
        except:
        	print('### except = ')
        	return False



 # -------------------------------------------------------代理池----------------------------------------------------
class ProxyPool:
    def __init__(self,proxy_finder):
        self.pool=[]
        self.proxy_finder=proxy_finder
        self.cominstan=CommanCalss()

    def get_proxies(self):   
        self.pool=self.proxy_finder.find()
        for p in self.pool:
            if self.cominstan._is_alive(p):
            	print('###continue')
            	continue
            else:
                self.pool.remove(p)
                print('###remove ')

    def get_one_proxy(self):
        return random.choice(self.pool)

    def writeToTxt(self,file_path):
        try:
            fp = open(file_path, "w+")
            for item in self.pool:
                fp.write(str(item) + "\n")
            fp.close()
        except IOError:
            print("fail to open file")


#-------------------------------------------------------获取代理方法----------------------------------------------------
#定义一个基类
class IProxyFinder:
    def __init__(self):
        self.pool = []

    def find(self):
        return

#西祠代理爬取
class XiciProxyFinder(IProxyFinder):
    def __init__(self, url):
        super(XiciProxyFinder,self).__init__()
        self.url=url
        self.cominstan = CommanCalss()

    def find(self):
        for i in range(1, 2):    ### 抓取http://www.xicidaili.com/wn/共10页的内容
            content = self.cominstan.getresponse(self.url + str(i))
            print('### content = ',content)
            soup = BeautifulSoup(content)
            ips = soup.findAll('tr')
            for x in range(2, len(ips)):
                ip = ips[x]
                tds = ip.findAll("td")
                if tds == []:
                    continue
                ip_temp = tds[1].contents[0] + ":" + tds[2].contents[0]
                self.pool.append(ip_temp)
        time.sleep(1)
        return  self.pool

#-------------------------------------------------------测试----------------------------------------------------
if __name__ == '__main__':
    finder = XiciProxyFinder("http://www.xicidaili.com/wn/")
    ppool_instance = ProxyPool(finder)
    ppool_instance.get_proxies()
    ppool_instance.writeToTxt("proxy.txt")