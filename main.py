from flask import Flask
from flask import (request, url_for, session)
#from pymongo import MongoClient
SECRET_KEY = 'development key'
app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = SECRET_KEY
# wrap the application
from werkzeug import DebuggedApplication
app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)
import logging
logger = logging.getLogger(__name__)
import json
#client = MongoClient('localhost', 27017)
#db = client.gae
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
import time
from google.appengine.ext import db
from google.appengine.api import users
import module
facebook = module.facebook


class Post(db.Model):
  message = db.StringProperty(required=True)
  name = db.StringProperty(required=True)
  photo = db.StringProperty(required=True)
  t = db.IntegerProperty(required=True)

@app.route('/api/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None, _external=True))
@app.route('/auth/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description'])
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    return 'Logged in as id=%s name=%s redirect=%s' % \
        (me.data['id'], me.data['name'], request.args.get('next'))

@app.route('/auth/logout')
def logout():
    oauth_token = session.pop('oauth_token', None)
    return redirect(request.referrer or url_for('log'))

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

@app.route('/api/test')
def test():
    """Return a friendly HTTP greeting."""
    return json.dumps({"Foo": ["bar", "can", "haz"]})

def filter(data, fields):
    keys = data.keys()
    for each in keys:
        if each not in fields:
            del data[each]
    return data
    

@app.route('/api/post', methods=["GET", "POST"])
def post():
    if request.method == 'POST':
        """ creat post """
        #data = {"message": "Hello", "name": "Eason Lin", "photo":"a"}
        data = request.get_json(force=True)
        data = filter(data, ["message", "name", "photo"])
        data["t"] = int(time.time())
        p = Post(**data)
        p.put()
        return ""
    else:
        """ list post """
        p = Post.all().order("-t")
        res = {"datas": [each._entity for each in p]}
        return json.dumps(res)

@app.route('/api/clean')
def clean():
     query = Post.all(keys_only=True)
     entries = query.fetch(1000)
     db.delete(entries)
     return ""

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
