# -*- coding: utf-8 -*-
# @Author: Teiei
# @Date:   2017-12-22 17:42:10
# @Last Modified by:   Teiei
# @Last Modified time: 2017-12-26 20:01:39
# -*- coding: utf-8 -*-

'''
	从复件 china_offical_markets_walmat_format.csv 等csv数据中提取出所属的县
'''
import re
import codecs
import csv

import requests
import time
import urllib.request

import datetime

'''
    通过经纬度得到格式化的地址
'''
def get_format_addr_from_lng_lat(lat,lng,ak):
    try:
        url2 = "http://api.map.baidu.com/geocoder/v2/?location=%s,%s&output=json&pois=1&ak=%s"%(lat ,lng,ak)
        #print('#### url2 = ',url2)
        format_json = requests.get(url2).json() 
       # req2 = urllib.request.urlopen(url2)#JSON格式的返回数据

        #respan_json2 = req2.read().decode("utf-8") #将其他编码的字符串解码成unicode
       # respan_python2 = json.loads(respan_json2)  ####  将json格式转为python数据结构
        #print('respan_python2 = ',respan_python2,file=log_file)
        #print('######　format_json_url2 = ',format_json,file=log_file)
        format_addr = format_json['result']['formatted_address']
        #print('### format_addr_url2 = ',format_addr,file=log_file)
       
        return format_addr
    except Exception as crawl_error:

        print(current_time(),"########### except 3 ######################",file=log_file)
        print("########### except 3 ######################")
        return none

### 通过百度地图获取格式化的地址，然后在格式化的地址中提取出地级市
def  get_format_addr_by_map(addr,ak):  ###
	q = addr   		### 要搜索的关键字
	region = '中国'
	ak = 'QPBpKbOkCqkkToYT5VaFixoz3hkykVBi' 
	try:
		#print('###  before url = ')
		url = 'http://api.map.baidu.com/place/v2/search?q={0}&region={1}&&output=json&ak={2}'.format(q, region, ak)
		#print('############# ### url = ',url)
		res_json = requests.get(url).json()
		record0 = res_json['results'][0]  ### 我们给定的地址，查询出来的应该只有一条，但是万一有多条，我们也只取一条，这个不保险 todo 
		time.sleep(1)
		format_addr = get_format_addr_from_lng_lat(record0['location']['lat'],record0['location']['lng'],ak)
		print('#### format addr = ',format_addr)

		### 提取地级市
		#result = re.match(r'(.+?市).+?', format_addr)
		
		return format_addr
	except:

		#print('#### except get_format_addr_by_map')
		print('############# except get_format_addr_by_map  url = ',url)
		return ' '


def format_addr(csvfile):
	print('begin')
	with codecs.open(csvfile,'r+',encoding='utf-8') as f:  
		lines = f.readlines()
	addrs=[]
	for line in lines:
		line = line.strip()
		list_line = line.split(',')
		print(list_line)       
		ak = 'QPBpKbOkCqkkToYT5VaFixoz3hkykVBi' 
		try:
			addr = list_line[2] # 
								#	
								#   "
								#	
		except:
			pass  

		re_result   =  re.match(r'(.+?市|.+?县).*?',addr)
		if   re_result: 
			city = re_result.group (1)
		elif len(addr) > 4:  ### 如果大于4说明就是不对的  则认为不是县，即一般的县不会大于4
			addr =  list_line[1] + addr 
			format_addr = get_format_addr_by_map(addr,ak)
			result = re.match(r'(.+?自治区|.+?省)(.+?自治州|.+?市|.+?盟)(.+?区|.+?市|.+?县|.+?旗).*?',format_addr)
			if result:
				city = result.group(3) 
				#print('return city  ===== ',city)
					
			else:
				city = format_addr
		elif addr == ' ':
			city = list_line[1]  ## 上海等直辖市如果没有县，则取区
		else:
			city = addr
		#print('city = ',city)
		addrs.append(city)

	print(addrs)
	with codecs.open(csvfile[:-4]+'_get_region.csv', 'w+', encoding='utf-8') as f:
		writer = csv.writer(f)
		writer.writerow(["县"])
		for addr in addrs:
			info_list = []
			info_list.append(addr)
			#print(info_list)
			writer.writerow(info_list)

if __name__ == '__main__':
	#csvfiles = ["china_offical_metro.csv","china_offical_markets_walmat.csv","china_offical_markets_rt.csv"]
	#market_names =["麦德龙","沃尔玛","大润发"]
	#for file in csvfiles:
	#	print(file)
	#for market_name in market_names:
	#	print(market_name)
	#for i in  range( int(len(csvfiles)) ):
	#	print(csvfiles[i])
	#	print(market_names[i])
	#	format_addr(csvfiles[i],market_names[i])
	#csvfile = "china_offical_markets_walmat_format.csv"  
	csvfile = "all_province_commanpy_info_all_country_formated_addr.csv" 
	format_addr(csvfile)