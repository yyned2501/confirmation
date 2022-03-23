from datetime import timedelta
from os import path


class BaseConfig:
    SECRET_KEY = "YY"
    PATH = path.split(path.realpath(__file__))[0]
    JSON_AS_ASCII = False
    BOOTSTRAP_SERVE_LOCAL = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024


class LocalConfig(BaseConfig):
    DEBUG = True
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    CELERY_BROKER_URL = "redis://:yy920120@yyned2501.synology.me:6379/0"
    CELERY_RESULT_BACKEND = "redis://:yy920120@yyned2501.synology.me:6379/0"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(minutes=1)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://yy:yy920120@localhost:3306/confirmation'
    CELERY_BROKER_URL = "redis://:yy920120@localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://:yy920120@localhost:6379/0"


class ProductionConfig(BaseConfig):
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(hours=1)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:anxin@888@localhost:3306/confirmation'
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': LocalConfig
}
