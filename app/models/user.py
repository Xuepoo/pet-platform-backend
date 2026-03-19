"""User model for authentication and profile management.

This module defines the User SQLAlchemy model with relationships
to pets, applications, reports, and social features.
"""

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    """User account model.
    
    Attributes:
        id: Primary key.
        full_name: User's display name.
        email: Unique email address for authentication.
        hashed_password: Bcrypt hashed password.
        is_active: Whether the account is active.
        is_superuser: Whether the user has admin privileges.
        age: Optional user age.
        gender: Optional gender.
        avatar: Optional avatar image URL.
        bio: Optional biography text.
        pets: Relationship to owned pets.
        applications: Relationship to adoption applications.
        reports: Relationship to lost/found reports.
        posts: Relationship to social posts.
        comments: Relationship to comments.
        post_likes: Relationship to post likes.
        comment_likes: Relationship to comment likes.
    """
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    avatar = Column(String, nullable=True)
    bio = Column(String, nullable=True)

    pets = relationship("Pet", back_populates="owner")
    applications = relationship("Application", back_populates="user")
    reports = relationship("Report", back_populates="user")
    
    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")
    post_likes = relationship("PostLike", back_populates="user")
    comment_likes = relationship("CommentLike", back_populates="user")
