import asyncio
from dataclasses import dataclass
from pprint import pprint
from typing import Sequence

from adaptix._internal.conversion.facade.func import get_converter
from sqlalchemy import ForeignKey
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, selectinload


@dataclass
class Address:
    id: int
    street: str
    city: str
    zip_code: str


@dataclass
class User:
    id: int
    name: str
    email: str
    address: Address


@dataclass
class AddressDTO:
    street: str
    city: str


@dataclass
class UserDTO:
    name: str
    email: str
    address: AddressDTO


class Base(DeclarativeBase):
    pass


class AddressTable(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    street: Mapped[str]
    city: Mapped[str]
    zip_code: Mapped[str]
    users: Mapped[list["UserTable"]] = relationship(
        back_populates="address",
        cascade="all, delete-orphan",
    )


class UserTable(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    address: Mapped[AddressTable] = relationship(
        back_populates="users",
    )


DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionMaker = async_sessionmaker(engine, expire_on_commit=False)


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionMaker() as session:
        address1 = AddressTable(street="Street 1", city="City A", zip_code="12345")
        address2 = AddressTable(street="Street 2", city="City B", zip_code="67890")
        session.add_all([address1, address2])
        await session.flush()

        user1 = UserTable(name="Alice", email="alice@example.com", address_id=address1.id)
        user2 = UserTable(name="Bob", email="bob@example.com", address_id=address2.id)
        session.add_all([user1, user2])
        await session.commit()

    async with AsyncSessionMaker() as session:
        stmt = select(UserTable).options(selectinload(UserTable.address))
        result = await session.scalars(stmt)
        user_models: Sequence[UserTable] = result.all()
        converter = get_converter(Sequence[UserTable], list[UserDTO])
        users = converter(user_models)
        pprint(users)


if __name__ == "__main__":
    asyncio.run(main())
