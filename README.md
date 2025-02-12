# Kragaht 📝🔥

Kragaht is a **Django-based web application** for creating, managing, and browsing posts with rich text formatting, a like system, and sorting functionality. It integrates **CKEditor** for content creation.

## **🚀 Features**
- 📝 **Rich Text Editing** using CKEditor.
- 📸 **Image Upload Support** for posts.
- 👍 **Like System** (Users can like posts with AJAX).
- 🔍 **Search & Sorting** (Sort posts by Name, Likes, or Creation Date).
- 📂 **Categories** (View posts by category).
- ❤️ **Liked Posts Section** (View posts you liked).
- 🔑 **Authentication** (Register, Login, Logout).
- 🎨 **Fully Responsive Dark-Themed UI**.



## **📦 Installation**
### **1. Clone the Repository**
```bash
git clone https://github.com/olzavadovskyi/Kragaht.git
cd Kragaht
```

### **2. Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate

# On Windows use: venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Configure the Database**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **5. Create a Superuser**
```bash
python manage.py createsuperuser
```

### **6. Run the Server**
```bash
python manage.py runserver
```

Now, open **http://127.0.0.1:8000/** in your browser!

---


## **🛠️ Tech Stack**
- **Backend:** Django, Python
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite (default, can be changed to PostgreSQL)
- **Editor:** CKEditor for Rich Text Editing

---

## **📂 Project Structure**
```
Kragaht/
│── posts/               # Main Django app
│   ├── migrations/      # Database migrations
│   ├── static/posts/    # CSS, JavaScript, images
│   ├── templates/posts/ # HTML templates
│   ├── views.py         # App views (functions)
│   ├── models.py        # Database models
│   ├── forms.py         # Django forms
│   ├── urls.py          # App URL routing
│── media/               # Uploaded images (user-generated content)
│── static/              # Static files
│── templates/           # Base templates
│── db.sqlite3           # SQLite database (can be changed)
│── manage.py            # Django management script
│── requirements.txt     # Dependencies
│── README.md            # This file
```

---

## **🛠 Configuration**
### **Static & Media Files (for Production)**
In `settings.py`, set:
```python
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_ROOT = BASE_DIR / "media"
```
Then, collect static files:
```bash
python manage.py collectstatic
```

---

## **📧 Contact**
- GitHub: Oleksandr(https://github.com/olzavadovskyi)
- Email: ol.zavadovskyi@gmail.com

