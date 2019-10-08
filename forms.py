from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField

class SelectCaseForm(FlaskForm):
    osmoLytes = BooleanField("Osmolality and Electrolytes", default=False)
    renal = BooleanField("Renal physiology", default=False)
    lipoprotein = BooleanField("Lipoprotein Metaoblism", default=False)
    hepatitisHiv = BooleanField("Viral Hepatitis / HIV", default=False)
    enzymes = BooleanField("Enzymology", default=False)
    submit = SubmitField("Submit")