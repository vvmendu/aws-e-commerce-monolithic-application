from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import logging
import os

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(config_name='default'):
    app = Flask(__name__)
    from config import config
    app.config.from_object(config[config_name])

    db.init_app(app)
    bcrypt.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    from routes.auth import auth_bp
    from routes.products import products_bp
    from routes.cart import cart_bp
    from routes.orders import orders_bp
    from routes.categories import categories_bp

    app.register_blueprint(auth_bp, url_prefix='/api/users')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(cart_bp, url_prefix='/api/cart')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    app.register_blueprint(categories_bp, url_prefix='/api/categories')

    from middleware.error_handler import register_error_handlers
    register_error_handlers(app)

    @app.route('/api/health', methods=['GET'])
    def health_check():
        try:
            db.session.execute(db.text('SELECT 1'))
            return jsonify({'status': 'healthy', 'service': 'ecommerce-backend', 'database': 'connected'}), 200
        except Exception as e:
            app.logger.error(f"Health check failed: {str(e)}")
            return jsonify({'status': 'unhealthy', 'service': 'ecommerce-backend', 'database': 'disconnected', 'error': str(e)}), 503

    @app.route('/api', methods=['GET'])
    def api_root():
        return jsonify({
            'message': 'E-Commerce API v1.0',
            'endpoints': {
                'auth': '/api/users',
                'products': '/api/products',
                'cart': '/api/cart',
                'orders': '/api/orders',
                'categories': '/api/categories'
            }
        }), 200

    return app

if __name__ == '__main__':
    env = os.environ.get('FLASK_ENV', 'development')
    app = create_app(env)
    app.run(host='0.0.0.0', port=5000, debug=(env == 'development'))
