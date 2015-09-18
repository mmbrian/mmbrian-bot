import urllib2, json, logging
import settings

def track(ip_address):
	req = urllib2.Request(settings.GEOIP_URL + ip_address)
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

        res = settings.GEOIP_FORMAT % (data['city'], 
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
	req = urllib2.Request(settings.IP_URL)
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