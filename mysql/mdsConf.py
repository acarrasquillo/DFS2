import os
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