from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize database
db = SQLAlchemy()
app = Flask(__name__)
migrate = Migrate()  # Initialize Flask-Migrate