import argparse
import logging
import sys
import time
import commands
import subprocess as sub
from os.path import expanduser
import os
import re
from os import rename
import shlex
import pickle
import netinfo
import random
from selenium import webdriver
from datetime import datetime
from pyvirtualdisplay import Display
#from tracerouteparser import TracerouteParser
#from operator import itemgetter
#from collections import Counter

TESTSUITE_LOG='suite.log'
TEST_LOG=time.strftime("%j-%Y")+'.log'
HOME_DIR=expanduser("~")
EXP_DIR=HOME_DIR+"/Desktop/one-time-test-suite/"
hostname = os.uname()[1]
SERVER_PARAM=""
fstat=open("TestStat.log",'w')
					

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
	elif test=='ipspoof':
                if len(args)!=2:
                        return False
                else:
                        return True
	elif test=='firewall':
                if len(args)!=2:
                        return False
                else:
                        return True
	elif test=='buffer':
                if len(args)!=2:
                        return False
                else:
                        return True
	
def run_curl(args):
	logTo(TEST_LOG,'Starting Curl with args . '+' '.join(args),'INFO','a')
	p=sub.Popen(["bash","curl.sh",HOME_DIR,args[0],args[1],args[2],args[3],EXP_DIR,"onetime/"+SERVER_PARAM])
	p.wait()
	logTo(TEST_LOG,'Finished Curl ','INFO','a')
	fstat.write('Finished Curl\n')

def run_iperf(args):
        logTo(TEST_LOG,'Starting Iperf with args . '+' '.join(args),'INFO','a')
	p=sub.Popen(["bash","iperf_tcp_up.sh",HOME_DIR,args[0],args[1],args[2],EXP_DIR,"onetime/"+SERVER_PARAM])
	p.wait()
        logTo(TEST_LOG,'Finished Iperf ','INFO','a')
	fstat.write('Finished Iperf\n')

def run_ping(args):
        logTo(TEST_LOG,'Starting Ping with args . '+' '.join(args),'INFO','a')
        p=sub.Popen(["bash","ping.sh",HOME_DIR,args,EXP_DIR])
        p.wait()
        logTo(TEST_LOG,'Finished Ping ','INFO','a')
def run_ping_gw():
	tcptrgw=open(EXP_DIR+'/'+'ping_gw_'+time.strftime("%s"),'w')
	FNULL=open(os.devnull,'w')
	logTo(TEST_LOG,'Starting Ping Gw ','INFO','a')
	ptr=sub.Popen(["tcptraceroute","-n","-i","ppp0","-m","1","-q","50","google.com"],stdout=tcptrgw,stderr=FNULL)
	ptr.wait()
	tcptrgw.close()
        logTo(TEST_LOG,'Finished Ping Gw ','INFO','a')

def run_tcptraceroute(args):
        logTo(TEST_LOG,'Starting TCPtraceroute with args . '+' '.join(args),'INFO','a')
        p=sub.Popen(["bash","tcptraceroute.sh",HOME_DIR,args,EXP_DIR])
        p.wait()
        logTo(TEST_LOG,'Finished tcptraceroute ','INFO','a')

def run_netalyzr():
	logTo(TEST_LOG,'Starting Netalyzr ','INFO','a')
	fnet=open(EXP_DIR+'/'+'netalyzr.txt','w')
        p=sub.Popen(["java","-jar","NetalyzrCLI.jar"],stdout=fnet)
        p.wait()
        logTo(TEST_LOG,'Finished Netalyzr ','INFO','a')
	fstat.write('Finished Netalyzr\n')

