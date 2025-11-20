from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib import messages
from .models import Matiere
from diplome.models import Anneeuniv
from etudiant.models import Inscriptionmat,Etudiant,Inscriptiondiplome
from .forms import CCForm
from services.calcul import  moyenneMat,calculderang

# Create your views here.

@login_required
def indexmatiere(request):
    templateData = {}
    templateData ['titre']= "Matiere"
    ListeMatiereS5 = Matiere.objects.filter(semestre='S5')
    ListeMatiereS6 = Matiere.objects.filter(semestre='S6')
    templateData ['matiereS5']= ListeMatiereS5
    templateData ['matiereS6']= ListeMatiereS6

    return render (request,'matiere/listematiere.html'
                  ,{'templateData': templateData} )

@login_required
def notes(request,code):
    matiere = Matiere.objects.get(codeapogee=code)
    anneeunivencours = Anneeuniv.objects.get(encours = True)
    alt = request.GET.get('alt','false').lower()=='true'
    ListeInscritmat =Inscriptionmat.objects.filter(matiere=matiere ,inscriptiondiplome__anneeuniv=anneeunivencours)
    if alt :
        ListeInscritmat=ListeInscritmat.filter(inscriptiondiplome__alternant=alt)
    ListeInscritmat = ListeInscritmat.exclude(moyenne__isnull = True)
    ListeInscritmat = ListeInscritmat.order_by('-moyenne')
    templateData = {}
    templateData ['titre']= "Notes: " + matiere.nom
    templateData ['matiere']= matiere  
    templateData ['listeinscritmat']=ListeInscritmat
    return render (request,'matiere/notesmatiere.html'
                  ,{'templateData': templateData} ) 

@login_required
@permission_required('gestiondejury.change_etudiant', raise_exception = True)
def editnotes(request,code,etudiant):
    matiere = Matiere.objects.get(codeapogee=code)
    anneeunivencours = Anneeuniv.objects.get(encours = True)
    etudiant= Etudiant.objects.get(id=etudiant)
    inscritmat = get_object_or_404(Inscriptionmat, inscriptiondiplome__etudiant = etudiant,matiere = matiere,inscriptiondiplome__anneeuniv = anneeunivencours)
    inscridipl = Inscriptiondiplome.objects.get(etudiant=etudiant,anneeuniv=anneeunivencours)
    if request.method == 'POST':
        notesCCform = CCForm(request.POST)

        if notesCCform.is_valid():
            # Récupérer les valeurs du formulaire
            cc1 = notesCCform.cleaned_data['CC1']
            cc2 = notesCCform.cleaned_data['CC2']
            cc3 = notesCCform.cleaned_data['CC3']
            matiere = Matiere.objects.get(codeapogee=code)



            inscritmat.notecc1 = cc1
            inscritmat.notecc2 = cc2
            inscritmat.notecc3 = cc3
            inscritmat.moyenne=moyenneMat(inscritmat)
            inscritmat.save()
            if inscritmat.moyenne>=10:
                inscritmat.statut = "ADM"
            elif inscritmat.statut != "ADJ":
                inscritmat.statut = "AJ"
            
            if inscritmat.inscriptiondiplome.alternant:
                listeInscrimat =Inscriptionmat.objects.filter(anneeuniv=anneeunivencours,matiere=matiere,inscriptiondiplome__alternant=True)
             
            else:

                listeInscrimat =Inscriptionmat.objects.filter(inscriptiondiplome__anneeuniv=anneeunivencours,matiere=matiere,inscriptiondiplome__alternant=False)
           
            calculderang(listeInscrimat)
            
            messages.success(request, "Notes de "+str(matiere.nom)+" "+str(etudiant.nom) + " "+str(etudiant.prenom)+ " changées")
            return redirect('etudiant:vue',id = etudiant.id)
    else :
        notesCCform = CCForm(inscrimat = inscritmat)
            


    templateData = {}
    templateData ['titre']= "Notes: " + matiere.nom
    templateData ['matiere']= matiere  
    templateData ['etudiant']=etudiant
    return render (request,'matiere/editnotes.html'
                  ,{'templateData': templateData,'notesCCform':notesCCform} ) 


@login_required
@permission_required('gestiondejury.change_etudiant', raise_exception = True)
def editnotesmatiere(request,code,alt,etudiantalpha):
    etudiantalpha =int(etudiantalpha)
    matiere = Matiere.objects.get(codeapogee=code)
    anneunivencours = Anneeuniv.objects.get(encours = True)
    ListeInscritmat =Inscriptionmat.objects.filter(matiere=matiere,inscriptiondiplome__anneeuniv=anneunivencours )

    if alt =="alt":
         ListeInscritmat =  ListeInscritmat.filter(inscriptiondiplome__alternant=True).order_by('inscriptiondiplome__etudiant__nom','inscriptiondiplome__etudiant__prenom')

    else:
         ListeInscritmat =  ListeInscritmat.filter(inscriptiondiplome____alternant=False).order_by('inscriptiondiplome__etudiant__nom','inscriptiondiplome__etudiant__prenom')

    inscritmat =  ListeInscritmat[etudiantalpha-1]
    if request.method == 'POST':
        notesCCform = CCForm(request.POST)

        if notesCCform.is_valid():
            # Récupérer les valeurs du formulaire
            cc1 = notesCCform.cleaned_data['CC1']
            cc2 = notesCCform.cleaned_data['CC2']
            cc3 = notesCCform.cleaned_data['CC3']
            matiere = Matiere.objects.get(codeapogee=code)
            inscritmat.notecc1 = cc1
            inscritmat.notecc2 = cc2
            inscritmat.notecc3 = cc3
            
            inscritmat.save()
            messages.success(request, "Notes de "+str(matiere.nom)+" "+str(inscritmat.inscriptiondiplome.etudiant.nom) +
                              " "+str(inscritmat.inscriptiondiplome.etudiant.prenom)+ " changées")
           
    else :
        notesCCform = CCForm(inscrimat = inscritmat)
            


    templateData = {}
    templateData ['titre']= "Notes: " + matiere.nom
    templateData ['matiere']= matiere  
    templateData ['etudiant']= inscritmat.inscriptiondiplome.etudiant
    templateData ['rangalpha']= etudiantalpha
    
    return render (request,'matiere/editnotesmatiere.html'
                  ,{'templateData': templateData,'notesCCform':notesCCform} ) 




