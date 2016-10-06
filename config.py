import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	# App set-up environment variables
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'kabdkjb893b39*B*(SB'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USE_TLS = False
	MAIL_USE_SSL = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

	# App context environment variables
	MIMINANI_MAIL_SUBJECT_PREFIX = '[MIMINANI]'
	MIMINANI_MAIL_SENDER = 'MIMINANI'
	MIMINANI_ADMIN = os.environ.get('MIMINANI_ADMIN')

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
		'sqlite:///'+os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
		'sqlite:///'+os.path.join(basedir, 'data-test.sqlite')
	# Disable Cross-Site-Request-Forgery Protection to enable Flask-Test and Selenium
	# testing suites to function properly
	WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///'+os.path.join(basedir, 'data.sqlite')

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
}

	