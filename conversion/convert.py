from dataclasses import dataclass

from adaptix import conversion


# Все дополнительные поля исходной модели, не найденные в целевой модели, просто игнорируются.


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


@dataclass
class UserDTO:
    name: str
    email: str
    address: AddressDTO


user = User(
    id=1,
    name="MNK",
    email="MNK@mail.ru",
    address=Address("Арсенальная ул., 9", "Санкт-Петербург", "195009")
)

user_dto = conversion.convert(user, UserDTO)

assert user_dto == UserDTO(
    name="MNK",
    email="MNK@mail.ru",
    address=AddressDTO(street="Арсенальная ул., 9", city="Санкт-Петербург")
)

print(user_dto)
