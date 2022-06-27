from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object(Config)
    app.app_context().push()
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app
