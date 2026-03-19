from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


# === Media Schemas ===
class PostMediaBase(BaseModel):
    url: str
    media_type: str


class PostMediaCreate(PostMediaBase):
    pass


class PostMediaResponse(PostMediaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


# === Comment Like Schemas ===
class CommentLikeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    created_at: datetime


# === Comment Schemas ===
class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    parent_id: Optional[int] = None


class CommentUpdate(BaseModel):
    content: Optional[str] = None


class CommentAuthor(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: Optional[str] = None
    avatar: Optional[str] = None


class CommentResponse(CommentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    post_id: int
    author_id: int
    parent_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    author: CommentAuthor
    likes_count: int = 0
    is_liked: bool = False


class CommentWithReplies(CommentResponse):
    replies: List["CommentWithReplies"] = []


# === Post Like Schemas ===
class PostLikeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    created_at: datetime


# === Post Schemas ===
class PostBase(BaseModel):
    title: Optional[str] = None
    content: str


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostAuthor(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: Optional[str] = None
    avatar: Optional[str] = None


class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime
    author: PostAuthor
    likes_count: int = 0
    comments_count: int = 0
    is_liked: bool = False
    media: List[PostMediaResponse] = []


class PostDetail(PostResponse):
    comments: List[CommentWithReplies] = []


class PostListResponse(BaseModel):
    items: List[PostResponse]
    total: int
    page: int
    per_page: int
    pages: int


# Self-referencing model update
CommentWithReplies.model_rebuild()
