# -*- coding: utf-8 -*-
# @Author: Teiei
# @Date:   2017-12-02 19:03:25
# @Last Modified by:   Teiei
# @Last Modified time: 2017-12-02 21:52:17
# @breif 抓取全国永辉超市门店信息
import codecs
import csv
import requests
from bs4 import BeautifulSoup
import time
import re
def get_hy():
	with codecs.open('china_offical_yh.csv','w+',encoding = 'gbk') as market_file:
		writer = csv.writer(market_file)
		writer.writerow(['品牌','商场名','地址','开店日期'])
		url = 'http://www.yonghui.com.cn/2008_store.asp?action=3'
		header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.3 Safari/537.36'}
		req = requests.get(url,headers=header)
		#html = req.text
		html = req.content.decode('gbk')  ### 注意这里如果要自己编码，必须content，而不能req.text
		print(html)							### content是二进制 
		soup = BeautifulSoup(html,'lxml')
		table_tags = soup.find_all('table',width='747')
		#print('########### table_tags = ',table_tags)
		for table_tag in table_tags[3:]:
			#print('###### table_tag ',table_tag)
			soup = BeautifulSoup(str(table_tag),'lxml')
			tr_tag0 = soup.find_all('tr')[0]
			print('##### find tr  ')
			soup = BeautifulSoup(str(tr_tag0),'lxml')
			td_tags = tr_tag0 = soup.find_all('td')
			info_list = []
			name = td_tags[0].div.div.get_text()  ### \r\n                          \xa0宁波市
			name = re.match(r'\r\n\s+(.+)', name).group(1)  ## 只取得宁波市
			addr = td_tags[1].div.div.get_text()
			created_time  = td_tags[3].div.div.get_text()
			info_list.append('永辉')
			info_list.append(name)
			info_list.append(addr)
			info_list.append(created_time)
			print(info_list)
			writer.writerow(info_list)
		'''
		soup = BeautifulSoup(html,'lxml')
		br_tag0 = soup.find_all('br')
		print('##### find br ')
		print(str(br_tag0))
		soup = BeautifulSoup(str(br_tag0),'lxml')
		table_tags = soup.find_all('table')
		print('##### find table ')
		print(table_tags)
		for table_tag in table_tags:
			print('###### table_tag ',table_tag)
			soup = BeautifulSoup(str(table_tag),'lxml')
			tr_tag0 = soup.find_all('tr')[0]
			print('##### find tr  ')
			soup = BeautifulSoup(str(tr_tag0),'lxml')
			td_tags = tr_tag0 = soup.find_all('td')
			info_list = []
			name = td_tags[0].div.div.get_text() 
			addr = td_tags[1].div.div.get_text()
			created_time  = td_tags[3].div.div.get_text()
			info_list.append('永辉')
			info_list.append(name)
			info_list.append(addr)
			print(info_list)
			writer.writerow(info_list)'''

if __name__ == '__main__':

	get_hy()