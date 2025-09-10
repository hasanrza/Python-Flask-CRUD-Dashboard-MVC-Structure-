"""
User Controller for handling user-related operations.
"""

import os
import uuid
from werkzeug.utils import secure_filename
from flask import request, redirect, url_for, flash, render_template
from app.models.user import User
from app.migrations.migration_manager import MigrationManager


class UserController:
    """Controller for user-related operations."""
    
    def __init__(self):
        self.upload_folder = os.path.join('static', 'uploads')
        self.allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        self.max_file_size = 5 * 1024 * 1024  # 5MB
        
        # Ensure upload directory exists
        os.makedirs(self.upload_folder, exist_ok=True)
    
    def allowed_file(self, filename):
        """Check if file extension is allowed."""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def handle_file_upload(self, file):
        """Handle file upload and return filename."""
        if file and file.filename and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            file_path = os.path.join(self.upload_folder, unique_filename)
            file.save(file_path)
            return unique_filename
        return None
    
    def index(self):
        """Display list of users."""
        # Run migrations to ensure database is up to date
        migration_manager = MigrationManager()
        migration_manager.run_migrations()
        
        users = User.all()
        return render_template('admin/users/list.html', users=users)
    
    def create_form(self):
        """Display create user form."""
        return render_template('admin/users/create.html')
    
    def store(self):
        """Create a new user."""
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        confirm_password = request.form.get("confirm_password") or ""
        
        # Validation
        if not name or not email or not password:
            flash("All fields are required.", "error")
            return render_template('admin/users/create.html')
        
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template('admin/users/create.html')
        
        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "error")
            return render_template('admin/users/create.html')
        
        # Handle image upload
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                image_path = self.handle_file_upload(file)
                if not image_path:
                    flash("Invalid file type. Please upload JPG, PNG, or GIF images only.", "error")
                    return render_template('admin/users/create.html')
        
        try:
            user = User.create(name, email, password, image_path)
            flash("User created successfully.", "success")
            return redirect(url_for('admin_users'))
        except ValueError as e:
            flash(str(e), "error")
            return render_template('admin/users/create.html')
        except Exception as e:
            flash("An error occurred. Please try again.", "error")
            return render_template('admin/users/create.html')
    
    def edit_form(self, user_id):
        """Display edit user form."""
        user = User.find_by_id(user_id)
        if not user:
            flash("User not found.", "error")
            return redirect(url_for('admin_users'))
        
        return render_template('admin/users/edit.html', user=user)
    
    def update(self, user_id):
        """Update user information."""
        user = User.find_by_id(user_id)
        if not user:
            flash("User not found.", "error")
            return redirect(url_for('admin_users'))
        
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        
        # Validation
        if not name or not email:
            flash("Name and email are required.", "error")
            return render_template('admin/users/edit.html', user=user)
        
        # Handle image upload
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                image_path = self.handle_file_upload(file)
                if not image_path:
                    flash("Invalid file type. Please upload JPG, PNG, or GIF images only.", "error")
                    return render_template('admin/users/edit.html', user=user)
        
        try:
            # Prepare update data
            update_data = {
                'name': name,
                'email': email
            }
            
            if password:
                update_data['password'] = password
            
            if image_path:
                update_data['image_path'] = image_path
            
            user.update(**update_data)
            flash("User updated successfully.", "success")
            return redirect(url_for('admin_users'))
        except ValueError as e:
            flash(str(e), "error")
            return render_template('admin/users/edit.html', user=user)
        except Exception as e:
            flash("An error occurred. Please try again.", "error")
            return render_template('admin/users/edit.html', user=user)
    
    def delete(self, user_id):
        """Delete user."""
        user = User.find_by_id(user_id)
        if not user:
            flash("User not found.", "error")
            return redirect(url_for('admin_users'))
        
        try:
            # Delete associated image file if exists
            if user.image_path:
                image_file_path = os.path.join(self.upload_folder, user.image_path)
                if os.path.exists(image_file_path):
                    os.remove(image_file_path)
            
            user.delete()
            flash("User deleted successfully.", "success")
        except Exception as e:
            flash("Failed to delete user.", "error")
        
        return redirect(url_for('admin_users'))