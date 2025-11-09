from django.urls import path,re_path
from . import views
app_name = "etudiant"
urlpatterns = [
    path('', views.indexetudiant, name='index'),
    re_path(r"^(?P<alt>(alt|nonalt|neu))/$",views.listeetudiant, name='liste'),
    path('<int:id>/', views.vueetudiant, name='vue'),
    path('add/', views.addetudiant, name ='addetudiant'),
    path('inscriptiondiplome/', views.addinscriptiondipl, name ='addinscriptiondipl'),
    path('inscriptionmat/<int:id>/', views.addinscriptionmat, name ='addinscriptionmat')

] 