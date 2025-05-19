from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from sqlalchemy_adaptix.models import Base
if TYPE_CHECKING:
    from .user import UserTable

class AddressTable(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    street: Mapped[str]
    city: Mapped[str]
    zip_code: Mapped[str]
    users: Mapped["UserTable"] = relationship("UserTable",
        back_populates="address",
        cascade="all, delete-orphan",
    )
