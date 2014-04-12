from flask import Flask
app = Flask(__name__)
app.config["DEBUG"] = True
# wrap the application
from werkzeug import DebuggedApplication
app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)
import json
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/test')
def test():
    """Return a friendly HTTP greeting."""
    return json.dumps({"Foo": ["bar", "can", "haz"]})

@app.route('/post')
def post():
    """ creat post """
    raise Exception("Hello")


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
