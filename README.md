# QBC - Question Bank Collection System

This is a web-based quiz application designed for students enrolled in the BS in Data Science course at IIT Madras. The application allows students to take quizzes, view analytics, and allows admins to manage subjects, chapters, quizzes, and questions.

## Features

- **User Dashboard**: Students can view and attempt quizzes, see their performance analytics, and track their progress.
- **Admin Dashboard**: Admins can manage subjects, chapters, quizzes, and questions. They can also view analytics related to student performance.
- **Quiz Analytics**: The application provides insights into quiz performance by subject, student qualifications, and more.
- **User Analytics**: Students can view their quiz attempts and performance per subject.

## Technology Stack

- **Backend Framework**: Flask 3.1.0
- **Database ORM**: SQLAlchemy 2.0.40
- **Authentication**: Flask-Login 0.6.3
- **Template Engine**: Jinja2 3.1.6
- **Database**: SQLite (default)
- **Additional Dependencies**: See requirements.txt

## Project Structure

```
QBC/
├── app.py                 # Main application entry point
├── requirements.txt       # Project dependencies
├── website/              # Main application package
│   ├── __init__.py       # Application factory and configuration
│   ├── auth.py           # Authentication related functions
│   ├── models.py         # Database models
│   ├── views.py          # Route handlers and views
│   ├── decorators.py     # Custom decorators
│   ├── static/          # Static files (CSS, JS, images)
│   └── templates/       # HTML templates
└── instance/            # Instance-specific files (database, config)
```

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd QBC
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Configuration

The application uses Flask's configuration system. Key configuration options can be set in the instance folder or through environment variables:

- `SECRET_KEY`: Used for session security
- `SQLALCHEMY_DATABASE_URI`: Database connection string
- `FLASK_ENV`: Development/Production environment

## Security Features

- Password hashing and secure storage
- CSRF protection
- Session management
- Role-based access control
- Secure password reset functionality

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
