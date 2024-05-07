from ..schemas import User, UserRoleEnum, Token, UserCreate
from fastapi.security import OAuth2PasswordRequestForm
from ..token import authenticate_user, create_access_token
from ..models import UserDB
from ..database import SessionLocal, get_db
from ..hashing import get_password_hash
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from ..token import ACCESS_TOKEN_EXPIRE_MINUTES
from ..oauth2 import get_current_active_user

router = APIRouter(
    tags=["Users"],
)

def get_user_by_username(db, username: str):
    return db.query(UserDB).filter(UserDB.username == username).first()

def get_user_by_email(db, email: str):
    return db.query(UserDB).filter(UserDB.email == email).first()

def create_user(db, username: str, email: str, password: str, fullname: str, phonenumber: int, address: str,role: UserRoleEnum):
    hashed_password = get_password_hash(password)
    db_user = UserDB(
        username=username,
        email=email,
        hashed_password=hashed_password,
        role=role,
        fullname=fullname,
        phonenumber=phonenumber,
        address=address
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: SessionLocal = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register/{role}/", response_model=User)
async def register_user(role: UserRoleEnum, user_data: UserCreate, db: SessionLocal = Depends(get_db)):
    existing_user_username = get_user_by_username(db, user_data.username)
    if existing_user_username:
        raise HTTPException(status_code=400, detail="Username already registered")
    existing_user_email = get_user_by_email(db, user_data.email)
    if existing_user_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    created_user = create_user(db, user_data.username, user_data.email, user_data.password, user_data.fullname, user_data.phonenumber, user_data.address,role)
    return created_user

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    try:
        return current_user
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/me", response_model=User)
async def update_user_me(user_data: UserCreate, current_user: User = Depends(get_current_active_user), db: SessionLocal = Depends(get_db)):
    try:
        user = get_user_by_username(db, current_user.username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Update user data
        user.username = user_data.username
        user.email = user_data.email
        user.hashed_password = get_password_hash(user_data.password)
        
        db.commit()
        db.refresh(user)
        
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


