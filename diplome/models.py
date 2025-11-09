from django.db import models

# Create your models here.
class Diplome(models.Model):
  
     codeapogee = models.CharField(max_length=25, unique = True)
     nom = models.CharField(max_length=255)

  

     def __str__(self):
        return self.nom 
     
class Anneeuniv(models.Model):
   anneeuniv=models.CharField(max_length=9,unique=True)
   encours =models.BooleanField()
   S2 = models.BooleanField(db_default=False)
   datedebut = models.DateField(null=True)

   def __str__(self):
        return self.anneeuniv