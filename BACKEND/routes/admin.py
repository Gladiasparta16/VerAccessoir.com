from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Product, Order

admin_bp = Blueprint('admin', __name__)

# GET ALL USERS (Admin)
@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user.is_admin:
            return jsonify({'error': 'Accès refusé'}), 403
        
        users = User.query.all()
        return jsonify([{
            'id': u.id,
            'email': u.email,
            'name': u.name,
            'is_admin': u.is_admin,
            'created_at': u.created_at.isoformat()
        } for u in users]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# GET ALL ORDERS (Admin)
@admin_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_all_orders():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user.is_admin:
            return jsonify({'error': 'Accès refusé'}), 403
        
        orders = Order.query.all()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# GET STATS (Admin)
@admin_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user.is_admin:
            return jsonify({'error': 'Accès refusé'}), 403
        
        total_users = User.query.count()
        total_products = Product.query.count()
        total_orders = Order.query.count()
        total_revenue = sum(order.total_amount for order in Order.query.all())
        
        return jsonify({
            'total_users': total_users,
            'total_products': total_products,
            'total_orders': total_orders,
            'total_revenue': total_revenue
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# UPDATE USER (Admin)
@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    try:
        admin_id = get_jwt_identity()
        admin = User.query.get(admin_id)
        
        if not admin.is_admin:
            return jsonify({'error': 'Accès refusé'}), 403
        
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        if 'is_admin' in data:
            user.is_admin = data['is_admin']
        
        db.session.commit()
        
        return jsonify({'message': 'Utilisateur mis à jour'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
