import unirest, logging
import settings
from urllib2 import quote as q
from urllib import quote_plus as qp
from bs4 import BeautifulSoup as BS
from tinyurl import *

from google.appengine.api import urlfetch
import json

def search(query, maxResults=7, pageToken=None):
	url = "https://zazkov-youtube-grabber-v1.p.mashape.com/search.video.php?maxResults=%s&query=%s" % (maxResults, q(query))
	if pageToken:
		url = url + ('&pageToken=%s' % pageToken)
	try:
		response = unirest.get(url,
		  headers={
		    "X-Mashape-Key": "7MRxI6ynAtmsh2Dyo4v55eIPAPHqp1H1BhmjsnZTIDbYblV1lc",
		    "Accept": "application/json"
		  }
		)
	except Exception, err:
		logging.error(err)
		return settings.ERROR_MSG
	if response.code == 200:
		if 'control' in response.body:
			ret = []
			nextPageToken = response.body['control']['nextPageToken']
			for i, res in enumerate(response.body['data']):
				title = res['title']
				vidId = res['videoId']
				ret.append('%s. %s [%s]\n' % (i+1, title, vidId))
			ret.append('Next Page Token: %s' % nextPageToken)
			return ''.join(ret)
	return settings.ERROR_MSG

# def getDownloadLinks(vidId):
# 	try:
# 		url = 'http://fitnessviet.com/'
# 		header = settings.FAKE_HEADER.copy()
# 		header['Referer'] = url
# 		response = unirest.post(url,
# 			headers= settings.FAKE_HEADER,
# 			params={
# 				"link": qp('https://www.youtube.com/watch?v=%s' % vidId) + '&submit=Download',
# 			}
# 		)
# 	except Exception, err:
# 		logging.error(err)
# 		return settings.ERROR_MSG + ' [No Response]'
# 	if response.code == 200:
# 		try:
# 			data = response.body
# 			soup = BS(data)
# 			links = soup.find_all('a')
# 			ret = []
# 			cookie = getCookie()
# 			for i, link in enumerate(links):
# 				tlink = getTinyUrl(link.get('href'), cookie)
# 				ret.append('%s. %s\n[%s]\n' % (i+1, link.previousSibling, tlink))
# 			if not len(ret):
# 				ret.append('No links found.\n')
# 			return ''.join(ret)
# 		except Exception, err:
# 			logging.error(err)
# 			return settings.ERROR_MSG + ' [Bad Response]'
# 	return settings.ERROR_MSG + ' [%s]' % response.status_code

def getYouTubeLink(vidId):
	return 'https://www.youtube.com/watch?v=%s' % vidId

def getDownloadLinks(vidId):
	url = "https://zazkov-youtube-grabber-v1.p.mashape.com/download.video.php?id=%s" % vidId
	try:
		# These code snippets use an open-source library.
		# response = unirest.get(url,
		#   headers={
		#     "X-Mashape-Key": "7MRxI6ynAtmsh2Dyo4v55eIPAPHqp1H1BhmjsnZTIDbYblV1lc",
		#     "Accept": "application/json"
		#   }
		# )
		urlfetch.set_default_fetch_deadline(60)
		response = urlfetch.fetch(url=url, 
			headers={
		    "X-Mashape-Key": "7MRxI6ynAtmsh2Dyo4v55eIPAPHqp1H1BhmjsnZTIDbYblV1lc",
		    "Accept": "application/json"
		  }
		)
	except Exception, err:
		logging.error(err)
		return settings.ERROR_MSG + ' [No Response]'
	# if response.code == 200:
	if response.status_code == 200:
		# if 'map' in response.body:
		data = json.loads(response.content)
		if 'map' in data:
			ret = []
			cookie = getCookie()
			# for i, res in enumerate(response.body['map']):
			for i, res in enumerate(data['map']):
				quality = res[1]
				link = getTinyUrl(res[2], cookie)
				size = res[4]
				ret.append('%s. %s (%s)\n[%s]\n' % (i+1, quality, size, link))
			return ''.join(ret)
	return settings.ERROR_MSG + ' [%s]' % response.status_code

