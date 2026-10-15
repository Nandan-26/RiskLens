from flask import Flask
from app.routes.health_routes import health_bp
from app.routes.business_routes import business_bp
from app.routes.scrape_routes import scrape_bp
from app.routes.risk_routes import risk_bp

def create_app():
    app = Flask(__name__)
    for bp in (health_bp, business_bp, scrape_bp, risk_bp):
        app.register_blueprint(bp)
    return app
