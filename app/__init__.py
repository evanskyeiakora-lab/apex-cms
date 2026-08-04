from flask import Flask
from datetime import datetime

from config import Config
from .extensions import db, migrate, login_manager
from app.context_processors import inject_settings


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Flask-Login Configuration
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    # Import Blueprints
    from .main import main_bp
    from .auth import auth_bp
    from .admin import admin_bp
    from .news import news_bp
    from .hero import hero_bp
    from .gallery import gallery_bp
    from .members import members_bp
    from .contact import contact_bp
    from .settings import settings_bp
    from .pages import pages_bp
    from .events import events_bp

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(news_bp)
    app.register_blueprint(hero_bp)
    app.register_blueprint(gallery_bp)
    app.register_blueprint(members_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(events_bp)

    # Global Context Processors
    app.context_processor(inject_settings)

    @app.context_processor
    def inject_now():
        return {
            "current_year": datetime.now().year
        }

    return app