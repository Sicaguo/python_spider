# -*- coding: utf-8 -*-
# @Author: Teiei
# @Date:   2017-12-23 11:04:40
# @Last Modified by:   Teiei
# @Last Modified time: 2017-12-23 22:04:24
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
def barh_plot2(labels,data,city): 
	    plt.rcParams['font.sans-serif'] = ['SimHei']
	    plt.rcParams['axes.unicode_minus'] = False
	    #labels= ['a','b','c','d']
	    #data=[1,2,3,4]
	    idx = np.arange(len(data))
	    fig = plt.figure(figsize=(15,15))
	    plt.ylim(ymax=35, ymin=0)
	    plt.xlim(xmax=15, xmin=-1)
	    #fig = plt.figure()
	    rect = plt.bar(idx,data  , color='green',alpha=0.5,width = 0.4)###plt.bar 横向
	    plt.xticks(idx,labels)
	    #plt.grid(axis='x')
	    plt.ylabel(city+'上市公司数量')
	    plt.xlabel('城市')

	    plt.title(city+'各辖区')
	    autolabel(rect)  
	    plt.savefig('.\\'+city+'\\'+city+'.jpg',dpi=150)
	    plt.show()
	    #
	    #fig = plt.figure()
	    
	   # plt.savefig(city+'.png')
def draw_graph(city):
	csvfile = '.\\'+city+'\\'+city+'.csv'
	print(csvfile)
	list_lines =  get_list_lines_from_csv(csvfile)
	#print(list_lines)
	dict_city_commany_num = get_labes_data(list_lines,-2)
	labels = []
	data=[]
	####  将dict 按 value排序  返回是一个list 
	list_city_commany_num = sorted(dict_city_commany_num.items(),key=lambda item :item[1],reverse = True)
	#list_city_commany_num = sorted(dict_city_commany_num.items(),key=lambda item :item[1])
	print(list_city_commany_num)
	for item in list_city_commany_num:
		print(item)
		labels.append(item[0])
		data.append(item[1])
	barh_plot2(labels,data,city)
if __name__ == '__main__':
	'''
	list_lines = get_list_lines_from_csv('zhejiang.csv') 
	cities = get_city_set(list_lines,-3)
	for city in cities:
		#print(city)
		draw_graph(city)
	'''
	
	#draw_graph('舟山市')
	draw_graph('杭州市')
