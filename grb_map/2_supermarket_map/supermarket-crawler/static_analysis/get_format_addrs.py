# -*- coding: utf-8 -*-

'''
	格式化csv文件中的地址 按XX省XX市XX县
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
        print('#### url2 = ',url2,file=log_file)
        format_json = requests.get(url2).json() 
       # req2 = urllib.request.urlopen(url2)#JSON格式的返回数据

        #respan_json2 = req2.read().decode("utf-8") #将其他编码的字符串解码成unicode
       # respan_python2 = json.loads(respan_json2)  ####  将json格式转为python数据结构
        #print('respan_python2 = ',respan_python2,file=log_file,file=log_file)
        #print('######　format_json_url2 = ',format_json,file=log_file,file=log_file)
        format_addr = format_json['result']['formatted_address']
        #print('### format_addr_url2 = ',format_addr,file=log_file,file=log_file)
       
        return format_addr
    except Exception as crawl_error:

        #print(current_time(file=log_file),"########### except 3 ######################",file=log_file)
        print("########### except 3 ######################",file=log_file)
        return none

### 通过百度地图获取格式化的地址，然后在格式化的地址中提取出地级市
def  get_format_addr_by_map(addr,ak):  ###
	q = addr   		### 要搜索的关键字
	region = '中国'
	ak = 'QPBpKbOkCqkkToYT5VaFixoz3hkykVBi' 
	try:
		#print('###  before url = ',file=log_file)
		url = 'http://api.map.baidu.com/place/v2/search?q={0}&region={1}&&output=json&ak={2}'.format(q, region, ak)
		print('### url = ',url,file=log_file)
		res_json = requests.get(url).json()
		record0 = res_json['results'][0]  ### 我们给定的地址，查询出来的应该只有一条，但是万一有多条，我们也只取一条，这个不保险 todo 
		time.sleep(1)
		format_addr = get_format_addr_from_lng_lat(record0['location']['lat'],record0['location']['lng'],ak)
		print('#### format addr = ',format_addr,file=log_file)

		### 提取地级市
		result = re.match(r'(.+?市).+?', format_addr)
		if result:
			city = result.group(1) 
			print('return city  ===== ',city,file=log_file)
			return city
		else:
			print('return format_addr  ===== ',format_addr,file=log_file)
			return format_addr
	except:

		print('#### except get_format_addr_by_map',file=log_file)
		return '  '
def  get_format_addr_by_map_region(addr,ak):  ###
	q = addr   		### 要搜索的关键字
	region = '中国'
	ak = 'QPBpKbOkCqkkToYT5VaFixoz3hkykVBi' 
	try:
		print('###  before url = ',file=log_file)
		url = 'http://api.map.baidu.com/place/v2/search?q={0}&region={1}&&output=json&ak={2}'.format(q, region, ak)
		print('### url = ',url,file=log_file)
		print('### url = ',url)
		res_json = requests.get(url).json()
		record0 = res_json['results'][0]  ### 我们给定的地址，查询出来的应该只有一条，但是万一有多条，我们也只取一条，这个不保险 todo 
		time.sleep(1)
		format_addr = get_format_addr_from_lng_lat(record0['location']['lat'],record0['location']['lng'],ak)
		print('######################## format addr = ',format_addr,file=log_file)
		print('######################## format addr = ',format_addr)

		### 提取地级市
		'''
		result = re.match(r'(.+?市).+?', format_addr)
		if result:
			city = result.group(1) 
			print('return city  ===== ',city,file=log_file)
			return city
		else:
			print('return format_addr  ===== ',format_addr,file=log_file)'''
		return format_addr
	except:

		print('#### except get_format_addr_by_map_region',file=log_file)
		return '  '

### 通过百度地图通过地址 提取地级市
def format_addr (csvfile,market_name):
	with open(csvfile,'r+') as f:
		lines = f.readlines()
	addrs=[]
	for line in lines[1:]:
		line = line.strip()
		list_line = line.split(',')
		print(list_line,file=log_file)       
		ak = 'QPBpKbOkCqkkToYT5VaFixoz3hkykVBi' 
		try:
			addr = list_line[2]     # 亳州的数据异常，多了一个换行
								#	沃尔玛,沃尔玛购物广场亳州魏武广场分店,亳州市光明路魏武广场西侧新天地国际购物中心地下第一层,"亳州
								#   "
								#	沃尔玛,沃尔玛购物广场合肥翡翠路分店,安徽省合肥市经济技术开发区芙蓉路与翡翠路交叉口港澳广场地上二、三层,合肥'''
		except:
			pass   ### 忽略沃尔玛亳州这种

		##
			  ### 这种是我们想要的，获取地级市级别 (不过有的县级市也会来这里干扰,比如常州溧阳市  所以也要format)
		if  re.match(r'(.+?自治州).+?', addr):
			city = re.match(r'(.+?自治州).+?', addr).group(1) 
			print('         city ######   is ',city,file=log_file)
			format_city = get_format_addr_by_map(city,ak)
			addrs.append(format_city)	
		elif  re.match(r'(.+?市).+?', addr):
			city = re.match(r'(.+?市).+?', addr).group(1) 
			print('         city ######   is ',city,file=log_file)
			format_city = get_format_addr_by_map(city,ak)
			addrs.append(format_city)

		elif re.match(r'(.+?区).*?', addr):
			city =  re.match(r'(.+?区).*?', addr).group(1)
			format_city = get_format_addr_by_map(city,ak)  ### 通过百度地图获取格式化的地址，然后在格式化的地址中提取出地级市
			addrs.append(format_city)
		elif re.match(r'(.+?县).*?', addr):
			city = re.match(r'(.+?县).*?', addr).group(1)       ### 区县肯定找的到
			format_city = get_format_addr_by_map(city,ak)
			addrs.append(format_city)
		elif re.match(r'(.+?号).*?', addr):
			city = re.match(r'(.+?号).*?', addr).group(1)
			format_city = get_format_addr_by_map(city,ak)
			if format_city:  ### 如果成功找到
				addrs.append(format_city)
			elif re.match(r'(.+?街).*?', addr):
				city = re.match(r'(.+?街).*?', addr).group(1)
				format_city = get_format_addr_by_map(city,ak)
				if format_city:  ### 如果成功找到
					addrs.append(format_city)  ### 不变
			else:    ### if not  , try the other method
				city = market_name +list_line[1]
				print('#######qqqqq  city1 = ',city ,file=log_file)
				format_city = get_format_addr_by_map(city,ak)
				if format_city:
					addrs.append(format_city) 

				

		else:     ### 极其不规则的地址  使用  家乐福 + 利辛人民路店 来搜索,如果失败，则提取广场搜索
			city = market_name+list_line[1]
			format_city = get_format_addr_by_map(city,ak)
			print('#######qqqqq  market_name + city = ',city ,file=log_file)
			if format_city:  ### 如果成功找到
				addrs.append(format_city)  ### 不变
			elif re.match(r'(.+?广场).*?', addr):		
				city = re.match(r'(.+?广场).*?', addr).group(1)
				print('#######qqqqq  广场 + city = ',city ,file=log_file)
				format_city = get_format_addr_by_map(city,ak)
				if format_city:  ### 如果成功找到
					addrs.append(format_city)  ### 不变
			elif re.match(r'(.+?街).*?', addr):
				
				city = re.match(r'(.+?街).*?', addr).group(1)
				print('#######qqqqq  街 + city = ',city ,file=log_file)
				format_city = get_format_addr_by_map(city,ak)
				if format_city:  ### 如果成功找到
					addrs.append(format_city)  ### 不变




	try:
		print('#### addrs = ',addrs,file=log_file)   #### 格式化地址
		with codecs.open(csvfile+'_formataddr.txt', 'w+', encoding='utf-8') as f:
			for add in addrs:
				writer = csv.writer(f)
				writer.writerow(add)
	except:
		pass 
	finally:

		with open(csvfile,'r+') as f:
			lines = f.readlines()
		with codecs.open(csvfile[:-4]+'_format.csv', 'w+', encoding='utf-8') as market_file:
			writer = csv.writer(market_file)
			writer.writerow(["品牌","商场名","地址","所属城市","格式化地址"])
			i = 0
			for line in lines[1:]:
				line = line.strip()
				list_line  = line.split(',')  
				list_line.append(addrs[i])
				writer.writerow(list_line)
				i = i+1
