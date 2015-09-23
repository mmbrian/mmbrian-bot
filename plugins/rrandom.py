import urllib2, logging
import settings

'''
This api returns REAL random numbers!
http://qrng.anu.edu.au/API/api-demo.php
'''

RAND_URL = 'https://qrng.anu.edu.au/API/jsonI.php?length=%s&type=%s&size=%s'

def rand(query):
	url, valid_params = '', False
	if not query:
		rtype, length, size = 'uint8', 1, 1
		valid_params = True
	else:    
		try:
			params = query.split(' ')
			assert len(params) == 3
			rtype, length, size = map(lambda s: s.strip(), params)
			assert rtype in ['uint8', 'uint16', 'hex16']
			length, size = int(length), int(size)
			valid_params = True
		except Exception, err:
			logging.error(err)
			return "Invalid format."
	if valid_params:
		url = RAND_URL % (length, rtype, size)
		req = urllib2.Request(url)
		try:
			f = urllib2.urlopen(req)
			response = f.read()
			f.close()
			data = json.loads(response)
			assert 'data' in data
			return str(data['data'])[1:-1]
		except Exception, err:
			logging.error(err)
			return settings.ERROR_MSG
	else:
		return "Invalid parameters."

