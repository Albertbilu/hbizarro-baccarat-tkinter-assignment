"""
A simple game of baccarat.
See https://en.wikipedia.org/wiki/Baccarat for more information.

Basic Rules:
- The player and banker are each dealt two cards.
- A third card may be dealt to either the player or banker depending on the total of their hand.
- The hand with the highest total wins.

Card Values:
- Aces are worth 1
- Face cards are worth 0
- All other cards are worth their pip value

Hand Values:
- The value of a hand is the sum of the values of its cards, modulo 10
(i.e., the maximum value of a hand is 9)
"""
from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple


class Suit(Enum):
    """A playing card suit."""


class Value(Enum):
    """A playing card value."""


class Card(NamedTuple):
    """A playing card."""

    value: Value
    suit: Suit

    def __repr__(self) -> str:
        ...


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

    @property
    def num_cards(self) -> int:
        """The number of cards remaining in the shoe."""

    def shuffle(self) -> None:
        """Shuffle the shoe."""

    def deal(self) -> Card:
        """Deal a card from the shoe.

        :return: A card
        """

    def reset(self) -> None:
        """Reset the shoe."""


def create_card(value: int | str, suit: str) -> Card:
    """Create a card from primitive types."""


class NotEnoughMoneyError(Exception):
    """Raised when a player does not have enough money to make a bet."""

    pass


class BetResult(Enum):
    """A bet type."""


class BaccaratHand:
    """A hand of cards."""

    def __init__(self) -> None:
        ...

    @property
    def total(self) -> int:
        """The total value of the hand."""

    @property
    def num_cards(self) -> int:
        """The number of cards in the hand."""

    @property
    def third_card(self) -> Card | None:
        """The third card in the hand, if any.

        :return: The third card in the hand, or None if there is no third card
        """

    @property
    def is_natural(self) -> bool:
        """Whether the hand is a natural win.
        A natural win is when the first two cards total 8 or 9.

        :return: True if the hand is a natural win, otherwise False
        """

    def add_card(self, card: Card) -> None:
        """Add a card to the hand.

        :param card: The card to add
        """

    def get_value(self) -> int:
        """Get the value of the hand.
        An ace is worth 1, face cards are worth 0, and all other cards are worth their pip value.
        A hand's value is the sum of the values of its cards, modulo 10
        (i.e., the maximum value of a hand is 9).

        :return: The value of the hand
        """

    def __repr__(self) -> str:
        ...


class Bet(NamedTuple):
    """A bet on the game.

    :param amount: The amount of the bet
    :param result: The bet type
    """

    amount: int
    result: BetResult


@dataclass
class Player:
    """A player.

    :param bankroll: the player's bankroll
    """

    bankroll: int

    def make_bet(self, amount: int, result: BetResult) -> Bet:
        """Make a bet.

        :param amount: The amount to bet
        :raises ValueError: If the bet amount is greater than the bankroll
        :return: A bet
        """

    def win_bet(self, amount: int) -> None:
        """Win a bet - add the amount to the bankroll.

        :param amount: The amount won
        """


class BaccaratTable:
    """A game of baccarat.

    :param num_decks: The number of decks to use in the shoe
    """

    shoe: Shoe
    player: Player | None
    bets: deque[Bet]
    player_hand: BaccaratHand | None
    banker_hand: BaccaratHand | None
    results: list[BetResult]

    def __init__(self, num_decks: int = 8) -> None:
        ...

    @property
    def num_games(self) -> int:
        """The number of games played."""

    @property
    def result_counts(self) -> dict[BetResult, int]:
        """The number of times each bet type has won."""

    def seat_player(self, player: Player) -> None:
        """Seat a player at the table.

        :param player: The player to seat
        """

    def place_bet(self, amount: int, result: BetResult) -> None:
        """Place a bet.

        :param amount: The amount to bet
        :param result: The bet type
        :raises ValueError: If the bet amount is greater than the player's bankroll
        """

    def play(self) -> None:
        """Play a game of baccarat."""

    def _deal(self) -> None:
        """Deal the cards."""

    def _play(self) -> BetResult:
        """Play the game."""

    def _settle_bets(self, result: BetResult) -> None:
        """Settle the bets.

        :param result: The result of the game
        """

    @classmethod
    def _log_draw(cls, who: str, hand: BaccaratHand) -> None:
        """OPTIONAL: Helper to log the results of a draw using the logging module."""


def get_baccarat_value(card: Card) -> int:
    """Get the value of a card for baccarat

    :param card: A playing card
    :return: The baccarat value of the card as an integer
    """


def does_player_draw(player_total: int) -> bool:
    """Determine if the player should draw a third card.

    :param player_total: The player's total
    :return: True if the player should draw a third card, otherwise False
    """


def does_banker_draw(banker_total: int, player_third_card_value: int | None) -> bool:
    """Determine if the banker should draw a third card.

    :param banker_total: The banker's total
    :param player_third_card_value: The value of the player's third card, if any
    :return: True if the banker should draw a third card, otherwise False
    """


def do_player_draw(player_hand: BaccaratHand, shoe: Shoe) -> None:
    """Draw a card for the player if needed.

    :param player_hand: The player's hand
    :param shoe: The shoe of cards
    :return: The player's hand
    """


def do_banker_draw(banker_hand: BaccaratHand, player_hand: BaccaratHand, shoe: Shoe) -> None:
    """Draw a card for the banker if needed.

    :param banker_hand: The banker's hand
    :param player_hand: The player's hand
    :param shoe: The shoe of cards
    :return: The banker's hand
    """


def check_natural(player_hand: BaccaratHand, banker_hand: BaccaratHand) -> BetResult | None:
    """Check for a natural win.

    :param player_hand: The player's hand
    :param banker_hand: The banker's hand
    :return: The bet type if a natural win, otherwise False
    """


def get_result(player_hand: BaccaratHand, banker_hand: BaccaratHand) -> BetResult:
    """Get the result of a game of baccarat.

    :param player_hand: The player's hand
    :param banker_hand: The banker's hand
    :return: The result of the game
    """


def settle_bet(bet: Bet, result: BetResult) -> int:
    """Settle a bet.

    :param bet: the bet
    :param result: the result of the game
    :return: the amount to pay out (0 if the bet loses)
    """
