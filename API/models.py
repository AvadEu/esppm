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


# Creates database schema and returns engine 
def init_all(conf: dict) -> Engine:
    """
    Function takes one argument: dictionary with keys [username, password, host, db_name] to connect to
    postgres database using psycopg2 connector. It build entire database schema declared in
    models.py file and returns sqlalchemy.engine.base.Engine object of that database.
    """
    # engine = create_engine(f"postgresql+psycopg2://{conf['username']}:{conf['password']}@{conf['host']}/{conf['db_name']}", echo=True)
    engine = create_engine("postgresql+psycopg2://tutorial:tutorial@localhost/test", echo=True)
    Base.metadata.create_all(bind=engine, checkfirst=True)
    return engine