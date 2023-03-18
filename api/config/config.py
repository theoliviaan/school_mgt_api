import os
from decouple import config
from datetime import timedelta
from api import create_app


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class Config:
    SECRET_KEY = config("SECRET_KEY", "secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REQUEST_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_SECRET_KEY = config("JWT_SECRET_KEY")


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" +os.path.join(BASE_DIR, "school_mgt.db")


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class ProdConfig(Config):
    # uri = config("DATABASE_URL")
    # if uri.startswith("postgres://"):
    #     uri = uri.replace("postgres://", "postgresql://", 1)
    #
    # SQLALCHEMY_DATABASE_URI = uri
    DEBUG = config("DEBUG", False, cast=bool)
    SQLALCHEMY_ECHO = False


config_dict = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "test": TestConfig
}