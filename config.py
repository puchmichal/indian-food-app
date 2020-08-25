import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "this-really-needs-to-be-changed"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL",
                                             'sqlite:///' + os.path.join(basedir, 'app.db'))
