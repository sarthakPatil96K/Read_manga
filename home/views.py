from django.shortcuts import render,HttpResponse,redirect
from datetime import datetime 
from home.models import contact 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout,login

#admin: patilsarthak password sarthak
#user anoj password SARTHAK@12
# Create your views here.
# def index(request):
#     if request.user.is_anonymous:
#         return redirect("/login")
#     return render(request,"index.html")
    #return HttpResponse("Hello sarthak here")
def popular(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request,"popular.html")
def ongoing(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request,"ongoing.html")
def action(request):
    if request.user.is_anonymous:
        return redirect("/login")
    from django.shortcuts import render
import requests

def action(request):
    if request.user.is_anonymous:
        return redirect("/login")
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
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request,"about.html")

def Contact(request):
    if request.user.is_anonymous:
        return redirect("/login")
    if request.method == "POST":
        name = request.POST.get('name')
        email =  request.POST.get('email')
        manga_req = request.POST.get('manga_req')
        Contact = contact(name = name,email = email,manga_req = manga_req,date =datetime.today())
        Contact.save()
    return render(request,"Contact.html")

def read(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request,"read.html")

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return redirect("/")
        else:
            # No backend authenticated the credentials
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")

def logout_user(request):
    logout(request)
    return redirect("/login")

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login

def signup_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})

        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already taken'})

        # Create the user
        user = User.objects.create_user(username=username, password=password)
        user.save()

        # Auto-login the user after signup
        login(request, user)
        return redirect("/")
    
    return render(request, 'signup.html')

from django.shortcuts import render
from .models import Manga

def genre_page(request, genre_name):
    if request.user.is_anonymous:
        return redirect("/login")
    mangas = Manga.objects.filter(genre__icontains=genre_name)
    return render(request, 'genre.html', {'mangas': mangas, 'genre_name': genre_name})

from django.shortcuts import render
from .models import Manga

def genre_page(request, genre_name):
    if request.user.is_anonymous:
        return redirect("/login")
    # Filter manga based on the genre
    manga_list = Manga.objects.filter(genre__icontains=genre_name)

    context = {
        'manga_info_list': manga_list,
        'genre_name': genre_name.capitalize()
    }
    
    return render(request, 'genre.html', context)
from django.shortcuts import render
from .models import Manga

def genre_manga_view(request, genre_name):
    if request.user.is_anonymous:
        return redirect("/login")
    mangas = Manga.objects.filter(genre__icontains=genre_name)
    return render(request, 'genre.html', {'manga_info_list': mangas})

from django.shortcuts import render, redirect
from django.templatetags.static import static

def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    
    # Use the {% static %} tag to reference images from the static folder
    genres = {
        'Action': static('images/action_img.jpg'),
        'Romance': static('images/romance_img.avif'),
        'Adventure': static('images/adventure_img.avif'),
        'Fantasy': static('images/fantacy_img.avif'),
        'Horror': static('images/horror_img.avif'),
        'Comedy': static('images/comedy_img.avif'),
        'Mystery': static('images/mystery_img.png'),
        'Sci-Fi': static('images/scifi_img.webp'),
        'Drama': static('images/drama_img.jpg')
    }
    
    return render(request, "index.html", {'genres': genres})


from django.shortcuts import render
from .models import Manga

def search_manga(request):
    query = request.GET.get('q')
    if query:
        mangas = Manga.objects.filter(title__icontains=query)
    else:
        mangas = Manga.objects.all()

    # Passing query and mangas to the template
    return render(request, 'search_result.html', {'mangas': mangas, 'query': query})

import os
from django.shortcuts import render, redirect
from django.templatetags.static import static
from .models import Manga

import os
from django.shortcuts import render, redirect
from .models import Manga

def read_manga(request, genre, manga_title, chapter_number):
    if request.user.is_anonymous:
        return redirect("/login")
    
    # Convert genre to match database format (capitalize first letter)
    genre = genre.capitalize()

    # Convert URL slug back to a proper title format (replace hyphens with spaces)
    formatted_title = manga_title.replace("-", " ")

    # Fetch the first available manga entry (avoid MultipleObjectsReturned error)
    manga = Manga.objects.filter(title__iexact=formatted_title, genre__iexact=genre).first()

    # Handle case where no manga is found
    if not manga:
        return render(request, "404.html", {"message": "Manga not found"}, status=404)

    # Path where manga chapters are stored
    manga_path = f"static/{formatted_title}/"
    chapter_path = os.path.join(manga_path, f"chapter-{chapter_number}")

    # Check if chapter exists
    chapter_exists = os.path.exists(chapter_path)

    if chapter_exists:
        # List all available pages for the chapter (if any)
        all_pages = sorted(
            [page for page in os.listdir(chapter_path) if page.endswith('.jpg') or page.endswith('.png')],
            key=lambda x: int(x.split('-')[1].split('.')[0])  # Sort by the page number
        )
    else:
        all_pages = []  # No pages found for the chapter

    # Prepare page numbers for display
    page_numbers = [page.split('-')[1].split('.')[0] for page in all_pages]

    context = {
        "manga": manga,
        "chapter_number": chapter_number,
        "chapter_exists": chapter_exists,
        "all_pages": all_pages,
        "page_numbers": page_numbers,  # Pass page numbers to template
        "cover_image_url": manga.image_url  # Pass the manga cover image URL to the template
    }

    return render(request, "read.html", context)



import random
from django.shortcuts import render
from .models import Manga

def popular_manga(request):
    if request.user.is_anonymous:
        return redirect("/login")
    all_manga = list(Manga.objects.all())
    random_manga = random.sample(all_manga, min(len(all_manga), 6))  # Get up to 6 random manga
    
    return render(request, "popular.html", {"random_manga": random_manga})
