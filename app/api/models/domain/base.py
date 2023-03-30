from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase
from sqlalchemy import TIMESTAMP, Column

from datetime import datetime


class Base(MappedAsDataclass, DeclarativeBase):
    created_at = Column(
        "created_at",
        TIMESTAMP(timezone=False),
        nullable=False,
        default=datetime.now().isoformat()
        )

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if not k.startswith('__')}
