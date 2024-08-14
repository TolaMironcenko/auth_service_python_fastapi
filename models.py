from sqlalchemy import Boolean, Column, Integer, String

from database import Base

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    group = Column(String, default="users")
    is_superuser = Column(Boolean, default=False)
    username = Column(String)
    
    def model_dump(self):
        return {
            "id": self.id, 
            "email": self.email, 
            "is_active": self.is_active, 
            "group": self.group, 
            "is_superuser": self.is_superuser, 
            "username": self.username
        }
