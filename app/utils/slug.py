import re

from slugify import slugify


def generate_unique_slug(model, title):
    """
    Generate a unique slug for a model.
    """

    base_slug = slugify(title)
    slug = base_slug
    counter = 1

    while model.query.filter_by(slug=slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug