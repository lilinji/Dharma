#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: detail_excel.py
# Author: lilinji
# mail: lilinji@XXXX.com
# Created Time: Mon 30 Jul 2018 01:14:57 PM CST
#########################################################################

import xlsxwriter
import xlrd
import xlwt
import re
import sys
from xlutils.copy import copy
from xlrd import open_workbook
import time
import datetime


HEAD = '''
注：
1）表头中统计时间：日期格式要求为月/日；时间段为：上一周的周一至周日（严格按照时间段要求反馈）；
2）反馈时间为：每周周一上午11：00前
3）严格按照模板统计反馈
'''
####################Read_Files_Class

class CustomOpen(object):
    def __init__(self, filename, method):
        self.file = open(filename, method)
    def __enter__(self):
        return self.file
    def __exit__(self, ctx_type, ctx_value, ctx_traceback):
        self.file.close()

Alibj={}
######################Aliyun
def ali_file():
    with CustomOpen('/root/Learn_Python/Excel/HPC/aliyunXXXX.txt', 'r') as f1:
            list1 = f1.readlines()
            for line in list1:
                    line = line.strip('\n')
                    line2 = re.split(':', line)# split : 输出数组行
                    Alibj[line2[0]] = line2[1]
            f1.close()

Alinj={}
######################Aliyun
def alinj_file():
    with CustomOpen('/root/Learn_Python/Excel/HPC/alinjXXXX.txt', 'r') as f1:
            list1 = f1.readlines()
            for line in list1:                    
                    line = line.strip('\n')
                    line2 = re.split(':', line)# split : 输出数组行
                    Alinj[line2[0]] = line2[1]
            f1.close()
Tjhpc={}
######################TJHPC
def tj_file():
    with CustomOpen('/root/Learn_Python/Excel/HPC/tjXXXX.txt', 'r') as f1:
            list1 = f1.readlines()
            for line in list1:
                    line = line.strip('\n')
                    line2 = re.split(':', line)# split : 输出数组行
                    Tjhpc[line2[0]] = line2[1]
            f1.close()

Njhpc={}
######################NJHPC
def nj_file():
    with CustomOpen('/root/Learn_Python/Excel/HPC/njXXXX.txt', 'r') as f1:
            list1 = f1.readlines()
            for line in list1:
                    line = line.strip('\n')
                    line2 = re.split(':', line)# split : 输出数组行
                    Njhpc[line2[0]] = line2[1]
            f1.close()

Ushpc={}
######################USHPC
def us_file():
    with CustomOpen('/root/Learn_Python/Excel/HPC/usXXXX.txt', 'r') as f1:
            list1 = f1.readlines()
            for line in list1:
                    line = line.strip('\n')
                    line2 = re.split(':', line)# split : 输出数组行
                    Ushpc[line2[0]] = line2[1]
            f1.close()

Sghpc={}
######################SGPHPC
def sgp_file():
    with CustomOpen('/root/Learn_Python/Excel/HPC/Singapore.txt', 'r') as f1:
            list1 = f1.readlines()
            for line in list1:
                    line = line.strip('\n')
                    line2 = re.split(':', line)# split : 输出数组行
                    Sghpc[line2[0]] = line2[1]
            f1.close()

######################RUN def
ali_file()
alinj_file()
tj_file()
nj_file()
us_file()
sgp_file()
print (Sghpc['Job_num'])
print (Tjhpc['one_NL500_prencent'][:5])

#for key in Sghpc:
#    print (Sghpc[key])



##############################
workbook = xlsxwriter.Workbook('HPC_WEEK_USE.xlsx')
worksheet = workbook.add_worksheet()
cell_format = workbook.add_format()
cell_format.set_pattern(1)  # This is optional when using a solid fill.
cell_format.set_bg_color('#F0F8FF')
cell_format.set_border(1)
cell_format.set_font_size(14)
merge_format = workbook.add_format({
    'bold':     True,
    'border':   1,
    'align':    'center',
    'valign':   'vcenter',
    'fg_color': '#F0F8FF',
    'font_size': 14,
    #'set_bold': 1,
})
merge_format_blue = workbook.add_format({
    'bold':     True,
    'border':   1,
    'align':    'center',
    'valign':   'vcenter',
    'fg_color': '#6699CC',
    'font_size': 18,
})

