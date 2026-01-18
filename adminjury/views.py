from django.shortcuts import render,redirect,get_object_or_404
from services.inscription import fonctioninscriptionsetudiant
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib import messages
from etudiant.models import Inscriptionmat,Inscriptiondiplome
from matiere.models import Matiere
from services.calcul import moyenneMat,calculderang,calculSem,calculderangSemestre,calculrangannee,calculNbreInscrit
from diplome.models import Anneeuniv
# Create your views here.

@login_required
@permission_required('etudiant.change_etudiant', raise_exception=True)
def inscription(request):
    fonctioninscriptionsetudiant()
    messages.info(request, "Création de notes fictives" )
    return redirect('home:index')

@login_required
@permission_required('etudiant.change_etudiant', raise_exception=True)
def nbrinscritmatiere(request):
    calculNbreInscrit()
    messages.info(request, "calcul du nombre d inscrit par matière" )
    return redirect('home:index')


@login_required
@permission_required('etudiant.change_etudiant', raise_exception=True)
def calculMoyenneMat(request,idmat,alt):
   

    anneeunivsession = request.session.get('anneesession')

    anneeuniv =get_object_or_404(Anneeuniv,anneeuniv=anneeunivsession)  
    if alt == "alt":
        listeInscrimat =Inscriptionmat.objects.filter(inscriptiondiplome__anneeuniv=anneeuniv,matiere=idmat,inscriptiondiplome__alternant=True)

    else:

        listeInscrimat =Inscriptionmat.objects.filter(inscriptiondiplome__anneeuniv=anneeuniv,matiere=idmat,inscriptiondiplome__alternant=False)

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
    #calcul de toutes les matières du semestre
  

    anneeunivsession = request.session.get('anneesession')

    anneeuniv =get_object_or_404(Anneeuniv,anneeuniv=anneeunivsession)  

    listematieres = Matiere.objects.filter(semestre=sem)
    for matiere in listematieres:

        if alt == "alt":
            listeInscrimat =Inscriptionmat.objects.filter(inscriptiondiplome__anneeuniv=anneeuniv,
                                                          inscriptiondiplome__alternant=True,matiere=matiere)            


        else:

            listeInscrimat =Inscriptionmat.objects.filter(inscriptiondiplome__anneeuniv=anneeuniv,
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

    anneeunivsession = request.session.get('anneesession')

    anneeuniv =get_object_or_404(Anneeuniv,anneeuniv=anneeunivsession)  

    listeInscritDiplomeSem = Inscriptiondiplome.objects.filter(anneeuniv=anneeuniv)
    if alt == "alt":
        listeInscritDiplomeSem=listeInscritDiplomeSem.filter(alternant=True)
    elif alt == "nonalt":
        listeInscritDiplomeSem=listeInscritDiplomeSem.filter(alternant=False)
    for inscridiplome in listeInscritDiplomeSem:
        if sem == 'S5':
            etud = inscridiplome.etudiant
            
          
            moyenneSem=calculSem(etud,'S5', anneeunivsession )
            
            inscridiplome.noteSem1 = moyenneSem[0]
            if inscridiplome.statutS1 != "ADJ":
                inscridiplome.statutS1 = moyenneSem[1]
        elif sem == 'S6':
            etud = inscridiplome.etudiant
            
          
            moyenneSem=calculSem(etud,'S6', anneeunivsession )
            
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

    anneeunivsession = request.session.get('anneesession')

    anneeuniv =get_object_or_404(Anneeuniv,anneeuniv=anneeunivsession)  

    listeInscritDiplome = Inscriptiondiplome.objects.filter(anneeuniv=anneeuniv)
    if alt == "alt":
        listeInscritDiplome=listeInscritDiplome.filter(alternant=True)
    elif alt == "nonalt":
        listeInscritDiplome=listeInscritDiplome.filter(alternant=False)
    for inscridiplome in listeInscritDiplome:
        if inscridiplome.noteSem1 is not None and inscridiplome.noteSem2 is not None:
            inscridiplome.noteAnnee = (inscridiplome.noteSem1 +inscridiplome.noteSem2)/2

            if inscridiplome.statutS1=="ADM" and inscridiplome.statutS2=="ADM":
                inscridiplome.statutDipl = "ADM"
            elif inscridiplome.statutS1!="ADJ":
                inscridiplome.statutDipl = "AJ"

            
        
            inscridiplome.save()
    calculrangannee(listeInscritDiplome)




    messages.info(request, "Calcul des moyennes et Rang : année")
    return redirect('etudiant:index') 

@login_required
@permission_required('etudiant.change_etudiant', raise_exception=True)
def reset(request):
    anneeunivsession = request.session.get('anneesession')

    anneeuniv =get_object_or_404(Anneeuniv,anneeuniv=anneeunivsession) 
    listeInscritDiplome = Inscriptiondiplome.objects.filter(anneeuniv=anneeuniv)
    for inscritdiplom in listeInscritDiplome:
        listematieres = Matiere.objects.all()
        for matiere in listematieres:
           if Inscriptionmat.objects.filter(inscriptiondiplome=inscritdiplom,matiere=matiere).exists():
               inscriptionmat = Inscriptionmat.objects.get(inscriptiondiplome=inscritdiplom,matiere=matiere)
               inscriptionmat.notecc1 = None
               inscriptionmat.notecc2 = None
               inscriptionmat.notecc3 = None
               inscriptionmat.moyenne = None
               inscriptionmat.statut = None
               inscriptionmat.rang = None
               inscriptionmat.pointjury = None
               inscriptionmat.save()






    messages.info(request, "Reset effectué")
    return redirect('etudiant:index' ) 




    
