from flask import (
    render_template,
    redirect,
    url_for,
    request
)

from . import settings_bp
from .forms import SettingsForm

from app.models import Settings

from app.utils.database import (
    save,
    commit
)

from app.utils.file_upload import replace_image

from app.utils.helpers import flash_success

from app.utils.constants import SETTINGS_FOLDER

from app.utils.permissions import super_admin_required


# ==========================================
# Site Settings
# ==========================================

@settings_bp.route(
    "/",
    methods=["GET", "POST"]
)
@super_admin_required
def index():

    # --------------------------------------
    # Get existing settings
    # --------------------------------------

    settings = Settings.query.first()

    # --------------------------------------
    # Create default settings if necessary
    # --------------------------------------

    if not settings:

        settings = Settings(
            site_name="Apex Citizens of Ghana"
        )

        save(settings)

    # --------------------------------------
    # Settings form
    # --------------------------------------

    form = SettingsForm(
        obj=settings
    )

    # --------------------------------------
    # Process form
    # --------------------------------------

    if form.validate_on_submit():

        # ==================================
        # General Information
        # ==================================

        settings.site_name = (
            form.site_name.data
        )

        settings.tagline = (
            form.tagline.data
        )

        settings.about = (
            form.about.data
        )


        # ==================================
        # Contact Information
        # ==================================

        settings.email = (
            form.email.data
        )

        settings.phone = (
            form.phone.data
        )

        settings.whatsapp = (
            form.whatsapp.data
        )

        settings.address = (
            form.address.data
        )


        # ==================================
        # Social Media
        # ==================================

        settings.facebook = (
            form.facebook.data
        )

        settings.instagram = (
            form.instagram.data
        )

        settings.twitter = (
            form.twitter.data
        )

        settings.youtube = (
            form.youtube.data
        )

        settings.linkedin = (
            form.linkedin.data
        )


        # ==================================
        # Footer
        # ==================================

        settings.footer_text = (
            form.footer_text.data
        )

        settings.copyright_text = (
            form.copyright_text.data
        )


        # ==================================
        # Google Map
        # ==================================

        settings.google_map = (
            form.google_map.data
        )


        # ==================================
        # SEO
        # ==================================

        settings.meta_title = (
            form.meta_title.data
        )

        settings.meta_description = (
            form.meta_description.data
        )

        settings.meta_keywords = (
            form.meta_keywords.data
        )


        # ==================================
        # Maintenance Mode
        # ==================================

        settings.maintenance_mode = (
            form.maintenance_mode.data
        )


        # ==================================
        # Logo
        # ==================================

        settings.logo = replace_image(
            settings.logo,
            form.logo.data,
            SETTINGS_FOLDER
        )


        # ==================================
        # Favicon
        # ==================================

        settings.favicon = replace_image(
            settings.favicon,
            form.favicon.data,
            SETTINGS_FOLDER
        )


        # ==================================
        # Save Changes
        # ==================================

        commit()

        flash_success(
            "Website settings updated successfully."
        )

        return redirect(
            url_for("settings.index")
        )


    # ======================================
    # Render Form
    # ======================================

    return render_template(
        "admin/settings/index.html",
        form=form,
        settings=settings
    )