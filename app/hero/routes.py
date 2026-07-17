from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import login_required

from . import hero_bp
from .forms import HeroForm

from app.extensions import db
from app.models import HeroSlide
from app.utils.file_upload import save_image


# ======================================
# Hero List
# ======================================

@hero_bp.route("/")
@login_required
def index():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    slides = (
        HeroSlide.query
        .order_by(
            HeroSlide.display_order.asc()
        )
        .paginate(
            page=page,
            per_page=10,
            error_out=False
        )
    )

    return render_template(
        "admin/hero/index.html",
        slides=slides
    )


# ======================================
# Create Slide
# ======================================

@hero_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():

    form = HeroForm()

    if form.validate_on_submit():

        filename = save_image(
            form.image.data,
            "hero"
        )

        slide = HeroSlide(
            title=form.title.data,
            subtitle=form.subtitle.data,
            image=filename,
            button_text=form.button_text.data,
            button_url=form.button_url.data,
            display_order=form.display_order.data,
            is_active=form.is_active.data
        )

        db.session.add(slide)
        db.session.commit()

        flash(
            "Hero slide created successfully.",
            "success"
        )

        return redirect(
            url_for("hero.index")
        )

    return render_template(
        "admin/hero/create.html",
        form=form
    )


# ======================================
# Edit Slide
# ======================================

@hero_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):

    slide = HeroSlide.query.get_or_404(id)

    form = HeroForm(obj=slide)

    if form.validate_on_submit():

        slide.title = form.title.data
        slide.subtitle = form.subtitle.data
        slide.button_text = form.button_text.data
        slide.button_url = form.button_url.data
        slide.display_order = form.display_order.data
        slide.is_active = form.is_active.data

        filename = save_image(
            form.image.data,
            "hero"
        )

        if filename:
            slide.image = filename

        db.session.commit()

        flash(
            "Hero slide updated successfully.",
            "success"
        )

        return redirect(
            url_for("hero.index")
        )

    return render_template(
        "admin/hero/edit.html",
        form=form,
        slide=slide
    )


# ======================================
# Delete Slide
# ======================================

@hero_bp.route("/delete/<int:id>")
@login_required
def delete(id):

    slide = HeroSlide.query.get_or_404(id)

    db.session.delete(slide)
    db.session.commit()

    flash(
        "Hero slide deleted successfully.",
        "success"
    )

    return redirect(
        url_for("hero.index")
    )