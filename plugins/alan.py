import urllib2
from urllib2 import quote, urlopen, Request

ALAN_URL = 'http://www.a-i.com/alan1/webface1_ctrl.asp?style=Alan&name=Alan'

def q(question):
	return ALAN_URL+ '&question=%s' % quote(question)

def sendAlanRequest(question = None, headers = None):
	if not question:
		url = ALAN_URL
		return urlopen(Request(url))
	else:
		url = q(question)
		return urlopen(Request(url, headers = headers))

def getAlanSessionCookieHeader(req):
	return {'Cookie': req.headers.dict['set-cookie']}

def readAlanResponse(req):
	prefix = '<option>answer ='
	plen = len(prefix)
	for line in req:
		if line.startswith(prefix): 
			req.close()
			return line[plen:].strip()
