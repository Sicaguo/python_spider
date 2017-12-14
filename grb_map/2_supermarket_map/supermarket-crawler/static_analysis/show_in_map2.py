'''
TODO :
1.由于pyecharts库的原因，以下城市无法标记在地图上
达州 coordinates is not found
红河哈尼族彝族自治 coordinates is not found
黄冈 coordinates is not found
楚雄彝族自治 coordinates is not found
大理白族自治 coordinates is not found
来宾 coordinates is not found
襄阳 coordinates is not found
抚州 coordinates is not found
晋中 coordinates is not found
吕梁 coordinates is not found
凉山彝族自治 coordinates is not found
眉山 coordinates is not found
丽江 coordinates is not found
临沧 coordinates is not found
普洱 coordinates is not found
文山壮族苗族自治 coordinates is not found
西双版纳傣族自治 coordinates is not found
宣城 coordinates is not found
池州 coordinates is not found
黔西南布依族苗族自治 coordinates is not found
延边朝鲜族自治 coordinates is not found
黔南布依族苗族自治 coordinates is not found
广安 coordinates is not found
商洛 coordinates is not found
白色 coordinates is not found
锡林郭勒 coordinates is not found
中卫 coordinates is not found

2. 正则表达式对 云南省西双版纳傣族自治州 这种无法提取出 西双版纳


注意
1.
data必须是tuple类型，list都不行  ,value必须为int类型
data = [
    ("海门", 9),("鄂尔多斯", 12),("招远", 12),("舟山", 12),("齐齐哈尔", 14),("盐城", 15),
    ("赤峰", 16),("青岛", 18),("乳山", 18),("金昌", 19),("泉州", 21),("莱西", 21),
    ("日照", 21),("胶南", 22),("南通", 23),("拉萨", 24),("云浮", 24),("梅州", 25)]
2.杭州必须为'杭州' 不能够为'浙江省杭州市'


'''
from openpyxl import load_workbook
from pyecharts import Geo
import codecs
import re
import time


def get_data_from_csvfile():
	csvfile = 'china_offical_total_region_city.xlsx'


	wb = load_workbook(csvfile)
	sheet = wb.get_sheet_by_name('Sheet0')  

	data = []
	
	i = 0
	for row in sheet.rows:  ### 第一行不要
		list_info =[]
		if i == 0:
			i = i+1
			continue
		#print(row[0].value) 
		#time.sleep(1)

		key = row[0].value   ### 城市名
		value = row[1].value ### 超市数量
		value = int(value)
		list_info.append(key)
		list_info.append(value)
		list_info = tuple(list_info)
		print(list_info)
		data.append(list_info)
	return data
f = open('citys_log.txt','w+')
data = get_data_from_csvfile()
#print(data)
#data = [['上海', '85'], ['成都', '66'], ['北京', '80'], ['沈阳', '37'], ['昆明', '29']]
#data = tuple(data)
#print(data)
geo = Geo("五大超市全国总和分布图", "家乐福+沃尔玛+大润发+麦德龙+永辉", title_color="#fff", title_pos="center",
width=1200, height=600, background_color='#404a59')
attr, value = geo.cast(data)

###  visual_text_color="#fff", 这个设置之后，左边那个图例才有有数字  #000代表'黑'   "#fff"代表'白'  label_text_color决定value值得颜色
geo.add("", attr, value, visual_range=[1,10], visual_text_color="#fff",is_label_show = True,label_text_size = 8,label_text_color ='#A9A9A9',label_pos = 'right'
 ,symbol_size=13, is_visualmap=True)
geo.show_config()
geo.render()