from flask import Flask
from flask import (request, url_for, session, redirect)
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
from module import Post

@app.route('/auth/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None, _external=True))

@app.route('/auth/status')
def status():
  if not session.get('oauth_token'):
    return json.dumps({'islogin': False})
  me = facebook.get('/me') 
  username = me.data["username"]
  return json.dumps({'username': username,
                     'islogin': True})  

@app.route('/api/picture')
def picture():
  return module.picture()
   
@app.route('/api/picture/<int:post_id>')
def post_picture(post_id):
  return module.post_picture(post_id)

@app.route('/auth/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description'])
    session['oauth_token'] = (resp['access_token'], '')
    return redirect('/message/index.html')

@app.route('/auth/logout')
def logout():
    oauth_token = session.pop('oauth_token', None)
    return redirect(request.referrer or '/message/index.html')

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

import base64
@app.route('/api/test')
def test():
    """Return a friendly HTTP greeting."""
    pic = module.picture()
    logger.info("data:image/jpeg;"+base64.b64encode(pic.data))
    return json.dumps({"Foo": ["bar", "can", "haz"]})

def filter(data, fields):
    keys = data.keys()
    for each in keys:
        if each not in fields:
            del data[each]
    return data
    
def get_posts():
    p = Post.all().order("-t")
    def to_dict(data, fields):
	rtn = {}
	for each in fields:
	    if each == "id":
		rtn["id"] = data.key().id()
	    else:
		rtn[each] = data._entity.get(each)
	return rtn
    return [to_dict(each, ["id", "t", "name", "message"]) for each in p]

@app.route('/api/post', methods=["GET", "POST"])
def post():
    if request.method == 'POST':
        """ creat post """
        #data = {"message": "Hello", "name": "Eason Lin", "photo":"a"}
        data = request.get_json(force=True)
        data = filter(data, ["message"])
        data["t"] = int(time.time())
        picture = module.picture()
        data["picture"] = picture.data
        me = facebook.get('/me')
        data["name"] = me.data["username"]
        data["content_type"] = picture.content_type
        p = Post(**data)
        id = p.put()
        return json.dumps({"id": p.key().id()})
    else:
        """ list post """
        p = Post.all().order("-t")
        def to_dict(data, fields):
            rtn = {}
            for each in fields:
                if each == "id":
                    rtn["id"] = data.key().id()
                else:
                    rtn[each] = data._entity.get(each)
            return rtn
        res = {"datas": get_posts()}
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


# ============================
# jinja2
# ===========================
import jinja2
import os
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        os.path.join(os.path.dirname(__file__),"templates")),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
def render_template(name, template_values={}):
    template = JINJA_ENVIRONMENT.get_template(name)
    return template.render(template_values)
@app.route('/web/login')
def web_login():
    return facebook.authorize(callback=url_for('web_facebook_authorized',
        next=request.args.get('next') or request.referrer or None, _external=True))
    pass

@app.route('/web/authorized')
@facebook.authorized_handler
def web_facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description'])
    session['oauth_token'] = (resp['access_token'], '')
    return redirect(url_for('web_index'))

@app.route('/web/index.html')
def web_index():
    posts = get_posts()
    if session.get('oauth_token'):
        me = facebook.get('/me')
        username = me.data["username"]
        return render_template('web_main.html', {"posts": posts, "name": username})
    else:
        return render_template('web_login.html', {"posts": posts})

@app.route('/web/logout')
def web_logout():
    oauth_token = session.pop('oauth_token', None)
    return redirect(url_for('web_index'))

