# Flask MVC Application Structure

This application has been refactored to follow a proper MVC (Model-View-Controller) pattern similar to Laravel.

## 📁 Project Structure

```
python/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── controllers/             # Controllers (Business Logic)
│   │   ├── __init__.py
│   │   └── user_controller.py   # User operations
│   ├── models/                  # Models (Database Entities)
│   │   ├── __init__.py
│   │   └── user.py             # User model
│   ├── views/                   # Views (Templates)
│   │   ├── base_admin.html     # Base admin template
│   │   └── admin/
│   │       └── users/          # User templates
│   │           ├── list.html
│   │           ├── create.html
│   │           └── edit.html
│   ├── migrations/              # Database Migrations
│   │   ├── __init__.py
│   │   ├── migration_manager.py # Migration system
│   │   └── migrations.py       # Migration files
│   └── config/                  # Configuration files
├── static/                      # Static files (CSS, JS, images)
│   └── uploads/                 # User uploaded images
├── templates/                   # Legacy templates (can be removed)
├── main.py                     # New entry point
├── migrate.py                  # Migration command
├── config.py                   # App configuration
```

## 🚀 How to Run

### 1. Run Migrations
```bash
python migrate.py
```

### 2. Start the Application
```bash
python main.py
```

## 📋 Features

### ✅ MVC Architecture
- **Models**: Handle database operations and business logic
- **Views**: Template files for rendering
- **Controllers**: Handle HTTP requests and responses
- **Migrations**: Database schema management

### ✅ User Management
- Create, Read, Update, Delete users
- Image upload functionality
- Form validation
- Professional admin interface

### ✅ Database Migrations
- Automatic schema creation
- Version control for database changes
- Easy rollback capabilities

## 🔧 Key Components

### Models (`app/models/user.py`)
- `User.create()` - Create new user
- `User.find_by_id()` - Find user by ID
- `User.find_by_email()` - Find user by email
- `User.all()` - Get all users
- `User.update()` - Update user information
- `User.delete()` - Delete user

### Controllers (`app/controllers/user_controller.py`)
- `index()` - List users
- `create_form()` - Show create form
- `store()` - Handle user creation
- `edit_form()` - Show edit form
- `update()` - Handle user updates
- `delete()` - Handle user deletion

### Migrations (`app/migrations/`)
- Automatic database setup
- Schema versioning
- Easy database updates

## 🎯 Benefits of MVC Structure

1. **Separation of Concerns**: Each component has a specific responsibility
2. **Maintainability**: Easy to modify and extend
3. **Testability**: Components can be tested independently
4. **Scalability**: Easy to add new features
5. **Code Reusability**: Models and controllers can be reused

To fully migrate:
1. Use `main.py` 
2. All templates are now in `app/views/`
3. Database operations go through models
4. Business logic goes in controllers
