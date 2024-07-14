from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    name: Mapped[str] = mapped_column(primary_key=True)