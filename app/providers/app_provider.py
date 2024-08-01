# import dash_bootstrap_components as dbc
import os
import flask
from dash import Dash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from config import constants
from app.providers.auth_provider import get_auth_blueprint, setup_login_routes, user_loader
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# app
app = flask.Flask(__name__)
app.template_folder = "../../resources/templates"
app.config.update(PREFERRED_URL_SCHEME="https")
app.secret_key = constants.APP_SECRET_KEY
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = constants.DATABASE_URL

# security
Talisman(app, content_security_policy=None)
CSRFProtect(app)


# database
app.config["SQLALCHEMY_DATABASE_URI"] = constants.DATABASE_URL
db = SQLAlchemy(app)
migrate = Migrate(app, db, directory="database/migrations")

# azure login
blueprint = get_auth_blueprint()
app.register_blueprint(blueprint, url_prefix="/login")
setup_login_routes(app)

# login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "azure.login"
login_manager.user_loader(user_loader)

# app base path
app_path = os.path.dirname(os.path.abspath(__file__)).replace("/app/providers", "")

# dash app
dash_app = Dash(
    __name__,
    use_pages=True,
    pages_folder=f"{app_path}/resources/pages",
    assets_folder=f"{app_path}/assets",
    server=app,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        "https://fonts.google.com/specimen/Open+Sans",
    ],
    external_scripts=[],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"name": "apple-mobile-web-app-capable", "content": "yes"},
    ],
)
dash_app.title = "Dashboard"
