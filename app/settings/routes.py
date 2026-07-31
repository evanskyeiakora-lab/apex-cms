from flask import (
    render_template,
    redirect,
    url_for,
    request
)
from flask_login import login_required

from . import settings_bp
from .forms import SettingsForm

from app.models import Settings

from app.utils.database import (
    save,
    commit
)

from app.utils.file_upload import (
    replace_image
)

from app.utils.helpers import (
    flash_success
)

from app.utils.constants import SETTINGS_FOLDER


# ==========================================
# Site Settings
# ==========================================

@settings_bp.route("/", methods=["GET", "POST"])
@login_required
def index():

    print("=" * 60)
    print("REQUEST METHOD:", request.method)

    settings = Settings.query.first()

    if not settings:
        settings = Settings(site_name="Apex Citizens of Ghana")
        save(settings)

    form = SettingsForm(obj=settings)

    print("FORM VALID:", form.validate_on_submit())

    if form.validate_on_submit():

        print("===== FORM DATA =====")
        print("Site Name:", form.site_name.data)
        print("Email:", form.email.data)
        print("Phone:", form.phone.data)

        settings.site_name = form.site_name.data
        settings.tagline = form.tagline.data
        settings.about = form.about.data

        settings.email = form.email.data
        settings.phone = form.phone.data
        settings.whatsapp = form.whatsapp.data
        settings.address = form.address.data

        settings.facebook = form.facebook.data
        settings.instagram = form.instagram.data
        settings.twitter = form.twitter.data
        settings.youtube = form.youtube.data
        settings.linkedin = form.linkedin.data

        settings.footer_text = form.footer_text.data
        settings.copyright_text = form.copyright_text.data

        settings.google_map = form.google_map.data

        settings.meta_title = form.meta_title.data
        settings.meta_description = form.meta_description.data
        settings.meta_keywords = form.meta_keywords.data

        settings.maintenance_mode = form.maintenance_mode.data

        settings.logo = replace_image(
            settings.logo,
            form.logo.data,
            SETTINGS_FOLDER
        )

        settings.favicon = replace_image(
            settings.favicon,
            form.favicon.data,
            SETTINGS_FOLDER
        )

        commit()

        print("===== AFTER COMMIT =====")
        print("Site Name:", settings.site_name)
        print("Email:", settings.email)
        print("Phone:", settings.phone)

        flash_success("Website settings updated successfully.")

        return redirect(url_for("settings.index"))

    if request.method == "POST":
        print("===== FORM ERRORS =====")
        print(form.errors)

        return render_template(
        "admin/settings/index.html",
        form=form,
        settings=settings
    )
        # -----------------------------
        # Logo
        # -----------------------------
        settings.logo = replace_image(
            settings.logo,
            form.logo.data,
            SETTINGS_FOLDER
        )

        # -----------------------------
        # Favicon
        # -----------------------------
        settings.favicon = replace_image(
            settings.favicon,
            form.favicon.data,
            SETTINGS_FOLDER
        )

        commit()

        flash_success(
            "Website settings updated successfully."
        )

        return redirect(
            url_for("settings.index")
        )

    return render_template(
        "admin/settings/index.html",
        form=form,
        settings=settings
    )