def run_selenium(landmark):
	display = Display(visible=0, size=(800, 600))
	display.start()
        logTo(TEST_LOG,'Selenium : Starting Selenium  for '+landmark,'INFO','a')
	interFace=open(HOME_DIR+'/Desktop/one-time-test-suite/iface.txt','r')
	tmp=interFace.readlines()
	iface=tmp[0].split('\n')[0]
	tmpstmp=datetime.now().strftime("%s")
	profile = webdriver.FirefoxProfile()
	profile.update_preferences()
	browser = webdriver.Firefox(firefox_profile=profile) # assign profile to browser
	browser.delete_all_cookies()
	logTo(TEST_LOG,' Selenium : Starting tcpdump .. ','INFO','a')
	tcpcmd='tcpdump -i '+iface+' -w '+EXP_DIR+'/'+'tcpdump_'+landmark.split('.')[0]+'_'+tmpstmp
	args=shlex.split(tcpcmd)
	ptcpdmp=sub.Popen((args))
	time.sleep(10)
	logTo(TEST_LOG,' Selenium : Starting get '+landmark,'INFO','a')
	browser.get('http://www.'+landmark)
	time.sleep(5)
	perfData=browser.execute_script('return window.performance.timing')
	fname=EXP_DIR+'/'+'perfdata_'+landmark.split('/')[0]
	fname=fname.replace('.','-')
	pickle.dump(perfData,open(fname,'wb'))
        logTo(TEST_LOG,'Selenium : Writing done to '+EXP_DIR+'/perfdata_'+landmark,'INFO','a')
	browser.quit()
	display.stop()
	ptcpdmp.terminate()
        logTo(TEST_LOG,'Finished Selenium for '+landmark,'INFO','a')

def run_CDN():
        logTo(TEST_LOG,'Starting CDNPerf','INFO','a')
	websites=pickle.load(open('testArgs/CDNargs','rb'))
	for cdn in websites:
		for (domname,cdndomname) in websites[cdn]['Partial']:
			logTo(TEST_LOG,'CDNPerf for '+domname,'INFO','a')
			f1=open(EXP_DIR+'/'+'cdnperf_'+domname+'_'+datetime.now().strftime("%s"),'w')
			p1 = sub.Popen(['tcptraceroute', '-n', domname, '-q', '10'], stdout=f1,stderr=sub.STDOUT)
			p1.wait()
			f1.close()
			f2=open(EXP_DIR+'/'+'cdnperf_'+cdndomname+'_'+datetime.now().strftime("%s"),'w')
			p2 = sub.Popen(['tcptraceroute', '-n', cdndomname, '-q', '10'], stdout=f2,stderr=sub.STDOUT)
			p2.wait()
			f2.close()	
        logTo(TEST_LOG,'Finished CDNperf ','INFO','a')
	fstat.write('Finished CDNperf\n')

def run_ipspoof(args):
        logTo(TEST_LOG,'Starting Ipspoof with args . '+' '.join(args),'INFO','a')
	p=sub.Popen(["bash","spoofingTests.sh",HOME_DIR,args[0],args[1],EXP_DIR,"onetime/"+SERVER_PARAM])
	p.wait()
        logTo(TEST_LOG,'Finished Ipspoof ','INFO','a')
	fstat.write('Finished Ip Spoofing\n')

def run_firewall(args):
        logTo(TEST_LOG,'Starting Statefull Firewall with args . '+' '.join(args),'INFO','a')
	p=sub.Popen(["bash","firewallTests.sh",HOME_DIR,args[0],args[1],EXP_DIR,"onetime/"+SERVER_PARAM])
	p.wait()
        logTo(TEST_LOG,'Finished Statefull Firewall ','INFO','a')
	fstat.write('Finished Statefull Firewall\n')

def run_buffer(args,srate1,srate2):
        logTo(TEST_LOG,'Starting Downlink Buffer with args . '+' '.join(args),'INFO','a')
	#logTo(TEST_LOG,HOME_DIR+' '+args[0]+' '+args[1]+' '+EXP_DIR+' '+"onetime/"+SERVER_PARAM+' '+str(srate1)+' '+str(srate2),'INFO','a')
	p=sub.Popen(["bash","downlinkBuffer.sh",HOME_DIR,args[0],args[1],EXP_DIR,"onetime/"+SERVER_PARAM,str(srate1),str(srate2)])
	p.wait()
	logTo(TEST_LOG,'Finished DownlinkBuffer ','INFO','a')
	logTo(TEST_LOG,'Starting Uplink Buffer with args . '+' '.join(args),'INFO','a')
	p=sub.Popen(["bash","uplinkBuffer.sh",HOME_DIR,args[0],args[1],EXP_DIR,"onetime/"+SERVER_PARAM,str(srate1),str(srate2)])
	p.wait()
        logTo(TEST_LOG,'Finished UplinkBuffer ','INFO','a')
	fstat.write('Finished Buffer\n')

