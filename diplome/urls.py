from django.urls import path
from . import views
app_name = "diplome"

urlpatterns = [
    path('annee/', views.indexannee, name='indexannee'),


]