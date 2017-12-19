import os
import subprocess
from subprocess import Popen, PIPE
from machines import *


if(HA):
	print("HA Environmet")
	mlist=m_list1
else:
	print("Non-HA Environment")
	mlist=m_list2

print (mlist)


os.chdir('/etc')
if os.path.isfile('/etc/exports'):
	print("Editing /etc/exports")
else:
	subprocess.call("touch exports",shell=True)
	print("Created exports....Editing exports")

try:	
	with open('/etc/exports','r') as myfile:
		lines=myfile.read()

	if(lines.find('/u02 '+mlist[0]+'(rw,sync,no_root_squash)')+1):
		print("/etc/exports already edited")
	else:
		with open('/etc/exports','a') as myfile:
			print("Editing exports file")
			for m in mlist:
				myfile.write('/u02 '+m+'(rw,sync,no_root_squash)\n')
except OSError as e:
	print (e)
	exit()

try:
	subprocess.call('service nfs restart',shell=True)
	subprocess.call('service nfs status',shell=True)
except OSError as e:
	print (e)
	exit()


print("Copy the command and run in all the nodes-- IDM, App01,App02,App03\n\nmount -t nfs "+nfs+":/u02 /u02\n\n")