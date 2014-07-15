from eve import Eve
from flask import Flask, url_for
from pymongo import MongoClient

# Database connection
client = MongoClient('localhost', 27017)
db = client.eve

# The Apps
flaskApp = Flask(__name__)
app = Eve(settings='conf/settings.py')

#@app.route('/')
#def api_root():
#    return 'Welcome'

@app.route('/articles')
def api_articles():
    return 'List of ' + url_for('api_articles')

#def post_get_callback(resource, request, payload):
#    print 'A GET on the "%s" endpoint was just performed!' % resource
#    return 'HEJ'

#app.on_post_GET += post_get_callback

if __name__ == '__main__':
    # Eve
    app.run()

    # Flask
    flaskApp.run()
