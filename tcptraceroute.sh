#!/bin/bash

homedir=$1
tmstmp=`date +%s`
server=$2
logdir=$3

maxhops=30
name=`echo ${server} | tr '.' '-'`
outputfile=$logdir/tcptraceroute_server_${name}_${tmstmp}.txt
now=`date +%s`
echo "$now" >> $outputfile
echo "===TCPTraceroute to Node : $server===" >> $outputfile

iface=`cat ${homedir}/Desktop/one-time-test-suite/iface.txt`
tmstmp1=`date +%s`
sudo tcptraceroute -n -i $iface -m $maxhops $server >> $outputfile 2>&1
echo "===================================================" >> $outputfile
now=`date +%s`
echo "$now" >> $outputfile
