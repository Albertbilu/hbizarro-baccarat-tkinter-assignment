"""Test the overall game logic."""
import pytest

from baccarat.game import BaccaratHand
from baccarat.game import BaccaratTable
from baccarat.game import BetResult
from baccarat.game import check_natural
from baccarat.game import get_result
from baccarat.game import Player
from baccarat.game import settle_bet
from baccarat.utils import Card
from baccarat.utils import Suit
from baccarat.utils import Value


@pytest.fixture
def table():
    """A table fixture."""
    return BaccaratTable(num_decks=1)


@pytest.fixture
def player():
    return Player(100)


def test_seating_player(table, player):
    """Test seating a player."""
    table.seat_player(player)
    assert table.player is player


def test_making_bet(table, player):
    """Test making a bet."""
    table.seat_player(player)
    table.place_bet(10, BetResult.PLAYER)

    assert len(table.bets) == 1
    assert table.bets[0].amount == 10
    assert table.bets[0].result == BetResult.PLAYER


def test_making_bet_with_no_player(table):
    """Test making a bet with no player seated."""
    with pytest.raises(ValueError):
        table.place_bet(10, BetResult.PLAYER)


def test_results_count(table):
    """Test the results count."""
    assert table.num_games == 0
    assert table.last_result is None
    assert table.result_counts == {
        BetResult.PLAYER: 0,
        BetResult.BANKER: 0,
        BetResult.TIE: 0,
    }

    table.results.append(BetResult.PLAYER)
    table.results.append(BetResult.PLAYER)
    table.results.append(BetResult.BANKER)
    table.results.append(BetResult.TIE)

    assert table.num_games == 4
    assert table.last_result == BetResult.TIE
    assert table.result_counts == {
        BetResult.PLAYER: 2,
        BetResult.BANKER: 1,
        BetResult.TIE: 1,
    }


def test_gameplay(table, player):
    table.seat_player(player)
    table.place_bet(10, BetResult.PLAYER)

    assert table.player_hand is None
    assert table.banker_hand is None
    assert table.results == []
    assert len(table.bets) == 1

    table.play()

    assert table.player_hand is not None
    assert table.banker_hand is not None
    assert len(table.results) == 1
    assert len(table.bets) == 0


def test_gameplay_fails_with_no_bets(table, player):
    table.seat_player(player)

    with pytest.raises(ValueError):
        table.play()


def test_shoe_reset(table, player):
    table.seat_player(player)
    table.place_bet(10, BetResult.PLAYER)

    assert table.shoe.num_cards == 52
    for _ in range(51):
        table.shoe.deal()

    assert table.shoe.num_cards == 1
    table.play()

    assert table.shoe.num_cards > 1
    assert table.player_hand.num_cards >= 2
    assert table.banker_hand.num_cards >= 2


def test_play_fails_with_no_deal(table, player):
    table.seat_player(player)
    table.place_bet(10, BetResult.PLAYER)

    assert table.player_hand is None
    assert table.banker_hand is None

    with pytest.raises(ValueError):
        table._play()


def test_check_natural():
    hand1 = BaccaratHand()
    hand1.cards.append(Card(suit=Suit.SPADES, value=Value.ACE))
    hand1.cards.append(Card(suit=Suit.SPADES, value=Value.TWO))

    hand2 = BaccaratHand()
    hand2.cards.append(Card(suit=Suit.SPADES, value=Value.ACE))
    hand2.cards.append(Card(suit=Suit.SPADES, value=Value.EIGHT))

    assert check_natural(hand1, hand2) == BetResult.BANKER
    assert check_natural(hand2, hand1) == BetResult.PLAYER
    assert check_natural(hand1, hand1) is None
    assert check_natural(hand2, hand2) == BetResult.TIE


def test_get_result():
    hand1 = BaccaratHand()
    hand1.cards.append(Card(suit=Suit.SPADES, value=Value.ACE))
    hand1.cards.append(Card(suit=Suit.SPADES, value=Value.TWO))

    hand2 = BaccaratHand()
    hand2.cards.append(Card(suit=Suit.SPADES, value=Value.ACE))
    hand2.cards.append(Card(suit=Suit.SPADES, value=Value.EIGHT))

    assert get_result(hand1, hand2) == BetResult.BANKER
    assert get_result(hand2, hand1) == BetResult.PLAYER
    assert get_result(hand1, hand1) == BetResult.TIE
    assert get_result(hand2, hand2) == BetResult.TIE


def test_settle_bet(player):
    bet1 = player.make_bet(10, BetResult.PLAYER)

    assert settle_bet(bet1, BetResult.PLAYER) == 20
    assert settle_bet(bet1, BetResult.BANKER) == 0
    assert settle_bet(bet1, BetResult.TIE) == 0

    bet2 = player.make_bet(10, BetResult.BANKER)

    assert settle_bet(bet2, BetResult.PLAYER) == 0
    assert settle_bet(bet2, BetResult.BANKER) == 19
    assert settle_bet(bet2, BetResult.TIE) == 0

    bet3 = player.make_bet(10, BetResult.TIE)

    assert settle_bet(bet3, BetResult.PLAYER) == 0
    assert settle_bet(bet3, BetResult.BANKER) == 0
    assert settle_bet(bet3, BetResult.TIE) == 80
