import logging
import unirest
from urllib import quote_plus as qp
import urllib2
import settings
from bs4 import BeautifulSoup as BS

def getTinyUrl(link, cookie):
	url = 'https://tinyurl.com/create.php?source=indexpage&url=' + qp(link) + '&submit=Make+TinyURL%21&alias='
	header = settings.FAKE_HEADER.copy()
	header['Upgrade-Insecure-Requests'] = 1
	header['Cookie'] = cookie
	header['Referer'] = 'https://tinyurl.com/'
	try:
		response = unirest.get(url,
		  headers=header
		)
	except Exception, err:
		logging.error(err)
		return 'NA'
	if response.code == 200:
		data = response.body
		soup = BS(data)
		for link in soup.find_all('a'):
			if 'new window' in link.text:
				ret = link.get('href')
				if not 'preview.' in ret:
					return ret
	return 'NA'

def getCookie():
	f = urllib2.urlopen('https://tinyurl.com/dyn/common')
	cookie = f.headers.dict['set-cookie']
	f.close()
	return cookie