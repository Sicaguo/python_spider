'''
  通过家乐福官网 爬取家乐福全国所有的门店信息

  原理 ： 通过header的cookie选项来指定要获取的城市，即_C4CookieKeyCityNum={}字段
  todo : 
    1.连续发请求会出错，必须time.sleep() 而且time.sleep()也不是很好，要等很久还不一定能取得
    2.for i in range(10): 这里应该要取得全国城市的数量
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

def get_carrefour():

  with codecs.open('china_offical_markets_rt.csv', 'w+', encoding='utf-8') as market_file:  ### 追加写
    writer = csv.writer(market_file)
    writer.writerow(["品牌","商场名","地址"])
    
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.3 Safari/537.36'}
    target_url= 'http://www.rt-mart.com.cn/store/store_map/1'    ###通过地图来寻找，每个省对应一个数字,这个可以从源代码中找到
    ##　获取所有的编号，存放在一个list里
    req = requests.get(url,headers=header)




    for i in range(10):
      i = i+1
      print("### city num = ",i)
      header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.3 Safari/537.36',
               'Cookie':'ASP.NET_SessionId=4qj3xf2izig5xtobr11fvh0g;  _C4CookieKeyCityNum={}; Hm_lvt_ad969e28d61c1bff627763d1cccefe7b=1511266659,\
               1511273012; Hm_lpvt_ad969e28d61c1bff627763d1cccefe7b=1511273750; __utmt=1; __utma=95004995.1315565076.1511266659.1511266659.1511273013.2;\
                __utmb=95004995.4.10.1511273013; __utmc=95004995; __utmz=95004995.1511266659.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'.format(i)}

    #header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.3 Safari/537.36',
    #        'Cookie':'ASP.NET_SessionId=4qj3xf2izig5xtobr11fvh0g; _C4CookieKeyCity={}; _C4CookieKeyCityNum=77; \
    #Hm_lvt_ad969e28d61c1bff627763d1cccefe7b=1511266659,1511273012; Hm_lpvt_ad969e28d61c1bff627763d1cccefe7b=1511273750; __utmt=1; \
    # __utma=95004995.1315565076.1511266659.1511266659.1511273013.2; __utmb=95004995.4.10.1511273013; __utmc=95004995; 
    #__utmz=95004995.1511266659.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'.format(city),}
      #time.sleep(1)
     
      try :
        time.sleep(3)
        html=requests.get('http://www.carrefour.com.cn/Store/Store.aspx',headers=header)
      
        data = html.text
        #print(html.text)

        pattern = re.compile(r'末页.+?page=(.+?)"></a>',re.S)
        result = re.findall(pattern , data)
        if (result):
          tatol_page = int(result[0])
        else:
          tatol_page = 1
        print('######## tatol_page = ',tatol_page)
        for j in range(tatol_page):
            j=j+1
            print('### page = ',j)
            
            url = "http://www.carrefour.com.cn/Store/Store.aspx?&page=%s"%(j)

            print("#### url = ",url)
            time.sleep(3)
            try:
              req = requests.get(url,headers=header)
              html = req.text
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
                print('####### except 1 ##########  city num = %d,page = %d'%(i,j))
                print('####### except 1 ##########  city num = %d,page = %d'%(i,j),file=log_file)
                pass
        
          
      except:
            print('####### except 1 ##########  city num = %d,page = %d'%(i,j))
            print('####### except 1 ##########  city num = %d,page = %d'%(i,j),file=log_file)
            
            pass


if(__name__ == '__main__'):
    log_file = open("./china_carrfour_log.txt", 'w+') 
    get_carrefour()
    log_file.close()
