from flask import Flask

from notifications.config import Config
from notifications.routes.health import health_bp
from notifications.routes.two_factor import two_factor_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(health_bp)
    app.register_blueprint(two_factor_bp)
    return app

