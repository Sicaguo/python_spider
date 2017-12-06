# -*- coding: utf-8 -*-
# @Author: Teiei
# @Date:   2017-12-06 22:35:07
# @Last Modified by:   Teiei
# @Last Modified time: 2017-12-06 23:57:36
import codecs ,csv
if __name__ == '__main__':
	
	
	
	
	market_file =  codecs.open('china_offical_markets_walmat.csv', 'w+', encoding='utf-8') 
	writer = csv.writer(market_file)
		#writer.writerow(["城市","家乐福数","沃尔玛数","大润发数","麦德龙数"，"永辉数"，"华润万家数"])
	writer.writerow(["城市","超市总数"])

	dict_citys={'a':1,'b':2}

	dict_citys = {'a': 1, 'b': 2}
	for  key in dict_citys:
		info_list = []
		info_list.append(key)
		info_list.append(dict_citys[key])	
		print(info_list)


