from datetime import datetime
from store import db
from store import bcrypt
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name= db.Column(db.String(length=60), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    gender= db.Column(db.String(length=10))
    email= db.Column(db.String(length=100), nullable=False, unique = True)
    password_hash = db.Column(db.String(length=60), nullable = False)
    address = db.Column(db.String(length=255))
   
    
    @property
    def password(self):
        raise AttributeError("Password is write only")
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
        
    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    
class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name= db.Column(db.String(length=100), nullable=False)
    description= db.Column(db.String(length=255), nullable=True)
    price = db.Column(db.Numeric(18, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(50))
    product_type = db.Column(db.String(20))
    
class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    user = db.relationship('Users', backref = 'orders', lazy = True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20))
    total_price = db.Column(db.Numeric(18,2), nullable = False)
    
class Order_items(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable= False) 
    order = db.relationship('Orders', backref = 'items', lazy = True)
    product = db.relationship('Products', backref = 'order_items', lazy = True)
    quantity = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Numeric(18,2), nullable = False)
    
    
    