import os
cwd = os.getcwd()  #/current working directory
#java_home='/scratch/jdk1.8.0_144/'
oracle_home = '/u01/app/oracle/product/12.1.0/dbhome_1'
oracle_base = '/u01/app/oracle' 
host = '10.120.0.2' #host name of current machine
client_path = cwd+'/database' # path of 'database' folder containing 'runInstaller.sh'
admin_pass='Manager1' # password for sys/system/admin accounts
cdb = 'testdb3' #container db name
pgdb = 'pdbtest3'
