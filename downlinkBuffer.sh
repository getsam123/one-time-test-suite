#!/bin/bash
# authors : Rahul,Aravindh & Sameer
# input : serverside dump's foldername, local experimnts foldername
#	: send rate = (200 and 250 for 2G) and (1000 and 2000 for 3G)
#output : clientside log file in experiments folder, serverside log file in dumps folder
conductTest(){
cliIp=$1
pacSize=$2
time=$3 #millisec
rate=$4 #packets/sec
serverparam=$5
expdir=$6
uname=$7
server=$8
timestamp=`date +%s`
actRate=`echo "${pacSize} * 8 * ${rate}/ 1024" | bc`
ssh ${uname}@${server} "mkdir -p ./dumps/${serverparam}"
sender_log="./dumps/${serverparam}/dl_send_${actRate}_${pacSize}_${timestamp}.log"
./src/ITGRecv/ITGRecv -Sp $9 &
ssh ${uname}@${server} "./BufferAnalysis/src/ITGSend/ITGSend -a $cliIp -Sdp $9 -T UDP -x ${expdir}/dl_recv_${actRate}_${pacSize}_${timestamp}.log -C ${rate} -t ${time} -c ${pacSize} -l ${sender_log}"
kill -2 $(ps aux | grep "src/ITGRecv" | awk '{print $2}')

}

homedir=$1
uname=$2
server=$3
logdir=$4
serverparam=$5
sRate1=$6
sRate2=$7
link=`cat ${homedir}/Desktop/one-time-test-suite/iface.txt`
clientip=`cat ${homedir}/Desktop/one-time-test-suite/ip.txt`

for pSize in 1400
do
 for sRate in $sRate1 $sRate2
 do  
	sleep 2
	x=`echo $RANDOM`
	y=100
	z=$(($x % $y))
	porte=$(($z * 100))
	port=$(($porte + 9000))
 	conductTest $clientip ${pSize} 10000 ${sRate} $serverparam $logdir $uname $server $port
        sleep 50
  done
done
