from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Order, OrderItem, Product, User

orders_bp = Blueprint('orders', __name__)

# CREATE ORDER
@orders_bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('items') or not data.get('total_amount'):
            return jsonify({'error': 'Données invalides'}), 400
        
        # Créer la commande
        order = Order(
            user_id=user_id,
            total_amount=data['total_amount'],
            status='pending'
        )
        
        # Ajouter les articles
        for item_data in data['items']:
            product = Product.query.get(item_data['product_id'])
            if not product:
                return jsonify({'error': f'Produit {item_data["product_id"]} non trouvé'}), 404
            
            # ⚠️ VALIDER LA QUANTITÉ
            try:
                quantity = int(item_data['quantity'])
                if quantity <= 0:
                    return jsonify({'error': 'Quantité doit être > 0'}), 400
            except (ValueError, TypeError):
                return jsonify({'error': 'Quantité invalide'}), 400
            
            # ⚠️ VÉRIFIER LE STOCK DISPONIBLE
            if product.stock < quantity:
                return jsonify({'error': f'Stock insuffisant pour {product.name} (disponible: {product.stock})'}), 400
            
            order_item = OrderItem(
                product_id=item_data['product_id'],
                quantity=quantity,
                price=product.price
            )
            order.items.append(order_item)
            
            # Réduire le stock
            product.stock -= quantity
        
        db.session.add(order)
        db.session.commit()
        
        return jsonify({'message': 'Commande créée', 'order': order.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# GET ALL ORDERS (for user)
@orders_bp.route('/', methods=['GET'])
@jwt_required()
def get_orders():
    try:
        user_id = get_jwt_identity()
        orders = Order.query.filter_by(user_id=user_id).all()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# GET ORDER BY ID
@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    try:
        user_id = get_jwt_identity()
        order = Order.query.get_or_404(order_id)
        
        # Vérifier que l'utilisateur est propriétaire de la commande
        if order.user_id != user_id:
            return jsonify({'error': 'Accès refusé'}), 403
        
        return jsonify(order.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

# UPDATE ORDER STATUS (Admin)
@orders_bp.route('/<int:order_id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        # Vérifier si admin
        if not user.is_admin:
            return jsonify({'error': 'Accès refusé'}), 403
        
        order = Order.query.get_or_404(order_id)
        data = request.get_json()
        
        if 'status' in data:
            order.status = data['status']
        
        db.session.commit()
        
        return jsonify({'message': 'Statut mis à jour', 'order': order.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# CANCEL ORDER
@orders_bp.route('/<int:order_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_order(order_id):
    try:
        user_id = get_jwt_identity()
        order = Order.query.get_or_404(order_id)
        
        if order.user_id != user_id:
            return jsonify({'error': 'Accès refusé'}), 403
        
        if order.status != 'pending':
            return jsonify({'error': 'Impossible d\'annuler cette commande'}), 400
        
        # Restaurer le stock
        for item in order.items:
            item.product.stock += item.quantity
        
        order.status = 'cancelled'
        db.session.commit()
        
        return jsonify({'message': 'Commande annulée', 'order': order.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
