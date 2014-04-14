from flask import Flask, redirect, url_for, session, request, flash
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
import module
facebook = module.facebook
SECRET_KEY = 'development key'
DEBUG = True
app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY


@app.route('/auth/log')
def log():
    me = facebook.get('/me')
    username = me.data["username"]
    return 'My name is %s' % me.data['name']

@app.route('/auth/picture')
def picture():
    return module.picture()

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
