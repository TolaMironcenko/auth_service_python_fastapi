from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import timedelta, timezone, datetime
import jwt

import models, schemas

SECRET_KEY="develop_secret_key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_token(db: Session, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")
        if user_id is None:
            return False
        db_user = get_user(db, user_id=user_id)
        if db_user is None:
            return False
        return True
    except:
        return False

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def create_access_token(data: schemas.User, expires_delta: timedelta | None = None):
    to_encode = data.model_dump()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def get_user(db: Session, user_id: int) -> schemas.User:
    return db.query(models.UserModel).filter(models.UserModel.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> schemas.User:
    return db.query(models.UserModel).filter(models.UserModel.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[schemas.User]:
    return db.query(models.UserModel).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate) -> schemas.User:
    hashed_password = hash_password(user.password)
    db_user = models.UserModel(
        email=user.email, 
        hashed_password=hashed_password,
        group=user.group,
        is_superuser=user.is_superuser,
        username=user.username
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return True
    
