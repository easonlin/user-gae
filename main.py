from flask import Flask
app = Flask(__name__)
import json
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return json.dumps({"Foo": ["bar", "can", "haz"]})
    #return "Hello"

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
