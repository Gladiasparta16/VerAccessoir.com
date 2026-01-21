from flask import Blueprint, request, jsonify
from models import db, Product
from flask_jwt_extended import jwt_required

products_bp = Blueprint("products", __name__)


# GET tous les produits
@products_bp.route("/", methods=["GET"])
def get_products():
    try:
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET un produit par ID
@products_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify(product.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


# CREATE produit (Admin)
@products_bp.route("/", methods=["POST"])
@jwt_required()
def create_product():
    try:
        from flask_jwt_extended import get_jwt_identity
        from models import User

        # ⚠️ VÉRIFIER QUE C'EST UN ADMIN
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or not user.is_admin:
            return jsonify({"error": "Accès refusé: administrateur requis"}), 403

        data = request.get_json()

        if not data or not data.get("name") or not data.get("price"):
            return jsonify({"error": "Données invalides"}), 400

        # ⚠️ VALIDER LE PRIX (doit être > 0)
        try:
            price = float(data["price"])
            if price <= 0:
                return jsonify({"error": "Le prix doit être supérieur à 0"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "Prix invalide"}), 400

        product = Product(
            name=data["name"],
            price=price,
            description=data.get("description", ""),
            image_url=data.get("image_url", ""),
            category=data.get("category", "autres"),
            stock=data.get("stock", 10),
        )

        db.session.add(product)
        db.session.commit()

        return jsonify({"message": "Produit créé", "product": product.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# UPDATE produit (Admin)
@products_bp.route("/<int:product_id>", methods=["PUT"])
@jwt_required()
def update_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        data = request.get_json()

        if "name" in data:
            product.name = data["name"]
        if "price" in data:
            product.price = data["price"]
        if "description" in data:
            product.description = data["description"]
        if "image_url" in data:
            product.image_url = data["image_url"]
        if "category" in data:
            product.category = data["category"]
        if "stock" in data:
            product.stock = data["stock"]

        db.session.commit()

        return (
            jsonify({"message": "Produit mis à jour", "product": product.to_dict()}),
            200,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# DELETE produit (Admin)
@products_bp.route("/<int:product_id>", methods=["DELETE"])
@jwt_required()
def delete_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Produit supprimé"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
