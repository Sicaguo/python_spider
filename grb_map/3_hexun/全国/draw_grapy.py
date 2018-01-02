# -*- coding: utf-8 -*-
# @Author: Teiei
# @Date:   2017-12-23 11:04:40
# @Last Modified by:   Teiei
# @Last Modified time: 2017-12-28 22:54:45
# 
# TODO 内存会爆
#  brief
#  1.画一个省所有地级市的图，比如宁波市，画的就是宁波市市各区的上市公司
#  2.画每个地级市的上市公司行业分布的扇形图

'''
 rbguo 2017-12-29 解决内存被耗尽的问题
  看到一个提示  同时在绘制的图太多了 
(`matplotlib.pyplot.figure`) are retained until explicitly closed and may consume too much memory
  绘图完了之后必须调用plt.close('all') 不然图片不会关闭，会一直占用内存，直到内存耗尽


'''
import gc
import numpy as np    
import matplotlib.mlab as mlab    
import matplotlib.pyplot as plt  

import re
import codecs
import csv

import requests
import time
import urllib.request

import datetime
import os 
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import shutil


####从csv读取数据,存放在list_lines里面
def get_list_lines_from_csv(csvfile):
	with codecs.open(csvfile,'r+',encoding='utf-8') as f:  
		lines = f.readlines()
	list_lines = []
	for line in lines[1:]:
		line = line.strip()
		list_line = line.split(',')
		list_lines.append(list_line)
	return list_lines

### 从list_lines 获取每个省的地级市\县的列表,取决于index  index=1 则市   index=2 则县
def get_city_set(list_lines,index):
	cities = set([])
	for list_line in list_lines:
		#print(list_line)
		city = list_line[index]   ### 市
		if city:
			cities.add(city)
	return cities
###  从表格中获取Index列的不同的值，返回一个set
def get_unique_item_set(list_lines,index):
	unique_items_set = set([])
	for list_line in list_lines:
		#print(list_line)
		item = list_line[index]   ### 
		if item:
			unique_items_set.add(item)
	return unique_items_set

####  list_lines是一个csv的list形式   这个函数做的类似于数据透视表  index = 1 统计地级市，2统计县
def get_labes_data(list_lines,index):  ### 比如如果这个csv是杭州的话  
	dict_city_commany_num = {}   ###{'滨江区':22,'上河区'：12...}

	#### 先遍历这个表中有哪些城市(有哪些key)
	cities = get_city_set(list_lines,index)

	for key in cities:
		dict_city_commany_num[key] = 0  ####  赋值为0
	for list_line in list_lines:
		region = list_line[index]
		dict_city_commany_num[region] = dict_city_commany_num[region] +1
	print(dict_city_commany_num)
	return dict_city_commany_num
####  从list_lines表格中获取第index列的数据透视表
####  index = 2 则获取的是一个市所有的县的上市公司透视表{'滨江区':22,'上河区'：12...}
#	  index = 3  获取的是一个市所有行业的数据透视表 {‘互联网’：9,'制药':8}
def get_unique_item_amount_dict(list_lines,index):	
	dict_colurmn_index = {}
	unique_items = get_unique_item_set(list_lines,index)
	for item in unique_items:     
		dict_colurmn_index[item]=0 ####  初始化为0
	for list_line in list_lines:
		item = list_line[index]
		dict_colurmn_index[item] = dict_colurmn_index[item] +1
	#print(dict_colurmn_index)
	return dict_colurmn_index	

def autolabel(rects):  
    for rect in rects:  
        height = rect.get_height()   ### plt.text第一个参数 (横坐标 ,纵坐标，要写的文本....)
        plt.text(rect.get_x() + rect.get_width() / 2, height, height, ha='center', va='bottom') 
def autolabel_0(rects):  
    for rect in rects:  
        width = rect.get_width()   ### plt.text第一个参数 (横坐标 ,纵坐标，要写的文本....)
        #print('width = ',width)
        height = rect.get_height() 
        #print('height = ',height)
        plt.text(width+1.2, rect.get_y(), width, ha='center', va='bottom') 

