from django.contrib import admin

from .models import Etudiant,Inscriptiondiplome,Inscriptionmat

class InscriptiondiplomeAdmin(admin.ModelAdmin) :
    exclude =[ "datedecisionDipl" ,"datedecisionS1","datedecisionS2"]
 
class InscriptionmatAdmin(admin.ModelAdmin) :
    exclude =[ "decisionmat" ]

class EtudiantAdmin(admin.ModelAdmin) :
    exclude =[ "avispoursuite","Nmoinsun","erasmus" ]


admin.site.register(Etudiant,EtudiantAdmin)

admin.site.register(Inscriptiondiplome, InscriptiondiplomeAdmin)

admin.site.register(Inscriptionmat,InscriptionmatAdmin)

# Register your models here.
