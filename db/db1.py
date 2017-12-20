import os
import subprocess
from subprocess import Popen, PIPE
from config import *
os.putenv('ORACLE_HOME',oracle_home)

cwd = os.getcwd()
print("At "+cwd)

try:
    subprocess.call('rm -rf /u01/app/oraInventory/',shell=True)
    subprocess.call('wget http://slc06uwv.us.oracle.com/ChefSoftware/Software/Common/Database/12c/12.1.0.2/V46095-01_1of2.zip',shell=True)
    subprocess.call('wget http://slc06uwv.us.oracle.com/ChefSoftware/Software/Common/Database/12c/12.1.0.2/V46095-01_2of2.zip',shell=True)
    subprocess.call('unzip V46095-01_1of2.zip',shell=True)
    subprocess.call('unzip V46095-01_2of2.zip',shell=True)
except OSError as e:
        print(e)
        exit()

try:
        os.chdir(client_path)
except OSError as err:
        print(err)
        exit()

try:
    subprocess.call('./runInstaller -silent -responseFile '+client_path+'/response/db_install.rsp -showProgress -ignorePrereq -ignoreSysPrereqs -waitforcompletion  oracle.install.option=INSTALL_DB_SWONLY UNIX_GROUP_NAME=dba INVENTORY_LOCATION=/u01/app/oraInventory SELECTED_LANGUAGES=en ORACLE_HOME='+oracle_home+' ORACLE_BASE='+oracle_base+' oracle.install.db.InstallEdition=EE oracle.install.db.isCustomInstall=false oracle.install.db.DBA_GROUP=dba oracle.install.db.OPER_GROUP=dba oracle.install.db.BACKUPDBA_GROUP=dba oracle.install.db.DGDBA_GROUP=dba oracle.install.db.KMDBA_GROUP=dba  SECURITY_UPDATES_VIA_MYORACLESUPPORT=false DECLINE_SECURITY_UPDATES=true', shell=True)
except OSError as err:
    print(err)
    exit()      
    
print "Run script db2.py with root privilages"
