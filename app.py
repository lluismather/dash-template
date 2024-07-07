from werkzeug.middleware.proxy_fix import ProxyFix

from app.providers.app_provider import app, dash_app, db
from app.providers.auth_provider import login_required
from config import constants
from resources.layouts import template

server = dash_app.server

dash_app.layout = template.layout()
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

for view_func in app.view_functions:
    if not view_func.startswith("azure"):
        app.view_functions[view_func] = login_required(app.view_functions[view_func])

if __name__ == "__main__":
    dash_app.run(
        host=constants.APP_HOST, 
        port=constants.APP_PORT,
        debug=constants.APP_DEBUG,
    )
