from app.models import Settings


def inject_settings():
    """
    Make the website settings available
    in every Jinja template.
    """

    settings = Settings.query.first()

    return {
        "settings": settings
    }