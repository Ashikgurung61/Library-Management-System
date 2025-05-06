from sqlalchemy import Column, String, DateTime, Enum
from database import Base
import enum

class RoleEnum(enum.Enum):
    student = "student"
    faculty = "faculty"
    admin = "admin"

class Users(Base):
    __tablename__ = "users"
    
    user_id = Column(String(20), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    phone = Column(String(15))
    role = Column(Enum(RoleEnum))
    registered_at = Column(DateTime)
    password = Column(String(25))
    
