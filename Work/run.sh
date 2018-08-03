#!/bin/bash
#########################################################################
# File Name: run.sh
# Author: lilinji
# mail: lilinji@novogene.com
# Created Time: Fri 03 Aug 2018 03:15:53 PM CST
#########################################################################


sh /root/Learn_Python/Excel/HPC/wget.sh 2>/dev/null 

/usr/local/bin/python3  /root/Learn_Python/Excel/detail_excel.py 

/usr/bin/python /root/Learn_Python/Excel/sendmail.py