def setconfig():
	config=open('Dialer','r')
	configmain=open('Dialermain','w')
	lines=config.readlines()
	for line in lines:
		configmain.write(line)
	configmain.write('\n[Dialer getisp]\n')
	devs=commands.getoutput('ls -1 /dev/ttyUSB*').split('\n')
	configmain.write('Modem = '+devs[2]+'\nInit1 = AT+COPS?\n')
	config.close()
	configmain.close()

def DoDial():	
	setconfig()
	dialout=open('dialout','w')
	p=sub.Popen(['sudo','wvdial','getisp','--config','Dialermain'],stdout=dialout,stderr=sub.STDOUT)
	p.wait()
	dialout.close()
	dialout=open('dialout','r')
	lines=dialout.readlines()
	for line in lines:
		if "+COPS: " in line:
			isp=line.split('\"')[1]
			break
	print isp
	fwvdial=open('wvdial_'+isp,'w')
	p=sub.Popen(['sudo','wvdial',isp,'--config','Dialermain'],stdout=fwvdial,stderr=sub.STDOUT)
	p.wait()
	fwvdial.close()
	



def runMaster(options):
	#TODO
	location='-'.join(options['L'])
	provider='-'.join(options['P'])
	contype='-'.join(options['C'])
	#DoDial()
	#sys.exit(0)
	#pdial=sub.Popen(["sudo","python","dial.py"])
	ifup=0
	while ifup!=1:
		try:
        		ip=netinfo.get_ip('ppp0')
			ifup=1
		except Exception as e:
			print "here"
			ifup=0
        ipf=open('ip.txt','w')
        ipf.write(ip)
        ipf.close()
        iperfport=open('iperf_port.txt','w')
        iperfport.write(str(random.randint(1500,10000)))
        iperfport.close()
	global EXP_DIR
        global SERVER_PARAM
        #print type(options['r'])
        timestamp=time.strftime('%s')
        if options['r']==None:
                #Adding Roaming  Test
                EXP_DIR=EXP_DIR+location+'_'+provider+'_'+contype+'/'+timestamp
                SERVER_PARAM=hostname+'/'+location+'_'+provider+'_'+contype+'/'+timestamp
	else:
		EXP_DIR=EXP_DIR+location+'_'+provider+'_'+contype+'/Roam/'+'_'.join(options['r'])+'_'+timestamp
                SERVER_PARAM=hostname+'/'+location+'_'+provider+'_'+contype+'/Roam/'+timestamp
	if options['re']!=None:
		EXP_DIR=options['re'][0]
		SERVER_PARAM=options['re'][1]
	if not os.path.exists(EXP_DIR):
		os.makedirs(EXP_DIR)
	fstat.write('Resume Args:\n 1.'+EXP_DIR+'\n'+'2.'+SERVER_PARAM+'\n')
	sigdict={}
	pickle.dump(sigdict,open(EXP_DIR+"/sigdict",'wb'))
	psigstr=sub.Popen(["python","sigstr.py","GSM",EXP_DIR])
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
	if options['l']:
		#Adding Latency Tests
                fping=open('testArgs/ping','r')
                lines=fping.readlines()
                lines=[x.split('\n')[0] for x in lines]
		if contype=='3g':
			pping=sub.Popen(["ping","-s","512","-n","106.187.35.87"])
		for line in lines:
			run_ping(line)
		fping.close()
		run_ping_gw()
		pping.terminate()
		fstat.write('Finished Latency\n')
	if options['T']:
		#Addding Tcptraceroute tests
		ftr=open('testArgs/tcptraceroute','r')
                lines=ftr.readlines()
                lines=[x.split('\n')[0] for x in lines]
		if contype=='3g':
			pping=sub.Popen(["ping","-s","512","-n","106.187.35.87"])
                for line in lines:
                        run_tcptraceroute(line)
                ftr.close()
		pping.terminate()
		fstat.write('Finished Tcptraceroute\n')
	if options['n']:
		#Adding ICSI Netalyzr Test
                run_netalyzr()
	if options['p']:
		#Adding PLT Selenium Test
                fplt=open('testArgs/selenium','r')
                lines=fplt.readlines()
                lines=[x.split('\n')[0] for x in lines]
                for line in lines:
                        run_selenium(line)
                fplt.close()
		fstat.write('Finished Selenium\n')
        if options['c']:
                #Adding CDN performance Test
		if contype=='3g':
			pping=sub.Popen(["ping","-s","512","-n","106.187.35.87"])
                run_CDN()
		pping.terminate()
        if options['i']:
                #Adding IP Spoofing  Test
                fipspoof=open('testArgs/ipspoof','r')
                lines=fipspoof.readlines()
                lines=[x.split('\n')[0] for x in lines]
                if argsFine(lines,'ipspoof'):
                	run_ipspoof(lines)
		else:
                        logTo(TESTSUITE_LOG,'Error in parsing Ipsoof args Missing or wrong Args in testArgs/ipspoof','ERROR','w')
                        sys.exit('Error! Check suite.log for more details...')
                fipspoof.close()
        if options['s']:
                #Adding Statefull Firewall Test
                ffire=open('testArgs/firewall','r')
                lines=ffire.readlines()
                lines=[x.split('\n')[0] for x in lines]
                if argsFine(lines,'firewall'):
                	run_firewall(lines)
		else:
                        logTo(TESTSUITE_LOG,'Error in parsing Iperf args Missing or wrong Args in testArgs/firewall','ERROR','w')
                        sys.exit('Error! Check suite.log for more details...')
                ffire.close()
        if options['b']:
                #Adding Buffer Size Test
		fbuff=open('testArgs/buffer','r')
                lines=fbuff.readlines()
                lines=[x.split('\n')[0] for x in lines]
		if contype=='3g':
			srate1=1000
			srate2=2000
		else:
			srate1=200
			srate2=250
                if argsFine(lines,'buffer'):
                	run_buffer(lines,srate1,srate2)
		else:
                        logTo(TESTSUITE_LOG,'Error in parsing Buffer args Missing or wrong Args in testArgs/buffer','ERROR','w')
                        sys.exit('Error! Check suite.log for more details...')
                fbuff.close()
	psigstr.terminate()
	#pdial.terminate()


