from django.contrib.auth.decorators import login_required,permission_required
from django.shortcuts import render,redirect
from .forms import AnneeForm, Semestre2Form, CreationAnneeForm 
from django.contrib import messages
from .models import Anneeuniv
from datetime import date, timedelta

# Create your views here.
@login_required
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

@permission_required('etudiant.change_etudiant', raise_exception=True)
@login_required
def S2(request):
    if request.method =='POST':
        form =Semestre2Form(request.POST)
        if form.is_valid():
            validerS2 = form.cleaned_data['validerS2']
            if validerS2:
                anneeuniEncours = Anneeuniv.objects.get(encours="True")
                anneeuniEncours.S2 = True
                
                messages.success(request,"Semestre 2 de l'année en cours: "+anneeuniEncours.anneeuniv +" validé")
            else:
                anneeuniEncours = Anneeuniv.objects.get(encours="True")
                anneeuniEncours.S2 = False
                messages.warning(request,"Semestre 2 de l'année en cours: "+anneeuniEncours.anneeuniv +" non validé")
            anneeuniEncours.save()
            return redirect('etudiant:index')
    else:
        form =Semestre2Form()
    templateData = {}
    templateData ['titre']= "Validation Semestre 2 "
    return render(request, 'diplome/formulaireannee.html', {'form': form, 'templatedata':templateData})

@permission_required('etudiant.change_etudiant', raise_exception=True)
@login_required
def creationannee(request):
    if request.method =='POST':
        form = CreationAnneeForm (request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']   # <-- RÉCUPÉRATION ICI
            if Anneeuniv.objects.filter(datedebut__year=date.year).exists():
                annee = Anneeuniv.objects.get(datedebut__year=date.year)
                messages.warning(request,'Il existe déja une année universitaire : ' + annee.anneeuniv )
            else:
                messages.success(request,'Année créée')
                anneencours = Anneeuniv.objects.get(encours=True)
                anneencours.encours=False
                annee = Anneeuniv.objects.create(anneeuniv = str(date.year)+"/"+str((date+timedelta(days=365)).year),
                                                 encours=True,
                                                 S2=False,datedebut=date)
                annee.save()
                anneencours.save()

    

            return redirect('etudiant:index')
    else:
        form =CreationAnneeForm()
    templateData = {}
    templateData ['titre']="Création année universitaire" 
    return render(request, 'diplome/formulaireannee.html', {'form': form, 'templatedata':templateData})  


        



