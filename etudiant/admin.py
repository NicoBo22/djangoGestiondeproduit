from django.contrib import admin

from .models import Etudiant,Inscriptiondiplome,Inscriptionmat

class InscriptiondiplomeAdmin(admin.ModelAdmin) :
    list_display = ["etudiant",'diplome','anneeuniv']
    exclude=["noteSem1",'rangSem1',"noteSem2",'rangSem2','noteAnnee',"statutDipl",'datedecisionDipl',
             'rangAnnee','statutS1','datedecisionS1','statutS2','datedecisionS2','avispoursuite','erasmus'
             ]

class InscriptionmatAdmin(admin.ModelAdmin) :
    exclude =[ "decisionmat" ]

class EtudiantAdmin(admin.ModelAdmin) :
    exclude =[ "avispoursuite","Nmoinsun","erasmus" ]


admin.site.register(Etudiant,EtudiantAdmin)

admin.site.register(Inscriptiondiplome, InscriptiondiplomeAdmin)

admin.site.register(Inscriptionmat,InscriptionmatAdmin)

# Register your models here.
