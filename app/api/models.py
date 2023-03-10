from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column
from sqlalchemy.engine.base import Engine


# Base class declaration
class Base(MappedAsDataclass, DeclarativeBase):
    pass


# Model for application user account
class User(Base):
    __tablename__ = "Users"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(String(25), nullable=False)
    first_name: Mapped[str] = mapped_column(String(35), nullable=False)
    last_name: Mapped[str] = mapped_column(String(35), nullable=False)
    password_hash: Mapped[bytes] = mapped_column(nullable=False)


# Model for encrypted data record
class Record(Base):
    __tablename__ = "Records"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    service: Mapped[str] = mapped_column(String(50), nullable=False)
    login: Mapped[bytes] = mapped_column(nullable=False)
    password: Mapped[bytes] = mapped_column(nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('Users.id'))


# Model for user kdf function salt
class Secret(Base):
    __tablename__ = "Secrets"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    content: Mapped[bytes] = mapped_column(init=False, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('Users.id'))
