from django.shortcuts import render,redirect

import pandas as pd
import math
from .forms import UploadFileForm
from django.contrib.auth.decorators import login_required,permission_required
from io import BytesIO
from etudiant.models import Inscriptiondiplome,Inscriptionmat,Etudiant
from diplome.models import Anneeuniv,Diplome
from matiere.models import Matiere
from django.contrib import messages


@login_required
@permission_required('gestiondejury.change_etudiant', raise_exception = True)
def upload_excel(request):
    data = None
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']

            # Lire le fichier Excel directement en mémoire
            file_in_memory = BytesIO(uploaded_file.read())
            df = pd.read_excel(file_in_memory)

            # Convertir les données en dictionnaire pour le template
            data = df.to_dict(orient='records')
    else:
        form = UploadFileForm()

    return render(request, 'tableurxl/upload_excel.html', {'form': form, 'data': data})


# Create your views here.
@login_required
@permission_required('gestiondejury.change_etudiant', raise_exception = True)
def upload_excelinsdiplome(request):
    data = None
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']

            # Lire le fichier Excel directement en mémoire
            file_in_memory = BytesIO(uploaded_file.read())
            df = pd.read_excel(file_in_memory)
            anneeunivencours = Anneeuniv.objects.get(encours = True)
            for row in df.itertuples(index=True):
                etudiant = Etudiant()
                etudiant.numero = row.code
                etudiant.nom = row.nom
                etudiant.prenom=row.prenom
                if row.Civil=="Monsieur":
                    etudiant.genre = Etudiant.Genre.Monsieur
                elif row.Civil=="Madame":
                    etudiant.genre = Etudiant.Genre.Madame
                etudiant.datedenaissance = row.dateNais
                etudiant.save()
                inscriptiondipl = Inscriptiondiplome()
                inscriptiondipl.etudiant=etudiant
                inscriptiondipl.Nmoinsun=row.Nmoinsun
                inscriptiondipl.anneeuniv=anneeunivencours
                inscriptiondipl.diplome=Diplome.objects.get(id=1)
                inscriptiondipl.save()


                if row.alternant =='x':
                    inscriptiondipl.alternant=True
                if row.neu == 'x':
                    inscriptiondipl.neu = True
                if row.iaL2 == 'x':
                    inscriptiondipl.iaL2 = True
                if row.redoublant == 'x':
                    inscriptiondipl.redoublant = True
                    inscription2 =Inscriptiondiplome()
                    inscription2.anneeuniv=Anneeuniv.objects.get(id = 1)
                    inscription2.etudiant=etudiant
                    inscription2.diplome=Diplome.objects.get(id=1)
                    inscription2.save()
                    diplome = Diplome.objects.get(id=1)  # ou filter selon besoin
                    listematieres = diplome.matieres.all()
                    for matiere in  listematieres:
                        insmat=Inscriptionmat()
                        insmat.matiere=matiere
                        insmat.inscriptiondiplome=inscription2
                        insmat.save()
                    inscriptiondipl.save() 
                    if row.kMKGIG30=="IP":
                        insmat=Inscriptionmat()
                        insmat.matiere=Matiere.objects.get(id=5)
                        insmat.inscriptiondiplome=inscriptiondipl
                        insmat.save()
                    if row.kMKXIM30=="IP":
                        insmat=Inscriptionmat()
                        insmat.matiere=Matiere.objects.get(id=7)
                        insmat.inscriptiondiplome=inscriptiondipl
                        insmat.save()
                    if row.kMKXIN20=="IP":
                        insmat=Inscriptionmat()
                        insmat.matiere=Matiere.objects.get(id=6)
                        insmat.inscriptiondiplome=inscriptiondipl
                        insmat.save()
                    if row.kMKXIL31=="IP":

                        insmat=Inscriptionmat()
                        insmat.matiere=Matiere.objects.get(id=11)
                        insmat.inscriptiondiplome=inscriptiondipl
                        insmat.save()                                      
                    if row.kMKGIG20=="IP":
                        insmat=Inscriptionmat()
                        insmat.matiere=Matiere.objects.get(id=4)
                        insmat.inscriptiondiplome=inscriptiondipl
                        insmat.save() 
                    if row.kMKXIF20=="IP":
                        insmat=Inscriptionmat()
                        insmat.matiere=Matiere.objects.get(id=8)
                        insmat.inscriptiondiplome=inscriptiondipl
                        insmat.save()                           
                    if row.kMKGIG10=="IP":
                        insmat=Inscriptionmat()
                        insmat.matiere=Matiere.objects.get(id=2)
                        insmat.inscriptiondiplome=inscriptiondipl
                        insmat.save()
                    if row.kMKXIS20=="IP":
                        insmat=Inscriptionmat()
                        insmat.matiere=Matiere.objects.get(id=3)
                        insmat.inscriptiondiplome=inscriptiondipl
                        insmat.save()
                    if row.kMKXIX20=="IP":
                        insmat=Inscriptionmat()
                        insmat.matiere=Matiere.objects.get(id=1)
                        insmat.inscriptiondiplome=inscriptiondipl
                        insmat.save()         
                    if row.kMKGIG40=="IP":
                        insmat=Inscriptionmat()
                        insmat.matiere=Matiere.objects.get(id=9)
                        insmat.inscriptiondiplome=inscriptiondipl
                        insmat.save()
                    if row.kMKXIT10=="IP":
                        insmat=Inscriptionmat()
                        insmat.matiere=Matiere.objects.get(id=10)
                        insmat.inscriptiondiplome=inscriptiondipl
                        insmat.save()                                        
                                                       
                else:

                    inscriptiondipl.save()
                    diplome = Diplome.objects.get(id=1)  # ou filter selon besoin
                    listematieres = diplome.matieres.exclude(id__in=[9,10])
                    for matiere in  listematieres:
                

                        insmat=Inscriptionmat()
                        insmat.matiere=matiere
                        insmat.inscriptiondiplome=inscriptiondipl
                        insmat.save()
                    if row.kMKGIG40 =="IP":
                        insmat=Inscriptionmat()
                        insmat.matiere = Matiere.objects.get(id=9)
                        insmat.inscriptiondiplome=inscriptiondipl
                        insmat.save()
                    else:
                        insmat=Inscriptionmat()
                        insmat.matiere = Matiere.objects.get(id=10)
                        insmat.inscriptiondiplome=inscriptiondipl
                        insmat.save()
                




                
            return redirect('etudiant:index')


            # Convertir les données en dictionnaire pour le template
            
    else:
        form = UploadFileForm()

    return render(request, 'tableurxl/upload_excel.html', {'form': form, 'data': data})

