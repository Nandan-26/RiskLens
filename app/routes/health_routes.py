from flask import Blueprint, jsonify
from app.database import get_db_connection
health_bp = Blueprint('health', __name__)
@health_bp.get('/api/health')
def health_check():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify(status='success', service='RiskLens API', database='healthy'), 200
    except Exception:
        return jsonify(status='degraded', service='RiskLens API', database='unhealthy'), 503
