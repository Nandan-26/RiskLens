from flask import Blueprint, request, jsonify
from app.services.business_service import BusinessService as S
business_bp = Blueprint('businesses', __name__, url_prefix='/api/businesses')

def failure(e):
    return jsonify(status='error', message=str(e)), 400

@business_bp.post('')
def create_business():
    try:
        data = request.get_json(silent=True)
        if not isinstance(data, dict): raise ValueError('Request body must be a JSON object.')
        return jsonify(status='success', data=S.create_business(data)), 201
    except ValueError as e: return failure(e)

@business_bp.get('')
def list_businesses():
    try:
        return jsonify(status='success', **S.get_all_businesses({'country':request.args.get('country'), 'industry':request.args.get('industry')}, request.args.get('page',1), request.args.get('limit',10))), 200
    except ValueError as e: return failure(e)

@business_bp.get('/<int:business_id>')
def get_business(business_id):
    result = S.get_business_by_id(business_id)
    return (jsonify(status='success',data=result),200) if result else (jsonify(status='error',message='Business record not found.'),404)

@business_bp.put('/<int:business_id>')
def update_business(business_id):
    try:
        data=request.get_json(silent=True)
        if not isinstance(data,dict): raise ValueError('Request body must be a JSON object.')
        result=S.update_business(business_id,data)
        return (jsonify(status='success',data=result),200) if result else (jsonify(status='error',message='Business record not found.'),404)
    except ValueError as e: return failure(e)

@business_bp.delete('/<int:business_id>')
def delete_business(business_id):
    if S.delete_business(business_id): return jsonify(status='success',message='Business record deleted successfully.'),200
    return jsonify(status='error',message='Business record not found.'),404
