from Survey.models import Survey, SurveyOption
from extensions import db

# Insérer le sondage (si absent)
if not Survey.query.get(3):
    survey = Survey(id=3, title="Test Survey 3", description="Un sondage de test pour vérifier les réponses", is_active=True)
    db.session.add(survey)
    db.session.commit()

# Insérer les options (si absentes)
if not SurveyOption.query.filter_by(survey_id=3).first():
    options = [
        SurveyOption(survey_id=3, option_text="Très mal", option_value=1),
        SurveyOption(survey_id=3, option_text="Mal", option_value=2),
        SurveyOption(survey_id=3, option_text="Moyen", option_value=3),
        SurveyOption(survey_id=3, option_text="Bien", option_value=4),
        SurveyOption(survey_id=3, option_text="Très bien", option_value=5)
    ]
    db.session.add_all(options)
    db.session.commit()

print("Sondage 3 et options insérés :", Survey.query.get(3), [opt.id for opt in SurveyOption.query.filter_by(survey_id=3).all()])