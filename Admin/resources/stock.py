# Admin/resources/stock.py
import os
from flask import request
from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from Lot.models import Stock
from Account.models import Account
from extensions import db
from datetime import datetime
from Admin.views import api
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

# Configuration pour le dossier d'upload des images
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

stock_model = api.model('Stock', {
    'id': fields.Integer(description='Stock ID'),
    'reward_id': fields.Integer(description='Reward ID'),
    'name': fields.String(description='Name of the item'),
    'quantity_available': fields.Integer(description='Quantity Available'),
    'price_tokens': fields.Float(description='Price in Tokens'),
    'unit_price_fcfa': fields.Float(description='Unit Price in FCFA'),
    'image_url': fields.String(description='Image URL'),
    'category': fields.String(description='Category'),
    'last_updated': fields.String(description='Last Updated')
})

stock_input_model = api.model('StockInput', {
    'reward_id': fields.Integer(required=True, description='Reward ID'),
    'name': fields.String(required=True, description='Name of the item'),
    'quantity_available': fields.Integer(required=True, description='Quantity Available'),
    'price_tokens': fields.Float(required=True, description='Price in Tokens'),
    'unit_price_fcfa': fields.Float(required=True, description='Unit Price in FCFA'),
    'category': fields.String(description='Category')
    # L'image sera gérée séparément via multipart/form-data
})

class StockList(Resource):
    @jwt_required()
    @api.marshal_with(stock_model, as_list=True)
    def get(self):
        user_id = get_jwt_identity()
        user = Account.query.filter_by(identifiant=user_id).first()

        if not user or not (user.is_admin or user.is_superuser):
            api.abort(403, "Accès interdit")
        stocks = Stock.query.all()
        return [stock.to_dict() for stock in stocks]

    @jwt_required()
    @api.expect(stock_input_model)
    @api.marshal_with(stock_model, code=201)
    def post(self):
        user_id = get_jwt_identity()
        user = Account.query.filter_by(identifiant=user_id).first()

        if not user or not user.is_superuser:
            api.abort(403, "Seuls les super admins peuvent ajouter du stock")

        # Gérer les données JSON et le fichier image
        if 'image' not in request.files:
            api.abort(400, "Aucune image fournie")
        file = request.files['image']
        if file.filename == '':
            api.abort(400, "Aucune image sélectionnée")
        if not allowed_file(file.filename):
            api.abort(400, "Type de fichier non autorisé. Utilisez PNG, JPEG ou GIF")

        data = request.form  # Les autres champs sont dans request.form
        reward_id = int(data.get('reward_id'))
        name = data.get('name')
        quantity_available = int(data.get('quantity_available'))
        price_tokens = float(data.get('price_tokens'))
        unit_price_fcfa = float(data.get('unit_price_fcfa'))
        category = data.get('category')

        # Sauvegarder l'image
        filename = secure_filename(file.filename)
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(file_path)

        # Vérifie si un stock existe déjà pour ce reward_id
        stock = Stock.query.filter_by(reward_id=reward_id).first()
        if stock:
            # Met à jour le stock existant
            stock.name = name
            stock.quantity_available = quantity_available
            stock.price_tokens = price_tokens
            stock.unit_price_fcfa = unit_price_fcfa
            stock.category = category
            stock.image_url = f"/{file_path}"
            stock.last_updated = datetime.utcnow()
            db.session.commit()
            return stock.to_dict(), 200
        else:
            # Crée un nouveau stock
            new_stock = Stock(
                reward_id=reward_id,
                name=name,
                quantity_available=quantity_available,
                price_tokens=price_tokens,
                unit_price_fcfa=unit_price_fcfa,
                image_url=f"/{file_path}",
                category=category
            )
            try:
                db.session.add(new_stock)
                db.session.commit()
                return new_stock.to_dict(), 201
            except IntegrityError as e:
                db.session.rollback()
                api.abort(400, f"Erreur d'intégrité : {str(e)}")

class StockDetail(Resource):
    @jwt_required()
    @api.marshal_with(stock_model)
    def put(self, stock_id):
        user_id = get_jwt_identity()
        user = Account.query.filter_by(identifiant=user_id).first()

        if not user or not user.is_superuser:
            api.abort(403, "Seuls les super admins peuvent modifier le stock")
        stock = Stock.query.get_or_404(stock_id)

        # Gérer les données et l'image (si fournie)
        data = request.form if 'image' in request.files else request.get_json()
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
                unique_filename = f"{timestamp}_{filename}"
                file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                file.save(file_path)
                # Supprimer l'ancienne image si elle existe
                if stock.image_url:
                    old_file_path = stock.image_url.lstrip('/')
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                stock.image_url = f"/{file_path}"

        stock.name = data.get('name', stock.name)
        stock.quantity_available = int(data.get('quantity_available', stock.quantity_available))
        stock.price_tokens = float(data.get('price_tokens', stock.price_tokens))
        stock.unit_price_fcfa = float(data.get('unit_price_fcfa', stock.unit_price_fcfa))
        stock.category = data.get('category', stock.category)
        stock.last_updated = datetime.utcnow()
        db.session.commit()
        return stock.to_dict()

    @jwt_required()
    def delete(self, stock_id):
        user_id = get_jwt_identity()
        user = Account.query.filter_by(identifiant=user_id).first()

        if not user or not user.is_superuser:
            api.abort(403, "Seuls les super admins peuvent supprimer le stock")
        stock = Stock.query.get_or_404(stock_id)
        # Supprimer l'image associée si elle existe
        if stock.image_url:
            file_path = stock.image_url.lstrip('/')
            if os.path.exists(file_path):
                os.remove(file_path)
        db.session.delete(stock)
        db.session.commit()
        return {"message": "Stock supprimé avec succès"}, 200