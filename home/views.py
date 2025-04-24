from django.shortcuts import get_object_or_404, render,HttpResponse,redirect
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
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

# Custom Signup Form to include email, first name, and last name
class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

def signup_user(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")  # Redirect to homepage after successful signup
        else:
            # Form is not valid, will render with errors
            return render(request, 'signup.html', {'form': form})
    else:
        form = CustomSignupForm()
    return render(request, 'signup.html', {'form': form})


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

 
 
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from .models import Manga
from .mangadex_api import get_manga_id, get_chapter_id, get_chapter_images, get_adjacent_chapters  # type: ignore


def read_manga(request, genre, manga_title, chapter_number):
    # Convert slugified title back to original format
    normalized_title = manga_title.replace("-", " ").replace(":", "")

    # Get manga object
    manga = get_object_or_404(Manga, title__iexact=normalized_title)

    manga_id = get_manga_id(manga.title)
    print(f"Fetched MangaDex ID: {manga_id}")  # Debugging

    chapter_id = get_chapter_id(manga_id, chapter_number)

    # Fetch cover image from database
    cover_image_url = manga.image_url  # ✅ FIXED: Use 'image_url' from the model

    if not chapter_id:
        chapter_exists = False
        all_pages = []
    else:
        chapter_exists = True
        all_pages = get_chapter_images(chapter_id)

    prev_chapter, next_chapter = get_adjacent_chapters(manga_id, chapter_number)

    # ✅ Fix: Ensure values are integers or None
    prev_chapter = int(prev_chapter) if prev_chapter is not None else None
    next_chapter = int(next_chapter) if next_chapter is not None else None

    print(f"Current Chapter: {chapter_number}, Previous: {prev_chapter}, Next: {next_chapter}")

    return render(request, "read.html", {
        "manga": manga,
        "genre": genre,
        "chapter_number": int(chapter_number),
        "chapter_exists": chapter_exists,
        "all_pages": all_pages,
        "prev_chapter": prev_chapter,  # ✅ FIXED: Now passes the actual chapter number
        "next_chapter": next_chapter,  # ✅ FIXED: Now passes the actual chapter number
        "cover_image_url": cover_image_url,
    })






import random
from django.shortcuts import render
from .models import Manga

def popular_manga(request):
    if request.user.is_anonymous:
        return redirect("/login")
    all_manga = list(Manga.objects.all())
    random_manga = random.sample(all_manga, min(len(all_manga), 6))  # Get up to 6 random manga
    
    return render(request, "popular.html", {"random_manga": random_manga})



