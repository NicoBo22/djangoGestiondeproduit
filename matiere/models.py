from django.db import models

from diplome.models import Anneeuniv


class Matiere(models.Model):

    
    codeapogee = models.CharField(max_length=25, unique = True)
    nom = models.CharField(max_length=255)
    semestre = models.CharField(max_length=2)
    coefcc1 = models.IntegerField()
    coefcc2 = models.IntegerField()
    coefcc3 = models.IntegerField()

    def __str__(self):
        return self.nom
    
# Create your models here.
class Nbreinscrit(models.Model):
    matiere =models.ForeignKey(Matiere, on_delete=models.CASCADE)
    anneeuniv=models.ForeignKey(Anneeuniv, on_delete=models.CASCADE)
    nbrInscrit=models.IntegerField()
    alt=models.BooleanField()
