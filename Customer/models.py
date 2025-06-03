from extensions import db
from datetime import datetime

class Customer(db.Model):
    __tablename__ = 'customer_customers'
    id = db.Column(db.BigInteger, primary_key=True)
    account_id = db.Column(db.BigInteger, db.ForeignKey('accounts_account.id'), nullable=True)  # Ajout de la clé étrangère
    customer_code = db.Column(db.String(50), nullable=False, unique=True)
    short_name = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    birth_date = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(50))
    street = db.Column(db.String(255), nullable=False)
    users = db.Column(db.Integer)
    category_id = db.Column(db.BigInteger, db.ForeignKey('category_category.id'))
    total = db.Column(db.Integer)
    solde = db.Column(db.BigInteger)
    category = db.relationship('Category', backref='customers')
    
    def __repr__(self):
        return f"<Customer {self.customer_code}>"

class Epargne(db.Model):
    __tablename__ = 'customer_epargne'
    id = db.Column(db.BigInteger, primary_key=True)
    customer_id = db.Column(db.BigInteger, db.ForeignKey('customer_customers.id'), nullable=False)
    numero = db.Column(db.String(50))
    libelle = db.Column(db.Text)
    solde = db.Column(db.BigInteger, nullable=False)
    date_ouverture = db.Column(db.String(50))
    customer = db.relationship('Customer', backref='epargnes')

    def __repr__(self):
        return f"<Epargne {self.customer_id} - {self.numero}>"

class Transaction(db.Model):
    __tablename__ = 'customer_deposit_withdrawal'
    id = db.Column(db.BigInteger, primary_key=True)
    customer_id = db.Column(db.BigInteger, db.ForeignKey('customer_customers.id'), nullable=False)
    compte = db.Column(db.String(50))
    libelle = db.Column(db.Text)
    code = db.Column(db.String(50))
    sens = db.Column(db.String(20))  # DEPOSIT or WITHDRAWAL
    montant = db.Column(db.Numeric(15, 2))
    deposit_date = db.Column(db.String(50))
    customer = db.relationship('Customer', backref='transactions')

    def __repr__(self):
        return f"<Transaction {self.customer_id} - {self.sens}>"

class SoldeDepotRecurrent(db.Model):
    __tablename__ = 'customer_solde_depotrecurrent'
    id = db.Column(db.BigInteger, primary_key=True)
    customer_id = db.Column(db.BigInteger, db.ForeignKey('customer_customers.id'), nullable=False)
    numero = db.Column(db.String(50), nullable=False)
    libelle = db.Column(db.String(255), nullable=False)
    solde = db.Column(db.BigInteger, nullable=False)
    date = db.Column(db.String(50), nullable=False)
    customer = db.relationship('Customer', backref='soldes')

    def __repr__(self):
        return f"<SoldeDepotRecurrent {self.customer_id} - {self.solde}>"

class Rebours(db.Model):
    __tablename__ = 'customer_rebours'
    id = db.Column(db.BigInteger, primary_key=True)
    customer_id = db.Column(db.BigInteger, db.ForeignKey('customer_customers.id'), nullable=False)
    jeton = db.Column(db.Integer, nullable=False)
    compte = db.Column(db.Integer, nullable=False)
    jour = db.Column(db.Integer, nullable=False)
    customer = db.relationship('Customer', backref='rebours')

    def __repr__(self):
        return f"<Rebours {self.customer_id} - {self.jeton}>"

class UnpaidAccount(db.Model):
    __tablename__ = 'customer_unpaid'
    id = db.Column(db.BigInteger, primary_key=True)
    customer_id = db.Column(db.BigInteger, db.ForeignKey('customer_customers.id'), nullable=False)
    terme = db.Column(db.Text)
    account = db.Column(db.String(50))
    product = db.Column(db.Text)
    code = db.Column(db.String(50))
    open_date = db.Column(db.String(50))
    maturity = db.Column(db.String(50))
    engagement = db.Column(db.Text)
    principal = db.Column(db.Text)
    due = db.Column(db.Text)
    overdue = db.Column(db.Integer)
    customer = db.relationship('Customer', backref='unpaid_accounts')

    def __repr__(self):
        return f"<UnpaidAccount {self.customer_id} - {self.account}>"

class CustomerDat(db.Model):
    __tablename__ = 'customer_dat'
    id = db.Column(db.BigInteger, primary_key=True)
    client_id = db.Column(db.BigInteger, db.ForeignKey('customer_customers.id'), nullable=False)
    compte = db.Column(db.String(50))
    montant = db.Column(db.BigInteger, nullable=False)
    date = db.Column(db.String(50), nullable=False)
    customer = db.relationship('Customer', backref='dat_records')

    def __repr__(self):
        return f"<CustomerDat {self.client_id} - {self.montant}>"