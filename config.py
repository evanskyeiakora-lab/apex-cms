import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "acg.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_FOLDER = "app/static/uploads"
NEWS_UPLOAD_FOLDER = "app/static/uploads/news"
GALLERY_UPLOAD_FOLDER = "app/static/uploads/gallery"
SLIDER_UPLOAD_FOLDER = "app/static/uploads/slides"

MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}