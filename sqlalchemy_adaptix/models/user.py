from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sqlalchemy_adaptix.models import Base


class UserTable(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    address = relationship("AddressTable",
        back_populates="users",
    )