### 通过百度地图通过地址 提取区/县/县级市级别
def format_addr_region (csvfile,market_name):
	with codecs.open(csvfile,'r+',encoding='utf-8') as f:  
		lines = f.readlines()
	addrs=[]
	for line in lines[1:]:
		line = line.strip()
		list_line = line.split(',')
		print(list_line,file=log_file)       
		ak = 'QPBpKbOkCqkkToYT5VaFixoz3hkykVBi' 
		try:
			addr = list_line[2]     # 亳州的数据异常，多了一个换行
								#	沃尔玛,沃尔玛购物广场亳州魏武广场分店,亳州市光明路魏武广场西侧新天地国际购物中心地下第一层,"亳州
								#   "
								#	沃尔玛,沃尔玛购物广场合肥翡翠路分店,安徽省合肥市经济技术开发区芙蓉路与翡翠路交叉口港澳广场地上二、三层,合肥'''
		except:
			pass   ### 忽略沃尔玛亳州这种

		##
			  ### 这种是我们想要的，获取地级市级别 (不过有的县级市也会来这里干扰,比如常州溧阳市  所以也要format)



		
		if re.match(r'(.+?区).*?', addr):
			city =  re.match(r'(.+?区).*?', addr).group(1)
			format_city = get_format_addr_by_map_region(city,ak)  ### 通过百度地图获取格式化的地址，然后在格式化的地址中提取出地级市
			addrs.append(format_city)	
		elif re.match(r'(.+?县).*?', addr):
			city =  re.match(r'(.+?县).*?', addr).group(1)
			format_city = get_format_addr_by_map_region(city,ak)  ### 通过百度地图获取格式化的地址，然后在格式化的地址中提取出地级市
			addrs.append(format_city)	
		elif re.match(r'(.+?镇).*?', addr):
			city =  re.match(r'(.+?镇).*?', addr).group(1)
			format_city = get_format_addr_by_map_region(city,ak)  ### 通过百度地图获取格式化的地址，然后在格式化的地址中提取出地级市
			addrs.append(format_city)	
		elif re.match(r'(.+?路).*?', addr):
			city =  re.match(r'(.+?路).*?', addr).group(1)
			format_city = get_format_addr_by_map_region(city,ak)  ### 通过百度地图获取格式化的地址，然后在格式化的地址中提取出地级市
			addrs.append(format_city)	
		elif re.match(r'(.+?号).*?', addr):
			city = re.match(r'(.+?号).*?', addr).group(1)
			format_city = get_format_addr_by_map_region(city,ak)
			if format_city:  ### 如果成功找到
				addrs.append(format_city)
			elif re.match(r'(.+?街).*?', addr):
				city = re.match(r'(.+?街).*?', addr).group(1)
				format_city = get_format_addr_by_map_region(city,ak)
				if format_city:  ### 如果成功找到
					addrs.append(format_city)  ### 不变
			else:    ### if not  , try the other method
				city = market_name +list_line[1]
				print('#######qqqqq  city1 = ',city ,file=log_file)
				format_city = get_format_addr_by_map_region(city,ak)
				if format_city:
					addrs.append(format_city) 
		else:     ### 极其不规则的地址  使用  家乐福 + 利辛人民路店 来搜索,如果失败，则提取广场搜索
			city = market_name+list_line[1]
			format_city = get_format_addr_by_map_region(city,ak)
			print('#######qqqqq  market_name + city = ',city ,file=log_file)
			if format_city:  ### 如果成功找到
				addrs.append(format_city)  ### 不变
			elif re.match(r'(.+?广场).*?', addr):		
				city = re.match(r'(.+?广场).*?', addr).group(1)
				print('#######qqqqq  广场 + city = ',city ,file=log_file)
				format_city = get_format_addr_by_map_region(city,ak)
				if format_city:  ### 如果成功找到
					addrs.append(format_city)  ### 不变
			elif re.match(r'(.+?街).*?', addr):
				
				city = re.match(r'(.+?街).*?', addr).group(1)
				print('#######qqqqq  街 + city = ',city ,file=log_file)
				format_city = get_format_addr_by_map_region(city,ak)
				if format_city:  ### 如果成功找到
					addrs.append(format_city)  ### 不变




	try:
		print('#### addrs = ',addrs,file=log_file)   #### 格式化地址
		with codecs.open(csvfile+'_formataddr.txt', 'w+', encoding='utf-8') as f:
			for add in addrs:
				writer = csv.writer(f)
				writer.writerow(add)
	except:
		pass 
	finally:

		with codecs.open(csvfile,'r+',encoding='utf-8') as f:  
			lines = f.readlines()
		with codecs.open(csvfile[:-4]+'_format.csv', 'w+', encoding='utf-8') as market_file:
			writer = csv.writer(market_file)
			writer.writerow(["品牌","商场名","地址","所属城市","格式化地址"])
			i = 0
			for line in lines[1:]:
				line = line.strip()
				list_line  = line.split(',')  
				list_line.append(addrs[i])
				writer.writerow(list_line)
				i = i+1
if __name__ == '__main__':
	#csvfiles = ["china_offical_metro.csv","china_offical_markets_walmat.csv","china_offical_markets_rt.csv"]
	#market_names =["麦德龙","沃尔玛","大润发"]
	#for file in csvfiles:
#		print(file,file=log_file)
	#for market_name in market_names:
	#	print(market_name,file=log_file)
	#for i in  range( int(len(csvfiles)) ):
	#	print(csvfiles[i],file=log_file)
	#	print(market_names[i],file=log_file)
	#	format_addr(csvfiles[i],market_names[i])
	csvfile = "china_offical_markets_walmat.csv"
	log_file = codecs.open('get_format_addrs.txt','w+',encoding='utf-8') 
	market_name = "沃尔玛"
	format_addr_region(csvfile,market_name)