hpc_format = workbook.add_format({
    'bold':     True,
    'border':   1,
    'align':    'center',
    'valign':   'vcenter',
    'fg_color': '#FFFFCC',
    'font_size': 14,
})

yun_format = workbook.add_format({
    'bold':     True,
    'border':   1,
    'align':    'center',
    'valign':   'vcenter',
    'fg_color': '#99FFFF',
    'font_size': 14,
})


worksheet.merge_range('A1:N1', '计算/存储资源', merge_format_blue)
worksheet.merge_range('A2:B2', '资源类型', merge_format)
worksheet.merge_range('C2:H2', '计算节点', merge_format)
worksheet.merge_range('I2:N2', '存储', merge_format)
worksheet.write('A3', '统计时间', cell_format)
worksheet.write('B3', '基地名称', cell_format)
worksheet.write('C3', '资源总量', cell_format)
worksheet.write('D3', '总任务数', cell_format)
worksheet.write('E3', 'cpu使用率\n(45％为阀值)', cell_format)
worksheet.write('F3', '内存使用率\n(50％为阀值)', cell_format)
worksheet.write('G3', '平均等待时间(s)', cell_format)
worksheet.write('H3', '平运行时间(h)', cell_format)
worksheet.write('I3', '一级存储(T)', cell_format)
worksheet.write('J3', '已使用(T)', cell_format)
worksheet.write('K3', '一级存储使用率%', cell_format)
worksheet.write('L3', '二级存储(T)', cell_format)
worksheet.write('M3', '已使用(T)', cell_format)
worksheet.write('N3', '二级存储使用率%', cell_format)
######  row
worksheet.write('B4', '北京(云)集群', cell_format)
worksheet.write('B5', '南京(云)集群', cell_format)
worksheet.write('B6', '天津集群', cell_format)
worksheet.write('B7', '南京集群', cell_format)
worksheet.write('B8', '美国集群', cell_format)
worksheet.write('B9', '新加坡集群', cell_format)
worksheet.write('B10', 'TOTAL', cell_format)
worksheet.write('C4', '136', cell_format)
worksheet.write('C5', '2', cell_format)
worksheet.write('C6', '406', cell_format)
worksheet.write('C7', '195', cell_format)
worksheet.write('C8', '32', cell_format)
worksheet.write('C9', '6', cell_format)
worksheet.write('C10', '785', cell_format)
###### Jobs 
Alibj_Job = int(Alibj['Job_num'])
Tjhpc_Job = int(Tjhpc['Job_num'])
Njhpc_Job = int(Njhpc['Job_num'])
Ushpc_Job = int(Ushpc['Job_num'])
Sghpc_Job = int(Sghpc['Job_num'])
TOTAL_Job =(Alibj_Job+Tjhpc_Job+Njhpc_Job+Ushpc_Job+Sghpc_Job)

#print (TOTAL_Job)
#int (Alibj['Job_num'])+int (Njhpc['Job_num'])+int (Sghpc['Job_num'])+int (Ushpc['Job_num'])+0)
worksheet.write('D4', Alibj['Job_num'], yun_format)
worksheet.write('D5', Alinj['Job_num'], yun_format)
worksheet.write('D6', Tjhpc['Job_num'], hpc_format)
worksheet.write('D7', Njhpc['Job_num'], hpc_format)
worksheet.write('D8', Ushpc['Job_num'], hpc_format)
worksheet.write('D9', Sghpc['Job_num'], yun_format)
worksheet.write('D10', TOTAL_Job, cell_format)

####### CPU
worksheet.write('E4', Alibj['CPU_USE'], yun_format)
worksheet.write('E5', Alinj['CPU_USE'], yun_format)
worksheet.write('E6', Tjhpc['CPU_USE'], hpc_format)
worksheet.write('E7', Njhpc['CPU_USE'], hpc_format)
worksheet.write('E8', Ushpc['CPU_USE'], hpc_format)
worksheet.write('E9', Sghpc['CPU_USE'], yun_format)
worksheet.write('E10','', cell_format)

