import pytest

from baccarat.game import BetResult
from baccarat.game import Player


@pytest.fixture()
def player():
    return Player(100)


def test_player_create(player):
    assert player.bankroll == 100


def test_player_make_bet(player):
    bet = player.make_bet(10, BetResult.PLAYER)
    assert bet.amount == 10
    assert bet.result == BetResult.PLAYER
    assert player.bankroll == 90


def test_player_make_bet_invalid_amount(player):
    with pytest.raises(ValueError):
        player.make_bet(101, BetResult.PLAYER)


def test_player_win_bet(player):
    player.win_bet(10)
    assert player.bankroll == 110
