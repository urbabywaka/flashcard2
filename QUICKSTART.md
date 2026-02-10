# 🚀 Quick Start Guide

## 5-Minute Setup

### 1. Install Django (if not already installed)
```bash
pip install django
```

### 2. Navigate to Project Directory
```bash
cd flashcard_app
```

### 3. Setup Database
```bash
python manage.py makemigrations accounts
python manage.py makemigrations flashcards
python manage.py migrate
```

### 4. Create Admin Account
```bash
python manage.py createsuperuser
```
Enter username, email (optional), and password when prompted.

### 5. Start the Server
```bash
python manage.py runserver
```

### 6. Open Your Browser
Go to: **http://127.0.0.1:8000**

---

## First Steps

1. **Sign Up**: Create a student account at http://127.0.0.1:8000/accounts/signup/
2. **Create Your First Flashcard**:
   - Click "Create Card" button
   - Add a topic (e.g., "Mathematics")
   - Enter a question (e.g., "What is 2+2?")
   - Enter an answer (e.g., "4")
   - Click "Create Flashcard"

3. **Start Studying**:
   - Click "Study Mode" in the navigation
   - Click on a card to flip it
   - Mark as "I Know This" or "Review Later"

4. **Track Your Progress**:
   - View dashboard for overview
   - Check "Statistics" for detailed analytics

---

## Common Commands

### Create new migrations after model changes
```bash
python manage.py makemigrations
```

### Apply migrations to database
```bash
python manage.py migrate
```

### Create admin/superuser account
```bash
python manage.py createsuperuser
```

### Run development server
```bash
python manage.py runserver
```

### Run on different port
```bash
python manage.py runserver 8080
```

### Access from other devices on network
```bash
python manage.py runserver 0.0.0.0:8000
```

### Collect static files (for production)
```bash
python manage.py collectstatic
```

### Open Django shell
```bash
python manage.py shell
```

---

## Troubleshooting

### "Django not found" error
```bash
pip install django
```

### Database errors
```bash
# Delete db.sqlite3 and run:
python manage.py migrate
python manage.py createsuperuser
```

### Port already in use
```bash
python manage.py runserver 8080
```

### Can't access admin panel
Make sure you created a superuser:
```bash
python manage.py createsuperuser
```

---

## Sample CSV for Import

Create a file named `sample_flashcards.csv` with this content:

```csv
Topic,Question (Front),Answer (Back)
Mathematics,What is the quadratic formula?,x = (-b ± √(b²-4ac)) / 2a
History,Who was the first US President?,George Washington
Science,What is the chemical formula for water?,H2O
Geography,What is the capital of France?,Paris
Literature,Who wrote Romeo and Juliet?,William Shakespeare
Biology,What is the powerhouse of the cell?,Mitochondria
Chemistry,What is the atomic number of Carbon?,6
Physics,What is Newton's First Law?,An object at rest stays at rest unless acted upon by an external force
Computer Science,What does CPU stand for?,Central Processing Unit
Mathematics,What is Pi approximately equal to?,3.14159
```

Then import it via the web interface at: Import Flashcards → Choose File → Import

---

## Next Steps

1. ✅ Create multiple flashcards
2. ✅ Organize by topics
3. ✅ Use study mode regularly
4. ✅ Track your progress
5. ✅ Export your data for backup
6. ✅ Try the dark mode toggle!

**Happy Learning! 🎓**
