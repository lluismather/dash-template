
from flask import redirect, session, url_for
from flask_dance.contrib.azure import azure, make_azure_blueprint
from config import constants


def get_auth_blueprint():
    blueprint = make_azure_blueprint(
        client_id=constants.AZURE_CLIENT_ID,
        client_secret=constants.AZURE_CLIENT_SECRET,
        tenant=constants.AZURE_TENANT_ID,
        scope=["openid", "email", "profile", "User.Read", "Group.Read.All"],
        redirect_to="azure_callback",
    )
    return blueprint


def login_required(func):
    def check_authorization(*args, **kwargs):
        if not azure.authorized or azure.token.get("expires_in") < 0:
            return redirect(url_for("azure.login"))
        else:
            return func(*args, **kwargs)

    return check_authorization


def setup_login_routes(app):
    
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
        post_logout_redirect_uri = constants.APP_URL + "/login"
        if "azure_oauth_token" in session:
            session.pop("azure_oauth_token")
        azure_logout_url = f"https://login.microsoftonline.com/{constants.AZURE_TENANT_ID}/oauth2/logout?client_id={constants.AZURE_CLIENT_ID}&post_logout_redirect_uri={post_logout_redirect_uri}"  # noqa
        return redirect(azure_logout_url)


def find_or_create_user(token):
    from app.models.users import User
    from app.models.oauth import OAuth
    from sqlalchemy.orm.exc import NoResultFound
    from app.providers.app_provider import db
    from flask_login import login_user

    u = azure.get("/v1.0/me").json()
    user_id = u["id"]

    blueprint = get_auth_blueprint()
    query = OAuth.query.filter_by(provider=blueprint.name, provider_user_id=user_id)
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(provider=blueprint.name, provider_user_id=user_id, token=token)

    if oauth.user:
        login_user(oauth.user)
    else:
        user = User(
            email=u["mail"], 
            name=u["displayName"], 
            azure_id=user_id,
        )
        oauth.user = user
        db.session.add_all([user, oauth])
        db.session.commit()
        login_user(user)

    return False
