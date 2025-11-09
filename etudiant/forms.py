from django import forms
from .models import Etudiant,Inscriptiondiplome
from matiere.models import Matiere

class EtudiantForm(forms.ModelForm):


    class Meta:
        model=Etudiant
        fields='__all__'

class InscriptiondiplForm(forms.ModelForm):


    class Meta:
        model=Inscriptiondiplome
        fields=["etudiant","diplome","anneeuniv"]


class MatiereSelectionForm(forms.Form):
    matieres = forms.ModelMultipleChoiceField(
        queryset=Matiere.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Selection des matières")
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['matieres'].queryset=Matiere.objects.all()
        self.initial['matieres'] = Matiere.objects.all()
