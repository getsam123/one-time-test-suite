#!/bin/bash
homedir=$1
iperf_duration=$2
server=$3
uname=$4
logdir=$5
serverparam=$6
tmstmp=`date +%s`

#iperf_uprate=`cat ${homedir}/conf | grep "IPERF_RATE_UPLINK"| grep -v "^#" | tr -d ' ' | cut -d '=' -f2`
#iperf_downrate=`cat ${homedir}/conf | grep "IPERF_RATE_DOWNLINK"| grep -v "^#" | tr -d ' ' | cut -d '=' -f2`

iperf_port=`cat ${homedir}/Desktop/one-time-test-suite/iperf_port.txt`
ssh ${uname}@${server} "mkdir -p ./dumps/${serverparam}"
dump_iperf_tcp_up_server="./dumps/${serverparam}/dump_iperf_tcp_up_server_$tmstmp"
dump_iperf_tcp_down_server="./dumps/${serverparam}/dump_iperf_tcp_down_server_$tmstmp"

outputfile="${logdir}/iperf_up_${tmstmp}.txt"
outputfile_server="./dumps/${serverparam}/iperf_server_op_${tmstmp}.txt"

dump_tcp_up_mp="${logdir}/tcpdump_TCP_up_iperf_op_${tmstmp}"
dump_tcp_down_mp="${logdir}/tcpdump_TCP_down_iperf_op_${tmstmp}"

now=`date +%s`
echo "$now" >> $outputfile

echo "===========>UPLINK : TCP Iperf to ${server} at $tmstmp===============" >>$outputfile
#Iperf Script
iface=`cat ${homedir}/Desktop/one-time-test-suite/iface.txt`
clientip=`cat ${homedir}/Desktop/one-time-test-suite/ip.txt`

ssh ${uname}@${server} "./start_iperf_tcpdump.sh $dump_iperf_tcp_up_server $clientip $iperf_duration $iperf_port" &
sleep 15
tcpdump host ${server} -i $iface -s 100 -w $dump_tcp_up_mp &
sleep 15
#ssh ${uname}@$server "iperf -s -p $iperf_port" &
ssh ${uname}@$server "./startiperf.sh $iperf_port $iperf_duration" &
sleep 60
iperf -c $server -p $iperf_port -t $iperf_duration >> $outputfile 2>&1
ssh ${uname}@$server "./killiperf.sh $iperf_port"
ssh ${uname}@${server} "./killtcpdump.sh $dump_iperf_tcp_up_server $clientip" &

kill -2 $(ps aux | grep "[t]cpdump host ${server} -i $iface" | awk '{print $2}')
sleep 60
echo "" >> $outputfile
echo "==============================================================" >> $outputfile
now=`date +%s`
echo "$now" >> $outputfile
