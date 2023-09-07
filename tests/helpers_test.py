import pytest

from baccarat.utils import Card
from baccarat.utils import create_card
from baccarat.utils import Suit
from baccarat.utils import Value


@pytest.mark.parametrize(
    "value, suit, expected",
    [
        (2, "hearts", Card(Value.TWO, Suit.HEARTS)),
        (3, "diamonds", Card(Value.THREE, Suit.DIAMONDS)),
        (4, "clubs", Card(Value.FOUR, Suit.CLUBS)),
        (5, "spades", Card(Value.FIVE, Suit.SPADES)),
        (6, "hearts", Card(Value.SIX, Suit.HEARTS)),
        (7, "diamonds", Card(Value.SEVEN, Suit.DIAMONDS)),
        (8, "clubs", Card(Value.EIGHT, Suit.CLUBS)),
        (9, "spades", Card(Value.NINE, Suit.SPADES)),
        (10, "hearts", Card(Value.TEN, Suit.HEARTS)),
        ("J", "diamonds", Card(Value.JACK, Suit.DIAMONDS)),
        ("Q", "clubs", Card(Value.QUEEN, Suit.CLUBS)),
        ("K", "spades", Card(Value.KING, Suit.SPADES)),
        ("A", "hearts", Card(Value.ACE, Suit.HEARTS)),
        ("A", "♦", Card(Value.ACE, Suit.DIAMONDS)),
        ("A", "♣", Card(Value.ACE, Suit.CLUBS)),
        ("A", "♠", Card(Value.ACE, Suit.SPADES)),
        ("A", "♥", Card(Value.ACE, Suit.HEARTS)),
    ],
)
def test_create_card(value, suit, expected):
    """Test the create card method."""
    assert create_card(value, suit) == expected


def test_create_card_invalid_value():
    """Test the create card method with an invalid value."""
    with pytest.raises(ValueError):
        create_card(1, "asdihasdin")
