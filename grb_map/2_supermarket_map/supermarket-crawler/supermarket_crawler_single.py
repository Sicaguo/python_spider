"""Supermarket Crawler

Crawl the locations of supermarkets in 26 cities.


renbin.guo added:
    bug 
        1.抓到的数据不全  比如拿上海麦德龙来分析就知道了(这个貌似不是bug )
                          解释：
                          程序中发出的url为
                          http://api.map.baidu.com/place/v2/search?q=%E9%BA%A6%E5%BE%B7%E9%BE%99&region=%E4%B8%8A%E6%B5%B7&page_size=20&page_num=0&output=json&ak=QPBpKbOkCqkkToYT5VaFixoz3hkykVBi
                          得到的确实只有9条。
                          而用浏览器搜索会得到11条,其中有条是冒牌的,另外有两条地点在一起.
    TODO : 
        1.将数据导入到excel中进行分析，存为csv用excel打开发现所有内容都在一个单元格
        2.麦德龙(常熟商场店) 31.684721 120.789353 经济技术开发区通港路99号  这个就不知道是哪里了，需要对地址进行结构化 /省/市/区/路/号
        3.爬取各家超市官网，统计数据，与地图的数据做对比。  
        4.要获取多个城市的多家超市，当线程太慢，需要开多任务
    history ；
        renbin.guo 2017-11-13 fix TODO1   use csv to write
        renbin.guo 2017-11-13 fix TODO2   格式化地址: 家乐福    31.241658   121.424219  白玉路101号 -->家乐福,31.241658,121.424219,上海市普陀区白玉路101号
        renbin.guo 2017-11-15 fix TODO3   add offical_market.py 


感谢：
http://blog.csdn.net/swjtuzbko/article/details/52709501  excel打开 uft-8的文件乱码--->使用notepad++ 转为ANSI编码
"""

import codecs
import requests
import time
import urllib.request

import csv
import datetime


'''
    定义log格式
'''
def current_time():
     return datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S')


  

'''
    通过经纬度得到格式化的地址
'''
def get_format_addr_from_lng_lat(lat,lng,ak):
    try:
        url2 = "http://api.map.baidu.com/geocoder/v2/?location=%s,%s&output=json&pois=1&ak=%s"%(lat ,lng,ak)
        #print('#### url2 = ',url2,file=log_file)
        format_json = requests.get(url2).json() 
       # req2 = urllib.request.urlopen(url2)#JSON格式的返回数据

        #respan_json2 = req2.read().decode("utf-8") #将其他编码的字符串解码成unicode
       # respan_python2 = json.loads(respan_json2)  ####  将json格式转为python数据结构
        #print('respan_python2 = ',respan_python2,file=log_file)
        #print('######　format_json_url2 = ',format_json,file=log_file)
        format_addr = format_json['result']['formatted_address']
        #print('### format_addr_url2 = ',format_addr,file=log_file)
       
        return format_addr
    except Exception as crawl_error:
        print(current_time(),"########### except 3 ######################",file=log_file)
        print("########### except 3 ######################")
        pass




