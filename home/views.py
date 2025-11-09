from django.shortcuts import render

# Create your views here.
def index(request):
    
    templateData = {}
    templateData ['titre']= "Accueil"
    return render(request, 'home/index.html',{'templateData': templateData})