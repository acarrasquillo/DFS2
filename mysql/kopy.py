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
# 				python copy <path of the file> <metadata-server-ip-address:path on the DFS> 
# 				
# 			Copy from DFS to computer:
# 				python copy <metadata-server-ip-address:path on the DFS> <path of the file> 
##############################################################
'''Copy Command'''
from socket import *
from mdsConf import mds_PORT, validateIP
import json
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
# If argument 1 is an ip
# Copy from DFS to computer (read)
s = socket(AF_INET,SOCK_STREAM)    # Create the server socket TCP protocol

# If argument 2 is an ip
# Copy from computer to DFS (write)
if validateIP(arg2.split(':')[0]):
	''' Argument 2 is the IP'''
	''' Make Copy from computer to DFS (write) '''
	mds_HOST = arg2.split(':')[0] # DFS Host
	print mds_HOST, mds_PORT
	s.connect((mds_HOST,mds_PORT))
	dfs_filePath = arg2.split(':')[1] # Path of the file in the dfs
	comp_filePath = arg1 #Path of the file in the computer
	message = "2"
	s.send(message)
	while True:
		'''Accept connections from DFS and Nodes on socket'''
		recievedMsg = s.recv(1024)
		data = json.loads(recievedMsg)
		msg = data.pop('msg')
		
		if msg == 0:
			print "Can't write a file there are no nodes available"
			break

		print "There are " + str(msg) + " nodes available"
		'''Split the file in n chunks, n=#nodes'''
		'''Send chunk n to node n''' 


		'''Copying chunks to nodes'''
		for node,host_port in data.items():
			'''Send the chunk to the node'''
		break



def makeChunks(inputFile,noOfNodes):
	'''read the file content '''
	try:
		f = open(inputFile, 'rb')
		data = f.read() # read all the contet pf the file
		f.close()
	except IOError as error:
		raise SystemExit("Error creating chunk directory: " + str(error))
	bytes = len(data)
	'''calculate the chunksizes'''
	chunkSize = bytes/noOfNodes
	noOfChunks = noOfNodes

	if(bytes%chunkSize):
		noOfChunks+=1

	print inputFile+','+'chunk,'+str(noOfNodes)+','+str(chunkSize)

	chunkList = []
	for i in range(0,bytes+1,chunkSize):
		fn1 = data[i:i] + chunkSize
		chunkList.append(("chunk%s",fn1)) %i

		j = json.dumps(dict(chunkList))

		return j

# #This function join all the chunks contained in list[]
# def joinChunks(list):

# 	#Go through all the chunks in list
# 	for data in list:

		
# 		#fl is the variable that will contain the joined chunks
# 		fl=None

# 		#put the ned data at the end of fl
# 		fl.append(data)
