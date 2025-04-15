# app/controllers/auth_controller.py
from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash
from flask import jsonify

def register_user(data):
    try:
        email = data.get("email")
        phone = data.get("phone")
        fullname = data.get("fullname")
        password = data.get("password")

        if not email or not fullname or not password:
            return jsonify({"error": "Email, nom complet et mot de passe sont requis."}), 400

        if User.query.filter((User.email == email) | (User.phone == phone)).first():
            return jsonify({"error": "Utilisateur déjà existant avec cet email ou téléphone."}), 409

        hashed_password = generate_password_hash(password)

        new_user = User(email=email, phone=phone, fullname=fullname, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Inscription réussie.", "user_id": new_user.id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
