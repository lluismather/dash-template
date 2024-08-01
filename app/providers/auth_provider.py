
from flask import redirect, session, url_for, render_template, request
import flask
from dash import get_asset_url
from flask_dance.contrib.azure import azure, make_azure_blueprint
from config import constants
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
import hashlib
import base64
from sqlalchemy import or_
from flask_login import current_user, logout_user


def get_auth_blueprint():
    return make_azure_blueprint(
        client_id=constants.AZURE_CLIENT_ID,
        client_secret=constants.AZURE_CLIENT_SECRET,
        tenant=constants.AZURE_TENANT_ID,
        scope=["openid", "email", "profile", "User.Read", "Group.Read.All"],
        redirect_to="azure_callback",
    )


def login_required(func):
    def check_authorization(*args, **kwargs):
        path = request.path
        excluded_paths = constants.AUTH_EXCLUDED_PATHS
        if path in excluded_paths:
            return func(*args, **kwargs)
        print(current_user)
        if (not azure.authorized or azure.token.get("expires_in", 1) < 0) and not current_user.is_authenticated:
            return redirect("/login")
        else:
            return func(*args, **kwargs)

    return check_authorization


def setup_login_routes(app):
    # main login page
    @app.route("/login", methods=["GET", "POST"])
    def login():
        from app.models.users import User
        from flask_login import login_user

        if current_user.is_authenticated:
            return redirect(constants.APP_URL)

        azure_url = url_for("azure.login")

        if "error" in request.args:
            return render_template(
                "login.html",
                form=login_form(),
                errors=["Invalid login"],
                azure_url=azure_url,
            )

        if azure.authorized:
            return redirect(url_for("azure_callback"))

        if request.method == "GET":
            return render_template(
                "login.html",
                form=login_form(),
                azure_url=azure_url,
            )

        email = request.form["email"].strip().lower()
        password = make_password_hash(request.form["password"].strip())
        user = User().query.filter(
            or_(
                User.email == email,
                User.slug == email,
            ),
        ).first()

        if (user and user.password == password):
            login_user(user)
            return redirect(constants.APP_URL)

        return redirect(url_for("login", error="Invalid login"))

    # azure callback
    @app.route("/azure/callback")
    def azure_callback():
        if not azure.authorized or azure.token.get("expires_in") < 0:
            return redirect(url_for("azure.login"))

        token = azure.token["access_token"]
        find_or_create_user(token)
        return redirect(constants.APP_URL)

    # logout logic
    @app.route("/logout")
    def logout():
        if azure.authorized:
            post_logout_redirect_uri = f"{constants.APP_URL}/login"
            if "azure_oauth_token" in session:
                session.pop("azure_oauth_token")
            azure_logout_url = f"https://login.microsoftonline.com/{constants.AZURE_TENANT_ID}/oauth2/logout?client_id={constants.AZURE_CLIENT_ID}&post_logout_redirect_uri={post_logout_redirect_uri}"  # noqa
            return redirect(azure_logout_url)
        else:
            logout_user()
            return redirect(constants.APP_URL)
    

def login_form():
    class LoginForm(FlaskForm):
        email = StringField("Name or Email", validators=[DataRequired(), Email()])
        password = PasswordField("Password", validators=[DataRequired()])
        submit = SubmitField("Submit")
    return LoginForm()


def find_or_create_user(token):
    from app.models.users import User
    from app.models.oauth import OAuth
    from app.models.roles import Role
    from app.models.role_user import RoleUser
    from sqlalchemy.orm.exc import NoResultFound
    from app.providers.app_provider import db
    from flask_login import login_user
    from slugify import slugify

    u = azure.get("/v1.0/me").json()
    user_id = u["id"]

    blueprint = get_auth_blueprint()
    query = OAuth.query.filter_by(provider=blueprint.name, provider_user_id=user_id)
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(provider=blueprint.name, provider_user_id=user_id, token=token)

    if oauth.user:
        user = oauth.user
        login_user(user)
    else:
        user = User(
            email=u["mail"], 
            name=u["displayName"], 
            slug=slugify(u["displayName"]),
            azure_id=user_id,
        )
        oauth.user = user
        db.session.add_all([user, oauth])
        db.session.commit()
        login_user(user)
    
    # add admin role
    if not user.roles:
        admin = Role.query.filter_by(name="admin").first()
        role_user = RoleUser(user_id=user.id, role_id=admin.id)
        db.session.add(role_user)
        db.session.commit()

    return False


def user_loader(user_id):
    from app.models.users import User
    return User.query.get(user_id)


def make_password_hash(password):
    seed = f"{password.strip()}{constants.APP_SECRET_KEY.strip()}"
    hashobj = hashlib.sha256(seed.encode("utf-8"))
    return base64.b64encode(hashobj.digest()).decode("utf-8")
