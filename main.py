import fix_path

import StringIO
import json
import logging
import random
import urllib
import urllib2
# import unirest

# for sending images
from PIL import Image
import multipart

# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2

TOKEN = '138881934:AAEqd4qcJUB4yjTt9cZe7f09Q5ldVY6w3pI'

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'

import settings
from plugins.translation import translate
from plugins.spellchecking import spellcheck

# ================================

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)
    translate_mode = ndb.BooleanProperty(indexed=False, default=False)


# ================================

def setEnabled(chat_id, yes):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()

def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False

def setTranslateMode(chat_id, status):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.translate_mode = status
    es.put()
def isTranslateMode(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.translate_mode
    return False    
    



# ================================

class MeHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url})))))


class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))

        update_id = body['update_id']
        message = body['message']
        message_id = message.get('message_id')
        date = message.get('date')
        text = message.get('text')
        fr = message.get('from')
        chat = message['chat']
        chat_id = chat['id']

        if not text:
            logging.info('no text')
            return

        def reply(msg=None, img=None):
            if msg:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'text': msg.encode('utf-8'),
                    'disable_web_page_preview': 'true',
                    'reply_to_message_id': str(message_id),
                })).read()
            elif img:
                resp = multipart.post_multipart(BASE_URL + 'sendPhoto', [
                    ('chat_id', str(chat_id)),
                    ('reply_to_message_id', str(message_id)),
                ], [
                    ('photo', 'image.jpg', img),
                ])
            else:
                logging.error('no msg or img specified')
                resp = None

            logging.info('send response:')
            logging.info(resp)

        if text.startswith('/'):
            text = text.lower()
            if text == '/start':
                reply('Bot enabled')
                setEnabled(chat_id, True)
            elif text == '/stop':
                if isTranslateMode(chat_id):
                    reply('Deactivated translation mode.')
                    setTranslateMode(chat_id, False)
                else:
                    reply('Bot disabled')
                    setEnabled(chat_id, False)
            elif text == '/image':
                img = Image.new('RGB', (512, 512))
                base = random.randint(0, 16777216)
                pixels = [base+i*j for i in range(512) for j in range(512)]  # generate sample image
                img.putdata(pixels)
                output = StringIO.StringIO()
                img.save(output, 'JPEG')
                reply(img=output.getvalue())
            elif text == '/german':
                reply('Activated translation mode. deactivate using /stop')
                setTranslateMode(chat_id, True)
            elif text == '/ip':
                req = urllib2.Request(settings.IP_URL)
                try:
                    f = urllib2.urlopen(req)
                    response = f.read()
                    f.close()
                    data = json.loads(response)
                    response = data['ip']
                    reply(response)
                except urllib2.HTTPError, err:
                    logging.error(err)
                    reply("Something went wrong :(")
            elif text.startswith('/track'):
                ip_address = text[6:].strip()
                req = urllib2.Request(settings.GEOIP_URL + ip_address)
                try:
                    f = urllib2.urlopen(req)
                    response = f.read()
                    f.close()
                    data = json.loads(response)
                    res = settings.GEOIP_FORMAT % (data['city'], 
                                                data['latitude'], data['longitude'],
                                                data['timezone'],
                                                data['country'], data['country_code'],
                                                data['region'], data['region_code'],
                                                data['isp'],
                                                data['postal_code'], data['area_code'])
                    reply(res)
                except urllib2.HTTPError, err:
                    logging.error(err)
                    reply("Something went wrong :(")
            elif text.startswith('/rand'):
                query = text[5:].lower().strip()
                url, valid_params = '', False
                if not query:
                    rtype, length, size = 'uint8', 1, 1
                    valid_params = True
                else:    
                    try:
                        params = query.split(' ')
                        assert len(params) == 3
                        rtype, length, size = map(lambda s: s.strip(), params)
                        assert rtype in ['uint8', 'uint16', 'hex16']
                        length, size = int(length), int(size)
                        valid_params = True
                    except Exception, err:
                        logging.error(err)
                        reply("Invalid format :(")
                if valid_params:
                    url = settings.RAND_URL % (length, rtype, size)
                    req = urllib2.Request(url)
                    try:
                        f = urllib2.urlopen(req)
                        response = f.read()
                        f.close()
                        data = json.loads(response)
                        assert 'data' in data
                        reply(str(data['data'])[1:-1])
                    except Exception, err:
                        logging.error(err)
                        reply("Something went wrong :(")
            elif text.startswith('/ge'):
                query = text[3:].strip()
                reply(translate(query))
            elif text.startswith('/correct'):
                reply(spellcheck(text[8:].strip()))
            else:
                reply('What command?')

        # CUSTOMIZE FROM HERE

        elif 'who are you' in text:
            reply('I\'m just a bot.')
        elif 'what time' in text:
            reply('I\'m not a watch you know, at least not yet.')
        else:
            if getEnabled(chat_id):
                if isTranslateMode(chat_id):
                    reply(translate(text))
                else:
                    reply(settings.COMMANDS_LIST)
            else:
                logging.info('not enabled for chat_id {}'.format(chat_id))


app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)
