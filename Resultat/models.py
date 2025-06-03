from extensions import db

class ResultatCriteria(db.Model):
    __tablename__ = 'resultat_criteria'
    id = db.Column(db.BigInteger, primary_key=True)
    criteria_name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<ResultatCriteria {self.criteria_name}>"

class ResultatTotal(db.Model):
    __tablename__ = 'resultat_total'
    id = db.Column(db.BigInteger, primary_key=True)
    customer_id = db.Column(db.BigInteger, db.ForeignKey('customer_customers.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    customer = db.relationship('Customer', backref='resultat_totals')

    def __repr__(self):
        return f"<ResultatTotal {self.customer_id} - {self.date}>"

class ResultatPoint(db.Model):
    __tablename__ = 'resultat_point'
    id = db.Column(db.BigInteger, primary_key=True)
    customer_id = db.Column(db.BigInteger, db.ForeignKey('customer_customers.id'), nullable=False)
    notation = db.Column(db.String(255), nullable=False)
    jeton = db.Column(db.Integer, nullable=False)
    mois = db.Column(db.String(50), nullable=False)
    montant = db.Column(db.BigInteger, nullable=False)
    date_notes = db.Column(db.Date, nullable=False)
    customer = db.relationship('Customer', backref='resultat_points')

    def __repr__(self):
        return f"<ResultatPoint {self.customer_id} - {self.mois}>"

class ClientRecompense(db.Model):
    __tablename__ = 'resultat_clientarecompense'
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('accounts_account.id'), nullable=False)
    customer_id = db.Column(db.BigInteger, db.ForeignKey('customer_customers.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.BigInteger, db.ForeignKey('category_category.id'))
    user = db.relationship('Account', backref='recompenses')
    customer = db.relationship('Customer', backref='client_recompenses')
    category = db.relationship('Category', backref='recompenses')

    def __repr__(self):
        return f"<ClientRecompense {self.customer_id} - {self.score}>"