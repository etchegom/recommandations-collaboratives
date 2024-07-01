from typing import Any


def dict_to_hash(data: dict[str, Any]) -> str:
    # TODO: test this trick
    return hash(frozenset(data.items()))
