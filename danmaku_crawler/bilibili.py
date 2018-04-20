# -*- coding：utf-8 -*-
# __author__ = 'engine'
# __time__ = '2018/4/19 21:39'
import re
import requests
import os
from wordcloud import WordCloud,ImageColorGenerator
import jieba
from scipy.misc import imread
import matplotlib.pyplot as plt
import random

#弹幕爬取
d = os.path.dirname(__file__)

start_url = input("输入B站视频地址：")
file_path = r'text\1.txt'

def get_flash_url(url):
    html_1 = requests.get(url)
    html_1.encoding = 'utf-8'
    fl_num = re.findall('"cid":(.*?),"page":\d,"from":"vupload"',html_1.text)[0]
    flash_url =  'https://comment.bilibili.com/'+str(fl_num)+'.xml'
    return flash_url

def get_flash(url):
    html = requests.get(url)
    html.encoding = 'utf-8'
    seg_list = re.findall('">(.*?)</d>',html.text)
    num = 0
    with open(file_path, 'w',encoding='utf-8') as f:
        for i in seg_list:
            print(i)
            f.write(i + '\n')
    f.close()
b = get_flash_url(start_url)
get_flash(b)

#文本分析和词云制作
stopwords = {}
isCN = 1
#在img的background_img中有三个已做好的jpg图像（作为背景）
n = random.randint(1,3)
background_img_path = r'img/background_img/'+str(n)+'.jpg'
text_path = 'text/1.txt'
font_path = 'fonts/YaHei.Consolas.1.11b.ttf'
stopwords_path = 'stopwords.txt'
img_name1 = 'DefaultColor.png'
img_name2 = 'All_by_image.png'

#可先自行添加相关词语
my_words_list = []

back_img = imread(os.path.join(d,background_img_path))

#词云属性
wordcloud = WordCloud(
    font_path=font_path,
    background_color="white",
    max_words=300,
    mask=back_img,
    max_font_size=400,
    random_state=42,
    margin=4,
    )

def add_word(list):
    for item in list:
        jieba.add_word(item)

add_word(my_words_list)

text = open(os.path.join(d,text_path),encoding='utf-8').read()

#jieba分词与数据清洗
def jiebaClearText(text):
    mywordlist = []
    seg_list = jieba.cut(text, cut_all=False)
    liststr = "/".join(seg_list)
    f_stop = open(stopwords_path)
    try:
        f_stop_text = f_stop.read()
    finally:
        f_stop.close()
    f_stop_seg_list = f_stop_text.split('\n')
    for myword in liststr.split('/'):
        if not(myword.strip() in f_stop_seg_list) and len(myword.strip())>1:
            mywordlist.append(myword)
    return ' '.join(mywordlist)

if isCN:
    text = jiebaClearText(text)

wordcloud.generate(text)
image_colors = ImageColorGenerator(back_img)
#生成词云
plt.imshow(wordcloud.recolor(color_func=image_colors))
plt.axis("off")
plt.show()
wordcloud.to_file(os.path.join(d,img_name2))