from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import config
from .graph import Graph
from .seed import Seed

# extension attribute references here
db = SQLAlchemy()
mail = Mail()
graph = Graph()
seed = Seed()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # initialise extensions and modules here
    db.init_app(app)
    mail.init_app(app)
    graph.init_app(app)
    seed.init_app(app, update_graph=app.config['SEED_UPDATE_GRAPH'] or True)

    # register app blueprints here

    from .api import api_bp as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