def supermarket_crawler():
    """Supermarket Crawler
    """
    cities = ['上海', '南京', '无锡', '常州', '苏州', '南通', '盐城', '扬州', '镇江', '泰州', '杭州', '宁波', '嘉兴', '湖州', '绍兴', '金华', '舟山', '台州', '合肥', '芜湖', '马鞍山', '铜陵', '安庆', '滁州', '池州', '宣城']
    #supermarkets = ['苏果', '家乐福', '世界联华', '沃尔玛', '欧尚', '大润发', '金润发', '卜蜂莲花', '华润万家', '永辉', '金鹰', '八佰伴', '华联', '好又多', '麦德龙']
    supermarkets = ['家乐福','沃尔玛','大润发',  '麦德龙']
    #cities = ['上海', '南京', '无锡', '常州', '苏州', '南通', '盐城', '扬州', '镇江', '泰州', '杭州', '宁波', '嘉兴', '湖州', '绍兴', '金华', '舟山', '台州', '合肥', '芜湖', '马鞍山', '铜陵', '安庆', '滁州', '池州', '宣城']
    #supermarkets = ['苏果', '家乐福', '世界联华', '沃尔玛', '欧尚', '大润发', '金润发', '卜蜂莲花', '华润万家', '永辉', '金鹰', '八佰伴', '华联', '好又多', '麦德龙']
    #cities = ['上海', '南京', '无锡', '常州', '苏州']
    #cities = ['上海']
    #supermarkets = ['家乐福','沃尔玛','大润发',  '麦德龙']
    # test_cities = ['上海', '南京']
    # test_supermarkets = ['苏果', '家乐福']
    page_size = 20
    ak = 'QPBpKbOkCqkkToYT5VaFixoz3hkykVBi' 

    # 要实现写入时编码为UTF-8，应使用codecs模块的open
    with codecs.open('supermarkets.csv', 'w', encoding='utf-8') as market_file:
        writer = csv.writer(market_file)
        writer.writerow(["商场名","经度","纬度","地址"])

        for city in cities:
            for supermarket_name in supermarkets:
                time.sleep(0.2)  ### renbin.guo added 必须加这个，不然我这里会发现supermarket_json = requests.get(url_total).json() 会exception
                url_total = 'http://api.map.baidu.com/place/v2/search?q={0}&region={1}&page_size={2}&output=json&ak={3}'.format(supermarket_name, city, page_size,ak)
                try:
                    
                    #print('### url_total = ',url_total,file=log_file)
                    supermarket_json = requests.get(url_total).json()   ### 我感觉requests直接把json转为了python数据结构
                    supermarket_num =  supermarket_json['total']
                    #print('##### type  supermarket_json = ',type(supermarket_json,file=log_file))  ##＃这里直接得到dict 
                    #print('##### supermarket_json = ',supermarket_json,file=log_file)
                    #print('#### supermarket_total = ',supermarket_num,file=log_file)

                    page_total = supermarket_num // 20 + 1
                    #print('#### page_total = ',page_total,file=log_file)
                    
                    for page_num in range(page_total):
                        url = 'http://api.map.baidu.com/place/v2/search?q={0}&region={1}&page_size={2}&page_num={3}&output=json&ak={4}'.format(supermarket_name, city, page_size, page_num,ak)
                        #print('### url = ',url,file=log_file)
                        supermarket_json = requests.get(url).json()
                        #print('##### supermarket_json2 = ',supermarket_json,file=log_file)

                        rest_size = page_size  ##　还剩余多少记录，默认为20
                        if(page_num == page_total - 1):
                            rest_size = supermarket_num - page_num * page_size  ## 如果是最后一页了，那么剩余的页数就不是20,而是小于20，要计算
                        for supermarket_num in range(rest_size):
                            try:
                                supermarket = supermarket_json['results'][supermarket_num]
                                #print(city, supermarket_name,file=log_file)
                                #print(city, supermarket_name)
                                #time.sleep(1) 
                                time.sleep(0.3)
                                format_addr = get_format_addr_from_lng_lat(supermarket['location']['lat'],supermarket['location']['lng'],ak)
                                #print("_________format add = ",format_addr,file=log_file)
                                ## windows换行需要\r\n  linux \n
                                #write_buf = '{0} {1} {2} {3}'.format(supermarket['name'], supermarket['location']['lat'], supermarket['location']['lng'], supermarket['address'])
                                write_buf = '{0} {1} {2} {3}'.format(supermarket['name'], supermarket['location']['lat'], supermarket['location']['lng'],format_addr)
                                #print('write_buf = ',write_buf,file=log_file)
                                #print('type write_buf = ',type(write_buf,file=log_file))
                                list_write_buf = write_buf.split(' ')
                                print(current_time(),list_write_buf,file=log_file)  ### 加入时间
                                print(current_time(),list_write_buf)
                                #print('list_write_buf = ',list_write_buf)
                                #market_file.write('{0}   {1}   {2} {3}\r\n'.format(supermarket['name'], supermarket['location']['lat'], supermarket['location']['lng'], supermarket['address']))
                                
                                writer.writerow(list_write_buf)
                            except Exception as crawl_error:
                                print(current_time(),"########### except 1 ######################",file=log_file)
                                print(current_time(),"########### except 1 ######################")
                                pass

                except Exception as crawl_error:
                    print(current_time(),"########### except 2 ######################",file=log_file)
                    print(current_time(),"########### except 2 ######################")
                    pass

if(__name__ == '__main__'):
    log_file = open("./sing_log.txt", 'w+') 
    supermarket_crawler()

