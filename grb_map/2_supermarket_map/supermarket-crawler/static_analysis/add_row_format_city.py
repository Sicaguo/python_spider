# -*- coding: utf-8 -*-

'''
	格式化csv文件中的地址 按XX省XX市XX县
'''
import re
import codecs
import csv

import requests
import time

import datetime
def add_city_to_csv(market_name,csvfile):
	with codecs.open(csvfile,"r+",encoding='utf-8')  as f:
		lines = f.readlines()
		for line in lines[1:]:
			info_list = []
			line = line.strip()
			list_line = line.split(',')
			print(list_line[-1]) 
			info_list.append(market_name)
			info_list.append(list_line[-1])
			format_addr =  list_line[-1]  ###　  安徽省合肥市肥东县  重庆市渝北区

			
			try:
				result =  re.match(r'(.+?自治区|.+?省|.+?市)(.+?市|.+?区|.+?自治州|.+?盟)(.+?市|.+?区|.+?县| ).*?',format_addr)
				format_addr3 = result.group(3)  ###　肥东县
			#处理4个直辖市以及省直管市 湖北省天门市创业大道辅路
			except: 
				result =  re.match(r'(.+?自治区|.+?省|.+?市)(.+[市|区|县]).*',format_addr)
				format_addr3 = result.group(2)	### 渝北区

			format_addr1 = result.group(1) ###   安徽省   重庆市 
			format_addr2 = result.group(2) ###   合肥市   渝北区
			if (format_addr3 in ['鼓楼区','江北区','白云区','新华区','桥西区','海州区','通州区',\
			'桥东区','长安区','西安区','铁西区','青山区','向阳区','和平区','普陀区','河东区','宝山区',\
			'铁东区','城关区','朝阳区','市中区','西湖区','永定区','城中区','南山区','新城区']):  ## (徐州 南京 福州 都有鼓楼区)  (重庆宁波都有江北区) 还有其他很多
				if(format_addr1  in ['北京市','上海市','天津市','重庆市']):
					format_addr3 = format_addr1+format_addr3
				else:
					format_addr3 = format_addr2+format_addr3

			info_list.append(format_addr1)
			info_list.append(format_addr2)
			info_list.append(format_addr3)

			print(info_list)
			writer.writerow(info_list)
if __name__ == '__main__':
	market_file = codecs.open('china_offical_total_region_city.csv',"w+",encoding='utf-8')  
	writer = csv.writer(market_file)
	writer.writerow(["品牌","地址","省+市","县"])
	csvfiles = ["china_offical_carrefour_format.csv","china_offical_markets_walmat_format.csv","china_offical_markets_rt_format.csv",
	"china_offical_metro_format.csv","china_offical_yh_format.csv"]
	market_names =["家乐福","沃尔玛","大润发","麦德龙","永辉"]
	i  = 0
	for csvfile in csvfiles:

		#csvfile = "china_offical_carrefour_format.csv"
		#log_file = codecs.open('get_city_from_formatmat_addr.txt','w+',encoding='utf-8') 
		add_city_to_csv(market_names[i],csvfile)
		i = i +1