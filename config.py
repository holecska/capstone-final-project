import os

class Config(object):
    DEBUG = os.getenv('DEBUG', 'False')

    DB_NAME = os.getenv('DB_NAME', 'capstone')
    DB_USERNAME = os.getenv('DB_USERNAME', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'admin')
    DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI =  os.getenv('DATABASE_URL')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}/{}".format(
                                                        Config.DB_USERNAME,
                                                        Config.DB_PASSWORD,
                                                        Config.DB_HOST,
                                                        Config.DB_NAME)

class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}/{}".format(
                                                        'postgres',
                                                        'admin',
                                                        '127.0.0.1:5432',
                                                        'capstone_test')
