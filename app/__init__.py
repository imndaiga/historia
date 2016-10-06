from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

# extension attribute references here
db = SQLAlchemy()

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	# initialise extensions here
	db.init_app(app)

	# register app blueprints here

	return app