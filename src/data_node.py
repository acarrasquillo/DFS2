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

from mdsConf import *
import sys


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
	chunkDir = os.path.join(BASE_DIR, path)

	pass


s = socket(AF_INET,SOCK_STREAM)    # Create the server socket TCP protocol
s.connect((mds_HOST,mds_PORT))

'''Send mensaje of nodereport and wait answer and print it'''
message = "0|%s|%s|%s" % (path,HOST,port)
s.send(message)
answer = s.recv(1024)

'''Close Socket'''
s.close()
print answer

'''Now create a new socket to listen for commands'''
s1 = socket(AF_INET,SOCK_STREAM)
s1.bind((HOST,port))
print 'Node binded in(%s,%s)' %(HOST,port)  
s1.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s1.listen(1)
i = 0 #counter for the chunks ids
while True:
	
	'''Accept connections on node socket'''
	
	conn,address = s1.accept()
	recievedMsg = conn.recv(1024)
	msg = recievedMsg.split('|')
	
	print "Recieved Message-->%s" %msg

	'''If command is 0 write chunk'''
	
	if msg[0] == '0': 

		'''Get the chunk size'''
		chunk_size = int(msg[1])
		print "Chunk size is %s" %chunk_size
		conn.send('Size Recieved')
		
		'''Recieve the chunk'''
		chunk = ''
		while len(chunk) < chunk_size:
			chunk+= conn.recv(chunk_size - len(chunk))
		print "Recieved size is chunk:\n%s" %len(chunk)

		try:#check if that file exists
			filepath = os.path.join(chunkDir, str(i))
			f= open(filepath,'wb')#if the file exists, open the file
			f.write(chunk)
			f.close()
			conn.sendall(str(i))
			i = i+1
		except IOError as error: #if file doesn't exist
   			print error
   			message = 'None' #data will contain a string explaining that the file doesn't exists
   			conn.sendall(message)
   	
   	if msg[0] == '1':
   		try:
	   		filepath = os.path.join(chunkDir, msg[1])
	   		f= open(filepath,'rb')
	   		data = f.read()
	   		f.close()
	   		datasize = str(len(data))
	   		print "Sending chunk size %s" %datasize
	   		conn.sendall(datasize)
	   		print conn.recv(1024) #Print kopy response
	   		conn.sendall(data) #send the chunk
	   	except IOError as error:
	   		print error
   			message = 'None' #data will contain a string explaining that the file doesn't exists
   			conn.send(message)
	'''Close connection'''
	conn.close()	