#######MEM
worksheet.write('F4', Alibj['MEM_USE'], yun_format)
worksheet.write('F5', Alinj['MEM_USE'], yun_format)
worksheet.write('F6', Tjhpc['MEM_USE'], hpc_format)
worksheet.write('F7', Njhpc['MEM_USE'], hpc_format)
worksheet.write('F8', Ushpc['MEM_USE'], hpc_format)
worksheet.write('F9', Sghpc['MEM_USE'], yun_format)
worksheet.write('F10', '', cell_format)

#######WAITE_TIME
worksheet.write('G4', Alibj['WAITE_TIME'], yun_format)
worksheet.write('G5', Alinj['WAITE_TIME'], yun_format)
worksheet.write('G6', Tjhpc['WAITE_TIME'], hpc_format)
worksheet.write('G7', Njhpc['WAITE_TIME'], hpc_format)
worksheet.write('G8', Ushpc['WAITE_TIME'], hpc_format)
worksheet.write('G9', Sghpc['WAITE_TIME'], yun_format)
worksheet.write('G10', '', cell_format)

#######RUN_TIME
worksheet.write('H4', Alibj['RUN_TIME'], yun_format)
worksheet.write('H5', Alinj['RUN_TIME'], yun_format)
worksheet.write('H6', Tjhpc['RUN_TIME'], hpc_format)
worksheet.write('H7', Njhpc['RUN_TIME'], hpc_format)
worksheet.write('H8', Ushpc['RUN_TIME'], hpc_format)
worksheet.write('H9', Sghpc['RUN_TIME'], yun_format)
worksheet.write('H10', '', cell_format)


######one_islion_total
Alibj_St = float(Alibj['one_islion_total'])
Alinj_St = float(Alinj['one_islion_total'])
Tjhpc_St = float(Tjhpc['one_islion_total'])
Njhpc_St = float(Njhpc['one_islion_total'])
Ushpc_St = float(Ushpc['one_islion_total'])
Sghpc_St = float(Sghpc['one_islion_total'])
TOTAL_St = (Alibj_St+Tjhpc_St+Njhpc_St+Ushpc_St+Sghpc_St+Alinj_St)

worksheet.write('I4', Alibj['one_islion_total'], yun_format)
worksheet.write('I5', Alinj['one_islion_total'], yun_format)
worksheet.write('I6', Tjhpc['one_islion_total'], hpc_format)
worksheet.write('I7', Njhpc['one_islion_total'], hpc_format)
worksheet.write('I8', Ushpc['one_islion_total'], hpc_format)
worksheet.write('I9', Sghpc['one_islion_total'], yun_format)
worksheet.write('I10', TOTAL_St, cell_format)

######one_islion_use
Alibj_Ut = float(Alibj['one_islion_use'])
Tjhpc_Ut = float(Tjhpc['one_islion_use'])
Njhpc_Ut = float(Njhpc['one_islion_use'])
Ushpc_Ut = float(Ushpc['one_islion_use'])
Sghpc_Ut = float(Sghpc['one_islion_use'])
TOTAL_Ut = (Alibj_Ut+Tjhpc_Ut+Njhpc_Ut+Ushpc_Ut+Sghpc_Ut)

worksheet.write('J4', Alibj['one_islion_use'], yun_format)
worksheet.write('J5', Alinj['one_islion_use'], yun_format)
worksheet.write('J6', Tjhpc['one_islion_use'], hpc_format)
worksheet.write('J7', Njhpc['one_islion_use'], hpc_format)
worksheet.write('J8', Ushpc['one_islion_use'], hpc_format)
worksheet.write('J9', Sghpc['one_islion_use'], yun_format)
worksheet.write('J10', TOTAL_Ut, cell_format)

