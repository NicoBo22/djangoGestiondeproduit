from django.urls import path
from . import views

app_name = "tableurxl"

urlpatterns = [
    path('upload/', views.upload_excel, name='upload_excel'),
    path('etudiants/', views.upload_excelinsdiplome, name='upload_excelinsdiplome'),
    path('entreenotes/<str:codemat>', views.upload_excelnotesmat, name='uploadexcelnotesmat'),
    path('entreenotes2/<str:codemat>', views.upload_excelnotesmat2, name='uploadexcelnotesmat2'),
]
