from django.shortcuts import render,redirect
from .forms import AnneeForm
from django.contrib import messages

# Create your views here.

def indexannee(request):
    if request.method == 'POST':
        form = AnneeForm(request.POST)
        if form.is_valid():
            annee = form.cleaned_data['annee']
            
            request.session['anneesession']=annee.anneeuniv
            messages.success(request,"L'année choisie : "+annee.anneeuniv )
            
            return redirect('etudiant:index')


    else:
        form = AnneeForm()
    templateData = {}
    templateData ['titre']= "Choix de l'année "
    return render(request, 'diplome/formulaireannee.html', {'form': form, 'templatedata':templateData})


