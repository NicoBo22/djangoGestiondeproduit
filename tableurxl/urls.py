from django.urls import path
from . import views

app_name = "tableurxl"

urlpatterns = [
    path('upload/', views.upload_excel, name='upload_excel'),
    path('uploadindipl/', views.upload_excelinsdiplome, name='upload_excelinsdiplome'),
]
