import os

from app.main.converters import IntegerConverter
from config import configs
from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.markdown import Markdown
from flask.ext.moment import Moment
from flask.ext.pagedown import PageDown
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap


db = SQLAlchemy()
moment = Moment()
bootstrap = Bootstrap()
pagedown = PageDown()
login_manager = LoginManager()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs[config])
    db.init_app(app)

    moment.init_app(app)
    Markdown(app)
    bootstrap.init_app(app)
    pagedown.init_app(app)
    login_manager.init_app(app)

    # default integer converter do not support negative numbers
    app.url_map.converters['integer'] = IntegerConverter
    login_manager.login_view = "main.login"

    from .main.views import main as main_blueprint
    from .auth.views import auth as auth_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    return app
