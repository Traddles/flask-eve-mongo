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
    PASSWORD=''
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
	allowed_fields = engine.DictField(required=False, db_field ="_fields")
	field_types = engine.DictField(required=False, db_field ="_types")
	lastname = engine.StringField(max_length=30, required=True)
	firstname = engine.StringField(max_length=30, required=False)
	def __unicode__(self):
		return self.lastname

@flask.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != flask.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != flask.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@flask.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@flask.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	People(lastname=request.form['lastname'], firstname=request.form['firstname']).save()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))


@flask.route('/update/<entry_id>', methods=['POST'])
def update_entry(entry_id):
	if not session.get('logged_in'):
		flash("This won't work unless you login")
		return redirect(url_for('show_entries'))
	update_object = get_by_id(entry_id)

	print "This is him:", update_object.lastname

	#People(lastname=request.form['lastname'], firstname=request.form['firstname']).save()
	s = ''
	for key in request.form:
		choice = request.form[key]
		print key, choice

		if choice in update_object.allowed_fields[key]:
			print "allright"
			choice = update_object.allowed_fields[key][choice]
		update_object[key] = choice

	update_object.save()
	flash('Update')
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

@flask.route('/')
def show_entries():
    entries = People.objects
    return render_template('show_entries.html', entries=entries)

def get_by_id(entry_id):
	entry = People.objects(id=entry_id)
	if not entry:
		abort(401)
	return entry[0]

if __name__ == '__main__':
	# Flask
	flask.run(host= '0.0.0.0')

	# Eve
	#app.run()

