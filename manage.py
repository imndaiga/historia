#!/usr/bin/env python3

from app import create_app, db
from app.email import send_email
from app.models import Node, GlobalEdge, GlobalGraph, Seed
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
import os

app = create_app(os.getenv('MIMINANI_CONFIG') or 'default')

# Instantiate extensions that modify app-runtimes here
manager = Manager(app)
migrate = Migrate(app, db)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

# Attach functions to app-runtime flags


def make_shell_context():
    return dict(db=db, Node=Node, GlobalEdge=GlobalEdge,
                GlobalGraph=GlobalGraph, app=app,
                send_email=send_email, Seed=Seed)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('forge', Seed())

if __name__ == '__main__':
    with app.app_context():
        basedir = os.path.abspath(os.path.dirname(__file__))
        if app.config['DEBUG'] and \
                (basedir in app.config['SQLALCHEMY_DATABASE_URI']):
            if not os.path.exists('data-dev.sqlite'):
                print('No development database present')
    manager.run()
