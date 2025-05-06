from sqlalchemy import Column, String
from database import Base

class User(Base):
    __tablename__ = "admin"
    username = Column(String(50), primary_key=True, index=True)
    password = Column(String(12), nullable=False)

    
if __name__ == "__main__":
    print("Defined columns:", User.__table__.columns.keys())
