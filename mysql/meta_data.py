import os
from socket import *
from mds_db import *
from mdsConf import mds_HOST, mds_PORT, BASE_DIR
import json

# Create an object of type mds_db
db = mds_db()

s = socket(AF_INET,SOCK_DGRAM)    # Create the server socket UDP protocol
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Allow socket to be reused
s.bind((mds_HOST,mds_PORT))  # Bind the server on mds_PORT 

print "Connecting to database..." 
db.Connect()

'''Create directory for files in project base path'''
try:
    os.makedirs(os.path.join(BASE_DIR, 'dfs-files'))
    dfsDir = os.path.join(BASE_DIR, 'dfs-files' )
except OSError as error:
	pass

while True:
	# Accept connections from nodes and clients on socket
	message = 'recibido'
	recievedMsg,address = s.recvfrom(1024)
	s.sendto(message,address)
s.close()
