from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey

from app.api.models.domain.base import Base


class Record(Base):
    __tablename__ = "Records"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    service: Mapped[str] = mapped_column(String(50), nullable=False)
    login: Mapped[bytes] = mapped_column(nullable=False)
    password: Mapped[bytes] = mapped_column(nullable=False)
    iv: Mapped[bytes] = mapped_column(nullable=False)
    owner: Mapped[str] = mapped_column(ForeignKey('Users.username'))
