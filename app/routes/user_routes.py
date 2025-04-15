from flask import Blueprint

user_bp = Blueprint('user', __name__)

@user_bp.route("/users", methods=["GET"])
def get_users():
    return {"message": "Liste des utilisateurs"}
