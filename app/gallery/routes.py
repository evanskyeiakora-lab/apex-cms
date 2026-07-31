from flask import (
    render_template,
    redirect,
    url_for,
    request,
    current_app
)

from flask_login import login_required

from . import gallery_bp
from .forms import GalleryForm

from app.models import Gallery

from app.utils.database import (
    save,
    commit,
    delete
)

from app.utils.file_upload import (
    replace_image,
    delete_image
)

from app.utils.helpers import flash_success

from app.utils.constants import GALLERY_FOLDER


# ==========================================
# Gallery List
# ==========================================
@gallery_bp.route("/")
@login_required
def index():

    search = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)

    query = Gallery.query

    if search:
        query = query.filter(
            Gallery.title.ilike(f"%{search}%")
        )

    galleries = query.order_by(
        Gallery.display_order.asc(),
        Gallery.created_at.desc()
    ).paginate(
        page=page,
        per_page=12,
        error_out=False
    )

    return render_template(
        "admin/gallery/index.html",
        galleries=galleries,
        search=search
    )


# ==========================================
# Create Gallery Image
# ==========================================
@gallery_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():

    form = GalleryForm()

    if form.validate_on_submit():

        gallery = Gallery(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            display_order=form.display_order.data,
            is_featured=form.is_featured.data,
        status=form.status.data        
        )

        gallery.generate_slug()

        gallery.image = replace_image(
            None,
            form.image.data,
            GALLERY_FOLDER
        )

        save(gallery)

        flash_success(
            "Gallery image added successfully."
        )

        return redirect(
            url_for("gallery.index")
        )

    if request.method == "POST":
        current_app.logger.warning(form.errors)

    return render_template(
        "admin/gallery/create.html",
        form=form
    )


# ==========================================
# Edit Gallery Image
# ==========================================
@gallery_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):

    gallery = Gallery.query.get_or_404(id)

    form = GalleryForm(obj=gallery)

    if form.validate_on_submit():

        gallery.title = form.title.data
        gallery.description = form.description.data
        gallery.category = form.category.data
        gallery.display_order = form.display_order.data
        gallery.is_featured = form.is_featured.data
        gallery.status = form.status.data
        gallery.generate_slug()

        gallery.image = replace_image(
            gallery.image,
            form.image.data,
            GALLERY_FOLDER
        )

        commit()

        flash_success(
            "Gallery updated successfully."
        )

        return redirect(
            url_for("gallery.index")
        )

    return render_template(
        "admin/gallery/edit.html",
        form=form,
        gallery=gallery
    )


# ==========================================
# Delete Gallery Image
# ==========================================
@gallery_bp.route("/delete/<int:id>")
@login_required
def remove(id):

    gallery = Gallery.query.get_or_404(id)

    delete_image(
        gallery.image,
        GALLERY_FOLDER
    )

    delete(gallery)

    flash_success(
        "Gallery image deleted successfully."
    )

    return redirect(
        url_for("gallery.index")
    )