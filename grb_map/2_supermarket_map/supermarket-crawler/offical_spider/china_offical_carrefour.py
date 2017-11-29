'''
  通过家乐福官网 爬取家乐福全国所有的门店信息

  原理 ： 通过header的cookie选项来指定要获取的城市，即_C4CookieKeyCityNum={}字段
  todo : 
    1.连续发请求会出错，必须time.sleep() 而且time.sleep()也不是很好，要等很久还不一定能取得
    2.for i in range(10): 这里应该要取得全国城市的数量
    3.todo  上海6个页面返回的都是一个第一个页面了         rbguo fix 2017-11-29  
'''
from urllib import request
from urllib import error
from urllib import parse
from http import cookiejar
import urllib
import re
import codecs
import csv
import requests
import time
from bs4 import BeautifulSoup
import random

def get_carrefour():

  with codecs.open('china_offical_markets.csv', 'w+', encoding='utf-8') as market_file:  ### 追加写
    writer = csv.writer(market_file)
    writer.writerow(["品牌","商场名","地址"])
    url='http://www.carrefour.com.cn/ws/city.ashx'
    proxy_pool = []
    with open('proxy.txt','r+') as f:
      lines = f.readlines() 
    for line in lines:
      proxy_pool.append(line.strip())
    print(proxy_pool)

    #proxies = { "http": "223.15.179.137:3128"} 
    proxies = { }
    for i in range(1):
      i = i+1
      print("### city num = ",i)
      '''
      header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.3 Safari/537.36',
               'Cookie':\
                'ASP.NET_SessionId=4qj3xf2izig5xtobr11fvh0g; \
                _C4CookieKeyCityNum={};\
                Hm_lvt_ad969e28d61c1bff627763d1cccefe7b=1511266659,\
                1511273012; \
                Hm_lpvt_ad969e28d61c1bff627763d1cccefe7b=1511273750; \
                __utmt=1; \
                __utma=95004995.1315565076.1511266659.1511266659.1511273013.2;\
                   __utmb=95004995.4.10.1511273013;\
                __utmc=95004995; \
                __utmz=95004995.1511266659.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'.format(i)}

      '''


      header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0',
               'Cookie':\
                'ASP.NET_SessionId=szgsnf3wzixv3b01vikajhps; \
                 _C4CookieKeyCityNum={}; \
                 Hm_lvt_ad969e28d61c1bff627763d1cccefe7b=1511771124; \
                 Hm_lpvt_ad969e28d61c1bff627763d1cccefe7b=1511771124;\
                 __utmt=1;\
                  __utma=148273317.89550502.1511771124.1511771124.1511771124.1;\
                   __utmb=148273317.1.10.1511771124;\
                    __utmc=148273317;\
                     __utmz=148273317.1511771124.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'.format(i)}
      #proxies = { "http": "http://10.10.1.10:3128", "https": "http://10.10.1.10:1080", } 
      #proxies = { "http": "http://180.126.77.175:39171", "https": "http://59.38.61.247:9797", } 
      #proxies = {'http':'125.46.0.62:53281','http':'182.139.161.64:9999','http':'112.250.65.222:53281','http':'61.155.164.109:3128','http':'113.79.74.83:9797',\

      
      
      #requests.get("http://example.org", proxies=proxies)  

      try :
        time.sleep(2)
        while(1):
          print('### proxies1 is : ',proxies)
          try:
            html=requests.get('http://www.carrefour.com.cn/Store/Store.aspx',headers=header,proxies=proxies,timeout=6)
            
            data = html.text
            print(data)
            print('#### state = ',html.status_code )
            #print(html.headers.Content-Length)
            
            if (html.status_code  == 200):  
              print('### cookies 1 = ',html.cookies.get_dict() )
              html.cookies.clear()
              print('### after cookies 1= ',html.cookies.get_dict() )
              print('###response headers = ',html.headers)
              print('before lenth')
              key = 'Content-Length'
              if key in html.headers:
                print('### yes has ')
                print(html.headers['Content-Length'])
                if html.headers['Content-Length'] > 313: ###　光返回200不够,还要验证确实是返回了目标数据
                  print('####### break1')
                  break
              else: ### 正常网页没有返回Content-Length
                print('####### break2')
                break

              

            proxies={'http': random.choice(proxy_pool)}
          except:
            print('#####　except2222')
            proxies={'http': random.choice(proxy_pool)}
            #pass

        #html=requests.get('http://www.carrefour.com.cn/Store/Store.aspx',headers=header)
        
        data = html.text
        print(data)

        pattern = re.compile(r'末页.+?page=(.+?)"></a>',re.S)
        result = re.findall(pattern , data)
        if (result):
          tatol_page = int(result[0])
        else:
          tatol_page = 1
        print('######## tatol_page = ',tatol_page)
        #print('####### data = ',data)
        html = data
        for j in range(tatol_page):
            j=j+1
            print('### page = ',j)
            if j != 1:

            
              url = "http://www.carrefour.com.cn/Store/Store.aspx?&page=%s"%(j)

              print("#### url = ",url)  
              time.sleep(2)
              try:
                #proxies = {} ## 让每次最先无代理的
                while(1):
                  print('### proxies2 is : ',proxies)
                  try:
                    html=requests.get(url,headers=header,proxies=proxies,timeout=6)  ##　rbguo fix Todo3 2017-11-29  

                   
                    print('#### state = ',html.status_code )
                    print(type(html.status_code))
                    if (html.status_code  == 200):
                      print('### cookies 2 = ',html.cookies.get_dict() )
                      html.cookies.clear()
                      print('### after cookies 2= ',html.cookies.get_dict() )
                      print('###response headers = ',html.headers)
                      if key in html.headers:
                        print('###　Content-Length =　',html.headers['Content-Length'])
                        if html.headers['Content-Length'] > 313: ###　光返回200不够,还要验证确实是返回了目标数据，被封时返回了数据，长度为312
                          print('####### break3')
                          break
                      else:
                          print('####### break4')
                          break  ### 正常网页没有返回Content-Length
                    proxies={'http': random.choice(proxy_pool)}
                  except:
                    proxies={'http': random.choice(proxy_pool)}
                    pass
                #req = requests.get(url,headers=header,proxies=proxies)
                #req = requests.get(url,headers=header)
                html = html.text
                print('##### html2 = ',html)
                #with open('html{}.html'.format(j),'w+') as fd:
                #  fd.write(html2)
                #print('######## html ',html)
                #with codecs.open('{}_guanzhou_{}.html'.format(i,j), 'a', encoding='utf-8') as fd:  ### 追加写
                #  fd.write(html)

                div_bf = BeautifulSoup(html)
                tbody = div_bf.find_all('tbody')
                tbody0 = BeautifulSoup(str(tbody[0]))
                #tbody = a_bf.find_all('tbody')
                #print('#### tbody0  = ',tbody0)
                #with codecs.open('tbody{}.txt'.format(j), 'a', encoding='utf-8') as fb:  ### 追加写
                #  fb.write(str(tbody0))
                
                tr = tbody0.find_all('tr')
                #print('##### tr[0] = ',str(tr[0]))
                #print('##### tr= ',tr)
                #print('####### type tr = ',type(tr))  ## 是一个class对象，但是可迭代
                for tri in tr:
                #  print(' ##### tri = ',tri)
                  tri = BeautifulSoup(str(tri))
                  a = tri.find_all('a')
                  name = a[0].string
                  addr = a[1].string
                  info_list = []
                  info_list.append(name)
                  info_list.append(addr)
                  info_list.insert(0,'家乐福'+addr[0:2])
                  print('#### info_list = ',info_list)
                  print('#### info_list = ',info_list,file=log_file)

                  writer.writerow(info_list)  
              except:
                  print('####### except 2 ##########  city num = %d,page = %d'%(i,j))
                  print('####### except 2 ##########  city num = %d,page = %d'%(i,j),file=log_file)
                  pass
            else:
              try:
                div_bf = BeautifulSoup(html)
                tbody = div_bf.find_all('tbody')
                tbody0 = BeautifulSoup(str(tbody[0]))
                #tbody = a_bf.find_all('tbody')
                #print('#### tbody0  = ',tbody0)
                #with codecs.open('tbody{}.txt'.format(j), 'a', encoding='utf-8') as fb:  ### 追加写
                #  fb.write(str(tbody0))
                  
                tr = tbody0.find_all('tr')
                #print('##### tr[0] = ',str(tr[0]))
                #print('##### tr= ',tr)
                #print('####### type tr = ',type(tr))  ## 是一个class对象，但是可迭代
                for tri in tr:
                #  print(' ##### tri = ',tri)
                  tri = BeautifulSoup(str(tri))
                  a = tri.find_all('a')
                  name = a[0].string
                  addr = a[1].string
                  info_list = []
                  info_list.append(name)
                  info_list.append(addr)
                  info_list.insert(0,'家乐福'+addr[0:2])
                  print('#### info_list = ',info_list)
                  print('#### info_list = ',info_list,file=log_file)

                  writer.writerow(info_list)     
              except:
                print('####### except 3 ##########  city num = %d,page = %d'%(i,j))
                print('####### except 3 ##########  city num = %d,page = %d'%(i,j),file=log_file)   
                pass

          
          
      except:
            print('####### except 1 ##########  city num = ',i)
            print('####### except 1 ##########  city num = ',i,file=log_file)
            pass


if(__name__ == '__main__'):
    log_file = open("./china_carrfour_log.txt", 'w+') 
    get_carrefour()
    log_file.close()
