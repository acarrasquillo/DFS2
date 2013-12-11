##############################################################
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
# command must:
# 		1. Write a file in the DFS
# 			a. Your client must send the data server the path, filename, and size of the file to write.
# 			b. After receiving the available data nodes the client must send to the data nodes the chunks of the file in round robin fashion.
# 		2. Read a file from the DFS
# 			a. Your client must contact the data server with the filename and wait for the nodes information returned by the metadata server.
# 			b. The client must then retrieve the information from the data nodes.        
#   
# 		usage:
# 			Copy from computer to DFS:
# 				python kopy.py <path of the file> <metadata-server-ip-address:path on the DFS> 
# 				
# 			Copy from DFS to computer:
# 				python kopy.py <metadata-server-ip-address:path on the DFS> <path of the file> 
##############################################################
'''Copy Command'''
from mdsConf import * 
import sys

try:
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
except:
    raise SystemExit("Usage:\n"
    					 + "Copy from computer to DFS:\n" 
    					 + "python copy <path of the file> <metadata-server-ip-address:path on the DFS>\n\n"
    					 + "Copy from DFS to computer:\n"
    					 + "python copy <metadata-server-ip-address:path on the DFS> <path of the file>"
    					 )

'''If argument 2 is an ip
   Copy from computer to DFS (write)'''

if validateIP(arg2.split(':')[0]):
	
	''' Argument 2 is the IP
	    Make Copy from computer to DFS (write) '''

	mds_HOST = arg2.split(':')[0] # DFS Host
	

	s = socket(AF_INET,SOCK_STREAM)    # Create the server socket TCP protocol
	s.connect((mds_HOST,mds_PORT))
	dfs_filePath = arg2.split(':')[1] # Path of the file in the dfs
	comp_filePath = arg1 #Path of the file in the computer
	message = "2"
	s.send(message)
	
	'''Accept connections from DFS and Nodes on socket'''
	
	recievedMsg = s.recv(1024)
	data = json.loads(recievedMsg)
	availNodes = data
	msg = data.pop('msg')
	s.close()
	if msg == 0:
		raise SystemExit("Can't write a file there are no nodes available")

	print "There are " + str(msg) + " nodes available"
	
	'''Split the file in n chunks, n=#nodes
	   Send chunk n to node n '''

	noOfNodes = msg
	chunksFiles = makeChunks(comp_filePath,noOfNodes)
	chunks = chunksFiles[0]
	fileSize = chunksFiles[1]

	
	'''Copying chunks to nodes'''
	
	result = sendChunks(data,chunks,dfs_filePath,fileSize)
	message = '3|'+result # add the command to the jason message

	'''If the function returned False raise error'''
	
	if result == False:
		raise SystemExit("Failed to copy file to datanodes")
		
	'''If function was good send message with the jason'''
	s1 = socket(AF_INET,SOCK_STREAM)    # Create the server socket TCP protocol
	s1.connect((mds_HOST,mds_PORT))
	s1.send(message)
	response = s1.recv(1042)
	s1.close()
	print response


elif validateIP(arg1.split(':')[0]):
	# If argument 2 is an ip
	dfs_filePath = arg1.split(':')[1] # Path of the file in the dfs
	mds_HOST = arg1.split(':')[0]
	# Copy from DFS to computer (read)
	print 'Command is a  read'

	'''Create socket to comunicate with Meta Data Server'''
	
	s = socket(AF_INET,SOCK_STREAM)    # Create the server socket TCP protocol
	s.connect((mds_HOST,mds_PORT)) # connect MDS

	'''Message the metadata the filepath on the dfs'''

	comp_filePath = arg2 #Path of the file in the computer
	message = "4|%s" %dfs_filePath
	s.send(message)

	'''Recieve the response from the MDS'''

	recievedMsg = s.recv(1024)
	s.close()
	
	if recievedMsg == 'False':
		pass

	else:
		'''Unpack the inodes from the json'''
		inodes = json.loads(recievedMsg)
		data = '' # string to save the file  

		'''Get the chunk from each node'''
		print "Inodes info"
		for node,info in inodes.items():
			host,port,chunkid = info[0],info[1],info[2]

			print "%s: Host-> %s Port-> %s Chunkid-> %s" %(node,host,port,chunkid)

			'''Create the socket to connect with node '''
			
			s = socket(AF_INET,SOCK_STREAM)    # Create the server socket TCP protocol
			s.connect((host,port)) # connect node
			s.send("1|%s" %chunkid) # ask for a chunk
			chunksize = s.recv(1024) #recieve the chunk size
			print "This is the chunksize message: %s" %chunksize
			s.send('Chunk size recieved')
			chunksize = int(chunksize)
			data = ''
			while len(data) < chunksize:
				print len(data)
				data+= s.recv(chunksize - len(data))#recieve the chunk

			#print 'Writed from node %s: \n Chunk%s-> %s' %(node,chunkid,recievedMsg)

			'''Open a file and write the data'''

			print "Writing %s bytes in file:" %len(data) 
			try:
				f= open(comp_filePath,'a+b')#if the file exists, open the file
				f.write(data)
				f.close()
			except IOError as error: #if error
	   			print error

   		'''Read the data written in the file'''
	try:
		f= open(comp_filePath,'rb')
		read = f.read()
		f.close()
		'''Print the data'''
		print "File size is: %s" %len(read)
	except IOError as error:
		print error




			


