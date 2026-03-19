from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import uuid
import io

from app import models
from app.api import deps
from app.core.config import settings
from app.core.storage import minio_client
from app.models.post import Post, Comment, PostLike, CommentLike, PostMedia
from app.schemas.post import (
    PostCreate, PostUpdate, PostResponse, PostDetail, PostListResponse,
    CommentCreate, CommentUpdate, CommentResponse, PostMediaResponse
)

router = APIRouter()


def post_to_response(post: Post, current_user_id: Optional[int] = None) -> PostResponse:
    """Convert Post model to PostResponse with computed fields"""
    is_liked = any(like.user_id == current_user_id for like in post.likes) if current_user_id else False
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        author_id=post.author_id,
        created_at=post.created_at,
        updated_at=post.updated_at,
        author=post.author,
        likes_count=len(post.likes),
        comments_count=len(post.comments),
        is_liked=is_liked,
        media=[PostMediaResponse.model_validate(m) for m in post.media]
    )


def comment_to_response(comment: Comment, current_user_id: Optional[int] = None) -> CommentResponse:
    """Convert Comment model to CommentResponse"""
    is_liked = any(like.user_id == current_user_id for like in comment.likes) if current_user_id else False
    return CommentResponse(
        id=comment.id,
        content=comment.content,
        post_id=comment.post_id,
        author_id=comment.author_id,
        parent_id=comment.parent_id,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
        author=comment.author,
        likes_count=len(comment.likes),
        is_liked=is_liked
    )


async def get_post_by_id(db: AsyncSession, post_id: int) -> Optional[Post]:
    result = await db.execute(
        select(Post)
        .options(
            selectinload(Post.author),
            selectinload(Post.media),
            selectinload(Post.likes),
            selectinload(Post.comments).selectinload(Comment.author),
            selectinload(Post.comments).selectinload(Comment.likes),
        )
        .where(Post.id == post_id)
    )
    return result.scalar_one_or_none()


async def get_comment_by_id(db: AsyncSession, comment_id: int) -> Optional[Comment]:
    result = await db.execute(
        select(Comment)
        .options(
            selectinload(Comment.author),
            selectinload(Comment.likes),
            selectinload(Comment.replies).selectinload(Comment.author),
        )
        .where(Comment.id == comment_id)
    )
    return result.scalar_one_or_none()


