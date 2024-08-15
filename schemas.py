from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    username: str
    group: str
    
class UserCreate(UserBase):
    password: str
    is_superuser: bool
    
class UserRegister(UserBase):
    password: str
    
class AuthUser(BaseModel):
    email: str
    password: str
    
class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
        
class Token(BaseModel):
    token: str
