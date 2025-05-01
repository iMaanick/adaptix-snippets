from dataclasses import dataclass

from adaptix import P
from adaptix.conversion import get_converter, link, coercer


# для приведения одного типа к другому используется coercer,
# но link имеет более высокий приоритет над общими преобразованиями

@dataclass
class Address:
    street: str
    city: str
    code: int  # Тип code: int


@dataclass
class User:
    id: int  # Тип id: int
    age: int
    name: str
    email: str
    address: Address


@dataclass
class AddressDTO:
    street: str
    city: str
    zip_code: str  # Тип zip_code: str


@dataclass
class UserDTO:
    id: str  # Тип id: str
    age: str
    name: str
    email: str
    address: AddressDTO


# Преобразование всех int полей в str, но link имеет более высокий приоритет над общими преобразованиями
convert_user_to_dto = get_converter(
    src=User,
    dst=UserDTO,
    recipe=[
        link(P[User].address.code, P[AddressDTO].zip_code, coercer=lambda x: "zip_code: " + str(x)),
        coercer(int, str, func=str)
    ],
)

user = User(
    id=1,
    age=18,
    name="MNK",
    email="mnk@mail.ru",
    address=Address(street="Арсенальная ул., 9", city="СПб", code=195009)
)

# Ожидаемый результат
expected = UserDTO(
    id="1",
    age="18",
    name="MNK",
    email="mnk@mail.ru",
    address=AddressDTO(street="Арсенальная ул., 9", city="СПб", zip_code="zip_code: 195009")
)

# Преобразуем и сравниваем
user_dto = convert_user_to_dto(user)
assert user_dto == expected

print(user_dto)
