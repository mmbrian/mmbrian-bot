import unirest, logging, urllib2, cStringIO, Image
import settings

def getQR(data, ecc = 'M', size = 4):
	try:
		response = unirest.post("https://aaryadev-qr-code-v1.p.mashape.com/?data=%s&ecc=%s&size=%s" % (data, ecc, size),
		  headers={
		    "X-Mashape-Key": "7MRxI6ynAtmsh2Dyo4v55eIPAPHqp1H1BhmjsnZTIDbYblV1lc",
		    "Content-Type": "application/x-www-form-urlencoded",
		    "Accept": "application/json"
		  }
		)
	except Exception, err:
		logging.error(err)
		return None
	if response.code == 200:
		if 'img_url' in response.body:
			url = response.body['img_url']
			url = url.replace('https', 'http')
			req = urllib2.Request(url, headers = settings.FAKE_HEADER)
			try:
				f = cStringIO.StringIO(urllib2.urlopen(req).read())
				return f.getvalue()
				# Converting to jpeg
				# img = Image.open(f).convert('RGB')
				# output = cStringIO.StringIO()
				# img.save(output, 'JPEG')
				# return output.getvalue()
			except Exception, err:
				logging.error(err)
				return None
	return None

