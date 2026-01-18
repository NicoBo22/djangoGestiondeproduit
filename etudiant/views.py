from django.contrib.auth.decorators import login_required,permission_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from .models import Inscriptionmat,Inscriptiondiplome,Etudiant
from diplome.models import Anneeuniv,Diplome
from matiere.models import Matiere
from .forms import EtudiantForm,InscriptiondiplForm,MatiereSelectionForm
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


@login_required
def indexetudiant(request):
    anneeunivsession = request.session.get('anneesession')

    anneeuniv =get_object_or_404(Anneeuniv,anneeuniv=anneeunivsession)  
    templateData = {}
    templateData ['titre']= "Etudiants"
    ListeInscritDiplome = Inscriptiondiplome.objects.filter(anneeuniv=anneeuniv).order_by('etudiant__nom','etudiant__prenom')
    templateData ['inscritdiplome']= ListeInscritDiplome
    templateData['anneeuniv'] = anneeuniv
    return render (request,'etudiant/listeetudiant.html'
                  ,{'templateData': templateData} )


@permission_required('etudiant.change_etudiant', raise_exception=True)
@login_required
def addetudiant(request):
    if request.method=='POST':
        form=EtudiantForm(request.POST)
        if form.is_valid():
            etudiant=form.save()
            
            return redirect('etudiant:addinscriptiondipl')
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
            return redirect('etudiant:addinscriptionmat',id = etudiant.id)
    else:
        form=InscriptiondiplForm()
    templateData = {}
    templateData ['titre']= "Inscription d'un etudiant "

    return render(request,'etudiant/inscriptiondipletudiant.html',{'form': form, 'templatedata':templateData})

@permission_required('etudiant.change_etudiant', raise_exception=True)
@login_required
def addinscriptionmat(request,id):
    etudiant = Etudiant.objects.get(id=id)
    anneeunivinscrit = Anneeuniv.objects.get(anneeuniv=request.session.get('anneesession')) 
    diplome = Diplome.objects.get(id=1)
    existe =Inscriptiondiplome.objects.filter(etudiant=etudiant,anneeuniv=anneeunivinscrit,diplome=diplome).exists()
    if existe:
        if request.method == "POST":
            form = MatiereSelectionForm(request.POST)
            if form.is_valid():
                inscriptiondipl = Inscriptiondiplome.objects.get(etudiant=etudiant,anneeuniv=anneeunivinscrit,diplome=diplome)

                matieres_selectionnees = form.cleaned_data['matieres']
            
                listematiere =Matiere.objects.all()
                for matiere in listematiere:

                    existeInscrMat=Inscriptionmat.objects.filter(inscriptiondiplome=inscriptiondipl,matiere=matiere).exists()

                    if (not existeInscrMat) and (matiere in matieres_selectionnees):
                        print(matiere.nom)
                        inscriptionmatiere = Inscriptionmat(inscriptiondiplome=inscriptiondipl,matiere=matiere)
                        inscriptionmatiere.save()
                    elif existeInscrMat and not (matiere in matieres_selectionnees):
                        inscriptionmatiere=Inscriptionmat.objects.filter(inscriptiondiplome=inscriptiondipl,matiere=matiere)
                        inscriptionmatiere.delete()
                return redirect('etudiant:vue',id=etudiant.id)
                        


        else:
            form = MatiereSelectionForm()
        templateData = {}
        templateData ['titre']= "Inscription matières " + etudiant.nom +" "+etudiant.prenom
        templateData ['etudiant']= etudiant 
        templateData ['annee']= anneeunivinscrit
        return render(request, "etudiant/inscriptionmat.html", {'form': form, 'templatedata':templateData})
    else:
        message = "Etudiant "+etudiant.nom+" "+etudiant.prenom+" n'est pas inscrit en "+anneeunivinscrit.anneeuniv
        messages.warning(request,message)
        return redirect('etudiant:index')




