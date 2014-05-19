homedir=$1
serverip=$2
user=$3
logdir=$4
serverparam=$5
ip=`cat ${homedir}/Desktop/one-time-test-suite/ip.txt`
ppp=`cat ${homedir}/Desktop/one-time-test-suite/iface.txt`
ssh ${user}@${serverip} "mkdir -p ./dumps/${serverparam}"
#ip=`ifconfig $ppp | perl -e '($ip) = map { /inet addr:(\d+\.\d+\.\d+\.\d+).*/ } <>; print "$ip\n"'`
ipstart=`echo $ip | cut -d'.' -f1`
ipsecond=`echo $ip | cut -d'.' -f2`
nodeid=`who | head -1 | cut -d" " -f1`
tstamp=`date +%s`
filename="./dumps/${serverparam}/server_spoof_${ip}_${tstamp}"
filename1="$logdir/client_spoof_${ip}_${tstamp}"
ssh ${user}@${serverip} "./start_tcpdump.sh $filename $ip" &
tcpdump -i $ppp host ${serverip}  -w $filename1 &
for i in 1 2
do
	sudo hping3 -c 10 -i 1  -S $serverip
	third=`shuf -i 1-254 -n1`
	fourth=`shuf -i 1-254 -n1`
	spoofed=`echo $ipstart"."$ipsecond"."$third"."$fourth`
	sudo hping3 -c 10 -i 1 -p 443  -S -a $spoofed $serverip  
	ipstart=`shuf -i 1-254 -n1`
	ipsecond=`shuf -i 1-254 -n1`
done
ssh ${user}@${serverip} "./killdump.sh $filename $clientip"
kill -2 $(ps aux | grep "[t]cpdump host ${serverip} " | awk '{print $2}')
