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
	recievedMsg, address = s.recvfrom(1024)
	msg = recievedMsg.split()
	# print msg
	if msg[0]=='0':
		print "Nodo Reportandose"

		node = msg[1]
		nodeHost = msg[2]
		nodePort = msg[3]
		db.AddDataNode(node, nodeHost, nodePort)
		print "Testing if node was inserted"
		print db.CheckNode(node)
		print "Testing all Available data nodes"
		for name, addr, port in  db.GetDataNodes():
			print name, addr, port
		message = 'Nodo Reportado'
	elif msg[0]=='1':
		print "List Command"

		message = '['
		#gather all the files and their size and display them
		print db.GetFiles()
		for data in db.GetFiles():
			message = message + '{ "File":"' + data[0]+'", "Size":"'+str(data[1])+'"},'
		message = message[0:len(message)-1] +']'
	elif msg[0] == '2':
		print "Command write"

		'''Answer with Available Data Nodes'''
		nodesList = [] # List of datanodes

		''''Message client a json with the list of nodes available'''
		for name, addr, port in  db.GetDataNodes():
			nodesList.append((name,(addr,port)))

		'''Add to the message the available nodes #'''	
		if len(nodesList) == 0:
			nodesList.append(('msg',0))
		else:
			nodesList.insert(0,('msg',len(nodesList)))

		''''Convert data to json format'''	
		message = json.dumps(dict(nodesList))
	# elif msg[0] =='3':
	s.sendto(message,address)
s.close()
