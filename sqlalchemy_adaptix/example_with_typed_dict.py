from dataclasses import dataclass
from pprint import pprint
from typing import TypedDict

from adaptix import P
from adaptix._internal.conversion.facade.provider import link
from adaptix.conversion import get_converter, link_function


@dataclass
class Address:
    id: int
    street: str


@dataclass
class User:
    id: int
    name: str
    address: Address


class SomeClass(TypedDict):
    u_id: int
    u_name: str
    a_id: int
    a_street: str


data = [
    SomeClass(u_id=1, u_name="Alice", a_id=1, a_street="Street 1"),
    SomeClass(u_id=2, u_name="Bob", a_id=2, a_street="Street 2"),
]

converter = get_converter(
    list[SomeClass],
    list[User],
    recipe=[
        link(P[SomeClass].u_id, P[User].id),
        link(P[SomeClass].u_name, P[User].name),
        link_function(lambda data: Address(data.get("a_id"), data.get("a_street")), P[User].address),
    ],

)

output = converter(data)

pprint(output)
