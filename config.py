import os


# Project root
BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)


# Instance directory
INSTANCE_DIR = os.path.join(
    BASE_DIR,
    "instance"
)


# Create the instance directory if it doesn't exist
os.makedirs(
    INSTANCE_DIR,
    exist_ok=True
)


class Config:

    # ==========================================
    # SECURITY
    # ==========================================

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "apex-development-secret-key"
    )


    # ==========================================
    # DATABASE
    # ==========================================

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(
            INSTANCE_DIR,
            "acg.db"
        )
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # ==========================================
    # FILE UPLOADS
    # ==========================================

    MAX_CONTENT_LENGTH = (
        5 * 1024 * 1024
    )

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "app",
        "static",
        "uploads"
    )

    ALLOWED_EXTENSIONS = {
        "jpg",
        "jpeg",
        "png",
        "webp"
    }


    # ==========================================
    # EMAIL CONFIGURATION
    # ==========================================

    MAIL_SERVER = "smtp.gmail.com"

    MAIL_PORT = 587

    MAIL_USE_TLS = True

    MAIL_USE_SSL = False

    MAIL_USERNAME = os.environ.get(
        "MAIL_USERNAME"
    )

    MAIL_PASSWORD = os.environ.get(
        "MAIL_PASSWORD"
    )

    MAIL_DEFAULT_SENDER = os.environ.get(
        "MAIL_DEFAULT_SENDER",
        "Apex Citizens of Ghana"
    )


    # ==========================================
    # ADMIN EMAIL
    # ==========================================

    ADMIN_EMAIL = os.environ.get(
        "ADMIN_EMAIL"
    )