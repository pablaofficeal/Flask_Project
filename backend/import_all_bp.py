from import_router_bp import (
    home_bpp,
)

def register_blueprints(app):
    app.register_blueprint(home_bpp)