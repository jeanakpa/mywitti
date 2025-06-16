# admin/resources/notifications.py
from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from Account.models import Account
from Lot.models import Notification
from Admin.views import api
from extensions import db

notification_model = api.model('Notification', {
    'id': fields.Integer(description='Notification ID'),
    'message': fields.String(description='Notification message'),
    'created_at': fields.String(description='Creation date'),
    'is_read': fields.Boolean(description='Whether the notification is read')
})

notifications_response_model = api.model('NotificationsResponse', {
    'msg': fields.String(description='Success message'),
    'notifications': fields.List(fields.Nested(notification_model), description='List of notifications')
})

class AdminNotifications(Resource):
    @jwt_required()
    @api.marshal_with(notifications_response_model)
    def get(self):
        admin_identifiant = get_jwt_identity()
        admin = Account.query.filter_by(identifiant=admin_identifiant).first()
        if not admin or not (admin.is_admin or admin.is_superuser):
            return {"msg": "Utilisateur non autorisé"}, 403
        notifications = Notification.query.filter_by(user_id=admin.id).order_by(Notification.created_at.desc()).all()
        notifications_data = [{
            'id': notification.id,
            'message': notification.message,
            'created_at': str(notification.created_at) if notification.created_at else "Unknown",
            'is_read': notification.is_read
        } for notification in notifications]
        return {'msg': 'Notifications récupérées avec succès', 'notifications': notifications_data}

class AdminNotificationDetail(Resource):
    @jwt_required()
    def delete(self, notification_id):
        admin_identifiant = get_jwt_identity()
        admin = Account.query.filter_by(identifiant=admin_identifiant).first()
        if not admin or not (admin.is_admin or admin.is_superuser):
            return {"msg": "Utilisateur non autorisé"}, 403

        notification = Notification.query.filter_by(id=notification_id, user_id=admin.id).first()
        if not notification:
            return {"msg": "Notification non trouvée ou non autorisée"}, 404

        db.session.delete(notification)
        db.session.commit()
        return {"msg": "Notification supprimée avec succès"}, 200

    @jwt_required()
    def patch(self, notification_id):  # Nouvelle méthode pour marquer comme lue
        admin_identifiant = get_jwt_identity()
        admin = Account.query.filter_by(identifiant=admin_identifiant).first()
        if not admin or not (admin.is_admin or admin.is_superuser):
            return {"msg": "Utilisateur non autorisé"}, 403

        notification = Notification.query.filter_by(id=notification_id, user_id=admin.id).first()
        if not notification:
            return {"msg": "Notification non trouvée ou non autorisée"}, 404

        notification.is_read = True
        db.session.commit()
        return {'msg': 'Notification marquée comme lue', 'notification': {
            'id': notification.id,
            'message': notification.message,
            'created_at': str(notification.created_at),
            'is_read': notification.is_read
        }}, 200