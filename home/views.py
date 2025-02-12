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
    from django.shortcuts import render
import requests

def action(request):
    # Fetch manga data for action category from the API (or you can filter data here based on category)
    response = requests.get("https://api.jikan.moe/v4/manga")
    all_manga_data = response.json().get('data', [])

    # Prepare the manga info to pass to the template
    manga_info_list = []
    for manga in all_manga_data:
        manga_info = {
            'title': manga.get('title', 'N/A'),
            'status': manga.get('status', 'N/A'),
            'synopsis': manga.get('synopsis', 'N/A'),
            'rating': manga.get('score', 'N/A'),
            'url': manga.get('images', {}).get('webp', {}).get('image_url', 'N/A')  # Use webp image URL
        }
        manga_info_list.append(manga_info)

    # Pass the manga data to the action.html template
    return render(request, "action.html", {'manga_info_list': manga_info_list})

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

 