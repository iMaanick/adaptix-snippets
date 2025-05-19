from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sqlalchemy_adaptix.models import Base
if TYPE_CHECKING:
    from .address import AddressTable

class UserTable(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    address: Mapped["AddressTable"] = relationship("AddressTable",
        back_populates="users",
    )
