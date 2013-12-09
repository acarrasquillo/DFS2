import os
from socket import *
from mds_db import *
import json

mds_PORT = 1000
mds_HOST = "localhost"
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def validateIP(address):
	if address=='localhost':
		return True
	else:
	    try:
	        host_bytes = address.split('.')
	        valid = [int(b) for b in host_bytes]
	        valid = [b for b in valid if b >= 0 and b<=255]
	        return len(host_bytes) == 4 and len(valid) == 4

	    except:
	        return False

###################################################################################
# Functions for write
###################################################################################

'''Function to make chunks'''

def makeChunks(inputFile,noOfNodes):
	print "Making Chunks"
	
	'''read the file content '''
	try:
		f = open(inputFile, 'r')
		data = f.read() # read all the contet pf the file
		f.close()
	except IOError as error:
		print "Error opening the file" + str(error)
		return False
	bytes = len(data)
	'''calculate the chunksizes'''
	chunkSize = bytes/noOfNodes
	chunkList = []
	k = 1
	for i in range(0,bytes,chunkSize):

		if k == noOfNodes:
			chunk_Data = data[i:]
			chunkList.append(chunk_Data)
			break

		else:	
			chunk_Data = data[i:i+chunkSize]
			chunkList.append(chunk_Data)

		k = k + 1			
	return [chunkList,bytes]


'''Function to send chunks'''
def sendChunks(nodes,chunkList,dfs_filePath,fileSize):

	'''For each available node send an chunk and recieve the chunk id'''
	print "Sending Chunks"
	inodes=[]#list for saving inodes
	i = 0
	for node,info in nodes.items():

		'''Create a tcp socket and connect with the node'''
		nodeAddress = ((info[0],info[1])) #node adress to send a chunk (HOST,PORT)
		sock = socket(AF_INET,SOCK_STREAM)    # Create the server socket TCP protocol
		sock.connect(nodeAddress) #connect with node
		chunksize = str(len(chunkList[i]))
		data =  "0|"+chunksize
		sock.send(data)# Send chunk[i] size and command 0
		print sock.recv(1024) #print sock answer
		sock.send(chunkList[i]) # send the chunk i on the list
		print "Sending chunk to %s (host:%s,port:%s)" %(node,nodeAddress[0],nodeAddress[1])
		chunkId = sock.recv(1024)# recieve chunk id
		print "Chunk recieved by the node and has id-> %s" %chunkId
		if chunkId == 'None':
			return False
			break
		sock.close() # close socket
		inodes.append((node,chunkId)) #append tuple (node,chunkid) to inode
		i = i+1

	'''return the (filepath,size) and [inodes] in a jason'''
	result = []
	result.append(('filepath', (dfs_filePath,str(fileSize))))
	result.append(('inodes',inodes))
	message = json.dumps(dict(result))
	return message