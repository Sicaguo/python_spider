'''
解析得到的地址的城市名称
'''
import re
import codecs
import csv
with open('china_offical_carrefour.csv','r+') as f:
	lines = f.readlines()
addrs=[]
for line in lines[1:]:
	addr = line.split(',')[2]
	addr = addr[:-1]  ### remove '\n'
	addrs.append(addr)
print('addrs = ',addrs)

i = 0
for addr in addrs:
	result = re.match(r'(.+?市).+?$', addr)
	if result:
		city = result.group(1) 
		addrs[i]=city
	elif re.match(r'(.+?区).*?', addr):
		city2 =  re.match(r'(.+?区).*?', addr).group(1)
		addrs[i]=city2
	elif re.match(r'(.+?号).*?', addr):
		city3 = re.match(r'(.+?号).*?', addr).group(1)
		addrs[i]=city3
	else:
		addrs[i]=addr
	i=i+1


print('#### addrs = ',addrs)

with open('china_offical_carrefour.csv','r+') as f:
	lines = f.readlines()
with codecs.open('china_offical_carrefour_format.csv', 'w+', encoding='utf-8') as market_file:
	writer = csv.writer(market_file)
	writer.writerow(["品牌","商场名","地址","所属城市"])
	i = 0
	for line in lines[1:]:
		list_line  = line.split(',')  
		list_line[2] =list_line[2][:-1] ## remove '\n'
		list_line.append(addrs[i])
		writer.writerow(list_line)
		i = i+1
