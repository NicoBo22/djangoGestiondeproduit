from django import forms
from .models import Anneeuniv



class AnneeForm(forms.Form):

    
    # Menu déroulant avec toutes les catégories
    annee = forms.ModelChoiceField(
        queryset=Anneeuniv.objects.all(),
        label="Choisir une catégorie",
        empty_label="-- Sélectionnez --"  # option par défaut
    )


class Semestre2Form(forms.Form):


    validerS2 = forms.BooleanField(
        label="Validation du second semestre",
        required=False
    )

class CreationAnneeForm(forms.Form):
        date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )