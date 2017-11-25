# -*- coding: utf-8 -*-
# @Author: Teiei
# @Date:   2017-11-23 19:43:01
# @Last Modified by:   Teiei
# @Last Modified time: 2017-11-25 07:40:00
# 
# TODO 1
# 1 .运行一段是就后会卡住print(city,file=log_file)打印完后
# 2.要加一个判断，如果保存的文件walmat_urls.txt不为空，则需要去除txt里面有了得城市。
# 3. 城市名market_name = td_tags[1].string 和 地址 market_addr =  td_tags[2].string到底是对应哪个td这里还要进一步对应，如下，可通过td数来判断。
'''
		比如 这个包含了城市名 --'上海' 那么td  tag就有7个
		 <tr height=68 style='height:51.0pt'>
		  <td class=style3 width=33 style='border-top:none;
		  width:25pt' rowspan="17">上海</td>
		  <td class=xl6832132 width=226 style='border-top:none;border-left:none;
		  width:170pt'>沃尔玛购物广场上海南浦大桥店</td>
		  <td class=xl7232132 width=176 style='border-top:none;border-left:none;
		  width:132pt'>浦东新区临沂北路252-262号由由-沃尔玛购物广场地上一层和地上二层</td>
		  <td class=xl7132132 width=64 style='border-top:none;border-left:none;
		  width:48pt'>021-50945881</td>
		  <td class=xl7132132 style='border-top:none;border-left:none;
		  width:223px'>公交：临沂北路龙阳路（119路；614路；640路；785路；973路；992路） <br>
		    地铁：轨道交通4号线</td>
		  <td class=style3 style='border-top:none;border-left:none; width: 68px;'>7:00-22:00</td>
		  <td class=style3 style='border-top:none;border-left:none; width: 64px;'><a href="#"
		  onclick="openwin('maps/shanghai/1014.htm')">查看地图</a></td>
		 </tr>

		下面没有包含，td tag就是6个
		  </tr>
		 <tr height=51 style='height:38.25pt'>
		  <td class=xl6832132 width=226 style='border-top:none;border-left:none;
		  width:170pt'>沃尔玛购物广场上海五角场分店</td>
		  <td class=xl7232132 width=176 style='border-top:none;border-left:none;
		  width:132pt'>上海市杨浦区淞沪路125号</td>
		  <td class=xl7132132 width=64 style='border-top:none;border-left:none;
		  width:48pt'>021-65115133</td>
		  <td class=xl7132132 style='border-top:none;border-left:none;
		  width:223px'>地铁10号线；公交55路 61路 99路 168路 307路 329路 406路 538路 713路 749路 817路
		  819路 850路 854路 937路 942路<span style='mso-spacerun:yes'>&nbsp;</span></td>
		  <td class=style3 style='border-top:none;border-left:none; width: 68px;'>7:30-22:00</td>
		  <td class=style3 style='border-top:none;border-left:none; width: 64px;'><a href="#"
		  onclick="openwin('maps/shanghai/1017.htm')">查看地图</a></td>
		 </tr>

'''
#	4.一次抓取可能抓取不全，比如虽然url正确，但是有时候网络不好，请求超时，\
#			结果中应该给出哪些省份没有抓取到。   ## rbguo fixed 2017-11-24  use excep3_urls
#	5.算法改进，现在计算机要请求34*34次,显然如果前面已经找到了的城市和序号，则不需要再找了。  ## rbguo fixed 2017-11-24  
#	6.安徽亳州市数据有点异常，所属城市没有抓到    rbguo fixed 2017-11-25  use td_tags[0].get_text()  
#	7.沃尔玛还有山姆店，但是程序没有实现抓取。
#	8.程序结构要修改，get_single_page通过全局变量city citys 依赖到了get_walmat_urls  rbguo fixed 2017-11-25 
#	
#	--------结论--------------
#	pingying.txt中要注意内蒙古，山西，陕西的写法
#	1.全国34个省区市中，只有25个分布有沃尔玛。
#	2.以下省份有合法的Url，但是没有分店 存放在excep3_urls中：
#	['http://www.wal-martchina.com/walmart/store/5_gansu.htm', 
#'http://www.wal-martchina.com/walmart/store/9_hainan.htm',
# 'http://www.wal-martchina.com/walmart/store/22_ningxia.htm',
# 'http://www.wal-martchina.com/walmart/store/23_qinghai.htm', 
#'http://www.wal-martchina.com/walmart/store/30_taiwan.htm']
#   3.以下省份连合法的url都没有，当然也没有分店，最后剩下的citys中
#    ['xianggang', 'aomen', 'xizang', 'xinjiang']

