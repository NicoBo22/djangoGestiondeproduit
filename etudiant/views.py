from django.contrib.auth.decorators import login_required,permission_required
from django.shortcuts import render,redirect
from .models import Inscriptionmat,Inscriptiondiplome,Etudiant
from diplome.models import Anneeuniv
from .forms import EtudiantForm,InscriptiondiplForm,MatiereSelectionForm
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


@login_required
def indexetudiant(request):
    anneeunivencours = Anneeuniv.objects.get(encours = True)

    templateData = {}
    templateData ['titre']= "Etudiants"
    ListeInscritDiplome = Inscriptiondiplome.objects.filter(anneeuniv=anneeunivencours).order_by('etudiant__nom','etudiant__prenom')
    templateData ['inscritdiplome']= ListeInscritDiplome
    templateData['anneeuniv'] = anneeunivencours
    return render (request,'etudiant/listeetudiant.html'
                  ,{'templateData': templateData} )


@permission_required('etudiant.change_etudiant', raise_exception=True)
@login_required
def addetudiant(request):
    if request.method=='POST':
        form=EtudiantForm(request.POST)
        if form.is_valid():
            etudiant=form.save()
            
            return redirect('etudiant:vue',id=etudiant.id)
    else:
        form=EtudiantForm()
    templateData = {}
    templateData ['titre']= "Création d'un etudiant "
    return render(request,'etudiant/creeretudiant.html',{'form': form, 'templatedata':templateData})


@permission_required('etudiant.change_etudiant', raise_exception=True)
@login_required
def addinscriptiondipl(request):
    if request.method=='POST':
        form=InscriptiondiplForm(request.POST)
        if form.is_valid():
            etudiant =form.cleaned_data['etudiant']

            form.save()
            return redirect('etudiant:inscriptionmat',id = etudiant.id)
    else:
        form=InscriptiondiplForm()
    templateData = {}
    templateData ['titre']= "Inscription d'un etudiant "

    return render(request,'etudiant/inscriptiondipletudiant.html',{'form': form, 'templatedata':templateData})

@permission_required('etudiant.change_etudiant', raise_exception=True)
@login_required
def addinscriptionmat(request):
    templateData = {}
    templateData ['titre']= "Inscription matières "
    if request.method == "POST":
        form = MatiereSelectionForm(request.POST)
        if form.is_valid():
            matieres_selectionnees = form.cleaned_data['matieres']
            # fais quelque chose avec matieres_selectionnees
    else:
        form = MatiereSelectionForm()

    return render(request, "etudiant/inscriptionmat.html", {'form': form, 'templatedata':templateData})



@login_required
def listeetudiant(request,alt):
    anneeunivencours = Anneeuniv.objects.get(encours = True)

    templateData = {}
    templateData ['titre']= "Etudiants"
    ListeInscritDiplome = Inscriptiondiplome.objects.filter(anneeuniv=anneeunivencours)
    if alt == 'alt':
        
        ListeInscritDiplome = ListeInscritDiplome.filter(etudiant__alternant=True).order_by('etudiant__nom','etudiant__prenom')
    elif alt == 'neu':
        ListeInscritDiplome = ListeInscritDiplome.filter(etudiant__neu=True).order_by('etudiant__nom','etudiant__prenom')
    else:
        ListeInscritDiplome = ListeInscritDiplome.filter(etudiant__alternant=False).order_by('etudiant__nom','etudiant__prenom')

    
    templateData ['inscritdiplome']= ListeInscritDiplome
    templateData['anneeuniv'] = anneeunivencours
    return render (request,'etudiant/listeetudiant.html'
                  ,{'templateData': templateData} )

@login_required
def vueetudiant(request, id): 
    etudiant = Etudiant.objects.get(id=id)

    anneeunivencours = Anneeuniv.objects.get(encours = True)
    listeinsdiplome = Inscriptiondiplome.objects.filter(etudiant=etudiant)
    listeinsdiplome =listeinsdiplome.order_by('anneeuniv__datedebut')
    try:
        inscridipl = listeinsdiplome.get(etudiant=etudiant,anneeuniv=anneeunivencours)
    except (ObjectDoesNotExist, ValueError, TypeError):
        inscridipl= None 
    
    ListeInscritmat =Inscriptionmat.objects.filter(etudiant=etudiant )
    if(not(anneeunivencours.S2)):
        ListeInscritmat = ListeInscritmat.filter(matiere__semestre ="S5")
    ListeInscritmat = ListeInscritmat.order_by('matiere__semestre')

    templateData = {}
    templateData ['titre']= "Etudiant : " + etudiant.nom +" "+  etudiant.prenom 
    templateData ['etudiant']= etudiant  
    templateData ['listeinscritmat']=ListeInscritmat
    templateData ['insdiplome']=inscridipl
    templateData ['listeinsdiplome']=listeinsdiplome
    templateData['S2']=anneeunivencours.S2
    return render (request,'etudiant/vueetudiant.html'
                  ,{'templateData': templateData} )   




