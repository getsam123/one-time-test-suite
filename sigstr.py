import subprocess as sub
import sys
import pickle
import time
EXP_DIR=sys.argv[2]
while True:
	sigdict=pickle.load(open(EXP_DIR+"/sigdict",'rb'))
	timestmp=time.strftime("%s")
	tmp=open('sigtmp','w')
	p=sub.Popen(["sudo","wvdial","SIGSTR"+sys.argv[1],"--config","Dialer"],stdout=tmp,stderr=sub.STDOUT)
	p.wait()
	tmp.close()
	tmp=open('sigtmp','r')
	lines=tmp.readlines()
	for line in lines:
		line=line.strip()
		if "CSQ:" in line:
			sig=line.split()[1].split(',')[0]
		if "CGREG:" in line:
			k=line.split()
			cid=''.join(k[-2:])
		if "COPS:" in line:
			opr=line.split(',')[-1:][0]
			prov=line.split(',')[-2:][0].replace('"','')
		if "SYSINFO:" in line:
			typ=line.split(',')[-1:][0]
	#TODO
	sigdict[timestmp]=(sig,cid,opr,prov,typ)
	pickle.dump(sigdict,open(EXP_DIR+"/sigdict",'wb'))
	time.sleep(10)
