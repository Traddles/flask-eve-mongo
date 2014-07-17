from eve import Eve
from flask import Flask, url_for, render_template, send_from_directory
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
from bson.objectid import ObjectId
import datetime


# Eve
app = Eve(settings='conf/settings.py')
# Flask
flask = Flask(__name__)
flask.config.update(
	DEBUG = True,
)
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
flask.session_interface = MongoEngineSessionInterface(engine)
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

	# meta = {
		# 'indexes' : ['-created_at'],
	# 	'ordering' : ['-created_at']
	# }

@flask.route("/add")
def add_one():
	People(lastname="addie").save()
	return "Saved one 'addie'"

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

if __name__ == '__main__':
	# Flask
	flask.run()

	# Eve
	app.run()

