import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import models
from db import db

from resources.items import blp as ItemBluePrint
from resources.store import blp as StoreBluePrint
from resources.category import blp as CategoryBluePrint
from resources.user import blp as UserBluePrint


def create_app(db_url=None):
    """
    Create app
    :param db_url: database url
    :return: flask app
    """
    app = Flask(__name__)

    # configs for Swagger Documentation
    app.config["API_TITLE"] = "Shopify Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True

    db.init_app(app)  # connect flask app with sqlalchemy

    migrate = Migrate(app, db)

    # Flask smorest extension around Flask
    api = Api(app)

    # jwt secret key
    # generate using secrets str(secrets.SystemRandom().getrandbits(128)).
    app.config["JWT_SECRET_KEY"] = "41114230394179597564573606699191778625"
    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    # Create database schemas at first request
    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBluePrint)
    api.register_blueprint(StoreBluePrint)
    api.register_blueprint(CategoryBluePrint)
    api.register_blueprint(UserBluePrint)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
