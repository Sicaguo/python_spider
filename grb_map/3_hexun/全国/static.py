# -*- coding: utf-8 -*-
# @Author: Teiei
# @Date:   2017-12-23 07:40:32
# @Last Modified by:   Teiei
# @Last Modified time: 2017-12-24 09:47:36
'''
	分类个各市的数据，每个是生成一个csv表
'''
import re
import codecs
import csv

import requests
import time
import urllib.request

import datetime
import os

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

'''
	遍历csvfile文件，通过倒数第三列(地级市)来拆分,每个地级市生成一个独立的csv文件
'''

def mkdir(path):

    # 引入模块

   
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        os.makedirs(path) 
        print(path+' 创建成功')
        return True
    else:

        # 如果目录存在则不创建，并提示目录已存在
        print(path+' 目录已存在')
        return False
def format_addr(csvfile,index):
	with codecs.open(csvfile,'r+',encoding='utf-8') as f:  
		lines = f.readlines()
	addrs=[]


	####从csv读取数据,存放在list_lines里面
	list_lines = []
	for line in lines[1:]:
		line = line.strip()
		list_line = line.split(',')
		list_lines.append(list_line)
		#print(list_line)    
	### 从list_lines 获取每个省的地级市\县的列表,取决于index  index=-3 则市   index=-2 则县
	cities = set([])
	for list_line in list_lines:
		#print(list_line)
		city = list_line[index]   ### 市
		if city:
			cities.add(city)
	print(cities)
	#### 创建地址地级市和县的对应关系
	'''
	{'鄞州区': '宁波市', '滨江区': '杭州市', '西湖区': '杭州市', \
	'下城区': '杭州市', '北仑区': '宁波市', '海曙区': '宁波市',\
	 '上虞区': '绍兴市', '乐清市': '温州 市', '拱墅区': '杭州市', '江干区': '杭州市'...}
	'''
	dict_city_region = {}
	for list_line in list_lines:
		#print(list_line)
		city = list_line[-3]   ### 市
		region = list_line[-2]  ### 县
		#print('#### region = %s,city = %s'%(region,city))
		dict_city_region[region] = city
	print(dict_city_region)
	#for key in dict_city_region:
		#print(key,dict_city_region[key])

	

	####  统计每个地级市的信息，单独存放在一个csv文件中
	if index == -3:
		for city in cities:
			mkdir(city)
			path = '.\\'+city+'\\'+ city + '.csv'
			with codecs.open(path, 'w+', encoding='utf-8') as f:
				writer = csv.writer(f)
				writer.writerow(["公司简称","公司全名","行业","销售额(万）","利润(万）","利润率","市","区县","办公地址"])
				#遍历每一条，然后写到对应的csv文件中去 效率有点低
				for list_line in list_lines:
					#print(list_line)
					current_city = list_line[index]
					if current_city == city:
						writer.writerow(list_line)
		return cities	
	####  统计每个县的信息，单独存放在一个csv文件中
	elif index == -2: 
		for region in cities:    ### 这里的region就是县了,通过映射看属于哪个市，以便创建文件夹
			city = dict_city_region[region]
			Dir = '.\\'+city+'\\'+region   ### .\绍兴市\诸暨市
			mkdir(Dir)
			path = Dir + '\\'+region+'.csv' ### .\绍兴市\诸暨市\诸暨市.csv
			
			with codecs.open(path, 'w+', encoding='utf-8') as f:
				writer = csv.writer(f)
				writer.writerow(["公司简称","公司全名","行业","所在省","注册地","办公地","官网","上市日期"])
				#遍历每一条，然后写到对应的csv文件中去 效率有点低
				for list_line in list_lines:
					print(list_line)
					current_region = list_line[index]
					if current_region == region:
						writer.writerow(list_line) 
	elif index == 0:  ### 统计每个省的信息，单独存放在一个csv文件中
		for city in cities:  ### 省
				mkdir(city)
				path = '.\\'+city+'\\'+ city + '.csv'
				with codecs.open(path, 'w+', encoding='utf-8') as f:
					writer = csv.writer(f)
					writer.writerow(["省","市","区县","公司简称","公司全名","行业","2017前3季度销售额(万）","利润(万）","利润率","股票代码","注册地址","办公地址","官网","上市日期"])
					#遍历每一条，然后写到对应的csv文件中去 效率有点低
					for list_line in list_lines:
						#print(list_line)
						current_city = list_line[index]
						if current_city == city:
							writer.writerow(list_line)
	return cities	

	
			
			
			
	'''
		re_result   =  re.match(r'(.+?市|.+?县).*?',addr)
		if   re_result: 
			city = re_result.group (1)
		elif len(addr) > 3:  ### 如果大于3说明就是不对的
			addr =  list_line[-10] + addr 
			format_addr = get_format_addr_by_map(addr,ak)
			result = re.match(r'(.+?自治区|.+?省)(.+?自治州|.+?市|.+?盟)(.+?区|.+?市|.+?县|.+?旗).*?',format_addr)
			if result:
				city = result.group(3) 
					
			else:
				city = format_addr
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
	'''

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
	prov_csvfile = "all_province_commanpy_info_all_country_formated_addr.csv"
	provinces = format_addr(prov_csvfile,0)    ###  ### 统计每个省的信息，单独存放在一个csv文件中
	#for province in provinces:
	#	format_addr('.\\'+city+'\\'+ city + '.csv',-2)
		#csvfile = "zhejiang.csv" 
		#cities = format_addr(csvfile,-3)  ####  这里的csvfile是 zhejiang.csv ,统计每个地级市的信息，单独存放在一个csv文件中
		#for city in cities:
			#format_addr('.\\'+city+'\\'+ city + '.csv',-2)  #### 统计每个县的信息，单独存放在一个csv文件中