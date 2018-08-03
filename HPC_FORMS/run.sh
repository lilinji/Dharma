#!/bin/bash
#########################################################################
# File Name: run.sh
# Author: lilinji
# mail: lilinji@novogene.com
# Created Time: Wed 01 Aug 2018 12:00:07 AM CST
#########################################################################

sh /root/HPC_FORMS/static_hpc_forms.sh >/root/HPC_FORMS/aliyun.txt

/usr/bin/ossutil cp -f  /root/HPC_FORMS/aliyun.txt  oss://3811/statics/aliyun.txt