#### 纵的条形图
def barh_plot1(labels,data,city,city_type):    ### 如果是作省的图,则刻度不一样，所以要区分 
	    plt.rcParams['font.sans-serif'] = ['SimHei']
	    plt.rcParams['axes.unicode_minus'] = False

	    idx = np.arange(len(data))
	    fig = plt.figure(figsize=(6,6))  ###调整图的大小
	    rect= plt.barh(idx, data, color='green',alpha=0.6)  ###alpha颜色深浅  ,height=1.1
	    plt.yticks(idx,labels)
	    #plt.grid(axis='x') ### 是否有格子线
	    if city_type == 1:
	    	plt.xlim(xmax=700, xmin=0)  ### 一个省内的上市公司假定不超过700 广东：600  浙江400
	    	plt.ylim(ymax=34, ymin=-1)  ### 一个中国省不超过34
	    elif city_type == 2:
	    	plt.xlim(xmax=310, xmin=0)  ### 一个省内的每个地级市的上市公司假定不超过310 深圳：300  杭州147
	    	plt.ylim(ymax=20, ymin=-1)  ### 一个省内的地级市假定不超过20
	    else:
	    	plt.xlim(xmax=125, xmin=0)   ### 一个地级市的上市公司假定不超过70 深圳南山123：  杭州滨江：35
	    	plt.ylim(ymax=15, ymin=-1)  ### 一个地级市内的区县数假定不超过15
	    plt.xlabel('上市公司数量')
	    plt.ylabel('城市')
	    plt.title(city+'各辖区上市公司数量')
	    autolabel_0(rect) 
	    plt.savefig('.\\'+city+'.png',dpi=150)  ### dpi是设置像素
	    fig.clear()
	    plt.close('all')
	    #plt.savefig('G:\study\\version_spider\python_spider\grb_map\\3_hexun\全国\江苏省\\'+city+'.png',dpi=150)
	    #plt.savefig(city+'.png',dpi=150)  ### dpi是设置像素
	    #plt.show()
#### 横的条形图
def barh_plot2(labels,data,city,city_type):   ### city_type =1  画全国  2 省   3 地级市
	    plt.rcParams['font.sans-serif'] = ['SimHei']
	    plt.rcParams['axes.unicode_minus'] = False
	    #labels= ['a','b','c','d']
	    #data=[1,2,3,4]
	    idx = np.arange(len(data))
	    fig = plt.figure(figsize=(5,5))   ###这个越小，保存出来的图片反而越大
	    if city_type == 1:
	    	plt.xlim(xmax=700, xmin=0)  ### 一个省内的上市公司假定不超过700 广东：600  浙江400
	    	plt.ylim(ymax=34, ymin=-1)  ### 一个中国省不超过34
	    elif city_type == 2:
	    	plt.xlim(xmax=310, xmin=0)  ### 一个省内的每个地级市的上市公司假定不超过310 深圳：300  杭州147
	    	plt.ylim(ymax=20, ymin=-1)  ### 一个省内的地级市假定不超过20
	    else:
	    	plt.xlim(xmax=125, xmin=0)   ### 一个地级市的上市公司假定不超过70 深圳南山123：  杭州滨江：35
	    	plt.ylim(ymax=15, ymin=-1)  ### 一个地级市内的区县数假定不超过15
	    #fig = plt.figure()
	    rect = plt.bar(idx,data  , color='green',alpha=0.5,width = 0.4)###plt.bar 横向
	    plt.yticks(idx,labels)
	    #plt.grid(axis='x')
	    plt.ylabel('上市公司数量')
	    plt.xlabel('城市')

	    plt.title(city+'各辖区各辖区上市公司数量')
	    autolabel(rect)  
	    #plt.savefig('.\\'+city+'.png',dpi=150)
	    #plt.savefig('G:\study\\version_spider\python_spider\grb_map\\3_hexun\全国\江苏省\\'+city+'.png',dpi=150)
	    plt.savefig(city+'.png',dpi=150)  ### dpi是设置像素
	    fig.clear()
	    plt.close('all')
	    #plt.show()
	    #
	    #fig = plt.figure()
	    
	   # plt.savefig(city+'.png')

###  画扇形图
def draw_pie(labels,data,city,city_type =2):
	plt.rcParams['font.sans-serif'] = ['SimHei']
	plt.rcParams['axes.unicode_minus'] = False

	fig = plt.figure(figsize=(10,10))
	plt.pie(data,labels=labels,autopct='%1.1f%%',labeldistance = 1.26,pctdistance = 1.05,radius=1.1) #画饼图（数据，数据对应的标签，百分数保留两位小数点
	if city_type == 1:
		plt.title(city+'境内上市公司各地级市分布')
	else:
		plt.title(city+'境内上市公司行业分布')
	#plt.savefig('.\\'+city+'_pie.png',dpi=150)
	
	#plt.savefig('G:\study\\version_spider\python_spider\grb_map\\3_hexun\全国\江苏省\\'+city+'_pie.png',dpi=150)
	plt.savefig('.\\'+city+'_pie.png',dpi=150)
	fig.clear()
	plt.close('all')
	#plt.show()

