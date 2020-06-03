import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
DATABASE_URL = 'postgres://postgres:1991@localhost:5432/fyyur'



# TODO IMPLEMENT DATABASE URL
#SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']#
SQLALCHEMY_TRACK_MODIFICATIONS = False#
#SQLALCHEMY_DATABASE_URI = database_uri