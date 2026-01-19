from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required,permission_required
from diplome.models import Anneeuniv,Diplome
from etudiant.models import Inscriptiondiplome,Inscriptionmat,Etudiant
from django.contrib import messages
from django.urls import reverse
from urllib.parse import urlencode
from .models import Jury
import  datetime
# Create your views here.

@login_required
def jury(request):
    listeJurys = Jury.objects.all().order_by("-datejury")
    templateData = {}
    templateData ['titre']= "Jury"
    templateData ['listeJurys']= listeJurys
    return render (request,'jury/listejurys.html'
                  ,{'templateData': templateData} )


@login_required
def jurydiplome(request,rang):
    anneeuniv = Anneeuniv.objects.get(encours = True)
    alt = request.GET.get('alt','false').lower()=='true'
    codeAPOGEE = request.GET.get('codeAPOGEE',"K3MKGE")
    diplomejury = Diplome.objects.get(codeapogee= codeAPOGEE)
    listeInscriptionDiplome =Inscriptiondiplome.objects.filter(diplome=diplomejury,
                                                      anneeuniv=anneeuniv,
                                                      alternant = alt)
    nbreetudiants = len( listeInscriptionDiplome)
    listeInscriptionDiplome=listeInscriptionDiplome.order_by("-noteAnnee")   
    etudiant =listeInscriptionDiplome[rang-1].etudiant
    inscridipl = listeInscriptionDiplome.get(etudiant=etudiant,anneeuniv=anneeuniv)

    listeinsdiplomeetu = Inscriptiondiplome.objects.filter(etudiant=etudiant)
    listeinsdiplomeetu =listeinsdiplomeetu.order_by('anneeuniv__datedebut')
    ListeInscritmatS6 =Inscriptionmat.objects.filter(inscriptiondiplome__etudiant=etudiant,matiere__semestre ="S6" )
    ListeInscritmatS5 =Inscriptionmat.objects.filter(inscriptiondiplome__etudiant=etudiant,matiere__semestre ="S5" )
    
    templateData = {}
    templateData ['titre']= "Jury diplome : " +anneeuniv.anneeuniv
    templateData ['annee']=anneeuniv
    templateData ['diplome']=diplomejury
    templateData ['etudiant']=etudiant
    templateData ['listeinsdiplome']=listeinsdiplomeetu
    templateData ['listeinscritmatS5']=ListeInscritmatS5
    templateData ['listeinscritmatS6']=ListeInscritmatS6
    templateData ['insdiplome']=inscridipl   
    templateData ['nbreetudiants']=nbreetudiants 
    templateData ['juryS5']=False

    return render (request,'jury/jurydiplomeetudiant.html'
                  ,{'templateData': templateData} )

@login_required
def juryS5(request,rang):
    anneeuniv = Anneeuniv.objects.get(encours = True)

    alt = request.GET.get('alt','false').lower()=='true'
    codeAPOGEE = request.GET.get('codeAPOGEE',"K3MKGE")
    diplomejury = Diplome.objects.get(codeapogee= codeAPOGEE)
    listeInscriptionDiplome =Inscriptiondiplome.objects.filter(diplome=diplomejury,
                                                      anneeuniv=anneeuniv,
                                                      alternant = alt)
    nbreetudiants = len( listeInscriptionDiplome)
    lpoursuiteEtude=[]
    liste = listeInscriptionDiplome.filter(avispoursuite ="TF")
    lpoursuiteEtude.append(len(liste))
    lpoursuiteEtude.append(len(liste)/ nbreetudiants *100)
    liste = listeInscriptionDiplome.filter(avispoursuite ="FA")
    lpoursuiteEtude.append(len(liste))
    lpoursuiteEtude.append(len(liste)/ nbreetudiants *100)
    liste = listeInscriptionDiplome.filter(avispoursuite ="RE")
    lpoursuiteEtude.append(len(liste))
    lpoursuiteEtude.append(len(liste)/ nbreetudiants *100)
    liste = listeInscriptionDiplome.filter(avispoursuite ="DE")
    lpoursuiteEtude.append(len(liste))
    lpoursuiteEtude.append(len(liste)/ nbreetudiants *100)



    listeInscriptionDiplome=listeInscriptionDiplome.order_by("-noteSem1")   
    etudiant =listeInscriptionDiplome[rang-1].etudiant
    inscridipl = listeInscriptionDiplome.get(etudiant=etudiant,anneeuniv=anneeuniv)

    listeinsdiplomeetu = Inscriptiondiplome.objects.filter(etudiant=etudiant)
    listeinsdiplomeetu =listeinsdiplomeetu.order_by('anneeuniv__datedebut')
    ListeInscritmat =Inscriptionmat.objects.filter(inscriptiondiplome__etudiant=etudiant,matiere__semestre ="S5" ).order_by("matiere__nom")
    
    templateData = {}
    templateData ['titre']= "Jury S5 : " +anneeuniv.anneeuniv
    templateData ['annee']=anneeuniv
    templateData ['diplome']=diplomejury
    templateData ['etudiant']=etudiant
    templateData ['listeinsdiplome']=listeinsdiplomeetu
    templateData ['listeinscritmatS5']=ListeInscritmat
    templateData ['insdiplome']=inscridipl   
    templateData ['nbreetudiants']=nbreetudiants 
    templateData ['juryS5']=True
    templateData ['poursuite']= lpoursuiteEtude
    return render (request,'jury/juryS5etudiant.html'
                  ,{'templateData': templateData} )


