# -*- coding: utf-8 -*-

'''
	从获取csv数据中提取出所属的省 市 县
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
        print('#### url2 = ',url2)
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
		print('### url = ',url)
		res_json = requests.get(url).json()
		record0 = res_json['results'][0]  ### 我们给定的地址，查询出来的应该只有一条，但是万一有多条，我们也只取一条，这个不保险 todo 
		time.sleep(1)
		format_addr = get_format_addr_from_lng_lat(record0['location']['lat'],record0['location']['lng'],ak)
		print('#### format addr = ',format_addr)

		### 提取地级市
		'''
		result = re.match(r'(.+?市).+?', format_addr)
		if result:
			city = result.group(1) 
			print('return city  ===== ',city)
			return city
		else:
			print('return format_addr  ===== ',format_addr)
			return format_addr
		'''
		return format_addr
	except:

		print('#### except get_format_addr_by_map')
		return ' '


def format_addr(csvfile):
	with open(csvfile,'r+') as f:
		lines = f.readlines()
	addrs=[]
	for line in lines[1:]:
		line = line.strip()
		list_line = line.split(',')
		print(list_line)       
		ak = 'QPBpKbOkCqkkToYT5VaFixoz3hkykVBi' 
		try:
			addr = list_line[-3] #   办公地址
								#	
								#   
								#	
		except:
			pass   ### 

		##
			  ### 这种是我们想要的，获取地级市级别 (不过有的县级市也会来这里干扰,比如常州溧阳市  所以也要format)

		info_list = []
		#info_list.append(list_line[0])
		print('list_line [7] =',addr )
		re_result =  re.match(r'(.+?自治区|.+?市|.+?省)(.+?自治州|.+?市|.+?盟)(.+?区|.+?市|.+?县).+?',addr)   ### 浙江省湖州市德清县武康镇志远北路636号
		if  re_result:  ### 内蒙古自治区鄂尔多斯市东胜区罕台轻纺街1号
			province = re_result.group (1)													     
			city = re_result.group (2)
			region = re_result.group (3)														
		elif re.match(r'(.+?市).+?',addr):  ##   处理直辖市
			 if re.match(r'(.+?市).+?',addr).group(1)  in ('北京市','天津市','上海市','重庆市'):  #### 上海市松江区思贤路3600号 
			 	if re.match(r'(.+?市)(.+?区|.+?县).+?',addr):  
			 		province = re.match(r'(.+?市)(.+?区|.+?县).+?',addr).group (1)
			 		city = re.match(r'(.+?市)(.+?区|.+?县).+?',addr).group (2)
			 		region= ' '
			 		else:  ### 深圳市南山区深南大道2号   长沙市高新区文轩路2号  上海市浦东大道1号
			 			if  re.match(r'(.+?路).+?',addr):
			 				addr =  re.match(r'(.+?路).+?',addr).group(1)
			 			elif re.match(r'(.+?大道).+?',addr):
			 				addr =  re.match(r'(.+?大道).+?',addr).group(1)
			 			format_city = get_format_addr_by_map(addr,ak)
			 			if re.match(r'(.+?市)(.+?区|.+?县).+?',format_city):   ##   处理直辖市
							province = re.match(r'(.+?市)(.+?区|.+?县).+?',addr).group (1)										## 成都市双流区西航港街道成新大件路289号也会被收录										   
							city = re.match(r'(.+?市)(.+?区|.+?县).+?',addr).group (2)   
							region= ' '
						else:
							province = format_city
							city = ' '
							region = ' '
		elif addr:  ### 如果不为空  通过百度地图提取试一下   
			if  re.match(r'(.+?路).+?',addr):
				addr =  re.match(r'(.+?路).+?',addr).group(1)
			elif re.match(r'(.+?大道).+?',addr):
				addr =  re.match(r'(.+?大道).+?',addr).group(1)
			format_city = get_format_addr_by_map(addr,ak)
			re_result =  re.match(r'(.+?自治区|.+?市|.+?省)(.+?自治州|.+?市|.+?盟)(.+?区|.+?市|.+?县).+?',format_city)   ### 浙江省绍兴市杭州湾上虞经济技术开发区
			if  re_result:  ### 浙江省湖州市德清县武康镇志远北路636号
				province = re_result.group (1)													    
				city = re_result.group (2)
				region = re_result.group (3)														
			elif re.match(r'(.+?市)(.+?区|.+?县).+?',format_city):   ##   处理直辖市
						province = re.match(r'(.+?市)(.+?区|.+?县).+?',addr).group (1)										## 成都市双流区西航港街道成新大件路289号也会被收录										   
						city = re.match(r'(.+?市)(.+?区|.+?县).+?',addr).group (2)   
						region= ' '
			else:
				province = format_city
				city = ' '
				region = ' '
			#print('######### format_city = ',format_city)
			#print('######## province = ',province)
			#print('##### city = ',city)
			#print('###### region = ',region)
		else:
			province = addr
			city = ' '
			region = ' '
		info_list.append(province)
		info_list.append(city)
		info_list.append(region)

	
		addrs.append(info_list)
		print('############### info_list = ',info_list)
		#time.sleep(1)
		'''
		if  re.match(r'(.+?自治州).+?', addr):
			city = re.match(r'(.+?自治州).+?', addr).group(1) 
			print('         city ######   is ',city)
			format_city = get_format_addr_by_map(city,ak)
			addrs.append(format_city)	
		elif  re.match(r'(.+?市).+?', addr):
			city = re.match(r'(.+?市).+?', addr).group(1) 
			print('         city ######   is ',city)
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
				print('#######qqqqq  city1 = ',city )
				format_city = get_format_addr_by_map(city,ak)
				if format_city:
					addrs.append(format_city) 

				

		else:     ### 极其不规则的地址  使用  家乐福 + 利辛人民路店 来搜索,如果失败，则提取广场搜索
			city = market_name+list_line[1]
			format_city = get_format_addr_by_map(city,ak)
			print('#######qqqqq  market_name + city = ',city )
			if format_city:  ### 如果成功找到
				addrs.append(format_city)  ### 不变
			elif re.match(r'(.+?广场).*?', addr):		
				city = re.match(r'(.+?广场).*?', addr).group(1)
				print('#######qqqqq  广场 + city = ',city )
				format_city = get_format_addr_by_map(city,ak)
				if format_city:  ### 如果成功找到
					addrs.append(format_city)  ### 不变
			elif re.match(r'(.+?街).*?', addr):
				
				city = re.match(r'(.+?街).*?', addr).group(1)
				print('#######qqqqq  街 + city = ',city )
				format_city = get_format_addr_by_map(city,ak)
				if format_city:  ### 如果成功找到
					addrs.append(format_city)  ### 不变

	'''	
	try:
		print('#### addrs = ',addrs)   #### 格式化地址
		with codecs.open(csvfile[:-4]+'_formataddr.txt', 'w+', encoding='utf-8') as f:
			writer = csv.writer(f)
			writer.writerow(["省","市","县"])
			for list_info_addr in addrs:
				writer.writerow(list_info_addr)
	
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
				list_line.append(addrs[i][0])
				list_line.append(addrs[i][1])
				list_line.append(addrs[i][2])
				writer.writerow(list_line)
				i = i+1 
			
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
	csvfile = "all_province_commanpy_info_all_country.csv"
	format_addr(csvfile)