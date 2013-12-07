###############################################################################
#
# Filename: test.py
# Author: Jose R. Ortiz and ... (hopefully some students contribution)
#
# Description:
#       Script to test the MySQL support library for the DFS project.
#
#

# This is how to import a local library
from mds_db import *

# Create an object of type mds_db
db = mds_db() 

# Connect to the database
print "Connecting to database" 
db.Connect() 

# Testing how to add a new node to the metadata server.
# Note that I used a node name, the address and the port.
# Address and port are necessary for connection.

print "Testing node addition"
db.AddDataNode("n0", "localhost", 80) 
db.AddDataNode("n1", "localhost", 80) 
print 
print "Testing if node was inserted"
print "A tupple with node name and connection info must appear"
print db.CheckNode("n0")
print

print "Testing all Available data nodes"
for name, address, port in  db.GetDataNodes():
	print name, address, port

print 

print "Inserting two files to DB"
db.InsertFile("/hola/cheo.txt", 20)
db.InsertFile("/opt/blah.txt", 30)
print

print "Choteando one of the steps of the assignment :) ..."
print "Files in the database"
for file, size in db.GetFiles():
	print file, size
print

print "Adding blocks to the file, duplicate message if not the first time running"
print "this script"
try:
	db.AddBlockToInode("/hola/cheo.txt",[("n0",1),("n1",1)])
except:
	print "Won't duplicate"
print

print "Testing retreiving Inode info"
fsize, chunks_info = db.GetFileInode("/hola/cheo.txt")

print "File Size is:", fsize
print "and can be constructed from: "
for  node, address, port, chunk in chunks_info:
	print node, address, port, chunk
print

print "Closing connection"
db.Close() 
