from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import uuid

try:
    from flask_jwt_extended import jwt_required, get_jwt
    JWT_AVAILABLE = True
except Exception:
    JWT_AVAILABLE = False
    def jwt_required(*a, **kw):
        def _decorator(f):
            return f
        return _decorator
    def get_jwt():
        return {}

from models import db, Reclamation

reclamations_bp = Blueprint('reclamations', __name__, url_prefix='/api/reclamations')

@reclamations_bp.route('', methods=['POST'])
def create_reclamation():
    data = request.get_json() or {}
    if not data.get('name') or not data.get('email') or not data.get('message'):
        return jsonify({'error': 'name, email et message requis'}), 400
    item = Reclamation(
        id=str(uuid.uuid4()),
        name=data.get('name'),
        email=data.get('email'),
        order_id=data.get('order_id'),
        message=data.get('message'),
        created_at=datetime.utcnow()
    )
    db.session.add(item)
    db.session.commit()
    current_app.logger.info('Nouvelle réclamation: %s', item.id)
    return jsonify({'id': item.id}), 201

@reclamations_bp.route('', methods=['GET'])
@jwt_required()
def list_reclamations():
    if JWT_AVAILABLE:
        claims = get_jwt() or {}
        if not claims.get('is_admin'):
            return jsonify({'error': 'admin required'}), 403
    else:
        if request.args.get('admin') != '1':
            return jsonify({'error': 'admin required (use ?admin=1 for local dev)'}), 403

    recs = Reclamation.query.order_by(Reclamation.created_at.desc()).all()
    return jsonify([{
        'id': r.id,
        'name': r.name,
        'email': r.email,
        'order_id': r.order_id,
        'message': r.message,
        'created_at': r.created_at.isoformat() + 'Z'
    } for r in recs]), 200

@reclamations_bp.route('/', methods=['GET'])
def get_reclamations():
    return jsonify([]), 200
