from django.test import TestCase

# Create your tests here.
import requests
import json
from bs4 import BeautifulSoup
import time

# Load the JSON data (example MAL genre API response)
json_data = {
  "data": [
    {"mal_id": 1, "name": "Action", "url": "https://myanimelist.net/manga/genre/1/Action", "count": 10035},
    {"mal_id": 2, "name": "Adventure", "url": "https://myanimelist.net/manga/genre/2/Adventure", "count": 4381},
    {"mal_id": 5, "name": "Avant Garde", "url": "https://myanimelist.net/manga/genre/5/Avant_Garde", "count": 85}
  ]
}

# Function to fetch and scrape each genre page
def scrape_genre_pages(data):
    results = {}

    for genre in data['data']:
        genre_namee = genre['name']
        genre_url = genre['url']
        print(f"Fetching {genre_namee} from {genre_url}...")

        try:
            # Send GET request with a user-agent header
            response = requests.get(genre_url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract manga titles and links from the genre page
            manga_list = []
            
            # Identify the correct CSS selector based on MAL's HTML structure
            for manga in soup.select('.manga_h3 a'):  # <-- Update this selector if necessary
                title = manga.text.strip()
                link = manga['href']
                manga_list.append({'title': title, 'link': link})

            results[genre_namee] = manga_list
            time.sleep(2)  # Avoid getting blocked by MAL

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {genre_namee}: {e}")
            results[genre_namee] = []  # Store an empty list if there's an error
    
    return results

# Scrape the data
scraped_data = scrape_genre_pages(json_data)
print(scraped_data)
# Save to a JSON file
with open("manga_genres.json", "w", encoding="utf-8") as f:
    json.dump(scraped_data, f, indent=4)

print("Scraping completed. Data saved to manga_genres.json.")
