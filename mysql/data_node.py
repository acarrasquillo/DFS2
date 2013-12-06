
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
#	The data node is the process that does receive and saves the chunks of information of the files. 
#	It must register with the metadata server as soon as it starts its execution.
# 	The data node also receives the data from the clients when the client wants to write a file, and 
# 	returns the data when the client wants to read a file.
# 	
# 	" Usage : ./data_node <port> <name of chunk directory>"
# 	
##############################################################\

from mdsConf import mds_PORT, mds_HOST, BASE_DIR
import sys
import os
from socket import *


HOST = 'localhost'

try:
    port = int(sys.argv[1])
    path = sys.argv[2]
except:
    raise SystemExit(" Usage : ./data-node <port> <name of chunk directory>")

try:
    os.makedirs(os.path.join(BASE_DIR, path))
    chunkDir = os.path.join(BASE_DIR, path)
except:
	pass

s = socket(AF_INET,SOCK_STREAM)    # Create the server socket TCP protocol
s.connect((mds_HOST,mds_PORT))
'''Mensaje'''
message = "0 %s %s %s" % (path,HOST,port)
s.send(message)
answer = s.recv(1024)
s.close()
print answer                                                                                                                                                                                                                                                                                           

while True:
	# Accept connections from nodes and clients on socket
	conn, addr = s.accept()
	recievedMsg = conn.recv(1024)
	print recievedMsg

s.close()