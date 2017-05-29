import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # App set-up environment variables
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kabdkjb893b39*B*(SB'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp-relay.sendinblue.com'
    MAIL_PORT = os.environ.get('MAIL_PORT') or 587
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SEED_AUTO = os.environ.get('SEED_AUTO')

    # App context environment variables
    HISTORIA_MAIL_SUBJECT_PREFIX = '[HISTORIA]'
    HISTORIA_MAIL_SENDER = 'HISTORIA <admin@historia.com>'
    HISTORIA_ADMIN = os.environ.get('HISTORIA_ADMIN')

    HISTORIA_GRAPHIQL = True

    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
    RECAPTCHA_DATA_ATTRS = {'size': 'normal'}

    BOOTSTRAP_SERVE_LOCAL = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data', 'data-dev.sqlite')
    GRAPH_PATH = os.environ.get('DEV_GRAPH_PATH') or os.path.join(
        basedir, 'data', 'graph-dev.gpickle')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data', 'data-test.sqlite')
    GRAPH_PATH = os.environ.get('TEST_GRAPH_PATH') or os.path.join(
        basedir, 'data', 'graph-test.gpickle')
    # Disable Cross-Site-Request-Forgery Protection to enable
    # Flask-Test and Selenium testing suites to function properly
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data', 'data.sqlite')
    GRAPH_PATH = os.environ.get('GRAPH_PATH') or os.path.join(
        basedir, 'data', 'graph.gpickle')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
