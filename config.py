import os

# Project root
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Instance directory
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")

# Create the instance directory if it doesn't exist
os.makedirs(INSTANCE_DIR, exist_ok=True)

print("DATABASE =", "sqlite:///" + os.path.join(INSTANCE_DIR, "acg.db"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "apex-development-secret-key")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL",
    "sqlite:///" + os.path.join(INSTANCE_DIR, "acg.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static", "uploads")

    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}