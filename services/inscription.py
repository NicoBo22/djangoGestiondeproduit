from etudiant.models import Inscriptionmat,Inscriptiondiplome,Etudiant
from matiere.models import Matiere
from diplome.models import Diplome,Anneeuniv
from random import gauss,choice

def fonctioninscriptionsetudiant():
    ListeEtudiants = Etudiant.objects.all()
    anneeunivencours = Anneeuniv.objects.get(encours = True)
    ListeMatiereS6 = Matiere.objects.filter(semestre='S6')
    diplome = Diplome.objects.get(id=1)
    for etudiant in ListeEtudiants:
        inscriptiondiplome = Inscriptiondiplome()
        inscriptiondiplome.etudiant=etudiant
        inscriptiondiplome.anneeuniv=anneeunivencours
       
        inscriptiondiplome.diplome =  diplome
        inscriptiondiplome.save()
        for i in [1,2,3,4,5,6,7,8,11]:

            inscriptionmatiere= Inscriptionmat()
            
            inscriptionmatiere.inscriptiondiplome=inscriptiondiplome
            inscriptionmatiere.matiere = Matiere.objects.get(id=i)
            inscriptionmatiere.notecc1 = calculNote()
            inscriptionmatiere.notecc2 = calculNote()
            inscriptionmatiere.notecc3 = calculNote()
           
            inscriptionmatiere.save()
        inscriptionmatiere= Inscriptionmat()
        inscriptionmatiere.inscriptiondiplome=inscriptiondiplome

        i = choice([9,10])

        inscriptionmatiere.matiere = Matiere.objects.get(id=i)
        inscriptionmatiere.notecc1 = calculNote()
        inscriptionmatiere.notecc2 = calculNote()
        inscriptionmatiere.notecc3 = calculNote()
     
        inscriptionmatiere.save()
        for matiere in ListeMatiereS6:
            inscriptionmatiere= Inscriptionmat()
            inscriptionmatiere.inscriptiondiplome=inscriptiondiplome
            inscriptionmatiere.matiere = matiere
            inscriptionmatiere.notecc1 = calculNote()
            inscriptionmatiere.notecc2 = calculNote()
            inscriptionmatiere.notecc3 = calculNote()
            inscriptionmatiere.save()

def calculNote():
    note = round(gauss(9,10),3)
    if note > 20:
        note = 19.5
    if note < 0:
        note = 2.5
    return note