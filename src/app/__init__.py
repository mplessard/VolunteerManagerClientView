from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import urllib

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models

def get_json(link):
	with urllib.request.urlopen(link) as url:
		myfile = url.read().decode('utf8')
	return json.loads(myfile)

app.jinja_env.globals.update(get_json=get_json)