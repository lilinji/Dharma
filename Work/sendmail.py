#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: sendmail.py
# Author: lilinji
# mail: lilinji@xxxx.com
# Created Time: Wed 01 Aug 2018 08:38:31 PM CST
#########################################################################

import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import time
import datetime
# 发件人地址，通过控制台创建的发件人地址

head = '''

<html><body>
<p>附件为集群使用情况:</p>
<br />
<br />
时间为
'''
food = '''
<br />
<br />
<br />
<br />
<br />
系统自动邮件请不要回复
请查收
祝好</body></html>
'''
#now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
week = time.strftime("%W")
weeklast = (int(week)-1)
NAME = "2018年第"+str (weeklast)+"周"

def sendmail(subject, msg, toaddrs, fromaddr, smtpaddr, password):
    '''
    @subject:邮件主题
    @msg:邮件内容
    @toaddrs:收信人的邮箱地址
    @fromaddr:发信人的邮箱地址
    @smtpaddr:smtp服务地址，可以在邮箱看，比如163邮箱为smtp.163.com
    @password:发信人的邮箱密码
    '''
    mail_msg = MIMEMultipart()
    if not isinstance(subject, unicode):
        subject = unicode(subject, 'utf-8')
    mail_msg['Subject'] = subject
    mail_msg['From'] = fromaddr
    mail_msg['To'] = ','.join(toaddrs)
    mail_msg.attach(MIMEText(msg, 'html', 'utf-8'))

    #######发送附件
    xlsxpart = MIMEApplication(open('HPC_WEEK_USE.xlsx', 'rb').read())
    xlsxpart["Content-Type"] = 'application/octet-stream'
    xlsxpart.add_header('Content-Disposition', 'attachment', filename='HPC_WEEK_USE.xlsx')
    mail_msg.attach(xlsxpart)

    try:
        s = smtplib.SMTP_SSL()
        s.connect(smtpaddr, 465)  # 连接smtp服务器
        s.login(fromaddr, password)  # 登录邮箱
        s.sendmail(fromaddr, toaddrs, mail_msg.as_string())  # 发送邮件
        s.quit()
    except Exception, e:
        print "Error: unable to send email"
        print traceback.format_exc()


if __name__ == '__main__':
    fromaddr = "it@xxxx.com"
    smtpaddr = "smtp.exmail.qq.com"
    toaddrs = ["xxx@xxxx.com","xxxx@xxxx.com","xxxx@xxxx.com"]
    subject = "集群每周报表"
    password = "xxxx"
    msg = (head+str (NAME)+food)
#    excelfile = "hello.xlsx"
    sendmail(subject, msg, toaddrs, fromaddr, smtpaddr, password)
