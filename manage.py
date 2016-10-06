#!/usr/bin/env python

from app import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os

app = create_app(os.getenv('MIMINANI_CONFIG') or 'default')

# Instantiate extensions that modify app-runtimes here
manager = Manager(app)
migrate = Migrate(app, db)

# Attach functions to app-runtime flags
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()