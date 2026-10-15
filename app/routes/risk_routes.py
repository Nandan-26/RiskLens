from flask import Blueprint, jsonify
from app.services.risk_service import RiskService
risk_bp = Blueprint('risk', __name__, url_prefix='/api/risk')
@risk_bp.get('/evaluate/<int:business_id>')
def evaluate(business_id):
    result=RiskService.evaluate_business_risk(business_id)
    return (jsonify(status='success',data=result),200) if result else (jsonify(status='error',message='Business record not found.'),404)
