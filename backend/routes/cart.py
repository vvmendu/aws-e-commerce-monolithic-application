from flask import Blueprint, request, jsonify, current_app
from app import db
from models.cart import Cart
from models.product import Product
from middleware.auth_middleware import token_required

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('', methods=['GET'])
@token_required
def get_cart(current_user):
    try:
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        items = [item.to_dict() for item in cart_items]
        total = sum(item['subtotal'] for item in items)
        return jsonify({'items': items, 'total': total, 'count': len(items)}), 200
    except Exception as e:
        current_app.logger.error(f"Cart fetch error: {str(e)}")
        return jsonify({'error': 'Failed to fetch cart'}), 500

@cart_bp.route('', methods=['POST'])
@token_required
def add_to_cart(current_user):
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        if not product_id:
            return jsonify({'error': 'product_id is required'}), 400
        product = Product.query.get(product_id)
        if not product or not product.is_active:
            return jsonify({'error': 'Product not found'}), 404
        if product.stock_qty < quantity:
            return jsonify({'error': 'Insufficient stock'}), 400
        existing = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
        if existing:
            existing.quantity += quantity
        else:
            cart_item = Cart(user_id=current_user.id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)
        db.session.commit()
        return jsonify({'message': 'Item added to cart'}), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Add to cart error: {str(e)}")
        return jsonify({'error': 'Failed to add item to cart'}), 500

@cart_bp.route('/<int:item_id>', methods=['DELETE'])
@token_required
def remove_from_cart(current_user, item_id):
    try:
        item = Cart.query.filter_by(id=item_id, user_id=current_user.id).first()
        if not item:
            return jsonify({'error': 'Cart item not found'}), 404
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item removed from cart'}), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Remove from cart error: {str(e)}")
        return jsonify({'error': 'Failed to remove item'}), 500
