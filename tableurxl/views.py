from django.shortcuts import render,redirect

import pandas as pd
from .forms import UploadFileForm
from django.contrib.auth.decorators import login_required,permission_required
from io import BytesIO
from etudiant.models import Inscriptiondiplome,Inscriptionmat
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

            for row in df.itertuples(index=True):

                inscriptiondipl = Inscriptiondiplome.objects.filter(etudiant__numero=row.Num).first()
                if inscriptiondipl is None:
                    print(row.nom, " : ",row.prenom)
                else:

                    if row.alternant =='x':
                        inscriptiondipl.alternant=True
                    if row.neu == 'x':
                        inscriptiondipl.neu = True
                    if row.iaL2 == 'x':
                        inscriptiondipl.iaL2 = True
                    if row.redoublant == 'x':
                        inscriptiondipl.redoublant = True
                    inscriptiondipl.save()
                
                
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
            ligne = 10
            nonInscritsdiplome=[]
            nonInscritsmatiere=[]
            while (pd.notna(df.iloc[ligne, 0] )):

                inscriptiondipl = Inscriptiondiplome.objects.filter(etudiant__numero=df.iloc[ligne, 0],anneeuniv=anneeunivencours).first()
                if inscriptiondipl is None:
                    nonInscritsdiplome.append([df.iloc[ligne, 0],df.iloc[ligne, 1],df.iloc[ligne, 2]])
                else:
                    inscriptionmat=Inscriptionmat.objects.filter(inscriptiondiplome = inscriptiondipl,matiere = matiere).first()
                    if inscriptionmat is None:
                        nonInscritsmatiere.append([df.iloc[ligne, 0],df.iloc[ligne, 1],df.iloc[ligne, 2]])
                    else:
                        inscriptionmat.notecc1=df.iloc[ligne, 11]
                        inscriptionmat.notecc2=df.iloc[ligne, 12]
                        inscriptionmat.notecc3=df.iloc[ligne, 13]
                        inscriptionmat.save()
                ligne+=1
            message = "Attention : "+ str(len(nonInscritsdiplome)) +" non inscrits diplome. "
            message+= str(len( nonInscritsmatiere))+" non inscrits matière"
            messages.warning(request, message )
            return redirect('matiere:notes',code = codemat)
    else:
    
        form = UploadFileForm()

    return render(request, 'tableurxl/upload_excel.html', {'form': form, 'data': data})



            



