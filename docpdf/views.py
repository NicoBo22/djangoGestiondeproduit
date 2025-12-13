import pdfkit
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required

from etudiant.models import Inscriptiondiplome,Inscriptionmat,Etudiant
from diplome.models import Anneeuniv,Diplome
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
# Create your views here.




@login_required
def avispoursuite(request,id):

    etudiant = Etudiant.objects.get(id=id)
    anneeunivencours = Anneeuniv.objects.get(encours = True)
    listeinsdiplome = Inscriptiondiplome.objects.filter(etudiant=etudiant)
    listeinsdiplome =listeinsdiplome.order_by('anneeuniv__datedebut')
    listeInscritmat =Inscriptionmat.objects.filter(inscriptiondiplome__etudiant=etudiant,matiere__semestre ="S5" )
    try:
        inscridipl = listeinsdiplome.get(etudiant=etudiant,anneeuniv=anneeunivencours)

    except (ObjectDoesNotExist, ValueError, TypeError):
        inscridipl= None
    if inscridipl is not None:
        if inscridipl.alternant :
            nbreetudiants = Inscriptiondiplome.objects.filter(anneeuniv=anneeunivencours,alternant = True).count()
        else :
            nbreetudiants = Inscriptiondiplome.objects.filter(anneeuniv=anneeunivencours,alternant = False).count()

    html = render_to_string("docpdf/document.html", {

        "etudiant": etudiant,
        "date":date.today(),
        "listemat":listeInscritmat,
        'insdiplome':inscridipl,
        "nbetud": nbreetudiants,
    })

    config = pdfkit.configuration(
        wkhtmltopdf=settings.PDFKIT_CONFIG['wkhtmltopdf']
    )
    options = {
    'encoding': "UTF-8",
    }
    pdf = pdfkit.from_string(html, False, configuration=config,options=options)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="document.pdf"'

    return response
