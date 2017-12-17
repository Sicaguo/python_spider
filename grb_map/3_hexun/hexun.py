# -*- coding: utf-8 -*-
# @Author: Teiei
# @Date:   2017-12-17 20:00:55
# @Last Modified by:   Teiei
# @Last Modified time: 2017-12-17 22:36:55
# -*- coding: utf-8 -*-
# @Author: Teiei
# @Date:   2017-11-24 15:46:06
# @Last Modified by:   Teiei
# @Last Modified time: 2017-11-24 17:14:16
# @breif: 在麦德龙官网爬取其全国门店地址
import re
import requests
import urllib,codecs,csv
from bs4 import BeautifulSoup
import datetime
import time

def  get_hexun():
	url = 'http://datainfo.stock.hexun.com/hybk/dygs.aspx?fld_areano=328000000'
	header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.3 Safari/537.36'}
	req = requests.get(url)
	html = req.text
	
	soup = BeautifulSoup(html)
	a_tags = soup.find_all('a','amal')
	urls = []
	for  a_tag in a_tags:
		print(a_tag.get_text())  ### 公司简称
		urls.append(a_tag.get('href'))
	print(urls)
	i = 0
	detail_urls = []
	for url in urls:
		#print('  for  url1  = ',url)
		if i%2:
			print('  for  url  = ',url)
			time.sleep(1)
			req = requests.get(url,headers=header)
			html = req.text
			#print(html)
			#with open('detail.html','wb+') as f:
			#	f.write(html)
			soup = BeautifulSoup(html)
			a_tag0 = soup.find_all('a',id = 'a_leftmenu_dt4_1')[0]  ### 公司资料网页
			detail_url = a_tag.get('href')
			print(detail_url)
			detail_urls.append(detail_url)
		i = i+1
	print('detail_urls = ',detail_urls)


	
if __name__ == '__main__':
	get_hexun();