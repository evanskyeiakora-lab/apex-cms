from flask import (
    render_template,
    request
)

from flask_login import login_required

from . import users_bp

from app.models import User


# ==========================================
# Users List
# ==========================================

@users_bp.route("/")
@login_required
def index():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    search = request.args.get(
        "search",
        ""
    ).strip()

    query = User.query

    if search:

        query = query.filter(
            User.first_name.ilike(f"%{search}%") |
            User.last_name.ilike(f"%{search}%") |
            User.username.ilike(f"%{search}%") |
            User.email.ilike(f"%{search}%")
        )

    users = (
        query
        .order_by(User.first_name.asc())
        .paginate(
            page=page,
            per_page=10,
            error_out=False
        )
    )
    

    return render_template(
        "admin/users/index.html",
        users=users,
        search=search
    )
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.extensions import db

from .forms import UserForm

from app.utils.file_upload import save_image

# ==========================================
# Create User
# ==========================================

@users_bp.route(
    "/create",
    methods=["GET", "POST"]
)
@login_required
def create():

    form = UserForm()

    if form.validate_on_submit():

        # Check username
        if User.query.filter_by(
            username=form.username.data
        ).first():

            flash(
                "Username already exists.",
                "danger"
            )

            return render_template(
                "admin/users/create.html",
                form=form
            )

        # Check email
        if User.query.filter_by(
            email=form.email.data
        ).first():

            flash(
                "Email address already exists.",
                "danger"
            )

            return render_template(
                "admin/users/create.html",
                form=form
            )

        filename = None

        if form.photo.data:

            filename = save_image(
                form.photo.data,
                "users"
            )

        user = User(

            first_name=form.first_name.data,

            last_name=form.last_name.data,

            username=form.username.data,

            email=form.email.data,

            phone=form.phone.data,

            photo=filename,

            role=form.role.data,

            is_active=form.is_active.data

        )

        user.set_password(
            form.password.data
        )

        db.session.add(user)

        db.session.commit()

        flash(
            "User created successfully.",
            "success"
        )

        return redirect(
            url_for("users.index")
        )

    return render_template(
        "admin/users/create.html",
        form=form
    )