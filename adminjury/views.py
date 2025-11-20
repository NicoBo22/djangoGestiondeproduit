from django.shortcuts import render,redirect
from services.inscription import fonctioninscriptionsetudiant
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib import messages
from etudiant.models import Inscriptionmat,Inscriptiondiplome
from matiere.models import Matiere
from services.calcul import moyenneMat,calculderang,calculSem,calculderangSemestre
from diplome.models import Anneeuniv
# Create your views here.

@login_required
@permission_required('etudiant.change_etudiant', raise_exception=True)
def inscription(request):
    fonctioninscriptionsetudiant()
    messages.info(request, "Inscription diplome et matières" )
    return redirect('home:index')

@login_required
@permission_required('etudiant.change_etudiant', raise_exception=True)
def calculMoyenneMat(request,idmat,alt):
    anneunivencours = Anneeuniv.objects.get(encours = True)
    if alt == "alt":
        listeInscrimat =Inscriptionmat.objects.filter(inscriptiondiplome__anneeuniv=anneunivencours,matiere=idmat,inscriptiondiplome__alternant=True)

    else:

        listeInscrimat =Inscriptionmat.objects.filter(inscriptiondiplome__anneeuniv=anneunivencours,matiere=idmat,inscriptiondiplome__alternant=False)

    for inscrimat in listeInscrimat:
        inscrimat.moyenne = moyenneMat(inscrimat)
        if inscrimat.moyenne >= 10:
            inscrimat.statut = "ADM"
        elif inscrimat.statut!= "ADJ":
            inscrimat.statut = "AJ"

        inscrimat.save()
        calculderang(listeInscrimat)


    
    messages.info(request, "Calcul des moyennes : "+Matiere.objects.get(id = idmat).nom)
    return redirect('etudiant:index')
        
@login_required
@permission_required('etudiant.change_etudiant', raise_exception=True)
def calculMoyenneSemestre(request,sem,alt):
    anneunivencours = Anneeuniv.objects.get(encours = True)
    listematieres = Matiere.objects.filter(semestre=sem)
    for matiere in listematieres:

        if alt == "alt":
            listeInscrimat =Inscriptionmat.objects.filter(inscriptiondiplome__anneeuniv=anneunivencours,
                                                          inscriptiondiplome__alternant=True,matiere=matiere)            


        else:

            listeInscrimat =Inscriptionmat.objects.filter(inscriptiondiplome__anneeuniv=anneunivencours,
                                                          inscriptiondiplome__alternant=False,matiere=matiere)

        for inscrimat in listeInscrimat:
            inscrimat.moyenne = moyenneMat(inscrimat)
            if inscrimat.moyenne is None:
                inscrimat.statut = "Sresul"
            else:
                if inscrimat.moyenne >= 10:
                    inscrimat.statut = "ADM"
                elif inscrimat.statut != "ADJ":
                    inscrimat.statut = "AJ"

            inscrimat.save()
            calculderang(listeInscrimat)
    messages.info(request, "Calcul des moyennes matières : "+sem)
    return redirect('etudiant:index') 

@login_required
@permission_required('etudiant.change_etudiant', raise_exception=True)
def calculSemestre(request,sem,alt):
    anneunivencours = Anneeuniv.objects.get(encours = True)
    listeInscritDiplomeSem = Inscriptiondiplome.objects.filter(anneeuniv=anneunivencours)
    if alt == "alt":
        listeInscritDiplomeSem=listeInscritDiplomeSem.filter(alternant=True)
    elif alt == "nonalt":
        listeInscritDiplomeSem=listeInscritDiplomeSem.filter(alternant=False)
    for inscridiplome in listeInscritDiplomeSem:
        if sem == 'S5':
            etud = inscridiplome.etudiant
            
          
            moyenneSem=calculSem(etud,'S5')
            
            inscridiplome.noteSem1 = moyenneSem[0]
            if inscridiplome.statutS1 != "ADJ":
                inscridiplome.statutS1 = moyenneSem[1]
        elif sem == 'S6':
            etud = inscridiplome.etudiant
            
          
            moyenneSem=calculSem(etud,'S6')
            
            inscridiplome.noteSem2 = moyenneSem[0]
            if inscridiplome.statutS2 != "ADJ":
                inscridiplome.statutS2 = moyenneSem[1]            
        
  
        inscridiplome.save()
    calculderangSemestre(listeInscritDiplomeSem,sem)


    messages.info(request, "Calcul des moyennes et Rang : "+sem)
    return redirect('etudiant:index') 



@login_required
@permission_required('etudiant.change_etudiant', raise_exception=True)
def calculAnnee(request,codeDipl,alt):
    return redirect('etudiant:index')    

    
