# app/routes/auth_routes.py
from flask import Blueprint, request, jsonify
from app.controllers.auth_controller import register_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    return register_user(data)
