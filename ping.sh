#!/bin/bash
homedir=$1
server=$2
logdir=$3
tmstmp=`date +%s`
pingCount=30
name=`echo ${server} | tr '.' '-'`
outputfile="${logdir}/ping_landmark_${name}_${tmstmp}.txt"

now=`date +%s`
echo "$now" >> $outputfile

echo "===Ping to Landmark : $server===" >> $outputfile
#iface=`cat $homedir/conf | grep "IFACE" | cut -d ' ' -f3`
iface=`cat ${homedir}/Desktop/one-time-test-suite/iface.txt`
pingCommand="ping -s 512 -I $iface -n -c $pingCount"
$pingCommand $server >> $outputfile 2>&1

echo "===================================================" >> $outputfile

now=`date +%s`
echo "$now" >> $outputfile
