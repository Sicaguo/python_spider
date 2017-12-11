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

from pyecharts import Geo
import codecs
import re

### 对于 ' 贵州省黔南布依族苗族自治州'这类的处理还有问题
def get_city(format_city):
	spical_city = ['上海市','北京市','天津市','重庆市']
	print('#### [format_city] = ',format_city)
	if format_city in spical_city:
		#print('if')
		return format_city
	else:
		#print('else')
		#print(format_city)    ### 注意这里的正则,广东省广州市 这类广州市就又'州'又有'市',所以这里为.+ 不能加?
		city = re.match(r'.+?[省|区](.+[市|州|盟])', format_city).group(1)
		#print('city = ',city)
		
		f.write(city+'\n')
		return city

def get_data_from_csvfile():
	csvfile = 'china_offical_markets_total.csv'

	with codecs.open(csvfile, 'r+', encoding='utf-8') as f:
		lines = f.readlines()
		data=[]

		for line in lines[1:]:
			list_info =[]
			line = line.strip()
			list_line = line.split(',')[0:2]
			list_line[1]=int(list_line[1])  ### 必须要把字符转为Int
			#print('#### list_line = ',list_line)
			list_line[0] = get_city(list_line[0])  ### 从浙江省杭州市提取'杭州市'
			list_line = tuple(list_line)  ### 转为tuple
			#print('#### list_line2 = ',list_line)
			#print('--------list_line[0]= \n',list_line[0])
			

			#print()
			#list_line = lin
			#print(list_line[0],list_line[1])    
			#list_info.append(list_line[0])
			#list_info.append(list_line[1])
			print(list_line)
			data.append(list_line)
		print(data)
		return data
f = open('citys_log.txt','w+')
data = get_data_from_csvfile()
#print(data)
#data = [['上海', '85'], ['成都', '66'], ['北京', '80'], ['沈阳', '37'], ['昆明', '29']]
#data = tuple(data)
#print(data)
geo = Geo("六大超市全国总和分布图", "家乐福+沃尔玛+大润发+麦德龙+永辉+华润万家", title_color="#fff", title_pos="center",
width=1200, height=600, background_color='#404a59')
attr, value = geo.cast(data)

###  visual_text_color="#fff", 这个设置之后，左边那个图例才有有数字  #000代表'黑'   "#fff"代表'白'  label_text_color决定value值得颜色
geo.add("", attr, value, visual_range=[1,90], visual_text_color="#fff",is_label_show = True,label_text_size = 8,label_text_color ='#A9A9A9',label_pos = 'right'
 ,symbol_size=13, is_visualmap=True)
geo.show_config()
geo.render()