import unirest, logging, urllib2
import settings
from random import random

CATEGORIES = ['famous', 'movies']

def getRandomQuote(category='famous', randomCategory=False):
	if randomCategory:
		category = CATEGORIES[int(random()*len(CATEGORIES))]
	try:
		response = unirest.post("https://andruxnet-random-famous-quotes.p.mashape.com/cat=%s" % category,
		  headers={
		    "X-Mashape-Key": "7MRxI6ynAtmsh2Dyo4v55eIPAPHqp1H1BhmjsnZTIDbYblV1lc",
		    "Content-Type": "application/x-www-form-urlencoded",
		    "Accept": "application/json"
		  }
		)
	except Exception, err:
		logging.error(err)
		return settings.ERROR_MSG
	if response.code == 200:
		if 'quote' in response.body:
			return '"%s"  %s (Category: %s)' % (response.body['quote'], response.body['author'], response.body['category'])
	return settings.ERROR_MSG