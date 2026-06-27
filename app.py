from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-12345')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    rating = db.Column(db.Float, default=0.0)
    reviews_count = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'stock_quantity': self.stock_quantity,
            'image_url': self.image_url,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'rating': self.rating,
            'reviews_count': self.reviews_count
        }

# Create tables
with app.app_context():
    db.create_all()
    # Add sample products if empty
    if Product.query.count() == 0:
        sample_products = [
            Product(
                name="Premium Wireless Headphones",
                description="High-quality wireless headphones with noise cancellation and 30-hour battery life. Perfect for music lovers and professionals.",
                price=199.99,
                category="Electronics",
                stock_quantity=45,
                image_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400",
                rating=4.8,
                reviews_count=156
            ),
            Product(
                name="Smart Fitness Tracker",
                description="Advanced fitness tracker with heart rate monitor, GPS, and sleep tracking. Waterproof and compatible with iOS and Android.",
                price=89.99,
                category="Electronics",
                stock_quantity=120,
                image_url="https://images.unsplash.com/photo-1576243345690-4e4b79b63288?w=400",
                rating=4.6,
                reviews_count=89
            ),
            Product(
                name="Organic Cotton T-Shirt",
                description="Comfortable and sustainable t-shirt made from 100% organic cotton. Available in multiple colors and sizes.",
                price=29.99,
                category="Clothing",
                stock_quantity=200,
                image_url="https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400",
                rating=4.5,
                reviews_count=234
            ),
            Product(
                name="Classic Leather Backpack",
                description="Handcrafted genuine leather backpack with multiple compartments. Perfect for daily use or travel.",
                price=149.99,
                category="Accessories",
                stock_quantity=35,
                image_url="https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400",
                rating=4.9,
                reviews_count=67
            ),
            Product(
                name="Stainless Steel Water Bottle",
                description="Eco-friendly vacuum insulated water bottle. Keeps drinks cold for 24 hours or hot for 12 hours.",
                price=24.99,
                category="Home & Kitchen",
                stock_quantity=150,
                image_url="https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400",
                rating=4.7,
                reviews_count=112
            ),
            Product(
                name="Wireless Charging Pad",
                description="Fast wireless charging pad compatible with all Qi-enabled devices. LED indicator and anti-slip design.",
                price=39.99,
                category="Electronics",
                stock_quantity=80,
                image_url="https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=400",
                rating=4.4,
                reviews_count=78
            )
        ]
        for product in sample_products:
            db.session.add(product)
        db.session.commit()

@app.route('/')
def index():
    """Home page with product listing"""
    page = request.args.get('page', 1, type=int)
    per_page = 9
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    
    query = Product.query
    
    if category:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(Product.name.contains(search) | Product.description.contains(search))
    
    products = query.paginate(page=page, per_page=per_page, error_out=False)
    categories = db.session.query(Product.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    return render_template('index.html', 
                         products=products, 
                         categories=categories,
                         current_category=category,
                         search_query=search)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Product detail page"""
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/api/products')
def api_products():
    """REST API endpoint for products"""
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@app.route('/api/product/<int:product_id>')
def api_product(product_id):
    """REST API endpoint for single product"""
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    """Add new product (admin functionality)"""
    if request.method == 'POST':
        try:
            product = Product(
                name=request.form['name'],
                description=request.form['description'],
                price=float(request.form['price']),
                category=request.form['category'],
                stock_quantity=int(request.form['stock_quantity']),
                image_url=request.form.get('image_url', ''),
                rating=float(request.form.get('rating', 0)),
                reviews_count=int(request.form.get('reviews_count', 0))
            )
            db.session.add(product)
            db.session.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error adding product: {str(e)}', 'danger')
    
    return render_template('add_product.html')

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    """Delete a product (admin functionality)"""
    product = Product.query.get_or_404(product_id)
    try:
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting product: {str(e)}', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
