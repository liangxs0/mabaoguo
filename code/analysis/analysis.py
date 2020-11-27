import pymongo
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from matplotlib.ticker import FuncFormatter

style.use('ggplot')     # 设置图片显示的主题样式

# 解决matplotlib显示中文问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
plt.rcdefaults()

fig, ax = plt.subplots()
fig.set_size_inches(18.5, 10.5)
width = 0.35


'''
mogodb的数据导入一长张表
'''
# client = pymongo.MongoClient("localhost", 27017)
# db = client["Mabaoguo"]
# table = db["Content"]
#
#
# data = pd.DataFrame(list(table.find()))
# data.to_csv("./data.csv")


def data_preview(data):
    print(data.head(5))

def switch_int(str_data:str):
    if '万' in str_data:
        d = str_data.replace('万', '')
        d = int(float(d) * 10000)
        return d
    else:
        return int(str_data)

def formatnum(x, pos):
    return '$%.1f$x$10^{4}$' % (x/100000)

def show_date_play(data):

    data =  data.head(20)
    y_pos = np.arange(20)
    error = np.random.rand(20)
    x = np.array(data['play_number'].values)
    formatter = FuncFormatter(formatnum)

    ax.barh(y_pos,x,xerr=error, align='center', color="green")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(data['video_date'])
    ax.invert_yaxis()
    ax.set_xlabel('play_number')
    ax.xaxis.set_major_formatter(formatter)

    ax.set_title('The relationship between play volume and date')
    for xx,y in enumerate(x):
        plt.text(y, xx, y, ha='center', fontsize=12, color="BLUE")
    ax.legend()

    plt.savefig('./first.png')

    plt.show()

def all_play_number(data):
    data = data.head(5)
    return data["play_number"].sum(), data["hide_number"].sum()

def top_10(data):
    data = data.sort_values(by='play_number', ascending=False)
    for da ,i in zip(data.iterrows(), range(0,10)):
        yield {
            '链接':da[1][0],
        '标题':da[1][1],
        '播放量':da[1][2],
        '弹幕量':da[1][3],
        '发布日期':da[1][4],
        'up主':da[1][5]
        }

def top1_10(data):
    data = data.sort_values(by='hide_number', ascending=False)
    for da ,i in zip(data.iterrows(), range(0,10)):
        yield {
            '链接':da[1][0],
        '标题':da[1][1],
        '播放量':da[1][2],
        '弹幕量':da[1][3],
        '发布日期':da[1][4],
        'up主':da[1][5]
        }

def top2_10(data):
    data = data.sort_values(by='video_date')
    for da ,i in zip(data.iterrows(), range(0,10)):
        yield {
            '链接':da[1][0],
        '标题':da[1][1],
        '播放量':da[1][2],
        '弹幕量':da[1][3],
        '发布日期':da[1][4],
        'up主':da[1][5]
        }

def main():
    p_dict = {
        'video_address':[],
        'video_title':[],
        'play_number':[],
        'hide_number':[],
        'video_date':[],
        'video_author':[],
    }
    data = pd.read_csv('data.csv', encoding='utf8')
    d_data = data.sort_values(by='video_date')

    for da in d_data.iterrows():
        p_dict['video_address'].append(da[1][2])
        p_dict['video_title'].append(da[1][3])
        p_dict['play_number'].append(switch_int(da[1][4]))
        p_dict['hide_number'].append(switch_int(da[1][5]))
        p_dict['video_date'].append(da[1][6])
        p_dict['video_author'].append(da[1][7])
    pd_data = pd.DataFrame(p_dict)
    data_preview(pd_data)
    # show_date_play(pd_data)
    print(all_play_number(pd_data))
    # top_10(pd_data)
    top10 = top_10(pd_data)
    for top in top10:
        print(top)
    print("-"*100)
    top10 = top1_10(pd_data)
    for top in top10:
        print(top)
    print("-" * 100)
    top10 = top2_10(pd_data)
    for top in top10:
        print(top)

    # plt.hist(pd_data['video_date'], bins=3)
    # plt.ylabel('高峰数量')
    # plt.xlabel('年份')
    # plt.title('登顶次数')
    # plt.savefig('./first_ascent_vs_year.png')
    # plt.show()

if __name__ == '__main__':
    main()



