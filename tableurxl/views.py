from django.shortcuts import render
import pandas as pd
from .forms import UploadFileForm
from django.contrib.auth.decorators import login_required,permission_required
from io import BytesIO



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
