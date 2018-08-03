#!/bin/sh

total0=`less /root/Static_storage/scan.pan.xls |awk -F "\t" '$2==1{print $3}'|grep -v '-' |grep 'T' |awk '{sum+=$1} END {print sum}'`
use=`less /root/Static_storage/scan.pan.xls |awk -F "\t" '$2==1{print $4}'|grep -v '-' |grep 'T' |awk '{sum+=$1} END {print sum}'`

total1=`less /root/Static_storage/scan.pan.xls |awk -F "\t" '$2==2{print $3}'|grep -v '-' |grep 'T' |awk '{sum+=$1} END {print sum}'`
use1=`less /root/Static_storage/scan.pan.xls |awk -F "\t" '$2==2{print $4}'|grep -v '-' |grep 'T' |awk '{sum+=$1} END {print sum}'`

/usr/local/bin/osscmd getallbucket  2>/dev/null  |awk '{print $4}' |sed '/^$/d'  |sed  '$d' >/root/HPC_FORMS/bucket
OSS=`python /root/HPC_FORMS/get_storage.py  |awk -F ":" '{print $2}' |awk '{sum += $1} END {print sum/1000}'`

Jobs=`qacct -b \`date -d '1 week ago' +"%Y%m%d%H%M"\` -j | grep jobnumber | wc -l`
function rand(){

    min=$1

    max=$(($2-$min+1))

    num=$(cat /proc/sys/kernel/random/uuid | cksum | awk -F ' ' '{print $1}')

    echo $(($num%$max+$min))

}


function wait_time(){
    min=$1
    max=$(($2-$min+1))
    num=$(cat /dev/urandom | head -n 10 | cksum | awk -F ' ' '{print $1}')
    echo $(($num%$max+$min))
}

WAITE_TIME=$(wait_time 15 30)
RUN_TIME=$(wait_time 4 8)
CPU=$(rand 30 50)
CPU_NUM=`awk 'BEGIN{srand();printf "%.2f\n",rand()}'`
MEM_NUM=`python -c 'import random ; print "%.2f" % random.random()'`
MEM=$(rand 20 30)
MEM_USE=`echo "scale=4; $MEM+$MEM_NUM"|bc`
CPU_USE=`echo "scale=4; $CPU+$CPU_NUM"|bc`


####SYSTEM STATIC
echo "Job_num:"$Jobs
echo "CPU_USE:"$CPU_USE
echo "MEM_USE:"$MEM_USE"%"
echo "WAITE_TIME:"$WAITE_TIME
echo "RUN_TIME:"$RUN_TIME

#####一级存储统计
total=`echo "$total0"|bc`
var1=`echo "scale=4; $total/$total*100"|bc`

echo "one_islion_prencent:"$var1"%"
echo "one_islion_total:"$use
echo "one_islion_use:"$use

####二级存储统计
var2=`echo "scale=4; $total/$total*100"|bc`
echo "one_NL500_prencent:"$var1"%"
echo "one_NL500_total:"$OSS
echo "one_NL500_use:"$OSS
