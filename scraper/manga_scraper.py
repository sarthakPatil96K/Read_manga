import os
import sys
import django
import requests
from bs4 import BeautifulSoup

# ✅ Set the root directory of your project
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

# ✅ Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anime_stream.settings')

# ✅ Initialize Django
django.setup()

from home.models import Manga

# ✅ Genre list
GENRES = {
    'Action': 1,
    'Adventure': 2,
    'Fantasy': 10,
    'Horror': 14,
    'Comedy': 4,
    'Romance': 22,
    'Mystery': 7,
    'Sci-Fi': 24,
    'Slice of Life': 36,
    'Supernatural': 37,
    'Drama': 8,
    'Sports': 30
}

BASE_URL = 'https://myanimelist.net/manga/genre/{}/{}'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def fetch_manga_data():
    for genre, genre_id in GENRES.items():
        url = BASE_URL.format(genre_id, genre)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # ✅ Targeting the correct div class
        manga_list = soup.find_all('div', class_='seasonal-anime js-seasonal-anime')

        for manga in manga_list:
            # Title
            title_tag = manga.find('h2', class_='h2_manga_title')
            title = title_tag.find('a').text if title_tag else None

            if not title or Manga.objects.filter(title__iexact=title).exists():
                continue  

            # Image
            image_tag = manga.find('img')
            image_url = image_tag['data-src'] if image_tag and 'data-src' in image_tag.attrs else ''

            # Description
            description_tag = manga.find('p', class_='preline')
            description = description_tag.text.strip() if description_tag else ''

            # Airing status
            status_tag = manga.find('span', class_='item finished')
            airing_status = "Ongoing" if not status_tag else "Completed"

            # Chapter count
            chapter_tag = manga.find('span', class_='js-chapter')
            chapter_text = chapter_tag.text if chapter_tag else '0'

            # Handle "?" by replacing it with "0"
            chapter_text = chapter_text.replace('?', '0')

            # Convert to integer
            chapter_count = int(chapter_text)


            # Rating
            rating_tag = manga.find('div', class_='scormem-item score')
            rating = float(rating_tag.text) if rating_tag and rating_tag.text.strip() != '?' else 0.0

            # ✅ Save to Database
            Manga.objects.update_or_create(
                title=title,
                defaults={
                    'image_url': image_url,
                    'description': description,
                    'genre': genre,
                    'airing_status': airing_status,
                    'chapter_count': chapter_count,
                    'rating': rating
                }
            )

if __name__ == "__main__":
    fetch_manga_data()
