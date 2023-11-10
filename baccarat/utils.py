import random
from enum import Enum
from itertools import product
from typing import NamedTuple


class Suit(Enum):
    """A playing card suit."""

    ...


class Value(Enum):
    """A playing card value."""

    ...


class Card(NamedTuple):
    """A playing card."""

    value: Value
    suit: Suit

    def __repr__(self) -> str:
        return f"[{self.value.value}{self.suit.value}]"


class Deck:
    """A deck of cards."""

    def __init__(self) -> None:
        ...


class Shoe:
    """A shoe of cards - multiple decks together.

    :param decks: The number of decks to use
    """

    cards: list[Card]
    discards: list[Card]

    def __init__(self, decks: int = 8) -> None:
        ...

    @property
    def num_decks(self) -> int:
        """The number of decks in the shoe."""
        ...

    @property
    def num_cards(self) -> int:
        """The number of cards remaining in the shoe."""
        ...

    def shuffle(self) -> None:
        """Shuffle the shoe."""
        ...

    def deal(self) -> Card:
        """Deal a card from the shoe.

        :return: A card
        """
        ...

    def reset(self) -> None:
        """Reset the shoe."""
        ...


def create_card(value: int | str, suit: str) -> Card:
    """Create a card from primitive types."""

    ...
