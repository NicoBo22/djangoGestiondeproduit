from etudiant.models import Inscriptionmat,Inscriptiondiplome,Etudiant
from matiere.models import Matiere
from diplome.models import Diplome,Anneeuniv
from random import gauss,choice

def fonctioninscriptionsetudiant():
    anneeunivencours = Anneeuniv.objects.get(encours = True)
    diplome = Diplome.objects.get(id=1)
    listeEtudiants = Etudiant.objects.filter(inscriptions__anneeuniv=anneeunivencours,inscriptions__diplome=diplome)
    for etudiant in listeEtudiants:
        inscriptiondiplome = Inscriptiondiplome.objects.get(etudiant=etudiant, diplome =diplome, anneeuniv =  anneeunivencours)
        listeinscritmat=Inscriptionmat.objects.filter(inscriptiondiplome=inscriptiondiplome)

        for inscriptionmatiere in listeinscritmat:
            

            inscriptionmatiere.notecc1 = calculNote()
            inscriptionmatiere.notecc2 = calculNote()
            inscriptionmatiere.notecc3 = calculNote()
        
            inscriptionmatiere.save()




def calculNote():
    note = round(gauss(9.5,6),3)
    if note > 20:
        note = 19.5
    if note < 0:
        note = 2.5
    return note