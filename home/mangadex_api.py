import requests

BASE_URL = "https://api.mangadex.org"

def get_manga_id(title):
    """Fetch Manga ID from MangaDex based on title."""
    url = f"{BASE_URL}/manga"
    params = {"title": title, "limit": 1}

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200 and data.get("result") == "ok":
        try:
            return data["data"][0]["id"]  # ✅ Correct UUID format
        except (KeyError, IndexError):
            print(f"❌ Manga ID not found for '{title}'")
            return None
    print(f"❌ API Error {response.status_code}: {data}")
    return None

def get_chapter_id(manga_id, chapter_number):
    """Fetch the chapter ID for a given manga and chapter number."""
    url = f"{BASE_URL}/chapter"
    params = {
        "manga": manga_id,
        "translatedLanguage[]": "en",
        "order[chapter]": "asc",
        "limit": 100
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"❌ API Error {response.status_code}: {response.text}")
        return None

    data = response.json()
    if not data.get("data"):
        print(f"⚠️ No chapters found for Manga ID: {manga_id}")
        return None

    for entry in data["data"]:
        if entry["attributes"].get("chapter") == str(chapter_number):
            return entry["id"]

    print(f"⚠️ Chapter {chapter_number} not found for Manga ID: {manga_id}")
    return None

def get_chapter_images(chapter_id):
    """Fetch all page images for a chapter."""
    url = f"{BASE_URL}/at-home/server/{chapter_id}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"❌ API Error {response.status_code}: {response.text}")
        return []

    data = response.json()
    if "baseUrl" not in data or "chapter" not in data:
        print("❌ Error: Missing expected keys in API response.")
        return []

    base_url = data["baseUrl"]
    hash_val = data["chapter"]["hash"]
    
    # ✅ Fetch high-quality images first
    images = [f"{base_url}/data/{hash_val}/{page}" for page in data["chapter"].get("data", [])]
    
    # ✅ Fallback to low-quality if needed
    if not images:
        images = [f"{base_url}/data-saver/{hash_val}/{page}" for page in data["chapter"].get("data-saver", [])]

    if not images:
        print("❌ Error: No images found for this chapter.")

    return images

def get_adjacent_chapters(manga_id, current_chapter):
    """Find the previous and next available chapter numbers."""
    url = f"{BASE_URL}/chapter"
    params = {
        "manga": manga_id,
        "translatedLanguage[]": "en",
        "order[chapter]": "asc",
        "limit": 100
    }

    chapters = []
    offset = 0

    while True:
        params["offset"] = offset
        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return None, None

        data = response.json()
        if not data.get("data"):
            break  # No more chapters

        for entry in data["data"]:
            chapter_str = entry["attributes"].get("chapter")
            if chapter_str and chapter_str.replace('.', '', 1).isdigit():
                chapters.append(float(chapter_str))  

        offset += len(data["data"])
        if offset >= data.get("total", 0):
            break  

    chapters = sorted(set(chapters))
    if not chapters:
        return None, None  

    current_chapter = float(current_chapter)
    prev_chapter = None
    next_chapter = None

    for i, ch in enumerate(chapters):
        if ch == current_chapter:
            prev_chapter = int(chapters[i - 1]) if i > 0 else None
            next_chapter = int(chapters[i + 1]) if i < len(chapters) - 1 else None
            break

    print(f"📌 Current: {current_chapter}, Prev: {prev_chapter}, Next: {next_chapter}")
    return prev_chapter, next_chapter  # ✅ Always return as integers or None
