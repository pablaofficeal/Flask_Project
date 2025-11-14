from import_router_bp import (
    home_bpp,
    register_bpp,
    login_bpp,
    swagger_bpp
)

def register_blueprints(app):
    app.register_blueprint(home_bpp)
    app.register_blueprint(register_bpp)
    app.register_blueprint(login_bpp)
    app.register_blueprint(swagger_bpp)