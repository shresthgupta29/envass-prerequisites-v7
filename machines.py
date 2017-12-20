HA = 0			#put HA = 1 for HA environment and 0 for Non_HA

IDM_NodeA= ["10.120.0.4","10.75.35.90"]   #Internal IP,External IP
App01_NodeA = ["10.120.0.3","10.75.35.81"]
App02_NodeA = ["10.120.0.6","10.75.35.89"]

IDM_NodeB = ["10.120.0.5","10.120.0.5"]
App01_NodeB = ["10.120.0.2","10.75.35.137"]
App02_NodeB = ["10.120.0.8","10.75.35.137"]
App03_NodeB = ["10.120.0.4","10.75.35.137"]

nfs='10.120.0.5' #internal ip of nfs

db=["10.120.0.2","10.75.35.87"] #Internal IP,External IP

zip_path = "" #path of the chefToolkit with the file itself Example : "/u02/app_files/PrimeeraXXXXXXXXXX.zip"  

m_list1 = [IDM_NodeA[0],IDM_NodeB[0],App01_NodeA[0],App01_NodeB[0],App02_NodeA[0],App02_NodeB[0]]
m_list2  = [IDM_NodeA[0],App01_NodeA[0],App02_NodeA[0]]
