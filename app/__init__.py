from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_graphql import GraphQLView

# extension attribute references here
db = SQLAlchemy()

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	# initialise extensions here
	db.init_app(app)

	# register app blueprints here
	from .api_schema import schema
	app.add_url_rule('/graphiql', view_func=GraphQLView.as_view('graphql',
		schema=schema, graphiql=app.config['MIMINANI_GRAPHIQL']))

	return app