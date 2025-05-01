from dataclasses import dataclass

from adaptix import P
from adaptix.conversion import impl_converter, from_param, link


# По умолчанию дополнительные параметры могут заменять поля только в модели верхнего уровня.
# Если вы хотите передать эти данные во вложенную модель, вам следует использовать conversion.from_param фабрику предикатов.

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


# Передаём дополнительные postal_code и id в сигнатуре
@impl_converter(recipe=[
    link(from_param("postal_code"), P[Address].zip_code)
])
def convert_user(dto: UserDTO, id: int, postal_code: str) -> User:
    ...


# Пример использования
user_dto = UserDTO(
    name="MNK",
    email="mnk@mail.ru",
    address=AddressDTO("Арсенальная ул., 9", "СПб")
)

user = convert_user(user_dto, id=1, postal_code="195009")

expected = User(
    id=1,
    name="MNK",
    email="mnk@mail.ru",
    address=Address(
        street="Арсенальная ул., 9",
        city="СПб",
        zip_code="195009",
    )
)

assert user == expected, f"Expected {expected}, got {user}"

print(user)
