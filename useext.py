from selenium import webdriver
from datetime import datetime
from pyvirtualdisplay import Display
import time
import sys
from os import rename
import shlex
import subprocess as sub
import commands
import pickle
display = Display(visible=0, size=(800, 600))
display.start()
import logging



def main(homedir,tmpst,landmark,op,logdir):
	expdir=logdir+'/'
	interFace=open('MultipleDongles/tmp/p'+op+'.txt','r')
	tmp=interFace.readlines()
	iface=tmp[0].split('\n')[0]
	tmpstmp=datetime.now().strftime("%s")
	profile = webdriver.FirefoxProfile()
	#profile.add_extension(extension="firebug-1.13.0a1.xpi")
	#profile.add_extension(extension="netExport.xpi")
	#profile.set_preference("app.update.enabled", False)
	#profile.set_preference("extensions.firebug.currentVersion", "1.13.0")
	#profile.set_preference("extensions.firebug.allPagesActivation", "on")
	#profile.set_preference("extensions.firebug.defaultPanelName", "net")
	#profile.set_preference("extensions.firebug.net.enableSites", True)
	#profile.set_preference("extensions.firebug.netexport.alwaysEnableAutoExport", True)
	#profile.set_preference("extensions.firebug.netexport.Automation", True)
	#profile.set_preference("extensions.firebug.netexport.showPreview", False)
	#profile.set_preference("extensions.firebug.netexport.defaultLogDir", expdir)
	profile.update_preferences()
	logging.info(homedir+','+expdir+','+landmark+','+op)
	logging.info('Starting firefox_profile..')
	browser = webdriver.Firefox(firefox_profile=profile) # assign profile to browser
	browser.delete_all_cookies()
	logging.info('Starting tcpdump')
	tcpcmd='sudo tcpdump -i '+iface+' -w '+expdir+'tcpdump_'+landmark.split('.')[0]+'_'+tmpstmp
	args=shlex.split(tcpcmd)
	p=sub.Popen((args))
	time.sleep(10)
	#a=[x.split(' ')[1] for x in commands.getoutput('ps aux | grep [t]cpdump | tr -s \' \'').split('\n')]
	# print datetime.now().strftime("%s")
	logging.info('Starting get '+landmark)
	browser.get('http://www.'+landmark)
	time.sleep(5)
	perfData=browser.execute_script('return window.performance.timing')
	if landmark=='disneyworld.disney.go.com/new-fantasyland/':
		fname=expdir+'perfdata_'+landmark.split('/')[0]
	else:
		fname=expdir+'perfdata_'+landmark
	pickle.dump(perfData,open(fname,'wb'))
	logging.info('writing done to '+expdir+'perfdata_'+landmark)
	#browser.set_page_load_timeout(300)
	#try:
	#	browser.get('http://www.'+landmark)
	# let HAR export
	#except Exception:
	#	pass
	logging.info("sleeping....")
	logging.info("quiting..")
	browser.quit()
	display.stop()
	p.terminate()



if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=sys.argv[5]+'/selenium.log',
                    filemode='w')
	logging.info('Starting main... for'+sys.argv[3])
	main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])

