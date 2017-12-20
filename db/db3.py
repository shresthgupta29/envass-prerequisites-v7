import os
import shutil
import subprocess
from subprocess import Popen, PIPE
from config import *
os.putenv('ORACLE_HOME',oracle_home)

try:
	os.chdir(oracle_home+'/bin')
except OSError as err:
	print(err)
	exit()
netca = raw_input("Did your run db1.py (y/n) ?\n")
if netca=='y':
	subprocess.call('./netca -silent -responseFile '+client_path+'/response/netca.rsp',shell=True)
else:
	print("Listener already configured")	

try:
	os.chdir(oracle_home+'/bin')
except OSError as err:
	print(err)
	exit()

try:
	subprocess.call('./dbca -silent -deleteDatabase -sourceDB '+cdb+' -sysDBAUserName sys -sysDBAPassword '+admin_pass,shell=True)
	subprocess.call('./dbca -silent -createDatabase -templateName General_Purpose.dbc -gdbName '+cdb+' -sid '+cdb+' -createAsContainerDatabase true -numberOfPDBs 1 -pdbName '+pgdb+' -pdbAdminPassword '+admin_pass+' -sysPassword '+admin_pass+' -systemPassword '+admin_pass+' -emConfiguration NONE -storageType FS -datafileDestination '+oracle_home+'/oradata -characterSet AL32UTF8 -nationalCharacterSet UTF8 -automaticMemoryManagement true -redoLogFileSize 100',shell=True)
except OSError as e:
	print("DB Creation error :")
	print (e)
	exit()
print('DB Create successfully\n')
try:
	os.chdir(oracle_home+'/network/admin')
	tnsnames = open("tnsnames.ora", "r")
except OSError as e:
	print(e)
	exit()
count=0
line = tnsnames.readline()
while not (line.strip().startswith('(ADDRESS')):
	print(line)
	count=count+1
	line=tnsnames.readline()
	if(count>50):
		break

print(line)
x= len(line)
port = line[x-7:-3]
print port
tnsnames.close()

with open("tnsnames.ora", "a") as myfile:	
    myfile.write("\n\n"+pgdb.upper()+" =\n  (DESCRIPTION =\n    (ADDRESS = (PROTOCOL = TCP)(HOST = "+host+")(PORT = "+port+"))\n    (CONNECT_DATA =\n      (SERVER = DEDICATED)\n      (SERVICE_NAME = "+pgdb+")\n    )\n  )")

try:
	os.chdir(oracle_home+'/network/admin')
	tnsnames = open("tnsnames.ora", "r")
except OSError as e:
	print(e)
	exit()

line = tnsnames.readline()
#while True:
#	line=tnsnames.readline()
#	print (line)
#	if "PORT" in line:
#		break;
#x= len(line)
#port = line[x-7:-3]
tnsnames.close()
#print ("Database setup done......{}.....at port{}".format(cdb,port))


conn = 'sys/'+admin_pass+'@'+cdb+' as sysdba'
session = subprocess.Popen([oracle_home+'/bin/sqlplus', '-S', conn], stdin=PIPE, stdout=PIPE, stderr=PIPE)
session.stdin.write('ALTER SYSTEM SET open_cursors=2000 SCOPE=BOTH;')
(stdout,stderr)=session.communicate()
print stdout

conn = 'sys/'+admin_pass+'@'+cdb+' as sysdba'
session = subprocess.Popen([oracle_home+'/bin/sqlplus', '-S', conn], stdin=PIPE, stdout=PIPE, stderr=PIPE)
session.stdin.write('alter system set processes=2000 scope=spfile;')
(stdout,stderr)=session.communicate()
print stdout


conn = 'sys/'+admin_pass+'@'+cdb+' as sysdba'
session = subprocess.Popen([oracle_home+'/bin/sqlplus', '-S', conn], stdin=PIPE, stdout=PIPE, stderr=PIPE)
session.stdin.write('@'+oracle_home+'/rdbms/admin/xaview;')
(stdout,stderr)=session.communicate()
print stdout


conn = 'sys/'+admin_pass+'@'+cdb+' as sysdba'
session = subprocess.Popen([oracle_home+'/bin/sqlplus', '-S', conn], stdin=PIPE, stdout=PIPE, stderr=PIPE)
session.stdin.write('grant select on v$pending_xatrans$ to sys;')
(stdout,stderr)=session.communicate()
print stdout


conn = 'sys/'+admin_pass+'@'+cdb+' as sysdba'
session = subprocess.Popen([oracle_home+'/bin/sqlplus', '-S', conn], stdin=PIPE, stdout=PIPE, stderr=PIPE)
session.stdin.write('grant select on v$xatrans$ to sys;')
(stdout,stderr)=session.communicate()
print stdout

conn = 'sys/'+admin_pass+'@'+cdb+' as sysdba'
session = subprocess.Popen([oracle_home+'/bin/sqlplus', '-S', conn], stdin=PIPE, stdout=PIPE, stderr=PIPE)
session.stdin.write('commit;')
(stdout,stderr)=session.communicate()
print stdout

