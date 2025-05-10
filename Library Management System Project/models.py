from sqlalchemy import Column, String, Enum, DateTime
from database import Base
import enum

class RoleEnum(enum.Enum):
    student = "student"
    faculty = "faculty"
    admin = "admin"

class StudentID(Base):
    __tablename__ = "users"
    
    user_id = Column(String(20), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    phone = Column(String(15))
    role = Column(Enum(RoleEnum))
    registered_at = Column(DateTime)
    password = Column(String(25))

class User(Base):
    __tablename__ = "admin"
    username = Column(String(50), primary_key=True, index=True)
    password = Column(String(12), nullable=False)

    
if __name__ == "__main__":
    print("Defined columns:", User.__table__.columns.keys())