@router.get("/", response_model=PostListResponse)
async def get_posts(
    page: int = 1,
    per_page: int = 20,
    author_id: Optional[int] = None,
    db: AsyncSession = Depends(deps.get_db),
    current_user: Optional[models.User] = Depends(deps.get_current_user_optional)
):
    """Get paginated list of posts"""
    skip = (page - 1) * per_page
    
    query = select(Post).options(
        selectinload(Post.author),
        selectinload(Post.media),
        selectinload(Post.likes),
        selectinload(Post.comments),
    )
    
    if author_id:
        query = query.where(Post.author_id == author_id)
    
    # Get total count
    count_query = select(func.count(Post.id))
    if author_id:
        count_query = count_query.where(Post.author_id == author_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar()
    
    # Get posts
    query = query.order_by(Post.created_at.desc()).offset(skip).limit(per_page)
    result = await db.execute(query)
    posts = result.scalars().all()
    
    user_id = current_user.id if current_user else None
    items = [post_to_response(p, user_id) for p in posts]
    
    return PostListResponse(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
        pages=(total + per_page - 1) // per_page if total else 0
    )


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_in: PostCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Create a new post"""
    db_obj = Post(
        title=post_in.title,
        content=post_in.content,
        author_id=current_user.id
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj, ["author", "media", "likes", "comments"])
    return post_to_response(db_obj, current_user.id)


@router.get("/{post_id}", response_model=PostDetail)
async def get_post(
    post_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: Optional[models.User] = Depends(deps.get_current_user_optional)
):
    """Get a single post with comments"""
    post = await get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    user_id = current_user.id if current_user else None
    response = post_to_response(post, user_id)
    
    # Build comments tree with nested replies
    def build_comment_tree(comments, parent_id=None):
        result = []
        for comment in comments:
            if comment.parent_id == parent_id:
                comment_resp = comment_to_response(comment, user_id)
                comment_resp_dict = comment_resp.model_dump()
                comment_resp_dict["replies"] = build_comment_tree(comments, comment.id)
                result.append(comment_resp_dict)
        return result
    
    return PostDetail(
        **response.model_dump(),
        comments=build_comment_tree(post.comments)
    )


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_in: PostUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Update a post (only by author)"""
    post = await get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    update_data = post_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(post, field, value)
    await db.commit()
    await db.refresh(post)
    return post_to_response(post, current_user.id)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Delete a post (only by author or admin)"""
    post = await get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    await db.execute(delete(Post).where(Post.id == post_id))
    await db.commit()


@router.post("/{post_id}/like", status_code=status.HTTP_201_CREATED)
async def like_post(
    post_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Like a post"""
    post = await get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check if already liked
    existing = await db.execute(
        select(PostLike).where(
            PostLike.post_id == post_id,
            PostLike.user_id == current_user.id
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Already liked")
    
    like = PostLike(post_id=post_id, user_id=current_user.id)
    db.add(like)
    await db.commit()
    
    return {"message": "Post liked"}


@router.delete("/{post_id}/like", status_code=status.HTTP_204_NO_CONTENT)
async def unlike_post(
    post_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Unlike a post"""
    result = await db.execute(
        delete(PostLike).where(
            PostLike.post_id == post_id,
            PostLike.user_id == current_user.id
        )
    )
    await db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=400, detail="Not liked")


@router.post("/{post_id}/media", response_model=PostMediaResponse)
async def upload_post_media(
    post_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Upload media for a post"""
    post = await get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    try:
        # Read file content
        content = await file.read()
        file_size = len(content)
        file_data = io.BytesIO(content)
        
        # Generate unique filename
        filename_ext = file.filename.split(".")[-1] if file.filename else "jpg"
        filename = f"posts/{uuid.uuid4()}.{filename_ext}"
        
        # Upload to Minio
        minio_client.put_object(
            bucket_name=settings.MINIO_BUCKET_NAME,
            object_name=filename,
            data=file_data,
            length=file_size,
            content_type=file.content_type
        )
        
        # Construct URL
        protocol = "https" if settings.MINIO_SECURE else "http"
        url = f"{protocol}://{settings.MINIO_ENDPOINT}/{settings.MINIO_BUCKET_NAME}/{filename}"
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not upload file: {str(e)}")
    
    media_type = "gif" if file.content_type == "image/gif" else "image"
    
    media = PostMedia(post_id=post_id, url=url, media_type=media_type)
    db.add(media)
    await db.commit()
    await db.refresh(media)
    return PostMediaResponse.model_validate(media)


# === Comment Routes ===
@router.get("/{post_id}/comments", response_model=List[CommentResponse])
async def get_comments(
    post_id: int,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(deps.get_db),
    current_user: Optional[models.User] = Depends(deps.get_current_user_optional)
):
    """Get comments for a post"""
    result = await db.execute(
        select(Comment)
        .options(
            selectinload(Comment.author),
            selectinload(Comment.likes),
            selectinload(Comment.replies).selectinload(Comment.author),
        )
        .where(Comment.post_id == post_id, Comment.parent_id == None)
        .order_by(Comment.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    comments = list(result.scalars().all())
    user_id = current_user.id if current_user else None
    return [comment_to_response(c, user_id) for c in comments]


@router.post("/{post_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    post_id: int,
    comment_in: CommentCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Create a comment on a post"""
    post = await get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db_obj = Comment(
        content=comment_in.content,
        post_id=post_id,
        author_id=current_user.id,
        parent_id=comment_in.parent_id
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj, ["author", "likes"])
    return comment_to_response(db_obj, current_user.id)


@router.put("/comments/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    comment_in: CommentUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Update a comment (only by author)"""
    comment = await get_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    update_data = comment_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(comment, field, value)
    await db.commit()
    await db.refresh(comment)
    return comment_to_response(comment, current_user.id)


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Delete a comment (only by author or admin)"""
    comment = await get_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    await db.execute(delete(Comment).where(Comment.id == comment_id))
    await db.commit()


@router.post("/comments/{comment_id}/like", status_code=status.HTTP_201_CREATED)
async def like_comment(
    comment_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Like a comment"""
    comment = await get_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    existing = await db.execute(
        select(CommentLike).where(
            CommentLike.comment_id == comment_id,
            CommentLike.user_id == current_user.id
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Already liked")
    
    like = CommentLike(comment_id=comment_id, user_id=current_user.id)
    db.add(like)
    await db.commit()
    
    return {"message": "Comment liked"}


@router.delete("/comments/{comment_id}/like", status_code=status.HTTP_204_NO_CONTENT)
async def unlike_comment(
    comment_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Unlike a comment"""
    result = await db.execute(
        delete(CommentLike).where(
            CommentLike.comment_id == comment_id,
            CommentLike.user_id == current_user.id
        )
    )
    await db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=400, detail="Not liked")
