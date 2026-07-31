import os
import uuid

from flask import current_app
from werkzeug.utils import secure_filename


def allowed_file(filename):
    """
    Check whether the uploaded file has an allowed extension.
    """
    if not filename or "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in current_app.config["ALLOWED_EXTENSIONS"]


def generate_unique_filename(filename):
    """
    Generate a unique filename while preserving the original extension.
    """
    extension = filename.rsplit(".", 1)[1].lower()
    return f"{uuid.uuid4().hex}.{extension}"


def save_image(file, folder):
    """
    Save an uploaded image and return the stored filename.
    """
    if not file or file.filename == "":
        return None

    if not allowed_file(file.filename):
        raise ValueError("Unsupported image format.")

    filename = generate_unique_filename(
        secure_filename(file.filename)
    )

    upload_folder = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        folder
    )

    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(upload_folder, filename)

    file.save(filepath)

    return filename


def delete_image(filename, folder):
    """
    Delete an image from disk.
    """
    if not filename:
        return

    filepath = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        folder,
        filename
    )

    if os.path.exists(filepath):
        os.remove(filepath)


def replace_image(old_image, new_file, folder):
    """
    Replace an existing image with a newly uploaded one.
    """
    if not new_file or new_file.filename == "":
        return old_image

    delete_image(old_image, folder)

    return save_image(new_file, folder)