@login_required
@permission_required('gestiondejury.change_etudiant', raise_exception = True)
def  upload_excelnotesmat(request,codemat):
    data = None
    anneeunivencours = Anneeuniv.objects.get(encours = True)
    matiere = Matiere.objects.get(codeapogee=codemat)



    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            file_in_memory = BytesIO(uploaded_file.read())
            df = pd.read_excel(file_in_memory)
            ligne = 12
            nonInscritsdiplome=[]
            nonInscritsmatiere=[]
            message = "Listes\n"
            while (pd.notna(df.iloc[ligne, 0] )):

                inscriptiondipl = Inscriptiondiplome.objects.filter(etudiant__numero=df.iloc[ligne, 0],anneeuniv=anneeunivencours).first()
                if inscriptiondipl is None:
                    nonInscritsdiplome.append([df.iloc[ligne, 0],df.iloc[ligne, 1],df.iloc[ligne, 2]])
                    message +=str(df.iloc[ligne, 0])+" : "+ str(df.iloc[ligne, 1])+'\n'
                else:
                    inscriptionmat=Inscriptionmat.objects.filter(inscriptiondiplome = inscriptiondipl,matiere = matiere).first()
                    if inscriptionmat is None:
                        nonInscritsmatiere.append([df.iloc[ligne, 0],df.iloc[ligne, 1],df.iloc[ligne, 2]])
                        message += str(df.iloc[ligne, 0])+" : "+ str(df.iloc[ligne, 1])+'\n'
                    else:
                        inscriptionmat.notecc1=df.iloc[ligne, 10]
                        inscriptionmat.notecc2=df.iloc[ligne, 11]
                        inscriptionmat.notecc3=df.iloc[ligne, 12]
  
                        inscriptionmat.save()
                ligne+=1
            message += "Attention : "+ str(len(nonInscritsdiplome)) +" non inscrits diplome. "
            message+= str(len( nonInscritsmatiere))+" non inscrits matière"
            messages.warning(request, message )
            return redirect('matiere:notes',code = codemat)
    else:
    
        form = UploadFileForm()

    return render(request, 'tableurxl/upload_excel.html', {'form': form, 'data': data})

@login_required
@permission_required('gestiondejury.change_etudiant', raise_exception = True)
def  upload_excelnotesmat2(request,codemat):
    data = None
    anneeunivencours = Anneeuniv.objects.get(encours = True)
    matiere = Matiere.objects.get(codeapogee=codemat)



    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            file_in_memory = BytesIO(uploaded_file.read())
            df = pd.read_excel(file_in_memory)
            
            nonInscritsdiplome=[]
            nonInscritsmatiere=[]
            message = "Listes\n"
            for index, row in df.iterrows():

                inscriptiondipl = Inscriptiondiplome.objects.filter(etudiant__numero=row['id'],anneeuniv=anneeunivencours).first()
                if inscriptiondipl is None:
                    nonInscritsdiplome.append([row['nom']])
                    message +=str(row['id'])+" : "+ str(row['nom'])+'\n'
                else:
                    inscriptionmat=Inscriptionmat.objects.filter(inscriptiondiplome = inscriptiondipl,matiere = matiere).first()
                    if inscriptionmat is None:
                        nonInscritsmatiere.append([row['nom']])
                        message += str([row['nom']])+" : "+ str([row['prenom']])+'\n'
                    else:
                        
                        inscriptionmat.notecc1=float([row['CC1']][0])
                        inscriptionmat.notecc2=float([row['CC2']][0])
                        inscriptionmat.notecc3=float([row['CC3']][0])
  
                        inscriptionmat.save()
               
            message += "Attention : "+ str(len(nonInscritsdiplome)) +" non inscrits diplome. "
            message+= str(len( nonInscritsmatiere))+" non inscrits matière"
            messages.warning(request, message )
            return redirect('matiere:notes',code = codemat)
    else:
    
        form = UploadFileForm()

    return render(request, 'tableurxl/upload_excel.html', {'form': form, 'data': data})


            



