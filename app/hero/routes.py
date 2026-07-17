from . import hero_bp


@hero_bp.route("/")
def index():
    return "Hero module is working!"