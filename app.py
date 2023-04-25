from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes.router import router
from database.db import db
from flask_migrate import Migrate
import os

# create the app
app = Flask(__name__)

# configure the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exams.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize the database
db.init_app(app)

# initialize the migration engine
migrate = Migrate(app, db)


# register the blueprints
app.register_blueprint(router) # Add routes from main router to app
