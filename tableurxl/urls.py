from django.urls import path
from . import views

app_name = "tableurxl"

urlpatterns = [
    path('upload/', views.upload_excel, name='upload_excel'),
]
