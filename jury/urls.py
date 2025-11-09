from django.urls import path
from . import views

app_name="jury"


urlpatterns = [
    path('',views.jury, name='indexjury'),
    path('S5/<int:rang>/', views.juryS5,name='juryS5'),
    path('decisionmat/<int:etud>/<int:mat>/', views.decisionmat, name='decisionmat' ),
    path('decisionS5/<int:etud>/', views.decisionS5, name='decisionS5' ),
    path('avis/<int:etud>/', views.avisPoursuiteEtude, name='avispoursuite' ),

]