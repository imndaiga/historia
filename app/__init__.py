from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_graphql import GraphQLView
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from config import config

# extension attribute references here
db = SQLAlchemy()
bootstrap = Bootstrap()
mail = Mail()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.welcome'

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	# initialise extensions here
	db.init_app(app)
	login_manager.init_app(app)
	bootstrap.init_app(app)
	mail.init_app(app)

	# register app blueprints here
	from .api_schema import schema
	app.add_url_rule('/graphiql', view_func=GraphQLView.as_view('graphql',
		schema=schema, graphiql=app.config['MIMINANI_GRAPHIQL']))

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	return app