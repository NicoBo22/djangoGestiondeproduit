from django.db import models
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
