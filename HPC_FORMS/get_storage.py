#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from aliyunsdkcore import client
from aliyunsdkcms.request.v20170301 import QueryMetricListRequest
import time,re,os,datetime
import json
 
#oss_list=['novocloud-test-zgkxy']
dict1={}

def ReadToFileUsePrint():
    with open('bucket', 'r') as f1:
         list3 = f1.readlines()
         for line in list3:
            line = line.strip('\n')
            line4 = re.split('\s+', line, re.M|re.I)# split 空格 输出数组行
            dict1[line4[0]]=line4

ReadToFileUsePrint()

oss_list = list(dict1.iterkeys())
#print oss_list
 
def gettodayoss(oss):
        global today_lechangecloud_GB
        clt = client.AcsClient('XXXXXXXXXXXXXXX','xxxxxxxxxxxxxxxxx','cn-beijing')
        request = QueryMetricListRequest.QueryMetricListRequest()
        request.set_accept_format('json')
        request.set_Project('acs_oss')
        request.set_Metric('MeteringStorageUtilization')
        today_time = time.strftime('%Y-%m-%d') +" 04:00:00"
        timestamp_today = int(time.mktime(time.strptime(today_time, "%Y-%m-%d %H:%M:%S"))) * 1000
        request.set_StartTime(timestamp_today)
        request.set_Dimensions("{\'BucketName\':"+ oss +"}")
        request.set_Period('3600')
        result = clt.do_action_with_exception(request)
        #print result
        strList = json.loads(result)
        #storage = int(re.split('"|}|:',result)[34])
        storage =strList["Datapoints"][0]['MeteringStorageUtilization']
        today_lechangecloud_GB = ('%.2f' %(storage/float(1073741824)))
        print oss+":"+today_lechangecloud_GB
#        print oss+"在"+today_time+"的容量大小是："+today_lechangecloud_GB+"GB。"
 
def getyesterdayoss(oss):
        global yes_lechangecloud_GB
        clt = client.AcsClient('XXXXXXXXXXXXXXX','xxxxxxxxxxxxxxxxx','cn-beijing')
        request = QueryMetricListRequest.QueryMetricListRequest()
        request.set_accept_format('json')
        request.set_Project('acs_oss')
        request.set_Metric('MeteringStorageUtilization')
        now_time = datetime.datetime.now()
        yes_time= now_time + datetime.timedelta(days=-1)
        yes_time_start = yes_time.strftime('%Y-%m-%d')+" 04:00:00"
        #yes_time_end = yes_time.strftime('%Y-%m-%d')+" 10:00:00"
        timestamp_yesterday_start = int(time.mktime(time.strptime(yes_time_start, "%Y-%m-%d %H:%M:%S"))) * 1000
        #timestamp_yesterday_end = int(time.mktime(time.strptime(yes_time_end, "%Y-%m-%d %H:%M:%S"))) * 1000
        request.set_StartTime(timestamp_yesterday_start)
        #request.set_EndTime(timestamp_yesterday_end)
        request.set_Dimensions("{\'BucketName\':"+ oss +"}")
        request.set_Period('3600')
        yes_result = clt.do_action_with_exception(request)
        #print yes_result
        #yes_storage = int(re.split('"|}|:',yes_result)[34])
        strList = json.loads(yes_result)
        yes_storage =strList["Datapoints"][0]['MeteringStorageUtilization']
        yes_lechangecloud_GB = ('%.2f' %(yes_storage/float(1073741824)))
        print oss+":"+yes_lechangecloud_GB
 
def getdiff(oss):
        diff = float(today_lechangecloud_GB) - float(yes_lechangecloud_GB)
        print "今天与昨天同一时间的云存储差值是"+str(diff)+"GB。"
 
if __name__ == "__main__":
        for oss in oss_list:
                oss = "'%s'"%oss
#                gettodayoss(oss)
                getyesterdayoss(oss)
#                getdiff(oss)
#print("整个脚本执行结束，感谢您的使用！")

