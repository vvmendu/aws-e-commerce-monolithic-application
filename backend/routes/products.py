from flask import Blueprint, request, jsonify, current_app
from app import db
from models.product import Product, Category, ProductImage
from sqlalchemy import or_

products_bp = Blueprint('products', __name__)

@products_bp.route('', methods=['GET'])
def get_products():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        query = Product.query.filter_by(is_active=True)
        category_slug = request.args.get('category')
        if category_slug:
            category = Category.query.filter_by(slug=category_slug).first()
            if category:
                query = query.filter_by(category_id=category.id)
        search_term = request.args.get('search')
        if search_term:
            search_pattern = f"%{search_term}%"
            query = query.filter(or_(
                Product.name.ilike(search_pattern),
                Product.description.ilike(search_pattern),
                Product.brand.ilike(search_pattern)
            ))
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        if request.args.get('featured') == 'true':
            query = query.filter_by(is_featured=True)
        if request.args.get('bestseller') == 'true':
            query = query.filter_by(is_bestseller=True)
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        if sort_by == 'price':
            query = query.order_by(Product.price.desc() if sort_order == 'desc' else Product.price.asc())
        elif sort_by == 'rating':
            query = query.order_by(Product.rating_avg.desc() if sort_order == 'desc' else Product.rating_avg.asc())
        elif sort_by == 'name':
            query = query.order_by(Product.name.desc() if sort_order == 'desc' else Product.name.asc())
        else:
            query = query.order_by(Product.created_at.desc() if sort_order == 'desc' else Product.created_at.asc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return jsonify({
            'products': [p.to_dict() for p in pagination.items],
            'pagination': {
                'page': page, 'per_page': per_page, 'total': pagination.total,
                'pages': pagination.pages, 'has_next': pagination.has_next, 'has_prev': pagination.has_prev
            }
        }), 200
    except Exception as e:
        current_app.logger.error(f"Product fetch error: {str(e)}")
        return jsonify({'error': 'Failed to fetch products'}), 500

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product or not product.is_active:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify({'product': product.to_dict(include_images=True)}), 200
    except Exception as e:
        current_app.logger.error(f"Product detail error: {str(e)}")
        return jsonify({'error': 'Failed to fetch product details'}), 500

@products_bp.route('/slug/<string:slug>', methods=['GET'])
def get_product_by_slug(slug):
    try:
        product = Product.query.filter_by(slug=slug, is_active=True).first()
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify({'product': product.to_dict(include_images=True)}), 200
    except Exception as e:
        current_app.logger.error(f"Product slug fetch error: {str(e)}")
        return jsonify({'error': 'Failed to fetch product'}), 500

@products_bp.route('/featured', methods=['GET'])
def get_featured_products():
    try:
        limit = min(request.args.get('limit', 10, type=int), 50)
        products = Product.query.filter_by(is_active=True, is_featured=True).order_by(Product.rating_avg.desc()).limit(limit).all()
        return jsonify({'products': [p.to_dict() for p in products]}), 200
    except Exception as e:
        current_app.logger.error(f"Featured products error: {str(e)}")
        return jsonify({'error': 'Failed to fetch featured products'}), 500

@products_bp.route('/bestsellers', methods=['GET'])
def get_bestsellers():
    try:
        limit = min(request.args.get('limit', 10, type=int), 50)
        products = Product.query.filter_by(is_active=True, is_bestseller=True).order_by(Product.rating_count.desc()).limit(limit).all()
        return jsonify({'products': [p.to_dict() for p in products]}), 200
    except Exception as e:
        current_app.logger.error(f"Bestsellers error: {str(e)}")
        return jsonify({'error': 'Failed to fetch bestsellers'}), 500
