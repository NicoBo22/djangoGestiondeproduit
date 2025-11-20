from diplome.models import Anneeuniv



def session_vars(request):


     return {
        'anneesession': request.session.get('anneesession',Anneeuniv.objects.get(encours = True).anneeuniv ),
        'diplome': request.session.get('diplome', "K3MKGE"),
    }