import re
import requests
import urllib,codecs,csv
from bs4 import BeautifulSoup
import datetime
def current_time():   ## 记录程序运行时间
     return datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S')
def get_walmat_urls():
   
	http_times = 0 ### 总共尝试的http请求次数
	citys = []
	ids = [x for x in range(1,35)]
	with open('pingying.txt','r+') as f:
		for line in f.readlines():
			citys.append(line[:-1])  ## 去掉'\n'
	print(citys,file=log_file)
	urls = []

	for id in ids:
		for city in citys:
			print(id,file=log_file)
			print(city,file=log_file)
			url = 'http://www.wal-martchina.com/walmart/store/'+str(id)+'_'+ city+'.htm'
			try:
				http_times  = http_times+1		
				get_single_page(url)   
				urls.append(url)	### 如果没有出错，则说明这个url是正确的
				citys.remove(city)	 ### rbguo fixed TODO5 2017-11-25 
				print('#### citys = ',citys,file=log_file)
				print('#### citys = ',citys)
				break;
			except:
				print('##### except1  ',file=log_file)
				print('##### except1  ')
				pass
	with open('walmat_urls.txt ','w+') as f:    ###将上次遍历得到的urls保存下来。
		f.write(str(urls))
	with open('excep3_urls.txt ','w+') as f:    ###将上次遍历得到的urls保存下来。
		f.write(str(excep3_urls))	
	print('### 共发送http url请求数：http requests  :',http_times)
	print('### 共发送http url请求数：http requests  :',http_times,file=log_file)
	return urls

