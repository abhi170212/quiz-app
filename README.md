# Django QuizHub - Coding Quizzes Platform

A comprehensive Django web application that allows users to register, login, and take coding quizzes on various programming languages. The platform includes social features like user profiles, upvoting, commenting, and a leaderboard system.

## Features

### 🔐 Authentication System
- User registration and login functionality
- Secure password authentication
- Profile management
- Logged-in users can access quizzes and profile pages
- Logout redirects to homepage

### 🏠 Home Page
- Display multiple coding quizzes from different languages
- Filter quizzes by programming language
- Quiz cards showing title, language, difficulty, and statistics
- Responsive design with modern UI

### 📝 Quiz System
- Multiple programming languages: Python, Java, C++, JavaScript, PHP, Ruby, Go, C
- Each quiz contains multiple-choice questions (MCQs)
- 4 options per question with only one correct answer
- Timer functionality for each quiz
- Score calculation and result display
- Quiz attempt history

### 👤 User Profiles
- Comprehensive user profile pages
- Display user details (username, email, bio, location)
- Quiz history and scores with pagination
- Social links (website, GitHub, LinkedIn)
- Profile picture upload support
- Statistics dashboard

### 🤝 Social Features
- **Upvoting System**: Users can upvote other users
- **Comments**: Leave comments on other users' profiles
- **Comment Management**: Profile owners can delete comments on their profiles
- **User Search**: Search for users by username or name
- **Follow System**: Users can follow each other (implemented)

### 🏆 Leaderboard
- Top performers ranked by average score
- Recent high scores display
- Achievement levels (Bronze, Silver, Gold, Platinum)
- User statistics comparison

### 💻 Frontend Technologies
- **HTML5** with semantic structure
- **CSS3** with modern styling and animations
- **Bootstrap 5** for responsive design
- **JavaScript** for interactive features
- **Font Awesome** icons
- **AJAX/Fetch API** for real-time interactions

## Technology Stack

### Backend
- **Django 5.2.5** - Web framework
- **Python 3.13** - Programming language
- **SQLite** - Database (development)
- **Pillow** - Image processing

### Frontend
- **Bootstrap 5.1.3** - CSS framework
- **Font Awesome 6.0** - Icons
- **Vanilla JavaScript** - Client-side scripting

## Installation and Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd quiz-app
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv quiz_env
   
   # On Windows:
   quiz_env\Scripts\activate
   
   # On macOS/Linux:
   source quiz_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django pillow
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Create sample data**
   ```bash
   python manage.py create_sample_data
   python manage.py create_test_users
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## Project Structure

```
quiz-app/
├── accounts/               # User authentication app
│   ├── models.py          # CustomUser model
│   ├── views.py           # Auth views
│   ├── forms.py           # Custom forms
│   └── urls.py            # Auth URLs
├── quizzes/               # Quiz management app
│   ├── models.py          # Quiz, Question, QuizAttempt models
│   ├── views.py           # Quiz views
│   ├── urls.py            # Quiz URLs
│   └── management/        # Management commands
├── profiles/              # User profiles app
│   ├── models.py          # UserProfile model
│   ├── views.py           # Profile views
│   └── urls.py            # Profile URLs
├── social/                # Social features app
│   ├── models.py          # Upvote, Comment, Follow models
│   ├── views.py           # Social interaction views
│   └── urls.py            # Social URLs
├── templates/             # HTML templates
│   ├── base/              # Base templates
│   ├── accounts/          # Auth templates
│   ├── quizzes/           # Quiz templates
│   └── profiles/          # Profile templates
├── static/                # Static files
│   ├── css/               # Custom CSS
│   └── js/                # JavaScript files
├── media/                 # User uploaded files
└── quizhub/              # Main project settings
    ├── settings.py        # Django settings
    ├── urls.py            # Main URL configuration
    └── wsgi.py            # WSGI configuration
```

## Key Features Implementation

### Quiz Timer System
- Real-time countdown timer
- Automatic submission when time expires
- Visual warnings at 5 minutes and 1 minute remaining
- Time tracking for performance analytics

### AJAX-Powered Social Features
- Real-time upvoting without page reload
- Dynamic comment addition and deletion
- Instant UI updates
- CSRF protection for security

### Responsive Design
- Mobile-first approach
- Bootstrap grid system
- Custom CSS animations and transitions
- Dark mode support (via CSS media queries)

### Security Features
- CSRF protection on all forms
- User authentication required for sensitive actions
- Input validation and sanitization
- Secure file upload handling

## Sample Data

The application includes management commands to create sample data:

### Quiz Categories
- **Python**: Fundamentals and Advanced topics
- **JavaScript**: Basic concepts and syntax
- **Java**: Programming basics and OOP concepts
- **C++**: Programming fundamentals
- **PHP**: Web development basics

### Test Users
- `alex_dev` - Full-stack developer
- `sarah_code` - Frontend specialist
- `mike_python` - Data scientist
- `jenny_java` - Backend developer

## API Endpoints

### Authentication
- `GET/POST /accounts/register/` - User registration
- `GET/POST /accounts/login/` - User login
- `POST /accounts/logout/` - User logout
- `GET /accounts/search/` - User search

### Quizzes
- `GET /` - Home page with quiz list
- `GET /quiz/<id>/` - Quiz details
- `GET /quiz/<id>/take/` - Take quiz
- `POST /quiz/<id>/submit/` - Submit quiz answers
- `GET /quiz/<id>/result/<attempt_id>/` - View results
- `GET /leaderboard/` - Leaderboard page

### Profiles
- `GET /profiles/profile/<username>/` - User profile
- `GET/POST /profiles/profile/<username>/edit/` - Edit profile
- `GET /profiles/my-profile/` - Current user's profile

### Social Features
- `POST /social/upvote/<username>/` - Toggle upvote
- `POST /social/comment/<username>/` - Add comment
- `POST /social/comment/delete/<id>/` - Delete comment
- `POST /social/follow/<username>/` - Toggle follow

## Admin Interface

The Django admin interface provides comprehensive management capabilities:

- **User Management**: View and manage all users
- **Quiz Management**: Create and edit quizzes and questions
- **Content Moderation**: Monitor comments and social interactions
- **Analytics**: View quiz attempts and user statistics

Access the admin interface at `/admin/` with superuser credentials.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Future Enhancements

- **Real-time Multiplayer Quizzes**: Compete with other users live
- **Quiz Creation Interface**: Allow users to create their own quizzes
- **Advanced Analytics**: Detailed performance insights
- **Mobile Application**: Native mobile app development
- **Integration with Coding Platforms**: GitHub, LeetCode integration
- **Video Explanations**: Add video explanations for quiz answers
- **Certification System**: Issue certificates for high performers




## Support

For support and questions, please open an issue in the repository or contact me.

---

**QuizHub** - Enhance your coding skills, one quiz at a time! 🚀
