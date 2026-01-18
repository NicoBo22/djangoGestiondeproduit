from django import forms


class CCForm(forms.Form):
    CC1 = forms.FloatField(
        label ="CC1",
        min_value=0.0,
        max_value=20.0,
        required=False)
    CC2 = forms.FloatField(
        label ="CC2",
        min_value=0.0,
        max_value=20.0,
        required=False)    
    CC3 = forms.FloatField(
        label ="CC3",
        min_value=0.0,
        max_value=20.0,
        required=False)
    ADJ = forms.BooleanField(
        label="ADJ",
        required=False)

    
    def __init__(self, *args, **kwargs):
        inscrimat = kwargs.pop('inscrimat', None)
        super().__init__(*args, **kwargs)
        if inscrimat:
            self.fields['CC1'].initial = inscrimat.notecc1
            self.fields['CC2'].initial = inscrimat.notecc2
            self.fields['CC3'].initial = inscrimat.notecc3
                       
            

