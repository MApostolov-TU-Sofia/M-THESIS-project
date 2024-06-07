from app import app

# Importing sub-route blueprints
from .modify.project_modify import route_project_bp

app.register_blueprint(route_project_bp, url_prefix='/project')