#######one_islion_prencent
worksheet.write('K4', Alibj['one_islion_prencent'][:5], yun_format)
worksheet.write('K5', Alinj['one_islion_prencent'][:5], yun_format)
worksheet.write('K6', Tjhpc['one_islion_prencent'][:5], hpc_format)
worksheet.write('K7', Njhpc['one_islion_prencent'][:5], hpc_format)
worksheet.write('K8', Ushpc['one_islion_prencent'][:5], hpc_format)
worksheet.write('K9', Sghpc['one_islion_prencent'][:5], yun_format)
worksheet.write('K10', '', cell_format)

########one_NL500_total
Alibj_Lt = float(Alibj['one_NL500_total'])
Alinj_Lt = float(Alinj['one_NL500_total'])
Tjhpc_Lt = float(Tjhpc['one_NL500_total'])
Njhpc_Lt = float(Njhpc['one_NL500_total'])
Ushpc_Lt = float(Ushpc['one_NL500_total'])
Sghpc_Lt = float(Sghpc['one_NL500_total'])

TOTAL_Lt = (Alibj_Lt+Alinj_Lt+Tjhpc_Lt+Njhpc_Lt+Ushpc_Lt+Sghpc_Lt)


worksheet.write('L4', Alibj['one_NL500_total'], yun_format)
worksheet.write('L5', Alinj['one_NL500_total'], yun_format)
worksheet.write('L6', Tjhpc['one_NL500_total'], hpc_format)
worksheet.write('L7', Njhpc['one_NL500_total'], hpc_format)
worksheet.write('L8', Ushpc['one_NL500_total'], hpc_format)
worksheet.write('L9', Sghpc['one_NL500_total'], yun_format)
worksheet.write('L10', TOTAL_Lt, cell_format)

########one_NL500_use
Alibj_Lu = float(Alibj['one_NL500_use'])
Alinj_Lu = float(Alinj['one_NL500_use'])
Tjhpc_Lu = float(Tjhpc['one_NL500_use'])
Njhpc_Lu = float(Njhpc['one_NL500_use'])
Ushpc_Lu = float(Ushpc['one_NL500_use'])
Sghpc_Lu = float(Sghpc['one_NL500_use'])
TOTAL_Lu = (Alibj_Lu+Alinj_Lu+Tjhpc_Lu+Njhpc_Lu+Ushpc_Lu+Sghpc_Lu)

worksheet.write('M4', Alibj['one_NL500_use'], yun_format)
worksheet.write('M5', Alinj['one_NL500_use'], yun_format)
worksheet.write('M6', Tjhpc['one_NL500_use'], hpc_format)
worksheet.write('M7', Njhpc['one_NL500_use'], hpc_format)
worksheet.write('M8', Ushpc['one_NL500_use'], hpc_format)
worksheet.write('M9', Sghpc['one_NL500_use'], yun_format)
worksheet.write('M10', TOTAL_Lu, cell_format)

##########one_NL500_prencent

worksheet.write('N4', Alibj['one_NL500_prencent'][:5], yun_format)
worksheet.write('N5', Alinj['one_NL500_prencent'][:5], yun_format)
worksheet.write('N6', Tjhpc['one_NL500_prencent'][:5], hpc_format)
worksheet.write('N7', Njhpc['one_NL500_prencent'][:5], hpc_format)
worksheet.write('N8', Ushpc['one_NL500_prencent'][:5], hpc_format)
worksheet.write('N9', Sghpc['one_NL500_prencent'][:5], yun_format)
worksheet.write('N10', '', cell_format)

##############day time
now_time = datetime.datetime.now()

yes_time = now_time + datetime.timedelta(days=-1)
week_time = now_time + datetime.timedelta(days=-7)
month1 = week_time.month
day1 = week_time.day
month2 = yes_time.month
day2 = yes_time.day
ad = str(month1) +'/'+str(day1)
ed = str(month2) +'/'+str(day2)
dayend = ad+'-'+ed
print (dayend)


worksheet.merge_range('A4:A9', dayend, merge_format)
worksheet.merge_range('A15:N16', HEAD, merge_format)
workbook.close()
