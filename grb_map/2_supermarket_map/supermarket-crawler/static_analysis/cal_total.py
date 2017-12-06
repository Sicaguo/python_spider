from openpyxl import load_workbook
import codecs,csv

def cal_total(files):
	for file in files:
		print('-----------file is: -----------------------------------------',file)
		wb = load_workbook(file)

		sheet = wb.get_sheet_by_name('Sheet0')  



		# 获取某个单元格的值，观察excel发现也是先字母再数字的顺序，即先列再行
		#b4 = sheet['B4']
		# 分别返回
		#print(f'({b4.column}, {b4.row}) is {b4.value}')  # 返回的数字就是int型

		# 除了用下标的方式获得，还可以用cell函数, 换成数字，这个表示B4
		#b4_too = sheet.cell(row=4, column=2)
		#print(b4_too.value)
		#b4_too = sheet.cell(4, 2)  ### 这样不行
		#print(b4_too.value)
		#
		# 获取最大行的最大列
		#print(sheet.max_row)
		#print(sheet.max_column)



		global dict_citys
		# 因为按行，所以返回A1, B1, C1这样的顺序
		i = 0
		for row in sheet.rows:  ### 第一行不要
			if i == 0:
				i = i+1
				continue
			print(row[0].value) 
			key = row[0].value   ### 城市名
			value = row[1].value ### 超市数量

			if key  in dict_citys:  ### 如果这个key存在了
				dict_citys[key] = dict_citys[key] + value
			else:
				dict_citys[key] =  value


			#for cell in row:
			#	print(cell.value)
		print('-----------over file is: -----------------------------------------',file)
		

		# A1, A2, A3这样的顺序
		#for column in sheet.columns:
		  #  for cell in column:
		   #     print(cell.value)
if __name__ == '__main__':
	market_file =  codecs.open('china_offical_markets_total.csv', 'w+', encoding='utf-8') 
	writer = csv.writer(market_file)
		#writer.writerow(["城市","家乐福数","沃尔玛数","大润发数","麦德龙数"，"永辉数"，"华润万家数"])
	writer.writerow(["城市","超市总数"])

	files = ['china_offical_carrefour_format.xlsx','china_offical_markets_walmat_format.xlsx','china_offical_markets_rt_format.xlsx'\
		,'china_offical_metro_format.xlsx','china_offical_yh_format.xlsx' ,'china_offical_huarun_format.xlsx']
	dict_citys = {}
	cal_total(files)
		#citys = citys[1:]
	print(dict_citys)
	for  key in dict_citys:
		info_list = []
		info_list.append(key)
		info_list.append(dict_citys[key])	
		print(info_list)
		writer.writerow(info_list)
	market_file.close()
