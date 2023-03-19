from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.api.models.domain.base import Base

class Secret(Base):
    __tablename__ = "Secrets"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    content: Mapped[bytes] = mapped_column(init=False, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('Users.id'))