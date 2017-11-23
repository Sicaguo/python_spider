# -*- coding: utf-8 -*-
# @Author: Teiei
# @Date:   2017-11-23 19:43:01
# @Last Modified by:   Teiei
# @Last Modified time: 2017-11-24 00:05:46
# 
# TODO 1
# 1 .运行一段是就后会卡住print(city)打印完后
# 2.要加一个判断，每个保存的walmat_urls不为空，则需要去除那里有了得城市。
import re
import requests
import urllib,codecs,csv
from bs4 import BeautifulSoup
def get_walmat_urls():

	citys = []
	ids = [x for x in range(1,35)]
	with open('pingying.txt','r+') as f:
		for line in f.readlines():
			citys.append(line[:-1])  ## 去掉'\n'
	print(citys)
	urls = []
	for id in ids:
		for city in citys:
			print(id)
			print(city)
			url = 'http://www.wal-martchina.com/walmart/store/'+str(id)+'_'+ city+'.htm'
			try:		
				get_single_page(url)   
				urls.append(url)	### 如果没有出错，则说明这个url是正确的
				break;
			except:
				print('##### except1  ')
				pass
	with open('walmat_urls.txt ','w+') as f:    ###将上次遍历得到的urls保存下来。
		f.write(urls)	
	return urls

def get_single_page(url):
	try:
		request = urllib.request.Request(url)
		response = urllib.request.urlopen(request)
		     
		print('type(response) = %s\n\n'%type(response))
		print('response.geturl() = %s\n\n'%response.geturl())
		print('response.info() = %s\n\n'%response.info())
		print('respense.getcode() = %s\n\n'%response.getcode())
		data = response.read()
		#data = data.decode('utf-8',ignore)     ### 同样，这里因为print(str)参数为str 所以需要unicode
		data= data.decode('gbk')
		soup = BeautifulSoup(data)
		tab_tag = soup.find_all('table')[1]
		#print(tab_tag)
		soup1 = BeautifulSoup(str(tab_tag))
		tr_tags = soup1.find_all('tr')   ###第0项目不是符合要求的
		#for tr in tr_tag[1:]:
		#	print('##### tr =', tr)
		with codecs.open('china_offical_markets_walmat.csv', 'a', encoding='utf-8') as market_file:  ### 追加写
			writer = csv.writer(market_file)

			info_list = []
			tr_tag1 = tr_tags[1]  ### 第1项目特殊
			soup2 = BeautifulSoup(str(tr_tag1))
			td_tags = soup2.find_all('td')
			market_name = td_tags[1].string
			market_addr =  td_tags[2].string
			info_list.append("沃尔玛")
			info_list.append(market_name)
			info_list.append(market_addr)
			print(info_list)
			writer.writerow(info_list)

			for tr_tag in tr_tags[2:]:
				info_list = []
				#print('##### tr_tag =', tr_tag)
				soup2 = BeautifulSoup(str(tr_tag))
				td_tags = soup2.find_all('td')
				city = td_tags[0].string
				market_name = td_tags[0].string
				market_addr =  td_tags[1].string
				info_list.append("沃尔玛")
				info_list.append(market_name)
				info_list.append(market_addr)
				print(info_list)
				writer.writerow(info_list)
			

				
	except:
		print('##### except2 : url =  ',url)
		raise


def get_walmat():
	with codecs.open('china_offical_markets_walmat.csv', 'w+', encoding='utf-8') as market_file:
		writer = csv.writer(market_file)
		writer.writerow(["品牌","商场名","地址"])
	urls = get_walmat_urls()
	#for url in urls:
	#	get_single_page(url)

if __name__ == '__main__':

	#with codecs.open('china_offical_markets_walmat.csv', 'w+', encoding='utf-8') as market_file:
	#	writer = csv.writer(market_file)
	#	writer.writerow(["品牌","商场名","地址"])
	get_walmat_urls()
	#url = 'http://www.wal-martchina.com/walmart/store/26_shanghai.htm'
	#get_single_page(url)