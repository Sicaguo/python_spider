import numpy as np    
import matplotlib.mlab as mlab    
import matplotlib.pyplot as plt  
def barh_plot2(): 

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    labels= ['a','b','c','d']
    data=[1,2,3,4]
    idx = np.arange(len(data))
    fig = plt.figure(figsize=(12,12))
    plt.barh(idx, data, color='b',alpha=0.6)
    plt.yticks(idx+0.4,labels)
    plt.grid(axis='x')
    plt.xlabel('XX事件次数')
    plt.ylabel('XX事件名称')
    plt.title('2015.1-2016.11月XX事件排行榜')
    plt.show()
barh_plot2()