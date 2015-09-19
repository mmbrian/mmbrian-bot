import unirest, logging
import settings

def spellcheck(query):
	try:
		response = unirest.get("https://montanaflynn-spellcheck.p.mashape.com/check/?text=%s" % query,
		  headers={
		    "X-Mashape-Key": "7MRxI6ynAtmsh2Dyo4v55eIPAPHqp1H1BhmjsnZTIDbYblV1lc",
		    "Accept": "application/json"
		  }
		)
	except Exception, err:
		logging.error(err)
		return settings.ERROR_MSG
	if response.code == 200:
		if 'suggestion' in response.body:
			return response.body['suggestion']
	return settings.ERROR_MSG