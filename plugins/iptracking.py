import urllib2, json, logging
import settings

IP_URL = 'http://jsonip.com/'
GEOIP_URL = 'http://www.telize.com/geoip/'
GEOIP_FORMAT = '''
%s | LA %s LO %s
TZ: %s
%s (%s)
%s (%s)
ISP: %s
PO: %s (%s)'''


def track(ip_address):
	req = urllib2.Request(GEOIP_URL + ip_address)
	try:
		f = urllib2.urlopen(req)
		response = f.read()
		f.close()
		data = json.loads(response)

		for detail in ['city', 'latitude', 'longitude', 
			'country', 'country_code', 'region', 'region_code',
			'isp', 'postal_code', 'area_code']:
			if not detail in data:
				data[detail] = 'NA'

		res = GEOIP_FORMAT % (data['city'], 
								data['latitude'], data['longitude'],
								data['timezone'],
								data['country'], data['country_code'],
								data['region'], data['region_code'],
								data['isp'],
								data['postal_code'], data['area_code'])
		return res
	except urllib2.HTTPError, err:
		logging.error(err)
		return settings.ERROR_MSG


def getip():
	req = urllib2.Request(IP_URL)
	try:
		f = urllib2.urlopen(req)
		response = f.read()
		f.close()
		data = json.loads(response)
		response = data['ip']
		return response
	except urllib2.HTTPError, err:
		logging.error(err)
		return settings.ERROR_MSG