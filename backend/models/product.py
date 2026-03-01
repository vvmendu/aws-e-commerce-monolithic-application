from app import db
from datetime import datetime

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    products = db.relationship('Product', backref='category', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'image_url': self.image_url,
            'is_active': self.is_active,
            'product_count': len(self.products)
        }

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    sale_price = db.Column(db.Numeric(10, 2))
    sku = db.Column(db.String(100), unique=True)
    stock_qty = db.Column(db.Integer, default=0, nullable=False)
    rating_avg = db.Column(db.Numeric(3, 2), default=0.00)
    rating_count = db.Column(db.Integer, default=0)
    brand = db.Column(db.String(100))
    weight_lbs = db.Column(db.Numeric(6, 2))
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    is_bestseller = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    images = db.relationship('ProductImage', backref='product', lazy=True, cascade='all, delete-orphan')
    attributes = db.relationship('ProductAttribute', backref='product', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, include_images=True):
        data = {
            'id': self.id,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'price': float(self.price),
            'sale_price': float(self.sale_price) if self.sale_price else None,
            'sku': self.sku,
            'stock_qty': self.stock_qty,
            'in_stock': self.stock_qty > 0,
            'rating_avg': float(self.rating_avg) if self.rating_avg else 0.0,
            'rating_count': self.rating_count,
            'brand': self.brand,
            'is_featured': self.is_featured,
            'is_bestseller': self.is_bestseller
        }
        if include_images and self.images:
            data['images'] = [img.to_dict() for img in self.images]
        return data

class ProductImage(db.Model):
    __tablename__ = 'product_images'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    alt_text = db.Column(db.String(255))
    is_primary = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'image_url': self.image_url,
            'alt_text': self.alt_text,
            'is_primary': self.is_primary
        }

class ProductAttribute(db.Model):
    __tablename__ = 'product_attributes'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    attr_key = db.Column(db.String(100), nullable=False)
    attr_value = db.Column(db.String(255), nullable=False)