@login_required
@permission_required('gestiondejury.change_etudiant', raise_exception = True)
def decisionmat(request,etud,mat):
    anneeencours = Anneeuniv.objects.get(encours =True)
    insmatetu = get_object_or_404(Inscriptionmat, inscriptiondiplome__etudiant = etud,matiere = mat,inscriptiondiplome__anneeuniv = anneeencours)
    insmatetu.statut = "ADJ"
    insmatetu.decisionmat = datetime.datetime.now()
    insmatetu.save()
    insDiplome = get_object_or_404(Inscriptiondiplome, etudiant = etud,anneeuniv = anneeencours)
   
    messages.success(request, "ADJ effectué" )
    if  insDiplome.alternant:
        if anneeencours.S2:
            rang = insDiplome.rangAnnee
            base_url = reverse('jury:juryDiplome',kwargs={'rang': rang})
        else:
            rang = insDiplome.rangSem1
            base_url = reverse('jury:juryS5',kwargs={'rang': rang})
        base_url = reverse('jury:juryS5',kwargs={'rang': rang})
        query_string =urlencode({'alt':'true'})
        url = f'{base_url}?{query_string}'
        return redirect(url) 

    if anneeencours.S2:
        rang = insDiplome.rangAnnee
        return redirect('jury:juryDiplome', rang = rang)
    else:
        rang = insDiplome.rangSem1
        return redirect('jury:juryS5', rang = rang)

@login_required
@permission_required('gestiondejury.change_etudiant', raise_exception = True)
def decisionS5(request,etud):
    anneeencours = Anneeuniv.objects.get(encours =True)
    insS5etu = get_object_or_404(Inscriptiondiplome, etudiant = etud,anneeuniv = anneeencours)
    insS5etu.statutS1 = 'ADJ'
    insS5etu.datedecisionS1=datetime.datetime.now()
    insS5etu.save()
    
    messages.success(request, "ADJ S5 effectué" )
    insDiplome = get_object_or_404(Inscriptiondiplome, etudiant = etud,anneeuniv = anneeencours)

    if insDiplome.alternant:
        if anneeencours.S2:
            rang = insS5etu.rangAnnee
            base_url = reverse('jury:juryDiplome',kwargs={'rang': rang})
        else:
            rang = insS5etu.rangSem1
            base_url = reverse('jury:juryS5',kwargs={'rang': rang})
        query_string =urlencode({'alt':'true'})
        url = f'{base_url}?{query_string}'
        return redirect(url)
     
    if anneeencours.S2: 
        rang = insS5etu.rangAnnee

        return redirect('jury:juryDiplome', rang = rang)
    else:
        rang = insS5etu.rangSem1
        return redirect('jury:juryS5', rang = rang)

@login_required
@permission_required('gestiondejury.change_etudiant', raise_exception = True)
def decisionS6(request,etud):
    anneeencours = Anneeuniv.objects.get(encours =True)
    insS6etu = get_object_or_404(Inscriptiondiplome, etudiant = etud,anneeuniv = anneeencours)
    insS6etu.statutS2 = 'ADJ'
    insS6etu.datedecisionS2=datetime.datetime.now()
    insS6etu.save()
    rang = insS6etu.rangAnnee
    messages.success(request, "ADJ S6 effectué" )
    insDiplome = get_object_or_404(Inscriptiondiplome, etudiant = etud,anneeuniv = anneeencours)

    if insDiplome.alternant:
        base_url = reverse('jury:juryS6',kwargs={'rang': rang})
        query_string =urlencode({'alt':'true'})
        url = f'{base_url}?{query_string}'
        return redirect(url) 

    return redirect('jury:juryDiplome', rang = rang)

@login_required
@permission_required('gestiondejury.change_etudiant', raise_exception = True)
def decisiondiplome(request,etud):
    anneeencours = Anneeuniv.objects.get(encours =True)
    insetu = get_object_or_404(Inscriptiondiplome, etudiant = etud,anneeuniv = anneeencours)
    insetu.statutDipl = 'ADJ'
    insetu.datedecisionDipl=datetime.datetime.now()
    insetu.save()
    rang = insetu.rangAnnee
    messages.success(request, "ADJ diplome effectué" )
    insDiplome = get_object_or_404(Inscriptiondiplome, etudiant = etud,anneeuniv = anneeencours)

    if insDiplome.alternant:
        base_url = reverse('jury:juryS6',kwargs={'rang': rang})
        query_string =urlencode({'alt':'true'})
        url = f'{base_url}?{query_string}'
        return redirect(url) 

    return redirect('jury:juryDiplome', rang = rang)


@login_required
@permission_required('gestiondejury.change_etudiant', raise_exception = True)
def avisPoursuiteEtude(request,etud):
    anneeencours = Anneeuniv.objects.get(encours =True)
   

    etudiant = Etudiant.objects.get(id=etud)
    insAvisetu = get_object_or_404(Inscriptiondiplome, etudiant = etud,anneeuniv = anneeencours)

    avis = request.GET.get('avis') 
    if avis == 'Tf':
         insAvisetu.avispoursuite = "TF"
    elif  avis == 'Fa':
         insAvisetu.avispoursuite = "FA"
    elif avis == 'Re':
          insAvisetu.avispoursuite = "RE"
    elif avis == 'De' :      
         insAvisetu.avispoursuite = "DE"
    insAvisetu.save()

    rang = insAvisetu.rangSem1
    messages.success(request, "Avis de poursuite d'étude réalisé" )
    if insAvisetu.alternant:
        base_url = reverse('jury:juryS5',kwargs={'rang': rang})
        query_string =urlencode({'alt':'true'})
        url = f'{base_url}?{query_string}'
        return redirect(url)       


    return redirect('jury:juryS5', rang = rang)