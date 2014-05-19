#!/bin/bash
# authors : Rahul,Aravindh & Sameer
# input : server address, serverside dump's foldername, local experimnts foldername
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
recvport=`shuf -i3000-10000 -n1`
actRate=`echo "${pacSize} * 8 * ${rate}/ 1024" | bc`
ssh ${uname}@${server} "sudo mkdir -p ./dumps/${serverparam}"
receiver_log="./dumps/${serverparam}/ul_recv_${actRate}_${pacSize}_${timestamp}.log"
ssh ${uname}@${server} "./BufferAnalysis/src/ITGRecv/ITGRecv -l ${receiver_log}" &
echo "started recv..."
sleep 30
echo "starting sender .... "
./src/ITGSend/ITGSend -a $cliIp -T UDP -rp ${recvport} -C ${rate} -t ${time} -c ${pacSize} -l ${expdir}/ul_send_${actRate}_${pacSize}_${timestamp}.log
ssh ${uname}@${server} "./killITGRecv.sh ${serverparam}"
echo "killed recv..."
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
        #echo ${pSize} ${packsRate} ${sRate} $i
	sleep 2
 	conductTest $3 ${pSize} 10000 ${sRate} $serverparam $logdir $uname $server
        sleep 50
  done
done

