from dataclasses import dataclass

from adaptix import P
from adaptix.conversion import get_converter, link


@dataclass
class Address:
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
    zip_code: str


@dataclass
class UserDTO:
    id: int
    username: str  # соответствует User.name
    email: str
    address: AddressDTO


# Связываем name (User) → username (UserDTO)
convert_user_to_dto = get_converter(
    src=User,
    dst=UserDTO,
    recipe=[link(P[User].name, P[UserDTO].username)],
)

user = User(
    id=1,
    name="MNK",
    email="mnk@mail.ru",
    address=Address("Арсенальная ул., 9", "СПб", "195009"),
)

expected = UserDTO(
    id=1,
    username="MNK",
    email="mnk@mail.ru",
    address=AddressDTO("Арсенальная ул., 9", "СПб", "195009"),
)

assert convert_user_to_dto(user) == expected

print(convert_user_to_dto(user))
