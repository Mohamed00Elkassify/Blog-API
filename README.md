# Blog API 📚

A simple Django REST API for a blog where users can create posts, comment, and like content.

## What does this do?

This is a **blog website backend** that lets you:
- Register and login users
- Create blog posts
- Add comments to posts
- Like posts and comments
- Organize posts with categories and tags

## What you need

- Python 3.8 or newer
- Basic knowledge of Django

## How to run this project

### Step 1: Download and setup

```bash
# 1. Go to the project folder
cd blog_project

# 2. Create a virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Mac/Linux

# 3. Install required packages
pip install -r requirements.txt
```

### Step 2: Setup the database

```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate

# Create an admin user (optional)
python manage.py createsuperuser
```

### Step 3: Run the server

```bash
python manage.py runserver
```

Now open your browser and go to: `http://127.0.0.1:8000/api/docs/`

## Main Features

### 🔐 User Accounts
- Users can register and login
- Each user has a profile with bio and avatar
- Only logged-in users can create posts

### 📝 Blog Posts
- Create, edit, and delete posts
- Add categories and tags to organize posts
- Search posts by title or content
- Only the author can edit their own posts

### 💬 Comments
- Add comments to any post
- Edit or delete your own comments
- Like/unlike posts and comments

## API Endpoints (the important ones)

### User stuff:
```
POST /api/auth/users/          # Register
POST /api/auth/jwt/create/     # Login
GET  /api/auth/users/me/       # Get my info
```

### Blog stuff:
```
GET  /api/blog/posts/          # See all posts
POST /api/blog/posts/          # Create new post (need login)
GET  /api/blog/posts/1/        # See specific post
PUT  /api/blog/posts/1/        # Edit post (only author)
POST /api/blog/posts/1/like/   # Like a post
```

### Comments:
```
GET  /api/blog/comments/       # See all comments
POST /api/blog/comments/       # Add comment (need login)
POST /api/blog/comments/1/like/ # Like a comment
```

## How to test the API

1. **Go to the documentation page**: `http://127.0.0.1:8000/api/docs/`
2. **First, register a user** using the `/api/auth/users/` endpoint
3. **Then login** using `/api/auth/jwt/create/` to get your token
4. **Use the token** in other requests (click "Authorize" button in docs)

## Files in this project

```
blog_project/
├── blog/              # Main blog app
│   ├── models.py      # Database tables (Post, Comment, etc.)
│   ├── views.py       # API endpoints
│   ├── serializers.py # Data formatting
│   └── urls.py        # URL routing
├── profiles/          # User profiles app
├── blog_project/      # Project settings
├── manage.py          # Django commands
└── requirements.txt   # Required packages
```

## What each file does

### `models.py` - Database Tables
- **Post**: Blog posts with title, content, author
- **Comment**: Comments on posts
- **Category**: Post categories (like "Technology", "Sports")
- **Tag**: Post tags (like "django", "python")
- **PostLike/CommentLike**: Track who liked what

### `views.py` - API Endpoints
- Handle requests (GET, POST, PUT, DELETE)
- Check permissions (who can do what)
- Return data in JSON format

### `serializers.py` - Data Format
- Convert database data to JSON
- Validate incoming data
- Control what fields are shown

## Common Issues & Solutions

### "Command not found" error
Make sure you're in the right folder and virtual environment is activated.

### "Permission denied" errors in API
You need to login first and include the token in your requests.

### Database errors
Try running: `python manage.py migrate` again.

### Can't access the API
Make sure the server is running: `python manage.py runserver`

## Want to add features?

1. **Add a new field to a model** → Update `models.py` → Run migrations
2. **Add a new API endpoint** → Add to `views.py` and `urls.py`
3. **Change what data is returned** → Update `serializers.py`

## Need help?

- Check the API docs: `http://127.0.0.1:8000/api/docs/`
- Look at the Django docs: https://docs.djangoproject.com/
- Check out Django REST Framework: https://www.django-rest-framework.org/

---

**This is a learning project! Feel free to experiment and break things - that's how you learn! 🎓**
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 6,
}
```

#### **Spectacular (Swagger) Configuration**
```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'Blog API',
    'DESCRIPTION': 'Core API endpoints for a blogging platform.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'TAGS': [
        {'name': 'Auth', 'description': 'Authentication & user management'},
        {'name': 'Profiles', 'description': 'User profile management'},
        {'name': 'Posts', 'description': 'Blog post operations'},
        {'name': 'Comments', 'description': 'Comment operations'},
    ],
}
```

## 🔧 Development

### Code Quality
- **Type hints** for better code documentation
- **Comprehensive docstrings**
- **Consistent naming conventions**
- **Modular architecture**

### Best Practices Implemented
- **Separation of concerns** between apps
- **Custom permissions** for fine-grained access control
- **Signal-based profile creation**
- **Property decorators** for computed fields
- **Comprehensive error handling**

### Adding New Features

1. **Create models** in appropriate app
2. **Write serializers** for API representation
3. **Implement ViewSets** with proper permissions
4. **Add URL patterns**
5. **Write comprehensive tests**
6. **Update API documentation**

## 🐛 Common Issues & Solutions

### Migration Issues
```bash
# Reset migrations if needed
python manage.py migrate --fake blog zero
python manage.py migrate --fake profiles zero
python manage.py makemigrations blog profiles
python manage.py migrate
```

### Permission Denied Errors
- Ensure proper JWT token in Authorization header
- Check if user has necessary permissions for the operation
- Verify token hasn't expired





### Environment Variables
```bash
# .env file
DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=your-database-url
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```


### Useful Commands
```bash
# Create new app
python manage.py startapp app_name

# Make migrations
python manage.py makemigrations

# Apply migrations  
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver

# Run tests
python manage.py test

# Django shell
python manage.py shell
```

## 👥 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