conn = 'sys/'+admin_pass+'@'+cdb+' as sysdba'
session = subprocess.Popen([oracle_home+'/bin/sqlplus', '-S', conn], stdin=PIPE, stdout=PIPE, stderr=PIPE)
session.stdin.write("select limit from dba_profiles where resource_name='PASSWORD_VERIFY_FUNCTION' and profile='DEFAULT';")
(stdout,stderr)=session.communicate()
print stdout

conn = 'sys/'+admin_pass+'@'+cdb+' as sysdba'
session = subprocess.Popen([oracle_home+'/bin/sqlplus', '-S', conn], stdin=PIPE, stdout=PIPE, stderr=PIPE)
session.stdin.write('alter profile default limit PASSWORD_VERIFY_FUNCTION null;')
(stdout,stderr)=session.communicate()
print stdout

####################################################################################################################
conn = 'sys/'+admin_pass+'@'+pgdb+' as sysdba'
session = subprocess.Popen([oracle_home+'/bin/sqlplus', '-S', conn], stdin=PIPE, stdout=PIPE, stderr=PIPE)
session.stdin.write('ALTER SYSTEM SET open_cursors=2000 SCOPE=BOTH;')
(stdout,stderr)=session.communicate()
print stdout

conn = 'sys/'+admin_pass+'@'+pgdb+' as sysdba'
session = subprocess.Popen([oracle_home+'/bin/sqlplus', '-S', conn], stdin=PIPE, stdout=PIPE, stderr=PIPE)
session.stdin.write('alter system set processes=2000 scope=spfile;')
(stdout,stderr)=session.communicate()
print stdout


conn = 'sys/'+admin_pass+'@'+pgdb+' as sysdba'
session = subprocess.Popen([oracle_home+'/bin/sqlplus', '-S', conn], stdin=PIPE, stdout=PIPE, stderr=PIPE)
session.stdin.write('@'+oracle_home+'/rdbms/admin/xaview;')
(stdout,stderr)=session.communicate()
print stdout


conn = 'sys/'+admin_pass+'@'+pgdb+' as sysdba'
session = subprocess.Popen([oracle_home+'/bin/sqlplus', '-S', conn], stdin=PIPE, stdout=PIPE, stderr=PIPE)
session.stdin.write('grant select on v$pending_xatrans$ to sys;')
(stdout,stderr)=session.communicate()
print stdout


conn = 'sys/'+admin_pass+'@'+pgdb+' as sysdba'
session = subprocess.Popen([oracle_home+'/bin/sqlplus', '-S', conn], stdin=PIPE, stdout=PIPE, stderr=PIPE)
session.stdin.write('grant select on v$xatrans$ to sys;')
(stdout,stderr)=session.communicate()
print stdout

conn = 'sys/'+admin_pass+'@'+pgdb+' as sysdba'
session = subprocess.Popen([oracle_home+'/bin/sqlplus', '-S', conn], stdin=PIPE, stdout=PIPE, stderr=PIPE)
session.stdin.write('commit;')
(stdout,stderr)=session.communicate()
print stdout

conn = 'sys/'+admin_pass+'@'+pgdb+' as sysdba'
session = subprocess.Popen([oracle_home+'/bin/sqlplus', '-S', conn], stdin=PIPE, stdout=PIPE, stderr=PIPE)
session.stdin.write("select limit from dba_profiles where resource_name='PASSWORD_VERIFY_FUNCTION' and profile='DEFAULT';")
(stdout,stderr)=session.communicate()
print stdout

conn = 'sys/'+admin_pass+'@'+pgdb+' as sysdba'
session = subprocess.Popen([oracle_home+'/bin/sqlplus', '-S', conn], stdin=PIPE, stdout=PIPE, stderr=PIPE)
session.stdin.write('alter profile default limit PASSWORD_VERIFY_FUNCTION null;')
(stdout,stderr)=session.communicate()
print stdout
#########################################################################################################################

conn = 'sys/'+admin_pass+'@'+cdb+' as sysdba'
session = subprocess.Popen([oracle_home+'/bin/sqlplus', '-S', conn], stdin=PIPE, stdout=PIPE, stderr=PIPE)
session.stdin.write('shutdown immediate;')
(stdout,stderr)=session.communicate()
print stdout

os.putenv('ORACLE_SID',cdb)
os.chdir(oracle_home+'/bin')
try:
	session = subprocess.Popen([oracle_home+'/bin/sqlplus', '/ as sysdba'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
except OSError as e:
	print(e)
	exit()	
session.stdin.write('startup;');
res = session.communicate()
print res[0]

conn = 'sys/'+admin_pass+'@'+cdb+' as sysdba'
session = subprocess.Popen([oracle_home+'/bin/sqlplus', '-S', conn], stdin=PIPE, stdout=PIPE, stderr=PIPE)
session.stdin.write('ALTER PLUGGABLE DATABASE '+pgdb+' OPEN;')
(stdout,stderr)=session.communicate()
print stdout



