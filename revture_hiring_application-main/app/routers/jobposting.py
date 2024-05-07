from fastapi import APIRouter, Depends, Header, HTTPException
from typing import List
from sqlalchemy.orm import Session
from ..schemas import JobPostCreate, User, ShowJobPost
from ..database import SessionLocal, get_db
from ..oauth2 import get_current_user
from ..models import JobPosting

router = APIRouter(
    tags=["Job Posts"],
)

@router.post("/job-posts/")
async def create_job_post(
    job_post_create: JobPostCreate,
    token: str = Header(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job_post = JobPosting(**job_post_create.dict(), user_id=current_user.id)
    db.add(job_post)
    db.commit()
    db.refresh(job_post)
    
    return job_post

@router.get("/job-posts/", response_model=List[ShowJobPost])
async def get_job_posts(
    token: str = Header(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job_posts = db.query(JobPosting).filter(JobPosting.user_id == current_user.id).all()
    return job_posts

@router.put("/job-posts/{job_post_id}")
async def update_job_post(
    job_post_id: int,
    job_post_update: JobPostCreate,
    token: str = Header(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job_post = db.query(JobPosting).filter(JobPosting.id == job_post_id).first()
    if not job_post:
        raise HTTPException(status_code=404, detail="Job post not found")
    if job_post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this job post")
    job_post.job_title = job_post_update.job_title
    db.commit()
    db.refresh(job_post)
    return job_post

@router.delete("/job-posts/{job_post_id}")
async def delete_job_post(
    job_post_id: int,
    token: str = Header(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job_post = db.query(JobPosting).filter(JobPosting.id == job_post_id).first()
    if not job_post:
        raise HTTPException(status_code=404, detail="Job post not found")
    if job_post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this job post")
    db.delete(job_post)
    db.commit()
    return {"message": "Job post deleted successfully"}
