from typing import NamedTuple

"""
Stores a result with a text message and if the result was successful or not.
"""


class Result(NamedTuple):
    text: str | None
    success: bool
