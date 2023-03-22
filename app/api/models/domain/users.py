from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from app.api.models.domain.base import Base


class User(Base):
    __tablename__ = "Users"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(String(25), nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String(35), nullable=False)
    last_name: Mapped[str] = mapped_column(String(35), nullable=False)
    password_hash: Mapped[bytes] = mapped_column(nullable=False)

    def get_token_payload(self):
        return {
            'username': self.username,
            'fist_name': self.first_name,
            'last_name': self.last_name
        }
