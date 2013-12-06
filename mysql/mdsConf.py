import os
from socket import inet_aton, error
mds_PORT = 1000
mds_HOST = "localhost"
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def ValidateIP(address):
	if 'localhost' == address:
		return True 

	try:
		inet_aton(address)
		return True
	except error:
		return False