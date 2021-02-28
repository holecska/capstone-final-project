DEBUG =  False
DB_NAME ='capstone'
DB_USERNAME = 'postgres'
DB_PASSWORD = 'admin'
DB_HOST = '127.0.0.1:5432'
DB_PATH = "postgresql://{}:{}@{}/{}".format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME)
