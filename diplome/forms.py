from django import forms
from .models import Anneeuniv


class AnneeForm(forms.Form):

    
    # Menu déroulant avec toutes les catégories
    annee = forms.ModelChoiceField(
        queryset=Anneeuniv.objects.all(),
        label="Choisir une catégorie",
        empty_label="-- Sélectionnez --"  # option par défaut
    )