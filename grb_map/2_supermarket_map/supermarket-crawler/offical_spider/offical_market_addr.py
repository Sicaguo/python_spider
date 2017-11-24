'''
	爬取上海各大超市的地址
'''

import urllib.request
import re
import codecs
import csv

def get_metro():
  #网址
  url = "http://www.metro.cn/stores"

  #请求
  request = urllib.request.Request(url)

  #爬取结果
  response = urllib.request.urlopen(request)

  data = response.read()

  #设置解码方式  这里不需要解码为unicode,不然write会出错
  #data = data.decode('utf-8')

  #打印结果
  #print(data)  ## renbin.guo added 
  #with open("./01_metro.html",'wb') as f:    ###　疑问，这里decode之后不就成了unicode吗?write不能写unicode啊?
  #    f.write(data)							###  解答 ： 'wb'的话可以写bytes 即uft-8等			
      										###  而如果是'w' 则必须写str 即 unicode,这时候就需要data.decode('utf-8')
  '''
  	这里也可以
  data = data.decode('utf-8')	
  with open("./01_douban.html",'wb') as f:
  f.write(data)	

  '''

      										
  data = data.decode('utf-8')			### 同样，这里因为print(str)参数为str 所以需要unicode
  #print(data)
  #打印爬取网页的各类信息

  #print('type(response) = %s\n\n'%type(response))
  #print('response.geturl() = %s\n\n'%response.geturl())
  #print('response.info() = %s\n\n'%response.info())
  #print('respense.getcode() = %s\n\n'%response.getcode())

  with codecs.open('offical_markets.csv', 'a', encoding='utf-8') as market_file:  ### 追加写
          writer = csv.writer(market_file)
          writer.writerow(["商场名","地址"])


          pattern = re.compile(r'<strong>上海(.+?)商场</strong></a><br>(.+?)<br>',re.S)

        ### ValueError: write to closed file  下面的writer.writerow(market_list)必须在with控制之下
        ### 不然
         # for mark_list  in re.findall(pattern , data):  
         #     print(mark_list)   ##('虹口', '\r\n\t\t\t\t\t\t\t\t\t\t\t上海市虹口区广粤路418号 ')
          for name,addr in re.findall(pattern , data):    ### 注意，这里的data必须为unicode 即str
          #for mark_list  in re.findall(pattern , data):  
             market_list=[]
             name ='上海'+name+'商场'
             #print('type name ,type addr =',type(name),type(addr)) 
             #addr 为'\r\n\t\t\t\t\t\t\t\t\t\t\t上海市虹口区广粤路418号 ' 所以需要正则提取
             addr = re.findall(r'\r\n\t*(.+?)$', addr)  ## 返回的是list 
             #print('type addr = ',type(addr))
             #print(name)
             #print(addr)
             market_list.append(name)
             market_list.append(str(addr[0])) 
             market_list.insert(0,'麦德龙')
             print(market_list)


             writer.writerow(market_list)
def get_carrefour():

  url = "http://www.carrefour.com.cn/Store/Store.aspx"
  request = urllib.request.Request(url)
  response = urllib.request.urlopen(request)
  data = response.read()                      
  data = data.decode('utf-8')     ### 同样，这里因为print(str)参数为str 所以需要unicode

  #print('type(response) = %s\n\n'%type(response))
  #print('response.geturl() = %s\n\n'%response.geturl())
  #print('response.info() = %s\n\n'%response.info())
  #print('respense.getcode() = %s\n\n'%response.getcode())

  pattern = re.compile(r'末页.+?page=(.+?)"></a>',re.S)
  tatol_page = int(re.findall(pattern , data)[0])
  #print('tatol_page = ',tatol_page)
  for i in range(tatol_page):
    url = "http://www.carrefour.com.cn/Store/Store.aspx?&page=%s"%(i+1)
    #print("#### i =  ,url = ",i,url)
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    data = response.read()                      
    data = data.decode('utf-8')     ### 同样，这里因为print(str)参数为str 所以需要unicode
    with codecs.open('offical_markets.csv', 'a', encoding='utf-8') as market_file:  ### 追加写
            writer = csv.writer(market_file)
            pattern = re.compile(r'clickto.+?<a href.+?\'>(.+?)店</a></td>.+?>上海市(.+?)</a>',re.S)
            for info_tuple  in re.findall(pattern , data):  
            	info_list = list(info_tuple)
            	info_list[0]='上海'+info_list[0]+'店'
            	info_list[1]='上海市'+info_list[1]
            	info_list.insert(0,'家乐福')
            	print(info_list)
            	writer.writerow(info_list)
def get_walmart():

  url = "http://www.wal-martchina.com/walmart/store/26_shanghai.htm"
  request = urllib.request.Request(url)
  response = urllib.request.urlopen(request)
  data = response.read()      
  #print('type(response) = %s\n\n'%type(response))
  #print('response.geturl() = %s\n\n'%response.geturl())
 # print('response.info() = %s\n\n'%response.info())
  #print('respense.getcode() = %s\n\n'%response.getcode())
          
  #data = data.decode('utf-8',ignore)     ### 同样，这里因为print(str)参数为str 所以需要unicode
  data= data.decode('gbk')
  
  with codecs.open('offical_markets.csv', 'a', encoding='utf-8') as market_file:  ### 追加写
            writer = csv.writer(market_file)
            pattern = re.compile(r'170pt\'>(.+?)</td>.+?<td class=.+?>(.+?)</td>',re.S)
            for info_tuple  in re.findall(pattern , data):  
            	info_list = list(info_tuple)
            	info_list.insert(0,'沃尔玛')    ## &nbsp;沃尔玛购物广场上海虹桥店  
            	if info_list[1][0] == '&':
            		info_list[1]=info_list[1][6:]
            	print(info_list)
            	writer.writerow(info_list)
              	

## darunfa  大润发
def get_rt_mark():
  url = "http://www.rt-mart.com.cn/store/detail/1001"
  request = urllib.request.Request(url)
  response = urllib.request.urlopen(request)
  data = response.read()      
  #print('type(response) = %s\n\n'%type(response))
  #print('response.geturl() = %s\n\n'%response.geturl())
  #print('response.info() = %s\n\n'%response.info())
  #print('respense.getcode() = %s\n\n'%response.getcode())
          
  #data = data.decode('utf-8',ignore)     ### 同样，这里因为print(str)参数为str 所以需要unicode
  #data= data.decode('gbk')
  data = data.decode('utf-8') 

  pattern = re.compile(r'st_link" href="(.+?)"',re.S)
  for store_link  in re.findall(pattern , data):  
    #print(store_link)
 
    url = store_link
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    data = response.read()  
    data = data.decode('utf-8') 
    with codecs.open('offical_markets.csv', 'a', encoding='utf-8') as market_file:  ### 追加写
              writer = csv.writer(market_file)
              pattern = re.compile(r'store_detail_head">.+?<p>(.+?)</p>.+?门店地址：(.+?)</p>',re.S)
              for info_tuple  in re.findall(pattern , data):             
                info_list = list(info_tuple)
                info_list.insert(0,'大润发')
                writer.writerow(info_list)
                print(info_list)

if(__name__ == '__main__'):
    get_metro()
    get_carrefour()
    get_walmart()
    get_rt_mark()