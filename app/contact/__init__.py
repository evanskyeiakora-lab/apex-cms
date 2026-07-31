from flask import Blueprint

contact_bp = Blueprint(
    "contact",
    __name__,
    url_prefix="/admin/contact"
)

from . import routes