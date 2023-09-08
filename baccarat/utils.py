import random
from enum import Enum
from itertools import product
from typing import NamedTuple


class Suit(Enum):
    """A playing card suit."""

    SPADES = "♠"
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"


class Value(Enum):
    """A playing card value."""

    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"


class Card(NamedTuple):
    """A playing card."""

    value: Value
    suit: Suit

    def __repr__(self) -> str:
        return f"[{self.value.value}{self.suit.value}]"


class Deck:
    """A deck of cards."""

    def __init__(self) -> None:
        self.cards = [Card(value, suit) for value, suit in product(Value, Suit)]


class Shoe:
    """A shoe of cards - multiple decks together.

    :param decks: The number of decks to use
    """

    cards: list[Card]
    discards: list[Card]

    def __init__(self, decks: int = 8) -> None:
        self._decks = decks

        self.cards = []
        self.discards = []

        for _ in range(decks):
            self.cards.extend(Deck().cards)

    @property
    def num_decks(self) -> int:
        """The number of decks in the shoe."""
        return self._decks

    @property
    def num_cards(self) -> int:
        """The number of cards remaining in the shoe."""
        return len(self.cards)

    def shuffle(self) -> None:
        """Shuffle the shoe."""
        random.shuffle(self.cards)

    def deal(self) -> Card:
        """Deal a card from the shoe.

        :return: A card
        """
        card = self.cards.pop()
        self.discards.append(card)

        return card

    def reset(self) -> None:
        """Reset the shoe."""
        self.cards.extend(self.discards)
        self.discards = []
        self.shuffle()


def create_card(value: int | str, suit: str) -> Card:
    """Create a card from primitive types."""

    if len(suit) > 1:
        if suit.lower() == "spades":
            suit = "♠"
        elif suit.lower() == "hearts":
            suit = "♥"
        elif suit.lower() == "diamonds":
            suit = "♦"
        elif suit.lower() == "clubs":
            suit = "♣"
        else:
            raise ValueError("Invalid suit")

    value_ = Value(value)
    suit_ = Suit(suit)

    return Card(value_, suit_)
