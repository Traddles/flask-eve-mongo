from eve import Eve
from flask import Flask, url_for, session, g, redirect, request, flash, render_template, send_from_directory
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
from flask.ext.mongoengine.wtf import model_form
from bson.objectid import ObjectId
import datetime


# Eve
app = Eve(settings='conf/settings.py')
# Flask
flask = Flask(__name__)
flask.config.update(dict(
	DEBUG = True,
    USERNAME='admin',
    PASSWORD='default'
))
flask.config['DEBUG_TB_PANELS'] = (
	'flask.ext.debugtoolbar.panels.versions.VersionDebugPanel',
	'flask.ext.debugtoolbar.panels.timer.TimerDebugPanel',
	'flask.ext.debugtoolbar.panels.headers.HeaderDebugPanel',
	'flask.ext.debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
	'flask.ext.debugtoolbar.panels.template.TemplateDebugPanel',
	'flask.ext.debugtoolbar.panels.logger.LoggingPanel',
	'flask.ext.mongoengine.panels.MongoDebugPanel'
)
flask.config["MONGODB_SETTINGS"] = {'DB': "eve"}
flask.config["SECRET_KEY"] = "M3\xbd\xe4\xa5 g\x13\x10\x98\xa8\xb3@\xb5z\xfd\x02J\x90\xfd\x9cC\x87\x11"

# Database connection
engine = MongoEngine(flask)
client = engine.connection
db = client.eve

# Model
class People(engine.DynamicDocument):
	created_at = engine.DateTimeField(default=datetime.datetime.now, required=True, db_field ="_created")
	updated_at = engine.DateTimeField(default=datetime.datetime.now, required=True, db_field ="_updated")
	lastname = engine.StringField(max_length=30, required=True)
	firstname = engine.StringField(max_length=30, required=False)
	def __unicode__(self):
		return self.name

@flask.route('/add', methods=['POST'])
def add_entry():
    # if not session.get('logged_in'):
    #     abort(401)
    People(lastname=request.form['lastname'], firstname=request.form['firstname']).save()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@flask.route("/look")
def search():
	obj = People.objects.get(lastname="obama")
	return obj.lastname

@flask.route('/articles')
def api_articles():
	r = ''
	for art in People.objects:
		r = r + " - " + art.lastname
	return 'List of ' + url_for('api_articles') + ":<br>\n" + r

# @flask.route('/')
# def index():
# 	return "<h1>Salam</h1>"

@flask.route('/')
def show_entries():
    entries = People.objects
    return render_template('show_entries.html', entries=entries)

if __name__ == '__main__':
	# Flask
	flask.run()

	# Eve
	app.run()

