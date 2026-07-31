from flask import flash


def flash_success(message):
    flash(message, "success")


def flash_error(message):
    flash(message, "danger")


def flash_warning(message):
    flash(message, "warning")


def truncate_text(text, length=100):
    if not text:
        return ""

    if len(text) <= length:
        return text

    return text[:length] + "..."


def get_settings():
    # Import here to avoid circular imports
    from app.models.settings import Settings

    return Settings.query.first()