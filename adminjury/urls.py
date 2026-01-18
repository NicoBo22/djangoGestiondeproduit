from django.urls import path,re_path
from . import views

app_name="adminjury"

urlpatterns = [
    path('creationnotes/',views.inscription, name='inscription'),
    path('nbrinscritmatiere/',views.nbrinscritmatiere,name = 'nbrinscritmatiere'),
    path('reset/',views.reset,name = 'reset'),
    re_path(r"^calculmoyennemat/(?P<idmat>[0-9])/(?P<alt>(alt|nonalt|tous))/$",views.calculMoyenneMat, name='calculmoyennemat'),
    re_path(r"^calculmoyennesem/(?P<sem>(S5|S6))/(?P<alt>(alt|nonalt|tous))/$",views.calculMoyenneSemestre, name='calculmoyennesemestre'),
    re_path(r"^calculsemestre/(?P<sem>(S5|S6))/(?P<alt>(alt|nonalt|tous))/$",views.calculSemestre, name='calculsemestre'),
    re_path(r"^calculannee/(?P<codeDipl>[A-Za-z0-9]{6})/(?P<alt>(alt|nonalt|tous))/$",views.calculAnnee, name='calculannee'),
    
]