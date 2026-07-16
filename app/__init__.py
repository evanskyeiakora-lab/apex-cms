from flask import Flask, app
from datetime import datetime

from config import Config
from .extensions import db, migrate, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
   # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

# Flask-Login configuration
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    # Import models
    from . import models

    # Register blueprints
    from .main import main_bp
    from .auth import auth_bp
    from .admin import admin_bp
    from .news import news_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(news_bp)

    @app.context_processor
    def inject_now():
        return {
            "current_year": datetime.now().year
        }

   

    return app