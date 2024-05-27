from .process import route_data_process_bp
from app import app

app.register_blueprint(route_data_process_bp, url_prefix='/data')