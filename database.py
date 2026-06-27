from app import db
from models import Product

def init_db():
    """Initialize the database with sample data"""
    db.create_all()
    
    # Check if products exist
    if Product.query.count() == 0:
        sample_products = [
            Product(
                name="Premium Wireless Headphones",
                description="High-quality wireless headphones with noise cancellation and 30-hour battery life.",
                price=199.99,
                category="Electronics",
                stock_quantity=45,
                image_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400",
                rating=4.8,
                reviews_count=156
            ),
            # Add more products as needed
        ]
        for product in sample_products:
            db.session.add(product)
        db.session.commit()
        print("Database initialized with sample products.")
