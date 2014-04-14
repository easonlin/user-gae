from flask import Flask
from flask import request
#from pymongo import MongoClient
app = Flask(__name__)
app.config["DEBUG"] = True
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


class Post(db.Model):
  message = db.StringProperty(required=True)
  name = db.StringProperty(required=True)
  photo = db.StringProperty(required=True)
  t = db.IntegerProperty(required=True)

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
