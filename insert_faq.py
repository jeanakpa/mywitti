from extensions import db
from Faq.models import FAQ

def seed_faqs():
    faqs = [
        FAQ(question="Comment puis-je consulter mon solde de jetons ?", answer="Vous pouvez consulter votre solde de jetons sur votre tableau de bord ou dans la section Profil de l'application."),
        FAQ(question="Que faire si ma commande est annulée ?", answer="Si votre commande est annulée, vous recevrez une notification expliquant la raison. Contactez l'agence RGK pour plus d'informations."),
        FAQ(question="Comment passer à la catégorie suivante ?", answer="Pour passer à la catégorie suivante, vous devez accumuler plus de jetons. Consultez votre tableau de bord pour voir combien de jetons il vous manque."),
        FAQ(question="Où puis-je récupérer ma commande validée ?", answer="Une fois votre commande validée, vous pouvez la récupérer à l'agence RGK. Apportez votre identifiant client."),
        FAQ(question="Comment ajouter un article à mes favoris ?", answer="Pour ajouter un article à vos favoris, accédez à la liste des récompenses et cliquez sur l'icône de cœur à côté de l'article.")
    ]
    db.session.bulk_save_objects(faqs)
    db.session.commit()