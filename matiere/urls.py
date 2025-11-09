from django.urls import path,re_path
from . import views
app_name = "matiere"
urlpatterns = [
    path('', views.indexmatiere, name='index'),
    path('notes/<str:code>', views.notes,name='notes'),
    path('editnotes/<str:code>/<int:etudiant>', views.editnotes,name='editnotes'),
    re_path(r'^editnotesmatiere/(?P<code>KM[A-Z]{4}\d{2})/(?P<alt>(alt|nonalt))/(?P<etudiantalpha>\d+)$',views.editnotesmatiere,name = 'editnotesmatiere')

]