from dataclasses import dataclass
from pprint import pprint

from adaptix import Retort, name_mapping


@dataclass
class Address:
    id: int
    street: str


@dataclass
class User:
    id: int
    name: str
    address: Address


@dataclass
class SomeClass:
    u_id: int
    u_name: str
    a_id: int
    a_street: str


data = {
    "u_id": 1,
    "u_name": "Alice",
    "a_id": 1,
    "a_street": "Street 1",
}
base_retort = Retort(recipe=[
    name_mapping(
        SomeClass,
        map={
            "a_id": ["address", "a_id"],
            "a_street": ["address", "a_street"],
        },
    ),
]
)
some_data = Retort().load(data, SomeClass)
pprint(some_data)
data2 = base_retort.dump(some_data)

retort = Retort(recipe=[
    name_mapping(
        User,
        map={
            "id": "u_id",
            "name": "u_name",
        }),
    name_mapping(
        Address,
        map={
            "id": "a_id",
            "street": "a_street",
        }),
])

user = retort.load(data2, User)
pprint(user)
