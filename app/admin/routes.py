from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from sqlalchemy import or_

from . import admin_bp

from app.extensions import db

from app.models import (
    User,
    News,
    HeroSlide,
    Event,
    Page,
    Gallery,
    Member,
    ContactMessage,
    MembershipApplication
)

from app.utils.permissions import admin_required

# ==========================================================
# ADMIN DASHBOARD
# ==========================================================

@admin_bp.route("/")
@admin_required
def dashboard():

    # ======================================================
    # DASHBOARD STATISTICS
    # ======================================================

    stats = {

        # --------------------------------------------------
        # NEWS
        # --------------------------------------------------

        "news": News.query.count(),

        "published_news": (
            News.query
            .filter(
                News.is_published.is_(True)
            )
            .count()
        ),

        "draft_news": (
            News.query
            .filter(
                News.is_published.is_(False)
            )
            .count()
        ),

        # --------------------------------------------------
        # HERO SLIDES
        # --------------------------------------------------

        "hero": HeroSlide.query.count(),

        # --------------------------------------------------
        # EVENTS
        # --------------------------------------------------

        "events": Event.query.count(),

        # --------------------------------------------------
        # PAGES
        # --------------------------------------------------

        "pages": Page.query.count(),

        # --------------------------------------------------
        # GALLERY
        # --------------------------------------------------

        "gallery": Gallery.query.count(),

        # --------------------------------------------------
        # MEMBERS
        # --------------------------------------------------

        "members": Member.query.count(),

        # --------------------------------------------------
        # USERS
        # --------------------------------------------------

        "users": User.query.count(),

        # --------------------------------------------------
        # CONTACT MESSAGES
        # --------------------------------------------------

        "messages": ContactMessage.query.count(),

        # --------------------------------------------------
        # MEMBERSHIP APPLICATIONS
        # --------------------------------------------------

        "membership_applications": (
            MembershipApplication.query.count()
        ),

        "approved_applications": (
            MembershipApplication.query
            .filter_by(
                status="Approved"
            )
            .count()
        ),

        "pending_applications": (
            MembershipApplication.query
            .filter_by(
                status="Pending"
            )
            .count()
        ),

        "rejected_applications": (
            MembershipApplication.query
            .filter_by(
                status="Rejected"
            )
            .count()
        )
    }


    # ======================================================
    # RECENT NEWS
    # ======================================================

    recent_news = (
        News.query
        .order_by(
            News.created_at.desc()
        )
        .limit(5)
        .all()
    )


    # ======================================================
    # RECENT EVENTS
    # ======================================================

    recent_events = (
        Event.query
        .order_by(
            Event.created_at.desc()
        )
        .limit(5)
        .all()
    )


    # ======================================================
    # RECENT CONTACT MESSAGES
    # ======================================================

    recent_messages = (
        ContactMessage.query
        .order_by(
            ContactMessage.created_at.desc()
        )
        .limit(5)
        .all()
    )


    # ======================================================
    # RECENT MEMBERS
    # ======================================================

    recent_members = (
        Member.query
        .order_by(
            Member.created_at.desc()
        )
        .limit(5)
        .all()
    )


    # ======================================================
    # RECENT GALLERY
    # ======================================================

    recent_gallery = (
        Gallery.query
        .order_by(
            Gallery.created_at.desc()
        )
        .limit(5)
        .all()
    )


    # ======================================================
    # HERO SLIDES
    # ======================================================

    recent_slides = (
        HeroSlide.query
        .order_by(
            HeroSlide.display_order.asc(),
            HeroSlide.id.asc()
        )
        .limit(5)
        .all()
    )


    # ======================================================
    # RECENT MEMBERSHIP APPLICATIONS
    # ======================================================

    recent_applications = (
        MembershipApplication.query
        .order_by(
            MembershipApplication.created_at.desc()
        )
        .limit(5)
        .all()
    )


    # ======================================================
    # RENDER DASHBOARD
    # ======================================================

    return render_template(
        "admin/dashboard.html",

        stats=stats,

        recent_news=recent_news,

        recent_events=recent_events,

        recent_messages=recent_messages,

        recent_members=recent_members,

        recent_gallery=recent_gallery,

        recent_slides=recent_slides,

        recent_applications=recent_applications
    )


# ==========================================================
# MEMBERSHIP APPLICATIONS
# ==========================================================

@admin_bp.route(
    "/membership-applications"
)
@admin_required
def membership_applications():

    search = request.args.get(
        "search",
        "",
        type=str
    ).strip()

    status = request.args.get(
        "status",
        "",
        type=str
    ).strip()


    # ======================================================
    # BASE QUERY
    # ======================================================

    query = MembershipApplication.query


    # ======================================================
    # SEARCH
    # ======================================================

    if search:

        search_term = f"%{search}%"

        query = query.filter(
            db.or_(
                MembershipApplication.full_name.ilike(
                    search_term
                ),
                MembershipApplication.email.ilike(
                    search_term
                ),
                MembershipApplication.phone.ilike(
                    search_term
                ),
                MembershipApplication.location.ilike(
                    search_term
                )
            )
        )


    # ======================================================
    # STATUS FILTER
    # ======================================================

    allowed_statuses = (
        "Pending",
        "Approved",
        "Rejected"
    )

    if status in allowed_statuses:

        query = query.filter(
            MembershipApplication.status == status
        )


    # ======================================================
    # APPLICATIONS
    # ======================================================

    applications = (
        query
        .order_by(
            MembershipApplication.created_at.desc()
        )
        .all()
    )


    # ======================================================
    # COUNTERS
    # ======================================================

    total_applications = (
        MembershipApplication.query.count()
    )

    pending_applications = (
        MembershipApplication.query
        .filter_by(
            status="Pending"
        )
        .count()
    )

    approved_applications = (
        MembershipApplication.query
        .filter_by(
            status="Approved"
        )
        .count()
    )

    rejected_applications = (
        MembershipApplication.query
        .filter_by(
            status="Rejected"
        )
        .count()
    )


    # ======================================================
    # RENDER
    # ======================================================

    return render_template(
        "admin/membership_applications/index.html",

        applications=applications,

        search=search,

        status=status,

        total_applications=total_applications,

        pending_applications=pending_applications,

        approved_applications=approved_applications,

        rejected_applications=rejected_applications
    )


