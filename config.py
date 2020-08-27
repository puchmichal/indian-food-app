import os

basedir = os.path.abspath(os.path.dirname(__file__))


class LocalConfig(object):
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "this-really-needs-to-be-changed"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
    USER_APP_NAME = "WM-Hindus"
    USER_ENABLE_EMAIL = False
    USER_ENABLE_USERNAME = True
    USER_REQUIRE_RETYPE_PASSWORD = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(object):
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "this-really-needs-to-be-changed"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    USER_APP_NAME = "WM-Hindus"
    USER_ENABLE_EMAIL = False
    USER_ENABLE_USERNAME = True
    USER_REQUIRE_RETYPE_PASSWORD = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
