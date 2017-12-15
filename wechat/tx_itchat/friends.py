import itchat
import json
import csv
import codecs
import csv
def plot_yun(text):
    wordlist = jieba.cut(text, cut_all=True)
    wl_space_split = " ".join(wordlist)
    coloring = np.array(Image.open("wechat.jpg"))
    wordcloud = WordCloud(background_color="white",max_words=2000,mask=coloring, max_font_size=60, random_state=42, scale=2, font_path="simhei.ttf").generate(wl_space_split)
    image_color = ImageColorGenerator(coloring)
    plt.imshow(wordcloud.recolor(color_func=image_color))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
# 好友地区分布
def friends_area(friends):
    provinces = []
    cities = []
    provinces.append([friend['Province'] for friend in friends[1:]])
    cities.append([friend['City'] for friend in friends[1:]])
    province = dict(Counter(provinces))
    city = dict(Counter(cities))
    return province, city
if __name__ == '__main__':
    # 传入True hotReload使得程序关闭后一定时间内也可以登录，该方法会生一个静态文件itchat.pkl，用于存储登陆的状态
    itchat.auto_login(hotReload=True)
    # 运用get_friends方法获得完整好友列表
    flist = itchat.get_friends(update=True)
    print(flist)
    print('###### type flist ',type(flist))
    #将数据保存到wechat.json文件中
    with open("wechat.json", 'w+', encoding='utf-8') as f:
        f.write(json.dumps(flist))
    print(flist)
    print('###### type flist ',type(flist))
    with codecs.open('friends_info.csv'''[:-4]+'_format.csv', 'w+', encoding='utf-8') as market_file:
        writer = csv.writer(market_file)
        writer.writerow(["网名","备注名","省份","城市"])
        for f_dict in flist:
            info_list = []
            info_list.append(f_dict['NickName'])
            info_list.append(f_dict['RemarkName'])
            info_list.append(f_dict['Province'])
            info_list.append(f_dict['City'])
            print(f_dict['NickName'],f_dict['RemarkName'], f_dict['Sex'],f_dict['Province'],f_dict['City'])
            writer.writerow(info_list)
            print('\n')
    #friends_area()