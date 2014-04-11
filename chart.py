#encoding=utf-8
__author__ = 'jinfeng'

import sys
import string
import numpy as np
import matplotlib as mpl
#关闭X-window
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

#源文件
source_file = 'Emmagee_TestResult_20140402150142.csv'
columns = 'timestamp, pss_mem, app_mem, remain_mem, app_cpu, total_cpu, flow, charge, current, temperature, voltage'
font = FontProperties(fname='simsun.ttc', size=14)

def process_data():

    column_types = 'S24, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6'


    #read the data by numpy
    np_data = np.genfromtxt(source_file, dtype=column_types, delimiter=',', skip_header=10,
                             skip_footer=4, names=columns, invalid_raise=False)

    return np_data


def draw_chart(np_data, column, title):

    fig = plt.figure()
    #设置图片尺寸，1600x900
    fig.set_size_inches(16, 9)

    ax1 = fig.add_subplot(111)
    ax1.set_title(title, fontproperties=font)

    ax1.plot(np_data[column], c='red', label=column)
    

    #get and modify x axis label
    times = process_x_labels(ax1, np_data['timestamp'])

    #modify x axis label
    ax1.set_xticklabels(times, rotation=90)

    #display the legend label
    plt.legend()

    # save as png
    plt.savefig(column + '.png')
    print 'saved chart to ' + column + '.png'

def draw_percent_chart():
    np_data = process_data()

    titles = ['时间', '应用占用内存比(%)', '应用占用CPU率(%)', 'CPU总使用率(%)']
    column_list = ['timestamp', 'app_mem', 'app_cpu', 'total_cpu']
    colors = ['blank', 'red', 'blue', 'green']

    fig = plt.figure()
    fig.set_size_inches(16, 9)

    for i in range(1, len(column_list)):
        ax1 = fig.add_subplot(111)
        title = unicode(titles[i], 'utf-8')
        ax1.plot(np_data[column_list[i]], c=colors[i], label=title)


    plt.legend(prop=font)
    plt.savefig('percentage.png')
    print 'saved chart to percentage.png'



def process_x_labels(ax1, t_temp):
    #获取默认的横坐标的信息
    labels = [item.get_text() for item in ax1.get_xticklabels()]

    idx = 0
    times = []
    length = len(t_temp)

    time_max_pt = len(labels)

    t_step=length / time_max_pt

    while idx < length:
        times.append(t_temp[idx])
        idx += t_step

    #数据中的最后一个时间点作为横坐标
    loop = time_max_pt / 3  

    for i in range(1, loop):
        times.remove(times[-1])
        #print i

    times.append(t_temp[-1]) 

    return times

def draw_all_single_chart():
    np_data = process_data()

    titles = ['时间', '应用占用内存PSS(MB)', '应用占用内存比(%)', '机器剩余内存(MB)', '应用占用CPU率(%)', 
                'CPU总使用率(%)', '流量(KB)', '电量(%)', '电流(mA)', '温度(C)', '电压(V)']
    column_list = columns.split(',')

    for i in range(1, len(column_list)):
        column = column_list[i].strip()
        title = unicode(titles[i], 'utf-8')
        draw_chart(np_data, column, title)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        source_file = sys.argv[1]
    draw_all_single_chart()
    draw_percent_chart()
