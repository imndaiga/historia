#!/usr/bin/env python3

from app import create_app, db
from app.email import send_email
from app.models import Node, GlobalEdge, GlobalGraph
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
import os
from datetime import date

app = create_app(os.getenv('MIMINANI_CONFIG') or 'default')

# Instantiate extensions that modify app-runtimes here
manager = Manager(app)
migrate = Migrate(app, db)

class Forge:
	@staticmethod
	@manager.command
	def seed():
		"""Seed fake family tree data"""
		if app.config['DEBUG']:
			n1 = Node(baptism_name='Chris', email='chris@family.com', dob=date(1900,11,1))
			n2 = Node(baptism_name='Christine', email='christine@family.com', dob=date(1910,12,2))
			n3 = Node(baptism_name='Charlie', email='charlie@family.com', dob=date(1925,10,3))
			n4 = Node(baptism_name='Carol', email='carol@family.com', dob=date(1930,8,4))
			links = {
				1: [n1,n2,1],
				2: [n1,n3,3],
				3: [n1,n4,3],
				4: [n2,n3,3],
				5: [n2,n4,3],
				6: [n3,n4,2]
			}
			db.session.add_all([n1,n2,n3,n4])
			result = Node.seed_node_family(links)
			return result
		return None

	@staticmethod
	def link_new_member(*args, **kwargs):
		if kwargs['type']=='daughter':
			links = {
				1:[args[0],args[4],3],
				2:[args[1],args[4],3],
				3:[args[2],args[4],2],
				4:[args[3],args[4],2]
			}
			db.session.add(args[4])
			Node.seed_node_family(links)
		elif kwargs['type']=='wife':
			link = {
				1:[args[0],args[1],1]
			}
			db.session.add(args[1])
			Node.seed_node_family(link)
		elif kwargs['type']=='child':
			links = {
				1:[args[0],args[2],3],
				2:[args[1],args[2],3]
			}
			db.session.add_all([args[1],args[2]])
			Node.seed_node_family(links)

	@staticmethod
	def count_edge_labels(**kwargs):
		data = kwargs['data']
		counts={}
		for index,edge in enumerate(data):
			if counts.get(data[index][2]['label']):
				counts[data[index][2]['label']]=counts[data[index][2]['label']]+1
			else:
				counts[data[index][2]['label']]=1
		return counts

@manager.command
def test():
	"""Run the unit tests."""
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)

# Attach functions to app-runtime flags
def make_shell_context():
	return dict(db=db, Node=Node, GlobalEdge=GlobalEdge, GlobalGraph=GlobalGraph, app=app, send_email=send_email, Forge=Forge)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	with app.app_context():
		basedir = os.path.abspath(os.path.dirname(__file__))
		if app.config['DEBUG'] and (basedir in app.config['SQLALCHEMY_DATABASE_URI']):
			if not os.path.exists('data-dev.sqlite'):
				print('No development database present')
	manager.run()