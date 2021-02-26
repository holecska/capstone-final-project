import os
class Config(object):
    DEBUG =  os.getenv('DEBUG', 'False')

    DB_NAME = os.getenv('DB_NAME', 'capstone')
    DB_USERNAME = os.getenv('DB_USERNAME', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'admin')
    DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
    DB_PATH = "postgresql://{}:{}@{}/{}".format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME)
