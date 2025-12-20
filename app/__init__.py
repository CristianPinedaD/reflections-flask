import json

from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import Config


def to_pretty_json(obj: dict) -> str:
    return json.dumps(obj, default=lambda o: o.__dict__, indent=4)


def page_not_found(e):
    return render_template("404.html"), 404


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

db = SQLAlchemy()
login = LoginManager()
login.login_view = "auth.login"

migrate = Migrate()
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)

    app.secret_key = config_class.SECRET_KEY
    app.jinja_env.filters["to_pretty_json"] = to_pretty_json
    app.config.from_object(config_class)
    app.static_folder = config_class.STATIC_FOLDER
    app.template_folder = config_class.TEMPLATE_FOLDER_MAIN

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)

    # blueprint registration
    from app.main import main_blueprint as main

    main.template_folder = Config.TEMPLATE_FOLDER_MAIN
    app.register_blueprint(main)

    from app.auth import auth_blueprint as auth

    auth.template_folder = Config.TEMPLATE_FOLDER_AUTH
    app.register_blueprint(auth)

    from app.errors import error_blueprint as errors

    errors.template_folder = Config.TEMPLATE_FOLDER_ERRORS
    app.register_blueprint(errors)

    return app
