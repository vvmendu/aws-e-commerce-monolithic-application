from flask import Blueprint, request, jsonify, current_app
from app import db
from models.product import Category

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('', methods=['GET'])
def get_categories():
    try:
        categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()
        return jsonify({'categories': [c.to_dict() for c in categories]}), 200
    except Exception as e:
        current_app.logger.error(f"Categories fetch error: {str(e)}")
        return jsonify({'error': 'Failed to fetch categories'}), 500

@categories_bp.route('/<string:slug>', methods=['GET'])
def get_category(slug):
    try:
        category = Category.query.filter_by(slug=slug, is_active=True).first()
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        return jsonify({'category': category.to_dict()}), 200
    except Exception as e:
        current_app.logger.error(f"Category fetch error: {str(e)}")
        return jsonify({'error': 'Failed to fetch category'}), 500
