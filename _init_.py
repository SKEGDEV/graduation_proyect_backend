'''
Hello and welcome to my REST API, this API use bcrypt to encrypt and decrypt the password, and pyjwt to use json web tokens to validate the
user and validate session tokens.
'''
#Flask initialization
from logging import debug
from flask import Flask
#Database initialization
from database import mysql
#environment variables
from os import getenv
from dotenv import load_dotenv
#CORS initialization
from flask_cors import CORS
#Blueprint initializations

#App config
app = Flask(__name__)
CORS(app)

#Database config
app.config['MYSQL_DATABASE_HOST'] = getenv("host")
app.config['MYSQL_DATABASE_USER'] = getenv("user")
app.config['MYSQL_DATABASE_PASSWORD'] = getenv("password")
app.config['MYSQL_DATABASE_DB'] = getenv("database")
mysql.init_app(app)

#blueprint config


#Server config
if __name__ == '__main__':
    load_dotenv()
    app.run(port=getenv('server_port'), host=getenv('server_host'), debug=True)
