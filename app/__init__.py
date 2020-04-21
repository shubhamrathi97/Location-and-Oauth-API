from flask import Flask

from Location.views import location_api
from Oauth.views import oauth_api
from .model import db

# Define App
app = Flask(__name__)

# Configuring app from config.py file
app.config.from_object('config')
app.init(db)
app.register_blueprint(oauth_api)
app.register_blueprint(location_api)
