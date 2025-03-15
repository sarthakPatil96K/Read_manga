from .models import Manga

def genres_list(request):
    genres = ['Action', 'Adventure', 'Fantasy', 'Horror', 'Comedy', 'Romance', 'Mystery', 'Sci-Fi', 'Slice of Life', 'Supernatural', 'Drama', 'Sports']
    return {'genres': genres}