def get_jpg_type_file(path, list_name):  
    for file in os.listdir(path):  
        file_path = os.path.join(path, file)  
        if os.path.isdir(file_path):  
            get_jpg_type_file(file_path, list_name)  
        elif os.path.splitext(file_path)[1] in ['.png','.jpg'] :  
            list_name.append(file_path)  
def watermark(imageFile):
	#设置所使用的字体
	font = ImageFont.truetype("c:/Windows/fonts/simsun.ttc", 20)
	#打开图片
	im1 = Image.open(imageFile)

	#画图
	draw = ImageDraw.Draw(im1)
	draw.text((160, 0), "数据来源\n公众号:数据地图迷\n版权所有", (255, 0, 0), font=font)    #设置文字位置/内容/颜色/字体
	#draw.text((400, 90), "数据地图迷", (255, 0, 0), font=font) 
	draw = ImageDraw.Draw(im1)                          #Just draw it!

	#另存图片
	#im1.save(imageFile[:-4]+"_watermark.png")
	im1.save(imageFile)  ### 覆盖掉原来的
def draw_graph_bar_city(city):     #### 这里的city 是 地级市  画一个地级市各区县的条形图
	csvfile = city+'.csv'
	#print(csvfile)
	list_lines =  get_list_lines_from_csv(csvfile)   ### 将csv文件提取为list
	#print(list_lines)
	#dict_city_commany_num = get_labes_data(list_lines,2)
	dict_item = get_unique_item_amount_dict(list_lines,2)  ### 获取第二列的数据透视表
	labels = []
	data=[]
	dict_item = sorted(dict_item.items(),key=lambda item :item[1],reverse = True)
	#print(dict_item)
	for item in dict_item:
		#print(item)
		labels.append(item[0])
		data.append(item[1])

	####  将dict 按 value排序  返回是一个list 
	#list_city_commany_num = sorted(dict_city_commany_num.items(),key=lambda item :item[1],reverse = True)
	'''
	list_city_commany_num = sorted(dict_city_commany_num.items(),key=lambda item :item[1])
	print(list_city_commany_num)
	for item in list_city_commany_num:
		print(item)
		labels.append(item[0])
		data.append(item[1])
	'''
	barh_plot1(labels,data,city,3)
	#draw_pie(labels,data,city)
def draw_graph_pie_city(city):     #### 这里的city 是 地级市  画一个地级市的行业扇形图
	csvfile = city+'.csv'
	#print(csvfile)
	list_lines =  get_list_lines_from_csv(csvfile)   ### 将csv文件提取为list
	#print(list_lines)
	#dict_city_commany_num = get_labes_data(list_lines,2)
	dict_item = get_unique_item_amount_dict(list_lines,5)  ### 获取第二列的数据透视表
	labels = []
	data=[]
	dict_item = sorted(dict_item.items(),key=lambda item :item[1],reverse = True)
	#print(dict_item)
	for item in dict_item:
		#print(item)
		labels.append(item[0])
		data.append(item[1])

	####  将dict 按 value排序  返回是一个list 
	#list_city_commany_num = sorted(dict_city_commany_num.items(),key=lambda item :item[1],reverse = True)
	'''
	list_city_commany_num = sorted(dict_city_commany_num.items(),key=lambda item :item[1])
	print(list_city_commany_num)
	for item in list_city_commany_num:
		print(item)
		labels.append(item[0])
		data.append(item[1])
	'''
	draw_pie(labels,data,city)
def draw_graph_province_bar_and_pie(province):

	list_lines =  get_list_lines_from_csv(province+'.csv')   ### 将csv文件提取为list
	dict_item = get_unique_item_amount_dict(list_lines,1)  ### 获取第1列的数据透视表
	labels = []
	data=[]
	dict_item = sorted(dict_item.items(),key=lambda item :item[1],reverse = True)
	#print(dict_item)
	for item in dict_item:
		#print(item)
		labels.append(item[0])
		data.append(item[1])
	draw_pie(labels,data,province,1)
	barh_plot1(labels,data,province,2)


