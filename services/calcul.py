from etudiant.models import Inscriptionmat
from matiere.models import Matiere,Nbreinscrit
from diplome.models import Anneeuniv
def moyenneMat(inscriptionmat):
    tuplenotesCC = (inscriptionmat.notecc1,inscriptionmat.notecc2,inscriptionmat.notecc3)
    moyenne = None
    if all(cc is not None for cc in tuplenotesCC):
        moyenne = inscriptionmat.matiere.coefcc1*max(inscriptionmat.notecc1,inscriptionmat.notecc3)
        moyenne += inscriptionmat.matiere.coefcc2*max(inscriptionmat.notecc2,inscriptionmat.notecc3)
        moyenne += inscriptionmat.matiere.coefcc3*inscriptionmat.notecc3
        moyenne /=100
        moyenne = round(moyenne,3)

    return moyenne   

def calculderangSemestre(listediplome,sem):
    if sem == "S5":
        listediplome =listediplome.order_by('-noteSem1')
        rang = 1
        nb = 1
        for i,inscridiplome in enumerate(listediplome):
            if i>0:
                if(inscridiplome.noteSem1 != listediplome[i-1].noteSem1):
                    rang = rang + nb
                    nb = 1
                else:
                    nb =nb +1
            inscridiplome.rangSem1 = rang
            inscridiplome.save()
    elif sem == "S6":
        listediplome =listediplome.order_by('-noteSem2')
       
        rang = 1
        nb = 1
        for i,inscridiplome in enumerate(listediplome):
            if i>0:
                if(inscridiplome.noteSem2 != listediplome[i-1].noteSem2):
                    rang = rang + nb
                    nb = 1
                else:
                    nb =nb +1
            inscridiplome.rangSem2 = rang
            inscridiplome.save()

 
        

def calculderang(listeInscrit):
    listeInscrit= listeInscrit.exclude(moyenne__isnull = True)
    listeInscrit=listeInscrit.order_by('-moyenne')
    rang = 1
    nb = 1
    for i,inscrimat in enumerate(listeInscrit):

        if i>0:
            if(inscrimat.moyenne != listeInscrit[i-1].moyenne):
                rang = rang + nb
                nb = 1
            else:
                nb = nb+1
        inscrimat.rang = rang
        inscrimat.save()

def calculSem(etudiant,sem) :
    #chercher les inscriptions matières
    somme =0
    nbADM =0
    nbMat = 0
    listemat = Matiere.objects.filter(semestre=sem)
    for mat in listemat:
        listeins=Inscriptionmat.objects.filter(inscriptiondiplome__etudiant=etudiant,matiere=mat).order_by("matiere_id","-inscriptiondiplome__anneeuniv")
        if len(listeins)>0:
            if listeins[0].moyenne is not None:
               
                somme+=listeins[0].moyenne
                if listeins[0].moyenne>=10.0:
                    nbADM +=1
                nbMat +=1
   
    if nbMat ==10:
        moyennesemestre = round(somme/10,3)
        if  nbADM ==10:
            statut = "ADM"
        else:
            statut = "AJ"   
    else :
        moyennesemestre = -1
        statut =None
    

    return [moyennesemestre ,statut] 

def calculrangannee(liste):
    listeInscrit= liste.exclude(noteAnnee__isnull = True)
    listeInscrit=listeInscrit.order_by('-noteAnnee')
    rang = 1
    nb = 1
    for i,inscritdipl in enumerate(listeInscrit):

        if i>0:
            if(inscritdipl.noteAnnee != listeInscrit[i-1].noteAnnee):
                rang = rang + nb
                nb = 1
            else:
                nb = nb+1
        inscritdipl.rangAnnee = rang
        inscritdipl.save()    

def calculNbreInscrit():
    anneeunivencours = Anneeuniv.objects.get(encours = True)
    listeMatieres = Matiere.objects.all()
    for matiere in listeMatieres:
        if Nbreinscrit.objects.filter(matiere = matiere,anneeuniv=anneeunivencours).exists():
            nb = Nbreinscrit.objects.filter(matiere = matiere,anneeuniv=anneeunivencours)
            nb.nbrInscrit =   Inscriptionmat.objects.filter(matiere =matiere,inscritdiplome__anneeuniv= anneeunivencours).count()
            nb.save()
        else:
            nbinscrit= Nbreinscrit()
            nbinscrit.matiere=matiere
            nbinscrit.anneeuniv=anneeunivencours
            nbinscrit.nbrInscrit = Inscriptionmat.objects.filter(matiere =matiere,inscriptiondiplome__anneeuniv= anneeunivencours).count()
            nbinscrit.save()