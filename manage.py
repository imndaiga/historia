#!/usr/bin/env python

from app import create_app, db
from app.models import Person, Node
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
import os

app = create_app(os.getenv('MIMINANI_CONFIG') or 'default')

# Instantiate extensions that modify app-runtimes here
manager = Manager(app)
migrate = Migrate(app, db)

# Attach functions to app-runtime flags
def make_shell_context():
	if app.config['DEBUG']:
		if not os.path.exists(app.config['SQLALCHEMY_DATABASE_URI']):
			db.create_all()
	return dict(db=db, Person=Person, Node=Node, app=app)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()