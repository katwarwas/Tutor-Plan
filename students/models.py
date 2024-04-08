from sqlalchemy import Column, Integer, String, Time, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy_utils import ChoiceType
from enum import Enum 

class DayEnum(Enum):
    monday = "Poniedziałek"
    tuesday = "Wtorek"
    wednesday = "Środa"
    thursday = "Czwartek"
    friday = "Piątek"

class Level(Enum):
    sp5 = "szkoła podstawowa 5 klasa"
    sp6 = "szkoła podstawowa 6 klasa"
    sp7 = "szkoła podstawowa 7 klasa"
    sp8 = "szkoła podstawowa 8 klasa"
    lo1 = "liceum 1 klasa"
    lo2 = "liceum 2 klasa"
    lo3 = "liceum 3 klasa"
    lo4 = "liceum 4 klasa"
    t1 = "technikum 1 klasa"
    t2 = "technikum 2 klasa"
    t3 = "technikum 3 klasa"
    t4 = "technikum 4 klasa"
    t5 = "technikum 5 klasa"
    

class ClassTime(Enum):
    t1 = "30 min"
    t2 = "45 min"
    t3 = "1 h"
    t5 = "1h 30 min"

class Students(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    level = Column(ChoiceType(Level), nullable=False)
    time = Column(Time(timezone=True), nullable=False)
    time2 = Column(ChoiceType(ClassTime), nullable=False, default = "1 h")
    day = Column(ChoiceType(DayEnum), nullable=False)
    price = Column(Integer, nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False, default=1)

    teacher = relationship("Teachers", foreign_keys=[teacher_id])

