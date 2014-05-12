import argparse
import logging
import sys



def argsFine(args,test):
	if test=='curl':
		if len(args)!=4:
			return False
		else:
			return True
	elif test=='iperf':
                if len(args)!=3:
                        return False
                else:
                        return True
	

def runMaster(options):
	#TODO
	location='_'.join(options['L'])
	provider='_'.join(options['P'])
	contype='_'.join(options['C'])
	test_add=[]
	if options['t']:
		#Adding Downlink Test
		fcurl=open('testArgs/curl','r')
		lines=fcurl.readlines()
		lines=[x.split('\n')[0] for x in lines]
		if argsFine(lines,'curl'):
			test_add.append('run_curl '+' '.join(lines)+'\n')
		else:
			logging.error('Error in parsing Curl args Missing or wrong Args in testArgs/curl')
			sys.exit('Error! Check ConfigError.log for more details...')
		fcurl.close()
		#Adding Iperf Uplink Test
                fperf=open('testArgs/iperf','r')
                lines=fperf.readlines()
                lines=[x.split('\n')[0] for x in lines]
                if argsFine(lines,'iperf'):
                        test_add.append('run_iperf_tcp_up '+' '.join(lines)+'\n')
                else:
                        logging.error('Error in parsing Iperf args: Missing or wrong Args in testArgs/iperf')
                        sys.exit('Error! Check ConfigError.log for more details...')
                fperf.close()
	fmaster=open('master.sh','r')
	fnewmaster=open('master1.sh','w')
	for line in fmaster.readlines():
		fnewmaster.write(line)
	for line in test_add:
		fnewmaster.write(line)
	print "done"


def main():
	parser = argparse.ArgumentParser(description='process ruralnetOneTime arguments')
	parser.add_argument('-t',action='store_true',help='Run Throughput Test')
        parser.add_argument('-l',action='store_true',help='Run Latency Test')
        parser.add_argument('-T',action='store_true',help='Run Traceroute Test')
        parser.add_argument('-i',action='store_true',help='Run Ip spoofing Test')
        parser.add_argument('-s',action='store_true',help='Run Statefull Firewall Test')
        parser.add_argument('-n',action='store_true',help='Run ICSI Netalyzr Test')
        parser.add_argument('-r',action='store_true',help='Run Roaming Test')
        parser.add_argument('-p',action='store_true',help='Run Page Load Time Test')
        parser.add_argument('-c',action='store_true',help='Run CDN performance Test')
        parser.add_argument('-b',action='store_true',help='Run Buffer Size Test')
	parser.add_argument('-L',nargs='+',help='Locaton of Test being conducted',required=True)
	parser.add_argument('-P',nargs='+',help='Provider of Test being conducted',required=True)
	parser.add_argument('-C',nargs='+',help='Connection type of Test being conducted umts/edge/evdo',required=True)
	args = parser.parse_args()
	runargs=vars(args)
	runMaster(runargs)
if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='ConfigError.log',
                    filemode='w')
	main()