def main():
	parser = argparse.ArgumentParser(description='process ruralnetOneTime arguments')
	parser.add_argument('-t',action='store_true',help='Run Throughput Test')
        parser.add_argument('-l',action='store_true',help='Run Latency Test')
        parser.add_argument('-T',action='store_true',help='Run Traceroute Test')
        parser.add_argument('-i',action='store_true',help='Run Ip spoofing Test')
        parser.add_argument('-s',action='store_true',help='Run Statefull Firewall Test')
        parser.add_argument('-n',action='store_true',help='Run ICSI Netalyzr Test')
        parser.add_argument('-r',nargs='*',help='Run Roaming Test')
        parser.add_argument('-p',action='store_true',help='Run Page Load Time Test')
        parser.add_argument('-c',action='store_true',help='Run CDN performance Test')
        parser.add_argument('-b',action='store_true',help='Run Buffer Size Test')
	parser.add_argument('-L',nargs='+',help='Locaton of Test being conducted',required=True)
	parser.add_argument('-P',nargs='+',help='Provider of Test being conducted',required=True)
	parser.add_argument('-C',nargs='+',help='Connection type of Test being conducted 3g/edge/evdo',required=True)
	parser.add_argument('-re',nargs='+',help='Resume the tests that did not complete due to disconnections ')
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

