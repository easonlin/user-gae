from flask import Flask, redirect, url_for, session, request, flash
from flask import make_response
import os
import httplib2
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


app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
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


@app.route('/auth/log')
def log():
    me = facebook.get('/me')
    username = me.data["username"]
    return 'My name is %s' % me.data['name']

import urllib3
@app.route('/auth/picture')
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

@app.route('/auth')
def index():
    return redirect(url_for('login'))


@app.route('/auth/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@app.route('/auth/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    return 'Logged in as id=%s name=%s redirect=%s' % \
        (me.data['id'], me.data['name'], request.args.get('next'))

@app.route('/auth/logout')
def logout():
    oauth_token = session.pop('oauth_token', None)
    logger.info("oauth_token %s", oauth_token)
    return redirect(request.referrer or url_for('log'))

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


if __name__ == '__main__':
    app.run()
