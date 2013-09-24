import zmq

context = zmq.Context()
controller = context.socket(zmq.PUB)
controller.bind("tcp://127.0.0.1:5559")

import json
keys = json.load(open('keys.json'))
sha_key = "%s&%s" % (keys['consumer_secret'], keys['access_token_secret'])

from hashlib import sha1
import hmac
requests = json.load(open('config.json'))
method = requests['method']
del requests['method']
import urllib2
url = requests['url']
del requests['url']
from codecs import encode
requests['oauth_nonce']=encode(open('/dev/urandom').read(16), 'hex')
import time
requests['oauth_timestamp']=str(int(time.time()))
requests = requests.items()
requests.sort()
oauth_string = urllib2.quote('&'.join(['%s=%s' % (k,v) for k,v in requests]),'')
request_string = '&'.join([method,urllib2.quote(url,''),oauth_string])
print request_string

import hmac
requests.append(('oauth_signature', urllib2.quote(encode(hmac.new(sha_key,request_string,sha1).digest(),'base64')[:-1], '')))
requests.sort()
header = str('Authorization: OAuth ' + ', '.join(['%s="%s"' % k for k in requests]))

import pycurl
c = pycurl.Curl()
print url
c.setopt(pycurl.URL,str(url))
c.setopt(pycurl.HTTPHEADER, [header])
c.setopt(pycurl.WRITEFUNCTION, controller.send)
c.setopt(pycurl.FOLLOWLOCATION, 1)
c.setopt(pycurl.MAXREDIRS, 5)
c.perform()

