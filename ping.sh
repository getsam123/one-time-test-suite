#!/bin/bash
homedir=$1
server=$2
logdir=$3
tmstmp=`date +%s`
#pingCount=`cat ${homedir}/conf | grep "PING_COUNT" |grep -v "#"| tr -d ' ' | cut -d '=' -f2`
pingCount=30
name=`echo ${server} | tr '.' '-'`
outputfile="${logdir}/ping_landmark_${name}_${tmstmp}.txt"

now=`date +%s`
echo "$now" >> $outputfile

echo "===Ping to Landmark : $server===" >> $outputfile
#iface=`cat $homedir/conf | grep "IFACE" | cut -d ' ' -f3`
iface=`cat ${homedir}/one-time-test-suite/iface.txt`
clientip=`cat ${homedir}/one-time-test-suite/ip.txt`
ping -I $iface -n -c $pingCount $server >> $outputfile 2>&1
echo "===================================================" >> $outputfile

now=`date +%s`
echo "$now" >> $outputfile
