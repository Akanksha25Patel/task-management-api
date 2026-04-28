from flask import Flask
from .extensions import db, jwt
from config import Config

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    # Register routes
    from .routes.auth import auth_bp
    from .routes.tasks import task_bp
    from .routes.users import user_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(task_bp, url_prefix="/tasks")
    app.register_blueprint(user_bp, url_prefix="/users")

    return app