from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import jwt

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/users/', response_model=schemas.User)
def create_user(token: str, user: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.User:
    if not crud.verify_token(db, token):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is not active")
    payload = crud.decode_token(token)
    if not payload.get("is_superuser"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not root")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user: 
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/api/register/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.User:
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(
    token: str, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
) -> list[schemas.User]:
    if not crud.verify_token(db, token):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is not active")
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)) -> schemas.User:
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/api/auth", response_model=schemas.User)
def auth_user(user: schemas.AuthUser, db: Session = Depends(get_db)) -> schemas.User:
    db_user = crud.get_user_by_email(db, user.email)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found")
    if not crud.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found")
    return db_user

@app.post("/api/token")
def get_token(user: schemas.AuthUser, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not crud.verify_password(user.password, db_user.hashed_password):
        return {"access": "reject"}
    jwt_token = crud.create_access_token(db_user)
    return {"token": jwt_token}

@app.post("/api/access")
def auth_by_token(token: str, db: Session = Depends(get_db)):
    if not crud.verify_token(db, token):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is not active")
    return {"access": "success"}

@app.post("/api/users/delete")
def delete_user(token: str, user_id: int = None, db: Session = Depends(get_db)):
    if not crud.verify_token(db, token):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is not active")
    if user_id is not None:
        payload = crud.decode_token(token)
        if payload.get("is_superuser"):
            if not crud.delete_user(db, user_id=user_id):
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Can't delete user")
            return {"status": "ok"}
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not root")
    payload = crud.decode_token(token)
    if not crud.delete_user(db, payload.get("id")):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Can't delete user")
    return {"status": "ok"}
        
                
        
