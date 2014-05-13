import argparse
import logging
import sys
import time
import subprocess as sub
from os.path import expanduser
import os 

TESTSUITE_LOG='suite.log'
TEST_LOG=time.strftime("%j-%Y")+'.log'
HOME_DIR=expanduser("~")
EXP_DIR=HOME_DIR+"/one-time-test-suite/"
hostname = os.uname()[1]

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
	elif test=='ping':
		if len(args)!=1:
			return False
                else:
                        return True
        elif test=='tcptraceroute':
                if len(args)!=1:
                        return False
                else:
                        return True
        elif test=='ping_gw':
                if len(args)!=1:
                        return False
                else:
                        return True
	
def run_curl(args):
	logTo(TEST_LOG,'Starting Curl with args . '+' '.join(args),'INFO','a')
	p=sub.Popen(["bash","curl.sh",HOME_DIR,args[0],args[1],args[2],args[3],EXP_DIR,"onetime/"+hostname+"/"+EXP_DIR])
	p.wait()
	logTo(TEST_LOG,'Finished Curl ','INFO','a')

def run_iperf(args):
        logTo(TEST_LOG,'Starting Iperf with args . '+' '.join(args),'INFO','a')
	p=sub.Popen(["bash","iperf_tcp_up.sh",HOME_DIR,args[0],args[1],args[2],EXP_DIR,"onetime/"+hostname+"/"+EXP_DIR)
	p.wait()
        logTo(TEST_LOG,'Finished Iperf ','INFO','a')

def run_ping(args):
        logTo(TEST_LOG,'Starting Ping with args . '+' '.join(args),'INFO','a')
        p=sub.Popen(["bash","ping.sh",HOME_DIR,args[0],args[1],args[2],EXP_DIR,"onetime/"+hostname+"/"+EXP_DIR)
        p.wait()
        logTo(TEST_LOG,'Finished Ping ','INFO','a')
def run_ping_gw():
	logTo(TEST_LOG,'Starting Ping Gw with args . '+' '.join(args),'INFO','a')
        p=sub.Popen(["bash","tcptraceroute_gw.sh",HOME_DIR,args[0],args[1],args[2],EXP_DIR,"onetime/"+hostname+"/"+EXP_DIR)
        p.wait()
        logTo(TEST_LOG,'Finished Ping Gw ','INFO','a')

def run_tcptraceroute(args):
        logTo(TEST_LOG,'Starting TCPtraceroute with args . '+' '.join(args),'INFO','a')
        p=sub.Popen(["bash","tcptraceroute.sh",HOME_DIR,args[0],args[1],args[2],EXP_DIR,"onetime/"+hostname+"/"+EXP_DIR)
        p.wait()
        logTo(TEST_LOG,'Finished tcptraceroute ','INFO','a')
def run_selenium(args):
        logTo(TEST_LOG,'Starting Selenium  with args . '+' '.join(args),'INFO','a')
        p=sub.Popen(["python","useext.py",HOME_DIR,args,EXP_DIR)
        p.wait()
        logTo(TEST_LOG,'Finished tcptraceroute ','INFO','a')
def run_CDN():
        logTo(TEST_LOG,'Starting CDNPerf with args . '+' '.join(args),'INFO','a')
        p=sub.Popen(["bash","tcptraceroute.sh",HOME_DIR,args[0],args[1],args[2],EXP_DIR,"onetime/"+hostname+"/"+EXP_DIR)
        p.wait()
        logTo(TEST_LOG,'Finished tcptraceroute ','INFO','a')	



def runMaster(options):
	#TODO
	location='-'.join(options['L'])
	provider='-'.join(options['P'])
	contype='-'.join(options['C'])
	global EXP_DIR
        if options['r']:
                #Adding Roaming  Test
                EXP_DIR=EXP_DIR+location+'_'+provider+'_'+contype+'/'+time.strftime('%s')
	else:
		EXP_DIR=EXP_DIR+location+'_'+provider+'_'+contype+'/Roam/'+options['r']+time.strftime('%s')
	if not os.path.exists(EXP_DIR):
		os.makedirs(EXP_DIR)

	if options['t']:
		#Adding Downlink Test
		fcurl=open('testArgs/curl','r')
		lines=fcurl.readlines()
		lines=[x.split('\n')[0] for x in lines]
		if argsFine(lines,'curl'):			
			run_curl(lines)
		else:
			logTo(TESTSUITE_LOG,'Error in parsing Curl args Missing or wrong Args in testArgs/curl','ERROR','w')
			sys.exit('Error! Check suite.log for more details...')
		fcurl.close()
		#Adding Iperf Uplink Test
                fperf=open('testArgs/iperf','r')
                lines=fperf.readlines()
                lines=[x.split('\n')[0] for x in lines]
                if argsFine(lines,'iperf'):
			run_iperf(lines)
                else:
                        logTo(TESTSUITE_LOG,'Error in parsing Iperf args Missing or wrong Args in testArgs/iperf','ERROR','w')
                        sys.exit('Error! Check suite.log for more details...')
                fperf.close()
	elif options['l']:
		#Adding Latency Tests
                fping=open('testArgs/ping','r')
                lines=fping.readlines()
                lines=[x.split('\n')[0] for x in lines]
		for line in lines:
			if argsFine(line,'ping'):
				run_ping(line)
			else:
				logTo(TESTSUITE_LOG,'Error in parsing Ping args Missing or wrong Args in testArgs/ping','ERROR','w')
				sys.exit('Error! Check suite.log for more details...')
		fping.close()
		run_ping_gw()
	elif options['T']:
		#Addding Tcptraceroute tests
		ftr=open('testArgs/tcptraceroute','r')
                lines=ftr.readlines()
                lines=[x.split('\n')[0] for x in lines]
                for line in lines:
                        if argsFine(line,'tcptraceroute'):
                                run_tcptraceroute(line)
                        else:
                                logTo(TESTSUITE_LOG,'Error in parsing Traceroute args Missing or wrong Args in testArgs/tcptraceroute','ERROR','w')
                                sys.exit('Error! Check suite.log for more details...')
                ftr.close()
	elif options['n']:
		#Adding ICSI Netalyzr Test
                run_netalyzr()
	elif options['p']:
		#Adding PLT Selenium Test
                fplt=open('testArgs/selenium','r')
                lines=fplt.readlines()
                lines=[x.split('\n')[0] for x in lines]
                for line in lines:
                        if argsFine(line,'selenium'):
                                run_selenium(line)
                        else:
                                logTo(TESTSUITE_LOG,'Error in parsing Selenium  args Missing or wrong Args in testArgs/selenium','ERROR','w')
                                sys.exit('Error! Check suite.log for more details...')
                fplt.close()
        elif options['c']:
                #Adding CDN performance Test
                run_CDN()
               	print "done"
        elif options['i']:
                #Adding IP Spoofing  Test
                #TODO
                print "done"
        elif options['s']:
                #Adding Statefull Firewall Test
                #TODO
                print "done"
        elif options['b']:
                #Adding Buffer Size Test
                #TODO
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

def logTo(fname,msg,msg_type,mode):
	logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s',filename=fname,filemode=mode)
	if msg_type=='ERROR':
		logging.error(msg)
	elif msg_type=='DEBUG':
		logging.debug(msg)
        elif msg_type=='INFO':
                logging.info(msg)
	else:
		logging.warning(msg)

if __name__ == '__main__':	
	main()

