from unittest import result
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends (oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
    #dataresponse = cursor.fetchone()
    
    dataresponse = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not dataresponse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} was not found")

    return dataresponse

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends (oauth2.get_current_user), limit: int = 10, pg: int = 1, title: Optional[str] =""):
    #cursor.execute("""SELECT * FROM posts""")
    #dataresponse = cursor.fetchall()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(title)).limit(limit).offset((pg-1)*limit).all()
    return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate,db: Session = Depends(get_db), current_user: int = Depends (oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",(post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()

    new_post = models.Post(user_id=current_user.id,**post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends (oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} was not found")
    if deleted_post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail=f"You do not own this post")
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def overwrite_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends (oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title =%s, content=%s, published=%s WHERE id = %s RETURNING *""",(post.title, post.content, post.published, id))
    #new_post = cursor.fetchone()
    #conn.commit()
    new_post = db.query(models.Post).filter(models.Post.id == id)
    if new_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} was not found")
    if new_post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail=f"You do not own this post")
    new_post.update(post.dict(),synchronize_session=False)
    db.commit()
    return new_post.first()