@login_required
def listeetudiant(request,alt):
    anneeunivsession = request.session.get('anneesession')

    anneeuniv =get_object_or_404(Anneeuniv,anneeuniv=anneeunivsession)  
    templateData = {}
    templateData ['titre']= "Etudiants"
    ListeInscritDiplome = Inscriptiondiplome.objects.filter(anneeuniv=anneeuniv)
    if alt == 'alt':
        
        ListeInscritDiplome = ListeInscritDiplome.filter(alternant=True).order_by('etudiant__nom','etudiant__prenom')
    elif alt == 'neu':
        ListeInscritDiplome = ListeInscritDiplome.filter(neu=True).order_by('etudiant__nom','etudiant__prenom')

    elif alt == 'nonalt':
        ListeInscritDiplome = ListeInscritDiplome.filter(alternant=False).order_by('etudiant__nom','etudiant__prenom')
        
    elif alt == 'redoubl':
        ListeInscritDiplome = ListeInscritDiplome.filter(redoublant=True).order_by('etudiant__nom','etudiant__prenom')


    
    templateData ['inscritdiplome']= ListeInscritDiplome
    templateData['anneeuniv'] = anneeuniv
    return render (request,'etudiant/listeetudiant.html'
                  ,{'templateData': templateData} )

@login_required
def vueetudiant(request, id): 
    anneeunivsession = request.session.get('anneesession')

    anneeuniv =get_object_or_404(Anneeuniv,anneeuniv=anneeunivsession) 
    etudiant = Etudiant.objects.get(id=id)

    anneeunivencours = Anneeuniv.objects.get(encours = True)
    listeinsdiplome = Inscriptiondiplome.objects.filter(etudiant=etudiant)
    listeinsdiplome =listeinsdiplome.order_by('anneeuniv__datedebut')
    try:
        inscridipl = Inscriptiondiplome.objects.get(etudiant=etudiant,anneeuniv=anneeuniv)

    except (ObjectDoesNotExist, ValueError, TypeError):
        inscridipl= None
    if inscridipl is not None:
        if inscridipl.alternant :
            nbreetudiants = Inscriptiondiplome.objects.filter(anneeuniv=anneeuniv,alternant = True).count()
        else :
            nbreetudiants = Inscriptiondiplome.objects.filter(anneeuniv=anneeuniv,alternant = False).count()


        
   
    ListeInscritmat =Inscriptionmat.objects.filter(inscriptiondiplome__etudiant=etudiant ,inscriptiondiplome__anneeuniv__datedebut__lte=anneeuniv.datedebut)
    if(not(anneeuniv.S2)):
        ListeInscritmat = ListeInscritmat.filter(matiere__semestre ="S5")
    ListeInscritmat = ListeInscritmat.order_by('matiere__semestre','matiere__nom','inscriptiondiplome__anneeuniv')

    templateData = {}
    templateData ['titre']= "Etudiant : " + etudiant.nom +" "+  etudiant.prenom 
    templateData ['etudiant']= etudiant  
    templateData ['listeinscritmat']=ListeInscritmat
    templateData ['insdiplome']=inscridipl
    templateData ['listeinsdiplome']=listeinsdiplome
    templateData['S2']=anneeuniv.S2 

    templateData['nbreetudiants'] = nbreetudiants
    return render (request,'etudiant/vueetudiant.html'
                  ,{'templateData': templateData} )   

@permission_required('etudiant.change_etudiant', raise_exception=True)
@login_required
def indexetudiantadmin(request):
    anneeunivsession = request.session.get('anneesession')
    anneeuniv =get_object_or_404(Anneeuniv,anneeuniv=anneeunivsession)  
    templateData = {}
    templateData ['titre']= "Etudiants"
    ListeInscritDiplome = Inscriptiondiplome.objects.filter(anneeuniv=anneeuniv).order_by('etudiant__nom','etudiant__prenom')
    templateData ['inscritdiplome']= ListeInscritDiplome
    templateData['anneeuniv'] = anneeuniv
    return render (request,'etudiant/listeetudiantadmin.html'
                  ,{'templateData': templateData} )



