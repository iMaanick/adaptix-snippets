from dataclasses import dataclass
from pprint import pprint

from adaptix import Retort, name_mapping, P, Provider


@dataclass
class Address:
    id: int
    street: str


@dataclass
class User:
    id: int
    name: str
    address: Address


data = {
    "u_id": 1,
    "u_name": "Alice",
    "a_id": 1,
    "a_street": "Street 1",
}


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

pprint(retort.load(data, User))
