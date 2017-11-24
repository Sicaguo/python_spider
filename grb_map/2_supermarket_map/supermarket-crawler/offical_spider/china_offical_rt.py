'''
  通过家乐福官网 爬取大润发全国所有的门店信息

  rbguo 2017-11-23 created 
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
import json

### 
def get_carrefour_all_page_urls():
  header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.3 Safari/537.36'}
  url= 'http://www.rt-mart.com.cn/store/store_map/1'    ###通过地图来寻找，每个省对应一个数字,这个可以从源代码中找到
    ##　获取所有的编号，存放在一个list里
  req = requests.get(url,headers=header)
  html = req.text
    #print('### html = ',html)
  #with open('rt.html','w') as f:
  #  f.write(html)
    #soup = BeautifulSoup(html)
  soup = BeautifulSoup(html,'html5lib')
  tag2= soup.find_all('div','rt_ListItem')
  nums =[]
  for item in tag2:
    print(item)
    num = item.get('province_no')
    nums.append(num)
    print(num)
  print(nums)
  map_urls=[]
  for i in nums:
    map_urls.append('http://www.rt-mart.com.cn/store/store_map/'+str(i))
    #print(map_urls)
  pattern = re.compile(r'storesJsonStr = \'\[(.+?)\]',re.S)
  pattern1 = re.compile(r'pk_id":"(.+?)"',re.S)
  store_ids = []
  for link in map_urls:
    print('#### link =  ',link)
    req = requests.get(link,headers=header)
    html = req.text
      #print(html)
    storesJsonStr = re.findall(pattern , html)[0]
    '''
        storesJsonStr : 
          {"pk_id":"1001","name":"闸北店","lng":"121.454387","lat":"31.304442"},{"pk_id":"1002","name":"杨浦店","lng":"121.528179","lat":"31.294656"},\
          {"pk_id":"1005","name":"大华店","lng":"121.427739876","lat":"31.286101826"},\
          {"pk_id":"1020","name":"松江店","lng":"121.226019","lat":"31.023366"},{"pk_id":"1023","name":"春申店","lng":"121.414572","lat":"31.113807"},\
          {"pk_id":"1027","name":"康桥店","lng":"121.585954","lat":"31.140193"},{"pk_id":"1033","name":"大宁店","lng":"121.45813","lat":"31.280569"},\
          {"pk_id":"1038","name":"奉贤店","lng":"121.451128","lat":"30.912129"},\
          {"pk_id":"1047","name":"曹安店","lng":"121.368202","lat":"31.25786"},\
          {"pk_id":"1055","name":"平型关店","lng":"121.473061","lat":"31.272665"},{"pk_id":"1063","name":"三林店","lng":"121.498179","lat":"31.15548"},\
          {"pk_id":"1066","name":"泗泾店","lng":"121.26735","lat":"31.123577"},{"pk_id":"1072","name":"华漕店","lng":"121.299324","lat":"31.217148"},\
          {"pk_id":"1106","name":"安亭店","lng":"121.166672","lat":"31.293619"},{"pk_id":"1122","name":"泥城店","lng":"121.827018","lat":"30.91532"},\
          {"pk_id":"1102","name":"美兰湖店","lng":"121.357999","lat":"31.415389"},{"pk_id":"1150","name":"南翔店","lng":"121.310666958","lat":"31.2975619164"}
        is a str  ,but not a json format   这个不能直接json解析,单个是可以的{"pk_id":"1001","name":"闸北店","lng":"121.454387","lat":"31.304442"}
        但是多个就不行了{"pk_id":"1001","name":"闸北店","lng":"121.454387","lat":"31.304442"},{"pk_id":"1002","name":"杨浦店","lng":"121.528179","lat":"31.294656"}
    '''
      #print('#### storesJsonStr = ',storesJsonStr) 
      #print(type(storesJsonStr))  
    pk_ids = re.findall(pattern1 , storesJsonStr)
    for pk_id in pk_ids:
      print('### pk_id = ',pk_id)
      store_ids.append(pk_id)
    #print(store_ids)
  store_urls = []
  for id in store_ids: 
    store_urls.append('http://www.rt-mart.com.cn/store/detail/' + str(id))
    #print(store_urls)
  return store_urls
    
def get_single_page_info(url):
  header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.3 Safari/537.36'}
  req = requests.get(url,headers=header)
  html = req.text
  print(html)
  soup = BeautifulSoup(html,'html5lib')
  store_name_div = soup.find_all('div',id = 'store_detail_head')[0]  ###  cannot soup.find_all('div','store_detail_head') ,it equal soup.find_all('div',class_='store_detail_head')
  store_name = store_name_div.p.get_text()
  print('## store_name = ',store_name)
  store_detail_content_div = soup.find_all('div',id = 'store_detail_content')[0]
  #addr = store_detail_content_div.p.get_text()
  #print('#### addr =' ,addr)
  soup = BeautifulSoup(str(store_detail_content_div))
  ps = soup.find_all('p')
  tag_addr   = ps[1]  # addr class tag
  addr_text  = tag_addr.get_text()      # 门店地址：上海市宝山区月罗路2380号       
  addr = addr_text[5:] 
  print('#### addr = ',addr)
  info_list=[]
  info_list.append('大润发')
  info_list.append(store_name)
  info_list.append(addr)
  print(info_list)
  return info_list

def get_rt_market():
  all_store_urls = get_carrefour_all_page_urls()
  print(all_store_urls)
  info_list = []
  with codecs.open('china_offical_markets_rt.csv', 'w+', encoding='utf-8') as market_file:  ### 追加写
    writer = csv.writer(market_file)
    writer.writerow(["品牌","商场名","地址"])
    for url in all_store_urls:
      print('########## url =  ',url)
      info_list = get_single_page_info(url)
      print('########## info_list = ',info_list)
      writer.writerow(info_list)

  

if(__name__ == '__main__'):
    log_file = open("./china_rt_log.txt", 'w+') 
    get_rt_market()
    #get_carrefour_all_page_urls()
    #get_single_page_info('http://www.rt-mart.com.cn/store/detail/1102')
    log_file.close()
