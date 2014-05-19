#!/bin/bash
homedir=$1
curlduration=$2
server=$3
largefile=$4
uname=$5
logdir=$6
serverparam=$7

tmstmp=`date +%s`
outputfile="${logdir}/curl_op_${tmstmp}.txt"
ssh ${uname}@${server} "mkdir -p ./dumps/${serverparam}"
sleep 15
dump_curl_mp="$logdir/tcpdump_curl_mp_${tmstmp}"
dump_curl_server="./dumps/${serverparam}/tcpdump_curl_server_${tmstmp}"

now=`date +%s`
echo "$now" >> $outputfile
#Curl Script

#Writing CLIENTIP & iface value here because iface might change after reconnection
iface=`cat ${homedir}/Desktop/one-time-test-suite/iface.txt`
clientip=`cat ${homedir}/Desktop/one-time-test-suite/ip.txt`


ssh ${uname}@${server} "./start_curl_tcpdump.sh $dump_curl_server $clientip $curlduration" &
sleep 15
tcpdump host ${server} -i $iface -s 100 -w $dump_curl_mp &
sleep 10

echo "=====      ${largefile} FILE    =====" >> ${outputfile}

curl -o /dev/null --interface $iface -w "\nTotal Time : %{time_total} Sec \t Lookup time : %{time_namelookup} Sec\tDownload Size : %{size_download} bytes\t Download Speed : %{speed_download}Bps" ${largefile} >> ${outputfile} 2>&1 &
sleep $curlduration

#Killing Curl Process
kill -9 $(ps -ef | grep '[c]url -o' | awk '{print $2}')

echo "==============================" >> ${outputfile}

#Killing Local TCPDump
kill -2 $(ps aux | grep "[t]cpdump host ${server} -i $iface" | awk '{print $2}')
ssh ${uname}@${server} "./killtcpdump.sh $dump_curl_server $clientip"
