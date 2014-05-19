homedir=$1
serverip=$2
user=$3
logdir=$4
serverparam=$5
clientip=`cat ${homedir}/Desktop/one-time-test-suite/ip.txt`
ppp=`cat ${homedir}/Desktop/one-time-test-suite/iface.txt`
ssh ${user}@${serverip} "mkdir -p ./dumps/${serverparam}"
tstamp=`date +%s`
nodeid=`who | head -1 | cut -d" " -f1`
#clientip=`ifconfig $ppp | perl -e '($ip) = map { /inet addr:(\d+\.\d+\.\d+\.\d+).*/ } <>; print "$ip\n"'`
filename="./dumps/${serverparam}/server_firewall_${tstamp}"
filename1="$logdir/client_firewall_${tstamp}"
ssh ${user}@${serverip} "./start_tcpdump.sh $filename $ip" &
tcpdump -i $ppp host ${serverip}  -w $filename1 &

ssh ${user}@${serverip} "sudo hping3 -c 10 -i 1 -p 443 -A   $clientip"
ssh ${user}@${serverip} "sudo hping3 -c 10 -i 1 -p 443 -F   $clientip"
ssh ${user}@${serverip} "sudo hping3 -c 10 -i 1 -p 443  -S   $clientip"

ssh ${user}@${serverip} "./killdump.sh $filename $clientip"
kill -2 $(ps aux | grep "[t]cpdump host ${serverip} " | awk '{print $2}')
