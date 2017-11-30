'''
解析得到的地址的城市名称
'''
'''
	从地址中提取地级市
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
        #print('#### url2 = ',url2,file=log_file)
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
        pass


def  get_format_addr_by_map(addr,ak):
	q = addr   		### 要搜索的关键字
	region = '中国'
	ak = 'QPBpKbOkCqkkToYT5VaFixoz3hkykVBi' 
	try:
		print('###  before url = ')
		url = 'http://api.map.baidu.com/place/v2/search?q={0}&region={1}&&output=json&ak={2}'.format(q, region, ak)
		print('### url = ',url)
		res_json = requests.get(url).json()
		record0 = res_json['results'][0]  ### 我们给定的地址，查询出来的应该只有一条，但是万一有多条，我们也只取一条，这个不保险 todo 
		format_addr = get_format_addr_from_lng_lat(record0['location']['lat'],record0['location']['lng'],ak)
		print('#### format addr = ',format_addr)
		return format_addr
	except:
		print('#### except get_format_addr_by_map')


def format_addr():
	with open('china_offical_carrefour.csv','r+') as f:
		lines = f.readlines()
	addrs=[]
	for line in lines[1:]:
		addr = line.split(',')[2]
		addr = addr[:-1]  ### remove '\n'
		addrs.append(addr)
	print('addrs = ',addrs)
	ak = 'QPBpKbOkCqkkToYT5VaFixoz3hkykVBi' 
	i = 0
	for addr in addrs:
		result = re.match(r'(.+?市).+?$', addr)  ### 这种是我们想要的，获取地级市级别 (不过有的县级市也会来这里干扰)
		if result:
			city = result.group(1) 
			addrs[i]=city
		elif re.match(r'(.+?区).*?', addr):
			city =  re.match(r'(.+?区).*?', addr).group(1)
			format_city = get_format_addr_by_map(city,ak)  ### 通过百度地图获取格式化的地址，然后在格式化的地址中提取出地级市
			addrs[i]=format_city
		elif re.match(r'(.+?号).*?', addr):
			city = re.match(r'(.+?号).*?', addr).group(1)
			format_city = get_format_addr_by_map(city,ak)
			addrs[i]=format_city
		else:
			addrs[i]=addr  ### 不变
		i=i+1


	print('#### addrs = ',addrs)   #### 格式化地址

	with open('china_offical_carrefour.csv','r+') as f:
		lines = f.readlines()
	with codecs.open('china_offical_carrefour_format_new.csv', 'w+', encoding='utf-8') as market_file:
		writer = csv.writer(market_file)
		writer.writerow(["品牌","商场名","地址","所属城市"])
		i = 0
		for line in lines[1:]:
			list_line  = line.split(',')  
			list_line[2] =list_line[2][:-1] ## remove '\n'
			list_line.append(addrs[i])
			writer.writerow(list_line)
			i = i+1
if __name__ == '__main__':
	format_addr()