"""
Test the game items.

Test the card class, the shoe class, and the hand class
"""
import pytest

from baccarat.game import BaccaratHand
from baccarat.utils import Card
from baccarat.utils import Shoe
from baccarat.utils import Suit
from baccarat.utils import Value


@pytest.fixture
def card():
    """A card fixture."""
    return Card(suit=Suit.SPADES, value=Value.ACE)


@pytest.fixture
def shoe():
    """A shoe fixture."""
    return Shoe(decks=1)


@pytest.fixture
def hand():
    """A hand fixture."""
    return BaccaratHand()


def test_card(card):
    """Test the card class."""
    assert card.suit is Suit.SPADES
    assert card.value is Value.ACE
    assert card.__repr__() == "[A♠]"


def test_shoe(shoe):
    """Test the shoe class."""
    assert shoe.num_cards == 52
    assert shoe.num_decks == 1

    shoe.shuffle()
    assert shoe.num_cards == 52
    assert len(shoe.discards) == 0

    shoe.deal()
    assert shoe.num_cards == 51
    assert len(shoe.discards) == 1

    shoe.reset()
    assert shoe.num_cards == 52
    assert len(shoe.discards) == 0


def test_hand(hand):
    assert hand.cards == []

    card1 = Card(suit=Suit.SPADES, value=Value.ACE)
    hand.cards.append(card1)

    assert hand.num_cards == 1
    assert hand.total == 1

    card2 = Card(suit=Suit.SPADES, value=Value.TWO)
    hand.cards.append(card2)

    assert hand.num_cards == 2
    assert hand.total == 3

    card1_repr = card1.__repr__()
    card2_repr = card2.__repr__()
    assert hand.__repr__() == f"BaccaratHand(total=3, cards=[{card1_repr}, {card2_repr}])"


def test_hand_add_card(hand):
    """Test adding a card to a hand."""
    assert hand.cards == []

    card1 = Card(suit=Suit.SPADES, value=Value.ACE)
    hand.add_card(card1)

    assert hand.num_cards == 1
    assert hand.total == 1

    card2 = Card(suit=Suit.SPADES, value=Value.TWO)
    hand.add_card(card2)

    assert hand.num_cards == 2
    assert hand.total == 3


def test_hand_third_card(hand):
    """Test the third card property."""
    assert hand.third_card is None

    card = Card(suit=Suit.SPADES, value=Value.ACE)
    hand.cards.append(card)

    assert hand.third_card is None

    card = Card(suit=Suit.SPADES, value=Value.TWO)
    hand.cards.append(card)

    assert hand.third_card is None

    card = Card(suit=Suit.SPADES, value=Value.THREE)
    hand.cards.append(card)

    assert hand.third_card is card


def test_hand_total(hand):
    """Test the hand total."""

    card1 = Card(suit=Suit.SPADES, value=Value.ACE)
    card2 = Card(suit=Suit.SPADES, value=Value.TWO)

    hand.cards.append(card1)
    hand.cards.append(card2)

    assert hand.total == 3

    card3 = Card(suit=Suit.SPADES, value=Value.THREE)
    hand.cards.append(card3)

    assert hand.total == 6

    card4 = Card(suit=Suit.SPADES, value=Value.FOUR)
    hand.cards.append(card4)

    assert hand.total == 0


def test_hand_is_natural(hand):
    """Test the is_natural property."""
    card1 = Card(suit=Suit.SPADES, value=Value.ACE)
    card2 = Card(suit=Suit.SPADES, value=Value.TWO)

    hand.cards.append(card1)
    hand.cards.append(card2)

    assert hand.is_natural is False

    card3 = Card(suit=Suit.SPADES, value=Value.SEVEN)
    hand.cards.append(card3)

    assert hand.is_natural is False

    card4 = Card(suit=Suit.SPADES, value=Value.EIGHT)
    card5 = Card(suit=Suit.SPADES, value=Value.NINE)
    card6 = Card(suit=Suit.SPADES, value=Value.TEN)

    hand.cards = [card4, card6]
    assert hand.is_natural is True

    hand.cards = [card5, card6]
    assert hand.is_natural is True
