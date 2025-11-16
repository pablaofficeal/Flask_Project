from import_router_bp import (
    home_bpp,
    register_bpp,
    login_bpp,
    swagger_bpp,
    github_oauth_bp,
    oauth_bpp,
    cpa_bpp,
    homes_bpp,
    profile_bpp,
    dpa_bpp,
    epa_bpp,
)

def register_blueprints(app):
    app.register_blueprint(home_bpp)
    app.register_blueprint(register_bpp)
    app.register_blueprint(login_bpp)
    app.register_blueprint(swagger_bpp)
    app.register_blueprint(github_oauth_bp)
    app.register_blueprint(oauth_bpp)
    app.register_blueprint(cpa_bpp)
    app.register_blueprint(homes_bpp)
    app.register_blueprint(profile_bpp)
    app.register_blueprint(dpa_bpp)
    app.register_blueprint(epa_bpp)