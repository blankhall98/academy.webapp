from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize database
db = SQLAlchemy()
app = Flask(__name__)