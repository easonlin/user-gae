from flask import make_response
import os
import httplib2
import urllib3
httplib2.CA_CERTS = \
    os.path.join(os.path.dirname(os.path.abspath(__file__ )), "cacert.pem")
from flask_oauth import OAuth
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

SECRET_KEY = 'development key'
DEBUG = True
FACEBOOK_APP_ID = '1474687689427487'
FACEBOOK_APP_SECRET = 'f824d0d58c7594f0e380c1367a1dd7a1'
oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)

def picture():
    me = facebook.get('/me')
    username = me.data["username"]
    http = urllib3.PoolManager()
    r = http.request('GET',
        'http://graph.facebook.com/%s/picture?type=large'\
         % username)
    content_type = r.getheader("content-type")
    response = make_response(r.data)
    response.headers['Content-Type'] = content_type
    return response

