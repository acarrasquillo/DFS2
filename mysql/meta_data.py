from mdsConf import *

# Create an object of type mds_db
db = mds_db()
print "Connecting to database..." 
db.Connect()

'''Set up server'''
s = socket(AF_INET,SOCK_STREAM)    # Create the server socket TCP protocol
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind((mds_HOST,mds_PORT))  # Bind the server on mds_PORT
s.listen(1) 
'''Create directory for files in project base path'''
   
while True:
	'''Accept connections on mds'''
	conn,address = s.accept()
	# Accept connections from nodes and clients on socket
	recievedMsg = conn.recv(1024)
	msg = recievedMsg.split(' ')
	print msg
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
	# 	db.AddBlockToInode("/hola/cheo.txt", [("n0", 1), ("n1", 1)])
	conn.send(message) #Send message	
	conn.close() #Close connection

s.close() 