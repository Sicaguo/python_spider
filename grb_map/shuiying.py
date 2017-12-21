#-*- coding:utf-8 -*-
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#设置所使用的字体
font = ImageFont.truetype("c:/Windows/fonts/simsun.ttc", 20)

#打开图片
imageFile = "shanghai.png"
im1 = Image.open(imageFile)

#画图
draw = ImageDraw.Draw(im1)
draw.text((160, 0), "数据来源\n公众号:数据地图迷\n版权所有", (255, 0, 0), font=font)    #设置文字位置/内容/颜色/字体
#draw.text((400, 90), "数据地图迷", (255, 0, 0), font=font) 
draw = ImageDraw.Draw(im1)                          #Just draw it!

#另存图片
im1.save(imageFile+"1.png")