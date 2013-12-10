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
# 	" Usage : python metadata.py"
# 	
##############################################################\
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
	msg = recievedMsg.split('|')
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
	
	elif msg[0] =='3':
		'''This command is for saving a file and inodes in db'''
		
		print "Saving filepath and inodes in DB"
		data = msg[1] # Jason Data
		
		print "Message recieved:\n Command: 3 \n Data:%s" %data

		'''Decode the jason string'''
		data = json.loads(data)

		'''Get the data in the json and format it to query the db'''

		dfsFilepath = data['filepath'][0] #path of the file in the dfs
		fileSize = int(data['filepath'][1])
		inodes = []
		for tl in data['inodes']:
			node = tl[0]
			chunkId = int(tl[1])
			inodes.append((node,chunkId))


		print "Recieved\n Filepath: %s,Size: %s \n inodes: %s" %(dfsFilepath,fileSize,inodes) # print data recieved
		
		'''Try save the file  in the db with the inodes info'''

		try:
			db.InsertFile(dfsFilepath,fileSize) #insert file in db
			db.AddBlockToInode(dfsFilepath,inodes)
			message = 'Filepath and inodes saved in MDS' # message to answer back
		except 0:
			print "Can't save the file %s file path exist on db" %dfsFilepath
			message = 'False'

		'''Test the file and inode info'''
		if message != 'False':
			
			print "Testing retreiving Inode info"
			
			fsize, chunks_info = db.GetFileInode(dfsFilepath)
			
			print "File Size is:", fsize
			
			print "and can be constructed from: "
			
			for  node, address, port, chunk in chunks_info:
				print node, address, port, chunk

	elif msg[0] == '4':

		dfs_filepath = msg[1] # get the dsf file path

		try:
			fileid, fsize = db.GetFileInfo(dfs_filepath)
		except:
			fileid = None 

		if fileid == None:
		 	print 'File doesn\'t exists in the DFS'
		 	message = 'False'

		else :
			'''Send the file inodes to the client'''
			inode = []

			print "Testing retreiving Inode info"
			
			fsize, chunks_info = db.GetFileInode(dfs_filepath)
			
			print "File Size is:", fsize
			
			print "and can be constructed from: "
			
			for  node, address, port, chunk in chunks_info:
				print node, address, port, chunk
				k,v = node,(address,port,chunk)
				inode.append((k,v))
				data = json.dumps(dict(inode))
				message = data



	
	'''Respond to the recieved connection and close the socket'''	
	conn.sendall(message) #Send message	
	conn.close() #Close connection

s.close() 