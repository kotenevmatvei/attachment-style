from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class TestYourself(Base):
    __tablename__ = "test_yourself"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime]
    q1: Mapped[float]
    q2: Mapped[float]
    q3: Mapped[float]
    q4: Mapped[float]
    q5: Mapped[float]
    q6: Mapped[float]
    q7: Mapped[float]
    q8: Mapped[float]
    q9: Mapped[float]
    q10: Mapped[float]
    q11: Mapped[float]
    q12: Mapped[float]
    q13: Mapped[float]
    q14: Mapped[float]
    q15: Mapped[float]
    q16: Mapped[float]
    q17: Mapped[float]
    q18: Mapped[float]
    q19: Mapped[float]
    q20: Mapped[float]
    q21: Mapped[float]
    q22: Mapped[float]
    q23: Mapped[float]
    q24: Mapped[float]
    q25: Mapped[float]
    q26: Mapped[float]
    q27: Mapped[float]
    q28: Mapped[float]
    q29: Mapped[float]
    q30: Mapped[float]
    q31: Mapped[float]
    q32: Mapped[float]
    q33: Mapped[float]
    q34: Mapped[float]
    q35: Mapped[float]
    q36: Mapped[float]
    q37: Mapped[float]
    q38: Mapped[float]
    q39: Mapped[float]
    q40: Mapped[float]
    q41: Mapped[float]
    q42: Mapped[float]
    