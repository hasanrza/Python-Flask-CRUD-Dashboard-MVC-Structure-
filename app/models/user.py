"""
User model for database operations.
"""

import mysql.connector as connector
from mysql.connector import errorcode
from werkzeug.security import generate_password_hash, check_password_hash
from config import AppConfig
from typing import List, Optional, Dict, Any


class User:
    """User model for database operations."""
    
    def __init__(self, id=None, name=None, email=None, password_hash=None, image_path=None, created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.image_path = image_path
        self.created_at = created_at
        self.updated_at = updated_at
    
    @staticmethod
    def get_connection():
        """Get database connection."""
        config = {
            "host": AppConfig.DB_HOST,
            "user": AppConfig.DB_USER,
            "password": AppConfig.DB_PASSWORD,
            "database": AppConfig.DB_NAME,
        }
        return connector.connect(**config)
    
    @classmethod
    def create(cls, name: str, email: str, password: str, image_path: str = None) -> 'User':
        """Create a new user."""
        password_hash = generate_password_hash(password)
        
        connection = cls.get_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO `users` (`name`, `email`, `password_hash`, `image_path`) VALUES (%s, %s, %s, %s)",
                (name, email, password_hash, image_path)
            )
            connection.commit()
            
            user_id = cursor.lastrowid
            return cls.find_by_id(user_id)
        except connector.Error as e:
            if e.errno == errorcode.ER_DUP_ENTRY:
                raise ValueError("Email already exists")
            raise
        finally:
            cursor.close()
            connection.close()
    
    @classmethod
    def find_by_id(cls, user_id: int) -> Optional['User']:
        """Find user by ID."""
        connection = cls.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT * FROM `users` WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            
            if result:
                return cls(**result)
            return None
        finally:
            cursor.close()
            connection.close()
    
    @classmethod
    def find_by_email(cls, email: str) -> Optional['User']:
        """Find user by email."""
        connection = cls.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT * FROM `users` WHERE email = %s", (email,))
            result = cursor.fetchone()
            
            if result:
                return cls(**result)
            return None
        finally:
            cursor.close()
            connection.close()
    
    @classmethod
    def all(cls) -> List['User']:
        """Get all users."""
        connection = cls.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT * FROM `users` ORDER BY id DESC")
            results = cursor.fetchall()
            
            return [cls(**result) for result in results]
        finally:
            cursor.close()
            connection.close()
    
    def update(self, name: str = None, email: str = None, password: str = None, image_path: str = None) -> bool:
        """Update user information."""
        connection = self.get_connection()
        cursor = connection.cursor()
        
        try:
            updates = []
            params = []
            
            if name is not None:
                updates.append("`name` = %s")
                params.append(name)
            
            if email is not None:
                updates.append("`email` = %s")
                params.append(email)
            
            if password is not None:
                password_hash = generate_password_hash(password)
                updates.append("`password_hash` = %s")
                params.append(password_hash)
            
            if image_path is not None:
                updates.append("`image_path` = %s")
                params.append(image_path)
            
            if not updates:
                return False
            
            params.append(self.id)
            query = f"UPDATE `users` SET {', '.join(updates)} WHERE id = %s"
            
            cursor.execute(query, params)
            connection.commit()
            
            # Update instance attributes
            if name is not None:
                self.name = name
            if email is not None:
                self.email = email
            if password is not None:
                self.password_hash = password_hash
            if image_path is not None:
                self.image_path = image_path
            
            return True
        except connector.Error as e:
            if e.errno == errorcode.ER_DUP_ENTRY:
                raise ValueError("Email already exists")
            raise
        finally:
            cursor.close()
            connection.close()
    
    def delete(self) -> bool:
        """Delete user."""
        connection = self.get_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute("DELETE FROM `users` WHERE id = %s", (self.id,))
            connection.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            connection.close()
    
    def check_password(self, password: str) -> bool:
        """Check if provided password matches user's password."""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'image_path': self.image_path,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"
