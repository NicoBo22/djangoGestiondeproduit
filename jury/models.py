from django.db import models
from diplome.models import Diplome,Anneeuniv

# Create your models here.
class Jury(models.Model):
    id = models.AutoField(primary_key=True)
    datejury = models.DateTimeField(null=True)
    anneeuniv=models.ForeignKey(Anneeuniv,on_delete=models.CASCADE)
    diplome=models.ForeignKey(Diplome,on_delete=models.CASCADE)
    semestre =models.CharField(max_length=3)
    alternant = models.BooleanField()
    fini = models.BooleanField(default=False)

    def __str__(self):
        nom =self.diplome.nom+' : '+ self.anneeuniv.anneeuniv
        if self.alternant:
            nom += ": alternants"
        return nom