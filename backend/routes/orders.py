from flask import Blueprint, request, jsonify, current_app
from app import db
from models.order import Order, OrderItem
from models.cart import Cart
from models.product import Product
from middleware.auth_middleware import token_required
import uuid

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('', methods=['GET'])
@token_required
def get_orders(current_user):
    try:
        orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
        return jsonify({'orders': [o.to_dict() for o in orders]}), 200
    except Exception as e:
        current_app.logger.error(f"Orders fetch error: {str(e)}")
        return jsonify({'error': 'Failed to fetch orders'}), 500

@orders_bp.route('', methods=['POST'])
@token_required
def create_order(current_user):
    try:
        data = request.get_json()
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 400
        subtotal = sum(float(item.product.price) * item.quantity for item in cart_items)
        tax = round(subtotal * 0.08, 2)
        shipping = 5.99 if subtotal < 50 else 0.00
        total = subtotal + tax + shipping
        order = Order(
            user_id=current_user.id,
            order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
            subtotal=subtotal,
            tax_amount=tax,
            shipping_cost=shipping,
            total_amount=total,
            shipping_addr=data.get('shipping_addr', {}),
            payment_method=data.get('payment_method', 'card'),
            payment_status='paid'
        )
        db.session.add(order)
        db.session.flush()
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                product_name=item.product.name,
                unit_price=item.product.price,
                quantity=item.quantity,
                subtotal=float(item.product.price) * item.quantity
            )
            db.session.add(order_item)
            db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Order created successfully', 'order': order.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Order creation error: {str(e)}")
        return jsonify({'error': 'Failed to create order'}), 500

@orders_bp.route('/<int:order_id>', methods=['GET'])
@token_required
def get_order(current_user, order_id):
    try:
        order = Order.query.filter_by(id=order_id, user_id=current_user.id).first()
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        return jsonify({'order': order.to_dict()}), 200
    except Exception as e:
        current_app.logger.error(f"Order fetch error: {str(e)}")
        return jsonify({'error': 'Failed to fetch order'}), 500
