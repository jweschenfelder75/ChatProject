from typing import NamedTuple


class Result(NamedTuple):
    text: str | None
    success: bool
