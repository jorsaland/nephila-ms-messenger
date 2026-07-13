"""
Defines the function that builds the Flask app.
"""


from flasgger import Swagger
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix


from app import controller
from app.constants import OPENAPI_VERSION, SWAGGER_TITLE
from app.env_vars import EnvVars


def build_app():
    
    """
    Builds the Flask app.
    """

    app = Flask(EnvVars.APP_NAME)
    app.config['JSON_AS_ASCII'] = False
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

    app.config['SWAGGER'] = {'openapi': OPENAPI_VERSION, 'title': SWAGGER_TITLE}
    Swagger(app)

    app.add_url_rule('/health', methods=['GET'], view_func=controller.health_check)

    app.add_url_rule('/send', methods=['POST'], view_func=controller.send_mail)

    return app