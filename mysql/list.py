from mdsConf import mds_PORT, mds_HOST
from mds_db import *
from socket import *
import json
import sys

try:
    HOST= sys.argv[1]
except:
	raise SystemExit(" Usage :  python list.py <meta data server ip-address>")

mds_HOST = sys.argv[1]
s = socket(AF_INET,SOCK_DGRAM) # Create the node socket UDP protocol
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Allow socket to be reused
s.bind((HOST,1002)) # Bind node on server <port>

# Send message to metadata server 
message = "1"
s.sendto(message,("localhost",mds_PORT))

while True:
	# Accept connections from nodes and clients on socket
	recievedMsg,address = s.recvfrom(1024)
	msj = recievedMsg
	break
s.close()
d = json.loads(msj)
for i in d:
	print i['File'] + " " + i['Size'] 