from django.urls import path
from . import views
app_name = "docpdf"
urlpatterns = [
    path('avispoursuiteetude/<int:id>/', views.avispoursuite, name='avispoursuite'),


]
