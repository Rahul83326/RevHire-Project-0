from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .schemas import User, UserRoleEnum, TokenData
from .database import SessionLocal, get_db
from .models import UserDB
from jose import jwt, JWTError
from .token import SECRET_KEY, ALGORITHM

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: Annotated[str, Depends(oauth2_schema)], db: SessionLocal = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: UserRoleEnum = UserRoleEnum(payload.get("role"))
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception
    user = db.query(UserDB).filter(UserDB.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return User(id=user.id, username=user.username, email=user.email, role=user.role, fullname=user.fullname, phonenumber=user.phonenumber, address=user.address)

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
    role: UserRoleEnum
):
    if current_user.role != role:
        raise HTTPException(status_code=403, detail="Permission denied")
    return current_user