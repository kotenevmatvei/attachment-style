import re
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TestYourself(Base):
    __tablename__ = "test_yourself"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime]
    test: Mapped[bool]
    age: Mapped[int]
    relationship_status: Mapped[str]
    gender: Mapped[str]
    therapy_experience: Mapped[str]
    anxious_q1: Mapped[int]
    anxious_q2: Mapped[int]
    anxious_q3: Mapped[int]
    anxious_q4: Mapped[int]
    anxious_q5: Mapped[int]
    anxious_q6: Mapped[int]
    anxious_q7: Mapped[int]
    anxious_q8: Mapped[int]
    anxious_q9: Mapped[int]
    anxious_q10: Mapped[int]
    anxious_q11: Mapped[int]
    anxious_q12: Mapped[int]
    anxious_q13: Mapped[int]
    anxious_q14: Mapped[int]
    secure_q15: Mapped[int]
    secure_q16: Mapped[int]
    secure_q17: Mapped[int]
    secure_q18: Mapped[int]
    secure_q19: Mapped[int]
    secure_q20: Mapped[int]
    secure_q21: Mapped[int]
    secure_q22: Mapped[int]
    secure_q23: Mapped[int]
    secure_q24: Mapped[int]
    secure_q25: Mapped[int]
    secure_q26: Mapped[int]
    secure_q27: Mapped[int]
    secure_q28: Mapped[int]
    avoidant_q29: Mapped[int]
    avoidant_q30: Mapped[int]
    avoidant_q31: Mapped[int]
    avoidant_q32: Mapped[int]
    avoidant_q33: Mapped[int]
    avoidant_q34: Mapped[int]
    avoidant_q35: Mapped[int]
    avoidant_q36: Mapped[int]
    avoidant_q37: Mapped[int]
    avoidant_q38: Mapped[int]
    avoidant_q39: Mapped[int]
    avoidant_q40: Mapped[int]
    avoidant_q41: Mapped[int]
    avoidant_q42: Mapped[int]


class TestYourPartner(Base):
    __tablename__ = "test_your_partner"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime]
    test: Mapped[bool]
    age: Mapped[int]
    relationship_status: Mapped[str]
    gender: Mapped[str]
    therapy_experience: Mapped[str]
    anxious_q1: Mapped[int]
    anxious_q2: Mapped[int]
    anxious_q3: Mapped[int]
    anxious_q4: Mapped[int]
    anxious_q5: Mapped[int]
    anxious_q6: Mapped[int]
    anxious_q7: Mapped[int]
    anxious_q8: Mapped[int]
    anxious_q9: Mapped[int]
    anxious_q10: Mapped[int]
    anxious_q11: Mapped[int]
    secure_q12: Mapped[int]
    secure_q13: Mapped[int]
    secure_q14: Mapped[int]
    secure_q15: Mapped[int]
    secure_q16: Mapped[int]
    secure_q17: Mapped[int]
    secure_q18: Mapped[int]
    secure_q19: Mapped[int]
    secure_q20: Mapped[int]
    secure_q21: Mapped[int]
    secure_q22: Mapped[int]
    avoidant_q23: Mapped[int]
    avoidant_q24: Mapped[int]
    avoidant_q25: Mapped[int]
    avoidant_q26: Mapped[int]
    avoidant_q27: Mapped[int]
    avoidant_q28: Mapped[int]
    avoidant_q29: Mapped[int]
    avoidant_q30: Mapped[int]
    avoidant_q31: Mapped[int]
    avoidant_q32: Mapped[int]
    avoidant_q33: Mapped[int]
