 
from django.shortcuts import render,HttpResponse
from datetime import datetime 
from home.models import contact 
# Create your views here.
def index(request):
    return render(request,"index.html")
    #return HttpResponse("Hello sarthak here")
def popular(request):
    return render(request,"popular.html")
def ongoing(request):
    return render(request,"ongoing.html")
def action(request):
    return render(request,"action.html")
def about(request):
    return render(request,"about.html")
def Contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email =  request.POST.get('email')
        manga_req = request.POST.get('manga_req')
        Contact = contact(name = name,email = email,manga_req = manga_req,date =datetime.today())
        Contact.save()
    return render(request,"Contact.html")

def read(request):
    return render(request,"read.html")