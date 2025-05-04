import asyncio
from dataclasses import dataclass
from pprint import pprint

from adaptix import Retort, name_mapping, P, Provider
from sqlalchemy import ForeignKey, text
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


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
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionMaker = async_sessionmaker(engine, expire_on_commit=False)


def address_loader(row):
    print(row)
    return Address(
        id=row['a_id'],
        street=row['a_street'],
        city=row['a_city'],
        zip_code=row['a_zip_code']
    )


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
        stmt = text("""
            SELECT 
                u.id AS u_id, u.name AS u_name, u.email AS u_email, u.address_id AS u_address_id,
                a.id AS a_id, a.street AS a_street, a.city AS a_city, a.zip_code AS a_zip_code
            FROM users u
            JOIN addresses a ON u.address_id = a.id
        """)

        result = await session.execute(stmt)
        rows = result.mappings().all()

        def with_prefix(pred: type, prefix: str, extra_in: list[str] | None = None) -> Provider:
            if extra_in is None:
                extra_in = []

            def prefix_extender(shape, field):
                return prefix + '_' + field.id

            return name_mapping(
                pred,
                map=[(P.ANY, prefix_extender)], extra_in=extra_in
            )

        retort = Retort(recipe=[
            with_prefix(User, 'u', ["address"]),
            with_prefix(Address, 'a'),

        ])

        pprint(retort.load(rows, list[User]))


if __name__ == "__main__":
    asyncio.run(main())
