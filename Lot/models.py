from extensions import db
from Account.models import Account
from Customer.models import Customer
from datetime import datetime

class Recompense(db.Model):
    __tablename__ = 'lot_recompenses'
    id = db.Column(db.BigInteger, primary_key=True)
    libelle = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    recompense_image = db.Column(db.String(255))
    jeton = db.Column(db.BigInteger, nullable=False)

    def __repr__(self):
        return f"<Recompense id={self.id} libelle={self.libelle}>"

class Favorite(db.Model):
    __tablename__ = 'lot_favorites'
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('accounts_account.id'), nullable=False)
    reward_id = db.Column(db.BigInteger, db.ForeignKey('lot_recompenses.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship('Account', backref='favorites')
    reward = db.relationship('Recompense', backref='favorites')

    def __repr__(self):
        return f"<Favorite user_id={self.user_id} reward_id={self.reward_id}>"

class CartItem(db.Model):
    __tablename__ = 'lot_cart_items'
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('accounts_account.id'), nullable=False)
    reward_id = db.Column(db.BigInteger, db.ForeignKey('lot_recompenses.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    added_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship('Account', backref='cart_items')
    reward = db.relationship('Recompense', backref='cart_items')

    def __repr__(self):
        return f"<CartItem user_id={self.user_id} reward_id={self.reward_id} quantity={self.quantity}>"

# Lot/models.py (modifié)
class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reward_id = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    quantity_available = db.Column(db.Integer, nullable=False)
    price_tokens = db.Column(db.Float, nullable=False)
    unit_price_fcfa = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255))
    category = db.Column(db.String(50))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "reward_id": self.reward_id,
            "name": self.name,
            "quantity_available": self.quantity_available,
            "price_tokens": self.price_tokens,
            "unit_price_fcfa": self.unit_price_fcfa,
            "image_url": self.image_url,
            "category": self.category,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None
        }


# Table de liaison entre Order et les articles
order_items = db.Table(
    'order_items',
    db.Column('order_id', db.BigInteger, db.ForeignKey('lot_orders.id'), primary_key=True),
    db.Column('reward_id', db.BigInteger, db.ForeignKey('lot_recompenses.id'), primary_key=True),
    db.Column('quantity', db.Integer, nullable=False, default=1)
)

class Order(db.Model):
    __tablename__ = 'lot_orders'
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('accounts_account.id'), nullable=False)
    customer_id = db.Column(db.BigInteger, db.ForeignKey('customer_customers.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')
    contact = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship('Account', backref='orders')
    customer = db.relationship('Customer', backref='orders')
    items = db.relationship('Recompense', secondary=order_items, backref=db.backref('orders', lazy='dynamic'))

    def __repr__(self):
        return f"<Order user_id={self.user_id} amount={self.amount} status={self.status}>"


class OrderItem(db.Model):
    __tablename__ = 'lot_order_items'
    id = db.Column(db.BigInteger, primary_key=True)
    order_id = db.Column(db.BigInteger, db.ForeignKey('lot_orders.id'), nullable=False)
    reward_id = db.Column(db.BigInteger, db.ForeignKey('lot_recompenses.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order = db.relationship('Order', backref='order_items')
    reward = db.relationship('Recompense')
    
class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_account.id'), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    is_read = db.Column(db.Boolean, default=False)  # Nouveau champ

    user = db.relationship('Account', backref='notifications')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Notification user_id={self.user_id}>"