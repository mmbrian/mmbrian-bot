import urllib2, json, logging
import settings

def translate(query, lang = 'de'):
	if lang == 'de':
		data = '{\'searchText\': \'' + query + '\', \'direction\': \'65540\', \'maxTranslationChars\':\'-1\'}'
		url = 'http://www.reverso.net/WebReferences/WSAJAXInterface.asmx/TranslateWS'
		req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
		try:
		    f = urllib2.urlopen(req)
		    response = f.read()
		    f.close()
		    data = json.loads(response)
		    response = data['d']['result']
		    return response
		except urllib2.HTTPError, err:
		    logging.error(err)
		    return settings.ERROR_MSG
	return 'I couldn\'t understand.'
