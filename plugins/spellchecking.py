import unirest, logging
import settings

def spellcheck(query):
	try:
		response = unirest.get("https://montanaflynn-spellcheck.p.mashape.com/check/?text=%s" % query,
		  headers={
		    "X-Mashape-Key": "2plRPiDIDamshILOX99O1p9Jc96Rp1ycpuyjsntHxWjaPJf3k8",
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