####  画一个省的图 包括
### 1.每个地级市辖内各区县的条形图
### 2.每个地级市的行业分布扇形图
### 3.一个省内所有地级市的条形图
### 4.一个省内所有地级市的扇形图
def draw_bar_pie_for_one_province(prov_csvfile):  ### prov_csvfile 为 广东省.csv
		print('##### prov_csvfile[:-4] = ',prov_csvfile[:-4])
		draw_graph_province_bar_and_pie(prov_csvfile[:-4])


		list_lines = get_list_lines_from_csv(prov_csvfile) 
		cities = get_city_set(list_lines,1)
		for city in cities:
			print('process... ',city)
			os.chdir(city) 
			pwd = os.getcwd()
			print('enter dir...',pwd)
			draw_graph_bar_city(city)
			#time.sleep(1)
			draw_graph_pie_city(city)
			os.chdir("..") 
			pwd = os.getcwd()
			print('exit dir ...',pwd)
		### 增加水印
		img_list = []
		get_jpg_type_file('.',img_list)
		#print('img_list = ',img_list)
		for image in img_list:
			#print(image)
			watermark(image)   ### 加水印
		
'''
1.画全国各省上市公司数量分布的条形图
2.画全国各省上市公司数量分布的扇形图
'''
def draw_all_country_bar_and_pie(all_country_csvfile):
	list_lines =  get_list_lines_from_csv(all_country_csvfile)   ### 将csv文件提取为list
	dict_item = get_unique_item_amount_dict(list_lines,0)  ### 获取第1列的数据透视表
	labels = []
	data=[]
	dict_item = sorted(dict_item.items(),key=lambda item :item[1],reverse = True)
	#print(dict_item)
	for item in dict_item:
		#print(item)
		labels.append(item[0])
		data.append(item[1])
	draw_pie(labels,data,'全国')
	barh_plot1(labels,data,'全国',1)
	watermark('全国.png') 
	watermark('全国_pie.png')
	#for image in img_list:
	#	watermark(image)   ### 加水印
	#	
### 将一个省中所有的图片复制到根目录下all_iamge
def copy_all_image_in_a_dir():
	if os.path.exists('all_iamge'):
		shutil.rmtree('all_iamge')
		print('remove')
	os.mkdir('all_iamge')
	img_list = []
	get_jpg_type_file('.',img_list)
	for  image in img_list:
		shutil.copy(image, 'all_iamge') 
	#return img_list
	

	'''
    for file in os.listdir(path):  
        file_path = os.path.join(path, file)  
        if os.path.isdir(file_path):  
            get_jpg_type_file(file_path, list_name)  
        elif os.path.splitext(file_path)[1] in ['.png','.jpg'] :  
            list_name.append(file_path)
    '''

if __name__ == '__main__':
	
	'''
	all_country_csvfile = "all_province_commanpy_info_all_country_formated_addr_final.csv"
	draw_all_country_bar_and_pie(all_country_csvfile)  ## 画全国的图

	### 画每个省的
	list_lines = get_list_lines_from_csv(all_country_csvfile)    ### 将csv文件转为一个list
	provinces = get_city_set(list_lines,0)
	#  print('listlines = ',list_lines)### 验证内存是否回收成功

	print(provinces)
	provinces = list(provinces)
	len_provinces = len(provinces)
	finished_len = 0
	#time.sleep(5)
	for province in provinces:
		os.chdir(".\\"+province)   #修改当前工作目录
		#pwd = os.getcwd()    #获取当前工作目录 进入到该省	
		print('已经完成.....[%d|%d]'%(finished_len,len_provinces))
		draw_bar_pie_for_one_province(province+'.csv')
		copy_all_image_in_a_dir()
		os.chdir("..")   ### 切换回全国目录
		finished_len = finished_len+1
	
	'''
	'''
	time.sleep(5)
	for province in provinces[10:20]:
		os.chdir(".\\"+province)   #修改当前工作目录
		pwd = os.getcwd()    #获取当前工作目录 进入到该省	
		draw_bar_pie_for_one_province(province+'.csv')
		os.chdir("..")   ### 切换回全国目录
		time.sleep(5)
	for province in provinces[20:32]:
		os.chdir(".\\"+province)   #修改当前工作目录
		pwd = os.getcwd()    #获取当前工作目录 进入到该省	
		draw_bar_pie_for_one_province(province+'.csv')
		os.chdir("..")   ### 切换回全国目录
	'''
	
	
	province = '江苏省'
	os.chdir(".\\"+province)   #修改当前工作目录
	#pwd = os.getcwd()    #获取当前工作目录 进入到该省	
	draw_bar_pie_for_one_province(province+'.csv')
	copy_all_image_in_a_dir()
	os.chdir("..")   ### 切换回全国目录
	
	
	
	