from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Account(db.Model):
    __tablename__ = 'accounts_account'
    id = db.Column(db.BigInteger, primary_key=True)
    password_hash = db.Column(db.String(255), nullable=True)  # Renommé de password à password_hash
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    identifiant = db.Column(db.String(255), nullable=False, unique=True)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_staff = db.Column(db.Boolean, nullable=False, default=False)
    is_superuser = db.Column(db.Boolean, nullable=False, default=False)

    def set_password(self, password):
        """Hache le mot de passe et le stocke dans password_hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Vérifie si le mot de passe correspond au hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Account {self.username}>"