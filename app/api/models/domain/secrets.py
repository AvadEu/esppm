from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.api.models.domain.base import Base

class Secret(Base):
    __tablename__ = "Secrets"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    content: Mapped[bytes] = mapped_column(nullable=False)
    owner: Mapped[str] = mapped_column(ForeignKey('Users.username'))