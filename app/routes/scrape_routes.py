from flask import Blueprint, jsonify
from app.services.scraper_service import ScraperService
scrape_bp = Blueprint('scrape', __name__, url_prefix='/api/scrape')
@scrape_bp.post('/practice-site')
def scrape():
    try:
        result=ScraperService.scrape_books_to_scrape()
        return jsonify(status='success', **result), 201
    except Exception:
        return jsonify(status='error',message='Scraping failed.'), 500
