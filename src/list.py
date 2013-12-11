##############################################################
#	DFS
#	
#	Project: Distributed File System
#	University of Puerto Rico, Rio Piedras Campus
#   Dept. of Computer Science
#   CCOM 4017: Operating Systems - Fall'13
#   
#   Instructor: 
#       Jose Ortiz-Ubarri
#                           
#   Group:
#       Roxana Gonzalez (xxx-xx-xxxx)
#       Miguel Roque (xxx-xx-xxxx)
#       Abimael Carrasquillo Ayala (xxx-xx-xxxx)
#	
#	This command list all the files and size that exist in the DFS
# 	
# 	" Usage : python list.py <metadata host>"
# 	
##############################################################\


from mdsConf import mds_PORT
from mds_db import *
from socket import *
import json
import sys

try:
    HOST= sys.argv[1]
except:
	raise SystemExit(" Usage :  python list.py <meta data server ip-address>")

mds_HOST = sys.argv[1]
s = socket(AF_INET,SOCK_STREAM)    # Create the server socket TCP protocol
s.connect((mds_HOST,mds_PORT))
'''Send message to metadata server''' 
message = "1"
s.send(message)
'''Recieve message'''
recievedMsg = s.recv(1024)
'''Close Socket'''
s.close()
try: 
	d = json.loads(recievedMsg)
	for i in d:
		print i['File'] + " " + i['Size'] 
except:
	print "There are no files in the database"