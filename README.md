# 📖 ReadManga – Online Manga Reading Platform

## 🚀 Project Overview

**ReadManga** is a Django-based web application that allows users to browse and read manga online.
The platform integrates a web scraping module to fetch manga metadata and display chapters dynamically through a clean web interface.

This project demonstrates full-stack web development using Django along with backend scraping logic.

---

## 🛠 Tech Stack

* **Backend:** Python, Django
* **Frontend:** HTML, CSS
* **Database:** SQLite3
* **Web Scraping:** Requests, BeautifulSoup (inside scraper module)
* **Version Control:** Git & GitHub

---

## 📂 Project Structure

```
Read_manga/
│
├── manage.py
├── db.sqlite3
├── manga_genres.json
│
├── home/              # Main Django app (views, urls, models)
├── scraper/           # Web scraping logic
├── templates/         # HTML templates
├── static/            # CSS, JS, Images
└── anime_stream/      # Additional module
```

---

## ✨ Features

* 📚 Browse manga titles
* 📂 Categorization by genres
* 🔎 Dynamic content loading via scraper module
* 🗂 SQLite database integration
* 🖥 Clean Django template-based UI
* ⚙ Modular app structure (home + scraper)

---

## ⚙ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/sarthakPatil96K/Read_manga.git
cd Read_manga
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

*(If requirements.txt is not available, install manually:)*

```bash
pip install django requests beautifulsoup4
```

### 4️⃣ Run Migrations

```bash
python manage.py migrate
```

### 5️⃣ Start the Server

```bash
python manage.py runserver
```

Now open:

```
http://127.0.0.1:8000/
```

---

## 🧠 How It Works

1. The **scraper module** fetches manga details from external sources.
2. Extracted metadata (title, genre, chapters, images) is processed.
3. Django views render the content using templates.
4. SQLite database stores structured information.
5. Users can browse and read manga via web interface.

---

## 📌 Learning Outcomes

This project demonstrates:

* Django project structuring
* App modularization
* Web scraping integration
* Database handling with ORM
* Template rendering
* Full-stack web development fundamentals

---

## 🔮 Future Improvements

* 🔐 User authentication (Login/Register)
* ❤️ Bookmark & reading history
* ⭐ Rating & review system
* ⚡ Pagination & performance optimization
* 🧠 Recommendation system (ML-based)
* 🚀 Deployment using Docker/Gunicorn/Nginx
* 🌐 REST API using Django REST Framework

---

## ⚠ Disclaimer

This project is built for educational purposes.
Ensure compliance with copyright policies when scraping or hosting content.

---

## 👨‍💻 Author

**Sarthak Patil**
GitHub: [https://github.com/sarthakPatil96K](https://github.com/sarthakPatil96K)

---

## ⭐ If You Like This Project

Give it a ⭐ on GitHub!

---

---

 
