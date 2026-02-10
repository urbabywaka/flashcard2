<<<<<<< HEAD
# flashcard2
flashcard
=======
# 🎓 FlashMaster - Full-Stack Django Flashcard Application

A modern, feature-rich flashcard web application built with Python Django to help students create, organize, and review flashcards for effective studying.

![Django](https://img.shields.io/badge/Django-4.2-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### Core Functionality
- **User Authentication**: Secure signup, login, and logout using Django's built-in authentication
- **CRUD Operations**: Create, read, update, and delete flashcards
- **User Privacy**: Each user's flashcards are private and isolated
- **Flashcard Properties**:
  - Front (Question)
  - Back (Answer)
  - Topic/Subject categorization
  - Created and updated timestamps

### Study Mode
- **Interactive Card Flipping**: Smooth CSS animations for flipping cards
- **Randomized Order**: Cards are shuffled for better learning
- **Progress Tracking**: Real-time progress bar and statistics
- **Quick Actions**:
  - "I Know This" button - marks cards as mastered
  - "Review Later" button - flags cards for future review
- **Keyboard Shortcuts**:
  - `Space/Enter`: Flip card
  - `→` or `k`: Mark as known
  - `←` or `r`: Mark for review
- **Topic Filtering**: Study specific subjects
- **Review Mode**: Focus only on cards not yet mastered

### User Interface
- **Modern Design**: Clean, student-friendly Bootstrap 5 interface
- **Fully Responsive**: Works seamlessly on mobile, tablet, and desktop
- **Dark Mode Toggle**: Switch between light and dark themes (saved in localStorage)
- **Smooth Animations**: Card flip effects and transitions
- **Progress Visualization**: Charts and statistics for tracking learning

### Additional Features
- **Search & Filter**: Find flashcards by content or topic
- **Statistics Dashboard**: 
  - Total cards, known cards, review cards
  - Topic breakdown with progress bars
  - Study session history
  - Success rates and performance metrics
- **Import/Export**: CSV support for bulk operations
- **Study Sessions**: Automatic tracking of study time and performance
- **Admin Panel**: Django admin interface for user and flashcard management

## 🏗️ Project Structure

```
flashcard_app/
├── flashcard_project/          # Main project configuration
│   ├── __init__.py
│   ├── settings.py            # Django settings
│   ├── urls.py                # Main URL configuration
│   ├── wsgi.py                # WSGI configuration
│   └── asgi.py                # ASGI configuration
├── accounts/                   # Authentication app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py               # Login and signup forms
│   ├── models.py
│   ├── urls.py
│   └── views.py               # Authentication views
├── flashcards/                 # Main flashcard app
│   ├── __init__.py
│   ├── admin.py               # Admin configuration
│   ├── apps.py
│   ├── forms.py               # Flashcard forms
│   ├── models.py              # Flashcard and StudySession models
│   ├── urls.py
│   └── views.py               # All flashcard views
├── templates/                  # HTML templates
│   ├── base.html              # Base template with navigation
│   ├── accounts/
│   │   ├── login.html
│   │   ├── signup.html
│   │   └── profile.html
│   └── flashcards/
│       ├── dashboard.html
│       ├── flashcard_list.html
│       ├── flashcard_form.html
│       ├── flashcard_detail.html
│       ├── flashcard_confirm_delete.html
│       ├── study_mode.html
│       ├── statistics.html
│       └── import_flashcards.html
├── static/                     # Static files (CSS, JS, images)
├── manage.py                   # Django management script
└── requirements.txt            # Python dependencies
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### Step-by-Step Setup

1. **Clone or Download the Project**
   ```bash
   # If using Git
   git clone <repository-url>
   cd flashcard_app
   
   # Or download and extract the ZIP file
   ```

2. **Create a Virtual Environment (Recommended)**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Database Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a Superuser (Admin Account)**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

6. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   - Main Application: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## 📖 Usage Guide

### For Students

1. **Sign Up**: Create a new account at `/accounts/signup/`
2. **Create Flashcards**: 
   - Click "Create Card" in the navigation
   - Fill in topic, question, and answer
   - Preview your card before saving
3. **Study Mode**:
   - Click "Study Mode" from the dashboard
   - Choose a topic or study all cards
   - Click cards to flip them
   - Mark as "Known" or "Review Later"
4. **Track Progress**:
   - View statistics on the dashboard
   - Check detailed analytics in the Statistics page
5. **Import/Export**:
   - Import flashcards from CSV files
   - Export your flashcards for backup

### For Administrators

1. **Access Admin Panel**: Log in at `/admin/`
2. **Manage Users**: View and moderate user accounts
3. **Manage Flashcards**: View all flashcards across users
4. **View Study Sessions**: Monitor learning activity

## 🔧 Configuration

### Database
By default, the app uses SQLite (`db.sqlite3`). To use PostgreSQL:

1. Install psycopg2: `pip install psycopg2-binary`
2. Update `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'flashcard_db',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

### Security Settings

Before deploying to production:

1. Change `SECRET_KEY` in `settings.py`
2. Set `DEBUG = False`
3. Update `ALLOWED_HOSTS` with your domain
4. Configure static files serving
5. Use environment variables for sensitive data

## 📊 Models

### Flashcard Model
- `user`: Foreign key to User (owner)
- `front`: TextField (question)
- `back`: TextField (answer)
- `topic`: CharField (subject/category)
- `created_at`: DateTimeField
- `updated_at`: DateTimeField
- `times_reviewed`: Integer (study tracking)
- `times_correct`: Integer (performance tracking)
- `last_reviewed`: DateTimeField
- `is_known`: Boolean (mastery status)

### StudySession Model
- `user`: Foreign key to User
- `started_at`: DateTimeField
- `ended_at`: DateTimeField
- `cards_studied`: Integer
- `cards_known`: Integer
- `topic`: CharField

## 🎨 Customization

### Themes
The app includes a light/dark mode toggle. Theme preference is saved in localStorage.

### Styling
- Bootstrap 5 for responsive design
- Custom CSS variables for easy theming
- Modify colors in `base.html` CSS variables:
  ```css
  :root {
      --primary-color: #6366f1;
      --secondary-color: #8b5cf6;
      --success-color: #10b981;
      ...
  }
  ```

## 🔐 Security Features

- **CSRF Protection**: All forms include CSRF tokens
- **Password Validation**: Django's built-in validators
- **User Authentication**: Session-based authentication
- **Private Data**: User flashcards are isolated
- **SQL Injection Prevention**: Django ORM protects against SQL injection
- **XSS Protection**: Template auto-escaping enabled

## 📱 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/accounts/signup/` | GET, POST | User registration |
| `/accounts/login/` | GET, POST | User login |
| `/accounts/logout/` | GET | User logout |
| `/accounts/profile/` | GET | User profile |
| `/flashcards/` | GET | Dashboard |
| `/flashcards/list/` | GET | List flashcards |
| `/flashcards/create/` | GET, POST | Create flashcard |
| `/flashcards/<id>/` | GET | View flashcard |
| `/flashcards/<id>/edit/` | GET, POST | Edit flashcard |
| `/flashcards/<id>/delete/` | GET, POST | Delete flashcard |
| `/flashcards/study/` | GET | Study mode |
| `/flashcards/<id>/mark/` | POST | Mark card (AJAX) |
| `/flashcards/export/` | GET | Export CSV |
| `/flashcards/import/` | GET, POST | Import CSV |
| `/flashcards/statistics/` | GET | View statistics |

## 🧪 Testing

Run Django tests:
```bash
python manage.py test
```

## 📝 CSV Import Format

Example CSV file for importing flashcards:
```csv
Topic,Question (Front),Answer (Back)
Mathematics,What is the Pythagorean theorem?,a² + b² = c²
History,When was the Declaration of Independence signed?,July 4 1776
Science,What is photosynthesis?,Process by which plants convert light into energy
```

## 🚀 Future Enhancements

Potential features for future development:
- [ ] Spaced Repetition System (SRS) algorithm
- [ ] Quiz mode with scoring
- [ ] Image support for flashcards
- [ ] Audio pronunciation for language learning
- [ ] Collaborative study sets
- [ ] Mobile app (React Native)
- [ ] Advanced analytics and insights
- [ ] Achievement system and gamification
- [ ] Social features (share sets, compete with friends)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Built with ❤️ using Django

## 🙏 Acknowledgments

- Django Framework
- Bootstrap 5
- Bootstrap Icons
- The open-source community

---

**Happy Studying! 📚**
>>>>>>> 0c028f7 (Initial commit)
