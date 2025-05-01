from dataclasses import dataclass
from pprint import pprint

from adaptix import P
from adaptix.conversion import get_converter, link_function, convert


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


@dataclass
class OutputDTO:
    users: list[UserDTO]
    user_ids: list[int]


@dataclass
class UserList:
    users: list[User]


convert_users_to_some_class = get_converter(
    UserList,
    OutputDTO,
    recipe=[
        link_function(
            lambda container: [convert(user, UserDTO) for user in container.users],
            P[OutputDTO].users
        ),
        link_function(
            lambda container: [user.id for user in container.users],
            P[OutputDTO].user_ids
        ),
    ],
)

users_container = UserList(
    users=[
        User(id=1, name="Alice", email="alice@example.com", address=Address("Street 1", "City A", "12345")),
        User(id=2, name="Bob", email="bob@example.com", address=Address("Street 2", "City B", "67890")),
    ]
)

some_class_instance = convert_users_to_some_class(users_container)

pprint(some_class_instance)
