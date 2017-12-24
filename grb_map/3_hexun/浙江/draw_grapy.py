# -*- coding: utf-8 -*-
# @Author: Teiei
# @Date:   2017-12-23 11:04:40
# @Last Modified by:   Teiei
# @Last Modified time: 2017-12-24 09:38:49
# 
#  brief 画一个省所有地级市的图，比如宁波市，画的就是宁波市市各区的上市公司
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

### 从list_lines 获取每个省的地级市\县的列表,取决于index  index=-3 则市   index=-2 则县
def get_city_set(list_lines,index):
	cities = set([])
	for list_line in list_lines:
		#print(list_line)
		city = list_line[index]   ### 市
		if city:
			cities.add(city)
	return cities

####  list_lines是一个csv的list形式   这个函数做的类似于数据透视表  index = -3 统计地级市，-2统计县
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
        plt.text(width+0.6, rect.get_y(), width, ha='center', va='bottom') 

#### 纵的条形图
def barh_plot1(labels,data,city):   
	    plt.rcParams['font.sans-serif'] = ['SimHei']
	    plt.rcParams['axes.unicode_minus'] = False

	    idx = np.arange(len(data))
	    fig = plt.figure(figsize=(6,6))  ###调整图的大小
	    rect= plt.barh(idx, data, color='green',alpha=0.6)  ###alpha颜色深浅  ,height=1.1
	    plt.yticks(idx,labels)
	    #plt.grid(axis='x') ### 是否有格子线
	    plt.xlim(xmax=35, xmin=0)
	    plt.ylim(ymax=15, ymin=-1)
	    plt.xlabel('上市公司数量')
	    plt.ylabel('城市')
	    plt.title(city+'各辖区上市公司数量')
	    autolabel_0(rect) 
	    plt.savefig('.\\'+city+'\\'+city+'.jpg',dpi=150)  ### dpi是设置像素
	    plt.savefig(city+'.jpg',dpi=150)  ### dpi是设置像素
	    #plt.show()
def barh_plot2(labels,data,city): 
	    plt.rcParams['font.sans-serif'] = ['SimHei']
	    plt.rcParams['axes.unicode_minus'] = False
	    #labels= ['a','b','c','d']
	    #data=[1,2,3,4]
	    idx = np.arange(len(data))
	    fig = plt.figure(figsize=(5,5))   ###这个越小，保存出来的图片反而越大
	    plt.ylim(ymax=35, ymin=0)
	    plt.xlim(xmax=15, xmin=-1)
	    #fig = plt.figure()
	    rect = plt.bar(idx,data  , color='green',alpha=0.5,width = 0.4)###plt.bar 横向
	    plt.yticks(idx,labels)
	    #plt.grid(axis='x')
	    plt.ylabel('上市公司数量')
	    plt.xlabel('城市')

	    plt.title(city+'各辖区各辖区上市公司数量')
	    autolabel(rect)  
	    plt.savefig('.\\'+city+'\\'+city+'.jpg',dpi=150)
	    plt.savefig(city+'.jpg',dpi=150)  ### dpi是设置像素
	    #plt.show()
	    #
	    #fig = plt.figure()
	    
	   # plt.savefig(city+'.png')
def get_jpg_type_file(path): 
	list_name = []
	for file in os.listdir(path):
		file_path = os.path.join(path, file)
		if os.path.splitext(file_path)[1]=='.jpg':
			list_name.append(file_path)
	return list_name
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
	im1.save(imageFile[:-4]+"_watermark.jpg")
def draw_graph(city):
	csvfile = '.\\'+city+'\\'+city+'.csv'
	print(csvfile)
	list_lines =  get_list_lines_from_csv(csvfile)
	#print(list_lines)
	dict_city_commany_num = get_labes_data(list_lines,-2)
	labels = []
	data=[]
	####  将dict 按 value排序  返回是一个list 
	#list_city_commany_num = sorted(dict_city_commany_num.items(),key=lambda item :item[1],reverse = True)
	list_city_commany_num = sorted(dict_city_commany_num.items(),key=lambda item :item[1])
	print(list_city_commany_num)
	for item in list_city_commany_num:
		print(item)
		labels.append(item[0])
		data.append(item[1])
	barh_plot1(labels,data,city)
if __name__ == '__main__':
	
	list_lines = get_list_lines_from_csv('zhejiang.csv') 
	cities = get_city_set(list_lines,-3)
	for city in cities:
		#print(city)
		draw_graph(city)
	img_list = get_jpg_type_file('.')
	for image in img_list:
		print(image)
		watermark(image)
	
	
	#draw_graph('舟山市')
	#draw_graph('杭州市')
