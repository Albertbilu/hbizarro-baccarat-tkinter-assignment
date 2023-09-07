"""Test the draw card method works for each scenario."""
import pytest

from baccarat.game import BaccaratHand
from baccarat.game import do_banker_draw
from baccarat.game import do_player_draw
from baccarat.game import does_banker_draw
from baccarat.game import does_player_draw
from baccarat.utils import Card
from baccarat.utils import create_card
from baccarat.utils import Shoe

ALL_TRUE = [True] * 10
ALL_FALSE = [False] * 10
T = True
F = False


@pytest.fixture()
def low_hand():
    """Create a hand with a low value."""
    hand = BaccaratHand()
    hand.add_card(create_card(2, "♠"))
    hand.add_card(create_card(2, "♠"))
    return hand


@pytest.fixture()
def high_hand():
    """Create a hand with a high value."""
    hand = BaccaratHand()
    hand.add_card(create_card(6, "♠"))
    hand.add_card(create_card(2, "♠"))
    return hand


@pytest.fixture()
def shoe():
    """Create a shoe with 10 spades."""
    return Shoe(decks=1)


def make_spade(value: int | str) -> Card:
    """Create a spade card with the given value."""
    return create_card(value, "♠")


def make_stand_range(banker: int, actions: list[bool]) -> list[tuple[int, Card, bool]]:
    """Create a list of scenarios where the banker stands."""
    values = (1, 2, 3, 4, 5, 6, 7, 8, 9, 0)
    return [(banker, player_value, action) for player_value, action in zip(values, actions)]


@pytest.mark.parametrize(
    "player_total, expected",
    [(t, True) for t in range(0, 6)] + [(t, False) for t in range(6, 10)],
)
def test_when_player_draws_third_card(player_total, expected):
    """Test the draw card method works for each scenario."""
    assert does_player_draw(player_total) == expected


@pytest.mark.parametrize(
    "banker_total, expected",
    [(t, True) for t in range(0, 6)] + [(t, False) for t in range(6, 10)],
)
def test_banker_draws_when_player_did_not_draw(banker_total, expected):
    """Test the draw card method works for each scenario."""
    assert does_banker_draw(banker_total, None) == expected


@pytest.mark.parametrize(
    "banker_total, player_third_card, expected",
    [
        *make_stand_range(0, ALL_TRUE),
        *make_stand_range(1, ALL_TRUE),
        *make_stand_range(2, ALL_TRUE),
        *make_stand_range(3, [T, T, T, T, T, T, T, F, T, T]),
        *make_stand_range(4, [F, T, T, T, T, T, T, F, F, F]),
        *make_stand_range(5, [F, F, F, T, T, T, T, F, F, F]),
        *make_stand_range(6, [F, F, F, F, F, T, T, F, F, F]),
        *make_stand_range(7, ALL_FALSE),
        *make_stand_range(8, ALL_FALSE),
        *make_stand_range(9, ALL_FALSE),
    ],
)
def test_banker_draw_when_player_did_draw(banker_total, player_third_card, expected):
    """Test the draw card method works for each scenario."""
    assert does_banker_draw(banker_total, player_third_card) == expected


def test_player_draws_with_low_hand(low_hand, shoe):
    """Test the draw card method works for each scenario."""
    assert low_hand.num_cards == 2
    do_player_draw(low_hand, shoe)
    assert low_hand.num_cards == 3


def test_player_does_not_draw_with_high_hand(high_hand, shoe):
    """Test the draw card method works for each scenario."""
    assert high_hand.num_cards == 2
    do_player_draw(high_hand, shoe)
    assert high_hand.num_cards == 2


def test_banker_draws_with_low_hand_because_player_did_not_draw(low_hand, shoe):
    """Test the draw card method works for each scenario."""

    banker = low_hand
    player = BaccaratHand()
    player.add_card(create_card(2, "♠"))
    player.add_card(create_card(2, "♠"))

    assert banker.num_cards == 2
    do_banker_draw(banker, player, shoe)
    assert banker.num_cards == 3


def test_banker_does_not_draw_with_high_hand_because_player_did_not_draw(high_hand, shoe):
    """Test the draw card method works for each scenario."""

    banker = high_hand
    player = BaccaratHand()
    player.add_card(create_card(2, "♠"))
    player.add_card(create_card(2, "♠"))

    assert banker.num_cards == 2
    do_banker_draw(banker, player, shoe)
    assert banker.num_cards == 2
