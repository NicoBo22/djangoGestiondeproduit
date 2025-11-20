from django.db import models
from diplome.models import Diplome,Anneeuniv
from matiere.models import Matiere


# Create your models here.
class Etudiant(models.Model):
    class Genre(models.TextChoices):
        Monsieur = 'M.'
        Madame = 'Mme'



    id = models.AutoField(primary_key=True)
    numero = models.IntegerField(unique=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    genre = models.CharField(choices=Genre.choices, max_length=5)

    datedenaissance = models.DateField( null=True)
    Nmoinsun = models.CharField(max_length=255, null=True,blank=True)


    photo = models.ImageField(upload_to='photos/', default='photos/image.jpg')

   

    def __str__(self):
        return self.nom+' '+ self.prenom
    
class Inscriptiondiplome(models.Model):
    class Statut(models.TextChoices):
        Admis = 'ADM'
        Admis_Jury = 'ADJ'
        Ajourne = 'AJ'
        SansResultat ='Sresul'
    class AvisPoursuite(models.TextChoices):
        TRESFAVORABLE ='TF', 'Avis très favorable'
        FAVORABLE = 'FA', 'Avis favorable'
        RESERVE = 'RE', 'Avis réservé'
        DEFAVORABLE = 'DE', 'Avis défavorable'
    class Erasmus(models.TextChoices):
        ENTRANT='E','Entrant'
        SORTANT = 'S','Sortant'

    etudiant = models.ForeignKey(Etudiant,on_delete=models.CASCADE, related_name="inscriptionDipEtud")
    diplome = models.ForeignKey(Diplome,on_delete=models.CASCADE, related_name="inscriptionDip")
    anneeuniv=models.ForeignKey(Anneeuniv,on_delete=models.CASCADE)
    noteSem1=models.FloatField(null=True,default=None,blank = True)
    rangSem1=models.IntegerField(null=True)
    noteSem2=models.FloatField(null=True,default=None,blank = True)
    rangSem2=models.IntegerField(null=True)
    noteAnnee=models.FloatField(null=True,default=None,blank = True)
    rangAnnee=models.IntegerField(null=True)
    statutDipl = models.CharField(null=True,choices=Statut.choices, max_length=6,blank=True,default =None)
    datedecisionDipl = models.DateTimeField(null=True,default=None)
    statutS1 = models.CharField(null=True,choices=Statut.choices, max_length=6,blank=True,default =None)
    datedecisionS1 = models.DateTimeField(null=True,default=None)
    statutS2 = models.CharField(null =True,choices=Statut.choices, max_length=6,blank=True,default =None)
    datedecisionS2 = models.DateTimeField(null=True,default=None)
    avispoursuite = models.CharField(choices=AvisPoursuite.choices, 
                                     max_length=2,null = True)
    erasmus = models.CharField(choices=Erasmus.choices,
                                     max_length=1,null = True, blank=True)
    iaL2 = models.BooleanField(default=False)
    alternant = models.BooleanField(default=False)
    neu = models.BooleanField(default=False)
    tierstemps = models.BooleanField(default=False)
    rse = models.BooleanField(default=False)
    redoublant =models.BooleanField(default=False)

    def __str__(self):
        return self.anneeuniv.anneeuniv + ' : ' +self.etudiant.nom +' '+self.diplome.nom      

class Inscriptionmat(models.Model):
    class Statut(models.TextChoices):
        Admis = 'ADM'
        Admis_Jury = 'ADJ'
        Ajourne = 'AJ'
        SansResultat ='Sresul'
    
    inscriptiondiplome = models.ForeignKey(Inscriptiondiplome,on_delete=models.CASCADE, null=True,)
    matiere = models.ForeignKey(Matiere,on_delete=models.CASCADE, related_name="matieres",related_query_name='mat')

    notecc1=models.FloatField(null=True)
    notecc2=models.FloatField(null=True)
    notecc3=models.FloatField(null=True)
    moyenne=models.FloatField(null=True)
    statut = models.CharField(null = True,choices=Statut.choices, max_length=6)
    decisionmat = models.DateTimeField(null=True)
    rang=models.IntegerField(null=True)

    def __str__(self):
        return self.anneeuniv.anneeuniv + ' : ' +self.etudiant.nom +' '+self.matiere.nom