import re
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional


class Base(DeclarativeBase):
    pass


class AssessYourself(Base):
    __tablename__ = "assess_yourself"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime]
    test: Mapped[bool]

    age: Mapped[int]
    relationship_status: Mapped[str]
    gender: Mapped[str]
    therapy_experience: Mapped[str]

    anxious_q1: Mapped[Optional[int]]
    anxious_q2: Mapped[Optional[int]]
    anxious_q3: Mapped[Optional[int]]
    anxious_q4: Mapped[Optional[int]]
    anxious_q5: Mapped[Optional[int]]
    anxious_q6: Mapped[Optional[int]]
    anxious_q7: Mapped[Optional[int]]
    anxious_q8: Mapped[Optional[int]]
    anxious_q9: Mapped[Optional[int]]
    anxious_q10: Mapped[Optional[int]]
    anxious_q11: Mapped[Optional[int]]
    anxious_q12: Mapped[Optional[int]]
    anxious_q13: Mapped[Optional[int]]
    anxious_q14: Mapped[Optional[int]]
    anxious_q15: Mapped[Optional[int]]
    anxious_q16: Mapped[Optional[int]]
    anxious_q17: Mapped[Optional[int]]
    anxious_q18: Mapped[Optional[int]]

    avoidant_q1: Mapped[Optional[int]]
    avoidant_q2: Mapped[Optional[int]]
    avoidant_q3: Mapped[Optional[int]]
    avoidant_q4: Mapped[Optional[int]]
    avoidant_q5: Mapped[Optional[int]]
    avoidant_q6: Mapped[Optional[int]]
    avoidant_q7: Mapped[Optional[int]]
    avoidant_q8: Mapped[Optional[int]]
    avoidant_q9: Mapped[Optional[int]]
    avoidant_q10: Mapped[Optional[int]]
    avoidant_q11: Mapped[Optional[int]]
    avoidant_q12: Mapped[Optional[int]]
    avoidant_q13: Mapped[Optional[int]]
    avoidant_q14: Mapped[Optional[int]]
    avoidant_q15: Mapped[Optional[int]]
    avoidant_q16: Mapped[Optional[int]]
    avoidant_q17: Mapped[Optional[int]]
    avoidant_q18: Mapped[Optional[int]]

    anxious_score: Mapped[Optional[float]]
    avoidant_score: Mapped[Optional[float]]
    secure_score: Mapped[Optional[float]]


class AssessOthers(Base):
    __tablename__ = "assess_others"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime]
    test: Mapped[bool]

    age: Mapped[int]
    relationship_status: Mapped[str]
    gender: Mapped[str]
    therapy_experience: Mapped[str]
    
    anxious_q1: Mapped[Optional[int]]
    anxious_q2: Mapped[Optional[int]]
    anxious_q3: Mapped[Optional[int]]
    anxious_q4: Mapped[Optional[int]]
    anxious_q5: Mapped[Optional[int]]
    anxious_q6: Mapped[Optional[int]]
    anxious_q7: Mapped[Optional[int]]
    anxious_q8: Mapped[Optional[int]]
    anxious_q9: Mapped[Optional[int]]
    anxious_q10: Mapped[Optional[int]]
    anxious_q11: Mapped[Optional[int]]

    secure_q1: Mapped[Optional[int]]
    secure_q2: Mapped[Optional[int]]
    secure_q3: Mapped[Optional[int]]
    secure_q4: Mapped[Optional[int]]
    secure_q5: Mapped[Optional[int]]
    secure_q6: Mapped[Optional[int]]
    secure_q7: Mapped[Optional[int]]
    secure_q8: Mapped[Optional[int]]
    secure_q9: Mapped[Optional[int]]
    secure_q10: Mapped[Optional[int]]
    secure_q11: Mapped[Optional[int]]

    avoidant_q1: Mapped[Optional[int]]
    avoidant_q2: Mapped[Optional[int]]
    avoidant_q3: Mapped[Optional[int]]
    avoidant_q4: Mapped[Optional[int]]
    avoidant_q5: Mapped[Optional[int]]
    avoidant_q6: Mapped[Optional[int]]
    avoidant_q7: Mapped[Optional[int]]
    avoidant_q8: Mapped[Optional[int]]
    avoidant_q9: Mapped[Optional[int]]
    avoidant_q10: Mapped[Optional[int]]
    avoidant_q11: Mapped[Optional[int]]

    anxious_score: Mapped[Optional[float]]
    avoidant_score: Mapped[Optional[float]]
    secure_score: Mapped[Optional[float]]
