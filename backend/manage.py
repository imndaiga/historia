#!/usr/bin/env python3

from app import create_app, db, graph, seed
from app.email import send_email
from app.models import Person, Link
from app.seed import fake
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
    return dict(db=db, Person=Person, Link=Link,
                graph=graph, app=app,
                send_email=send_email, seed=seed, fake=fake)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('forge', seed)

if __name__ == '__main__':
    with app.app_context():
        basedir = os.path.abspath(os.path.dirname(__file__))
        data_dir = os.path.join(basedir, 'data')
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        if basedir in app.config['SQLALCHEMY_DATABASE_URI']:
            if not os.path.exists(app.config['SQLALCHEMY_DATABASE_URI']):
                print('No development database is present!')
    manager.run()