# ==========================================================
# VIEW MEMBERSHIP APPLICATION
# ==========================================================

@admin_bp.route(
    "/membership-applications/<int:id>"
)
@admin_required
def view_membership_application(id):

    application = (
        MembershipApplication.query
        .get_or_404(id)
    )

    return render_template(
        "admin/membership_applications/view.html",
        application=application
    )


# ==========================================================
# UPDATE MEMBERSHIP APPLICATION STATUS
# ==========================================================

@admin_bp.route(
    "/membership-applications/<int:id>/status/<string:status>",
    methods=["POST"]
)
@admin_required
def update_membership_application_status(
    id,
    status
):

    application = (
        MembershipApplication.query
        .get_or_404(id)
    )


    # ======================================================
    # VALIDATE STATUS
    # ======================================================

    allowed_statuses = (
        "Pending",
        "Approved",
        "Rejected"
    )

    if status not in allowed_statuses:

        flash(
            "Invalid application status.",
            "danger"
        )

        return redirect(
            url_for(
                "admin.view_membership_application",
                id=application.id
            )
        )


    # ======================================================
    # PREVENT STATUS CHANGE ON CONVERTED APPLICATION
    # ======================================================

    if application.is_converted:

        flash(
            "A converted application cannot have its status changed.",
            "warning"
        )

        return redirect(
            url_for(
                "admin.view_membership_application",
                id=application.id
            )
        )


    # ======================================================
    # UPDATE STATUS
    # ======================================================

    application.status = status


    try:

        db.session.commit()

    except Exception:

        db.session.rollback()

        flash(
            "The application status could not be updated.",
            "danger"
        )

        return redirect(
            url_for(
                "admin.view_membership_application",
                id=application.id
            )
        )


    flash(
        f"Application has been marked {status.lower()}.",
        "success"
    )

    return redirect(
        url_for(
            "admin.view_membership_application",
            id=application.id
        )
    )


# ==========================================================
# CONVERT APPLICATION TO MEMBER
# ==========================================================

@admin_bp.route(
    "/membership-applications/<int:id>/convert",
    methods=["POST"]
)
@admin_required
def convert_membership_application(id):

    application = (
        MembershipApplication.query
        .get_or_404(id)
    )


    # ======================================================
    # ALREADY CONVERTED
    # ======================================================

    if application.is_converted:

        flash(
            "This application has already been converted to a member.",
            "warning"
        )

        return redirect(
            url_for(
                "admin.view_membership_application",
                id=application.id
            )
        )


    # ======================================================
    # ONLY APPROVED APPLICATIONS CAN BE CONVERTED
    # ======================================================

    if application.status != "Approved":

        flash(
            "Only an approved application can be converted to a member.",
            "warning"
        )

        return redirect(
            url_for(
                "admin.view_membership_application",
                id=application.id
            )
        )


    # ======================================================
    # CREATE MEMBER
    # ======================================================

    member = Member(

        full_name=application.full_name,

        position="Member",

        biography=None,

        photo=None,

        email=application.email,

        phone=application.phone,

        facebook=None,

        linkedin=None,

        twitter=None,

        display_order=1,

        is_active=True
    )


    # ======================================================
    # SAVE MEMBER + APPLICATION TOGETHER
    # ======================================================

    try:

        db.session.add(member)

        db.session.flush()

        application.is_converted = True

        # IMPORTANT:
        # The current MembershipApplication model
        # uses member_id, not converted_member_id.

        application.member_id = member.id

        db.session.commit()

    except Exception:

        db.session.rollback()

        flash(
            "The application could not be converted to a member.",
            "danger"
        )

        return redirect(
            url_for(
                "admin.view_membership_application",
                id=application.id
            )
        )


    # ======================================================
    # SUCCESS
    # ======================================================

    flash(
        f"{member.full_name} has been successfully converted to a member.",
        "success"
    )

    return redirect(
        url_for(
            "admin.view_membership_application",
            id=application.id
        )
    )


# ==========================================================
# DELETE MEMBERSHIP APPLICATION
# ==========================================================

@admin_bp.route(
    "/membership-applications/<int:id>/delete",
    methods=["POST"]
)
@admin_required
def delete_membership_application(id):

    application = (
        MembershipApplication.query
        .get_or_404(id)
    )


    # ======================================================
    # PROTECT CONVERTED APPLICATIONS
    # ======================================================

    if application.is_converted:

        flash(
            "A converted membership application cannot be deleted.",
            "warning"
        )

        return redirect(
            url_for(
                "admin.view_membership_application",
                id=application.id
            )
        )


    # ======================================================
    # DELETE
    # ======================================================

    try:

        db.session.delete(application)

        db.session.commit()

    except Exception:

        db.session.rollback()

        flash(
            "The membership application could not be deleted.",
            "danger"
        )

        return redirect(
            url_for(
                "admin.view_membership_application",
                id=application.id
            )
        )


    flash(
        "Membership application deleted successfully.",
        "success"
    )

    return redirect(
        url_for(
            "admin.membership_applications"
        )
    )