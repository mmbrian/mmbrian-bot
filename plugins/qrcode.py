import unirest, logging, urllib2, cStringIO, Image
import settings

FAKE_HEADER = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def getQR(data, ecc = 'M', size = 4):
	try:
		response = unirest.post("https://aaryadev-qr-code-v1.p.mashape.com/?data=%s&ecc=%s&size=%s" % (data, ecc, size),
		  headers={
		    "X-Mashape-Key": "2plRPiDIDamshILOX99O1p9Jc96Rp1ycpuyjsntHxWjaPJf3k8",
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
			req = urllib2.Request(url, headers = FAKE_HEADER)
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

