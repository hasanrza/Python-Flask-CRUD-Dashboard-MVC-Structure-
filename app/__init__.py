"""
Flask application factory with MVC structure.
"""

from flask import Flask
from config import AppConfig
from app.controllers.user_controller import UserController
from app.migrations.migration_manager import MigrationManager


def create_app():
    """Create and configure the Flask application instance."""
    import os
    
    # Get the directory where this file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    
    app = Flask(__name__, 
                template_folder=os.path.join(parent_dir, 'templates'),
                static_folder=os.path.join(parent_dir, 'static'))
    app.config.from_object(AppConfig)
    app.secret_key = AppConfig.SECRET_KEY
    
    # Configure file upload settings
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size
    
    # Initialize controller
    user_controller = UserController()
    
    # Register routes
    register_routes(app, user_controller)
    
    return app


def register_routes(app, user_controller):
    """Register all application routes."""
    
    @app.route("/", methods=["GET"])
    def home():
        """Redirect root to the registration page."""
        from flask import redirect, url_for
        return redirect(url_for("register"))
    
    @app.route("/register", methods=["GET", "POST"])
    def register():
        """Render the registration form and handle submissions."""
        from flask import request, redirect, url_for, flash, render_template
        from werkzeug.security import generate_password_hash
        from app.models.user import User
        
        if request.method == "POST":
            name = (request.form.get("name") or "").strip()
            email = (request.form.get("email") or "").strip().lower()
            password = request.form.get("password") or ""

            if not name or not email or not password:
                flash("All fields are required.", "error")
                return render_template("register.html")

            try:
                User.create(name, email, password)
                flash("Registration successful!", "success")
                return redirect(url_for("register"))
            except ValueError as e:
                flash(str(e), "error")
            except Exception as e:
                flash("An error occurred. Please try again.", "error")

        return render_template("register.html")
    
    # Admin routes
    @app.route("/admin", methods=["GET"])
    def admin_dashboard():
        """Admin landing page: redirect to users list for now."""
        from flask import redirect, url_for
        return redirect(url_for("admin_users"))
    
    @app.route("/admin/users", methods=["GET"])
    def admin_users():
        """List users for admin management."""
        return user_controller.index()
    
    @app.route("/admin/users/create", methods=["GET"])
    def admin_users_create_form():
        """Display create user form."""
        return user_controller.create_form()
    
    @app.route("/admin/users/create", methods=["POST"])
    def admin_users_create():
        """Create a new user."""
        return user_controller.store()
    
    @app.route("/admin/users/<int:user_id>/edit", methods=["GET"])
    def admin_users_edit_form(user_id):
        """Display edit user form."""
        return user_controller.edit_form(user_id)
    
    @app.route("/admin/users/<int:user_id>/edit", methods=["POST"])
    def admin_users_edit(user_id):
        """Edit an existing user."""
        return user_controller.update(user_id)
    
    @app.route("/admin/users/<int:user_id>/delete", methods=["POST"])
    def admin_users_delete(user_id):
        """Delete a user by id."""
        return user_controller.delete(user_id)
