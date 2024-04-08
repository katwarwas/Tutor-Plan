from sqlalchemy import Column, Integer, String, Time, LargeBinary
from database import Base


class Teachers(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(LargeBinary, nullable=False)
    