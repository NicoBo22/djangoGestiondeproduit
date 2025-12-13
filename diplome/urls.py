from django.urls import path
from . import views
app_name = "diplome"

urlpatterns = [
    path('annee/', views.indexannee, name='indexannee'),
    path('S2/', views.S2, name="valideS2"),
    path('creationannee/', views.creationannee, name='creationannee'),


]