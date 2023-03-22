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
