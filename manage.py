#!/usr/bin/env python

from app import create_app, db
from app.models import Node, Edge
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
import os
from datetime import date

app = create_app(os.getenv('MIMINANI_CONFIG') or 'default')

# Instantiate extensions that modify app-runtimes here
manager = Manager(app)
migrate = Migrate(app, db)

# Attach functions to app-runtime flags
def make_shell_context():
	return dict(db=db, Node=Node, Edge=Edge, app=app)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def forge():
	"""Seed fake family tree data"""
	if app.config['DEBUG']:
		n1 = Node(baptism_name='John', dob=date(1901,1,1))
		n2 = Node(baptism_name='Mary', dob=date(1902,2,2))
		n3 = Node(baptism_name='Jack', dob=date(1910,3,3))
		n4 = Node(baptism_name='Mark', dob=date(1920,4,4))
		links = {
			1:[n1,n2,0],
			2:[n1,n3,1],
			3:[n1,n4,1],
			4:[n2,n4,1],
			5:[n2,n3,1],
			6:[n3,n4,0]
		}
		Node.seed_node_family(links)
		return links
	return None


@manager.command
def test():
	"""Run the unit tests."""
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
	with app.app_context():
		basedir = os.path.abspath(os.path.dirname(__file__))
		if app.config['DEBUG'] and (basedir in app.config['SQLALCHEMY_DATABASE_URI']):
			if not os.path.exists('data-dev.sqlite'):
				print('No development database present')
	manager.run()