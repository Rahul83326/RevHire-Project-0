from fastapi import APIRouter, Depends, Header, HTTPException
from ..schemas import  JobApplicationCreate, User, showJobApplication
from ..database import SessionLocal, get_db
from ..models import JobApplication
from ..oauth2 import get_current_user
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    tags=["Job Applications"],
)

@router.post("/job-applications/")
async def create_job_application(
    job_application_create: JobApplicationCreate,  
    token: str = Header(...),  
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job_application = JobApplication(**job_application_create.dict(), user_id=current_user.id)
    db.add(job_application)
    db.commit()
    db.refresh(job_application)
    
    return job_application

@router.get("/job-applications/", response_model=List[showJobApplication])
async def get_job_applications(
    token: str = Header(...),  
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job_applications = db.query(JobApplication).filter(JobApplication.user_id == current_user.id).all()
    return job_applications

@router.put("/job-applications/{job_application_id}")
async def update_job_application(
    job_application_id: int,
    job_application_update: JobApplicationCreate,
    token: str = Header(...),  
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job_application = db.query(JobApplication).filter(JobApplication.id == job_application_id).first()
    if not job_application:
        raise HTTPException(status_code=404, detail="Job application not found")
    if job_application.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this job application")
    job_application.job_title = job_application_update.job_title
    db.commit()
    db.refresh(job_application)
    return job_application

@router.delete("/job-applications/{job_application_id}")
async def delete_job_application(
    job_application_id: int,
    token: str = Header(...),  
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job_application = db.query(JobApplication).filter(JobApplication.id == job_application_id).first()
    if not job_application:
        raise HTTPException(status_code=404, detail="Job application not found")
    if job_application.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this job application")
    db.delete(job_application)
    db.commit()
    return {"message": "Job application deleted successfully"}