def get_single_page(url):
	try:
		print('#### http request : url = ',url ,file=log_file)
		print('#### http request : url = ',url )
		request = urllib.request.Request(url)
		response = urllib.request.urlopen(request)
		     
		#print('type(response,file=log_file) = %s\n\n'%type(response))
		#print('response.geturl(,file=log_file) = %s\n\n'%response.geturl())
		#print('response.info(,file=log_file) = %s\n\n'%response.info())
		print('respense.getcode(,file=log_file) = %s\n\n'%response.getcode())
		## rbguo fix TODO5 2017-11-24  这里由于外部也正在for city in citys: 正在引用city 这样搞会不会问题？
		#ids.remove(id)	## rbguo fix TODO5 2017-11-24  id不用删除，因为有break
		
		try:      ###如果上面都执行到了，说明url正确,但是可能解析出错，这里记录url正确，但是最终每次成功的url
			data = response.read()
			#data = data.decode('utf-8',ignore)     ### 同样，这里因为print(str,file=log_file)参数为str 所以需要unicode
			data= data.decode('gbk')
			soup = BeautifulSoup(data)
			tab_tag = soup.find_all('table')[1]
			#print(tab_tag,file=log_file)
			soup1 = BeautifulSoup(str(tab_tag))
			tr_tags = soup1.find_all('tr')   ###第0项目不是符合要求的
			#for tr in tr_tag[1:]:
			#	print('##### tr =', tr,file=log_file)
			with codecs.open('china_offical_markets_walmat.csv', 'a', encoding='utf-8') as market_file:  ### 追加写
				writer = csv.writer(market_file)

			
				## rbguo fix TODO3  2017-11-24
				for tr_tag in tr_tags[1:]:
					#print('########## tr_tag',str(tr_tag))
					soup2 = BeautifulSoup(str(tr_tag))
					td_tags = soup2.find_all('td')
					#print('#### type(td_tags)',type(td_tags))
					#print('#### len ',len(td_tags))
					info_list = []
					if(len(td_tags) == 7): ## 如果有7个td_tag则第一个就是城市名
						#market_city = td_tags[0].string  
						market_city = td_tags[0].get_text()   ## fix TODO6 亳州<br>多了个<br>用string获取为none
						market_name = td_tags[1].string
						market_addr = td_tags[2].string
						info_list.append("沃尔玛")
						info_list.append(market_name)
						info_list.append(market_addr)
														### 同样，一个url的第一个记录必然tag==7这样就不怕market_city没有定义了
						info_list.append(market_city)	### 如果只有6个tag则一定是某个城市有多个分店，所以这里的market_city就是前面7个的那个
						print(info_list,file=log_file)
						print(info_list)
						writer.writerow(info_list)	
						#print(market_addr)
						#print(market_name)
						#print(market_city)
					elif(len(td_tags) == 6):  ### 沈阳的源代码非常异常 所以要限定为6 但是这样还是有错，沈阳的地址会写成大连的。
						#print('no == 7')
						#print('##### tr_tag =', tr_tag,file=log_file)
						market_name = td_tags[0].string
						market_addr =  td_tags[1].string
						info_list.append("沃尔玛")
						info_list.append(market_name)
						info_list.append(market_addr)
													### 同样，一个url的第一个记录必然tag==7这样就不怕market_city没有定义了
						info_list.append(market_city)	### 如果只有6个tag则一定是某个城市有多个分店，所以这里的market_city就是前面7个的那个
						#print(info_list,file=log_file)
						print(info_list)
						writer.writerow(info_list)
						#print('\t',market_addr)
						#print('\t',market_name)   ### 大连的 打印这个在我的xp电脑会出错，应该还是编码问题。在win10上没有问题
						#print('\t',market_city)
					elif(len(td_tags) == 1):  ### 专为沈阳写的
						market_city = td_tags[0].string
						print('### 沈阳 market_name ',market_city)



						
					
		except:
			
			print('##### except3 : url =  ',url,file=log_file)
			print('##### except3 : url =  ',url)
			excep3_urls.append(url)
			raise
			

				

				
	except:
		print('##### except2 : url =  ',url,file=log_file)
		print('##### except2 : url =  ',url)
		raise
		


def get_walmat():
	with codecs.open('china_offical_markets_walmat.csv', 'w+', encoding='utf-8') as market_file:
		writer = csv.writer(market_file)
		writer.writerow(["品牌","商场名","地址","所属城市"])
	urls = get_walmat_urls()

if __name__ == '__main__':
	start_time  = current_time()
	log_file = open("./china_walmart_log.txt", 'w+') 
	excep3_urls =[]  ### 记录url正确,并且请求也得到回应，但是解析出错的url (可能各个页面的结构会有不同导致)
					 ### 另外，台湾新疆宁夏青海西藏等省没有门店，但是url也是合法的，所以会被记住
	get_walmat()
	#url = 'http://www.wal-martchina.com/walmart/store/1_anhui.htm'
	#url = 'http://www.wal-martchina.com/walmart/store/20_liaoning.htm'
	#url ='http://www.wal-martchina.com/walmart/store/26_shanghai.htm'
	#et_single_page(url)
	end_time  = current_time()
	print('### 程序起始时间 start at :',start_time)
	print('### 程序结束时间 end at :',end_time)
	print('### 程序起始时间 start at :',start_time,file=log_file)
	print('### 程序结束时间 end at :',end_time,file=log_file)	
	log_file.close()

