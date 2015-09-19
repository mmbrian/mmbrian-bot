import urllib2, json, logging
import unirest
import settings
from spellchecking import spellcheck

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

def lookup(exp, lang = 'en', spellchecked = False, showAttribution = False):
	if lang == 'en':
		try:
			# quote is similar to javascript's escape method
			response = unirest.get("https://montanaflynn-dictionary.p.mashape.com/define?word=%s" % urllib2.quote(exp),
			  headers={
			    "X-Mashape-Key": "7MRxI6ynAtmsh2Dyo4v55eIPAPHqp1H1BhmjsnZTIDbYblV1lc",
			    "Accept": "application/json"
			  }
			)
		except Exception, err:
			logging.error(err)
			return settings.ERROR_MSG
		if response.code == 200:
			ret, msg = [], ''
			for i, definition in enumerate(response.body['definitions']):
				if showAttribution:
					ret.append('%s. %s\n(%s)\n' % (i+1, definition['text'], definition['attribution']))
				else:
					ret.append('%s. %s\n' % (i+1, definition['text']))
			if ret:
				if spellchecked:
					msg = 'Results for "%s"\n' % exp
				return msg + ''.join(ret)
			else:
				if spellchecked:
					return 'I couldn\'t find a definition for that.'
				# Check if expression was misspelled
				return lookup(spellcheck(exp), spellchecked = True)
		return settings.ERROR_MSG
	return 'I couldn\'t understand.'