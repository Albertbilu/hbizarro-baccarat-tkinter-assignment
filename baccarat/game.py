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
import logging
import math
import sys
from collections import Counter
from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple

from .utils import Card
from .utils import Shoe
from .utils import Value

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="TABLE (%(asctime)s): %(message)s",
)


class NotEnoughMoneyError(Exception):
    """Raised when a player does not have enough money to make a bet."""

    pass


class BetResult(Enum):
    """A bet type."""

    PLAYER = "Player"
    BANKER = "Banker"
    TIE = "Tie"


class BaccaratHand:
    """A hand of cards."""

    def __init__(self) -> None:
        self.cards: list[Card] = []

    @property
    def total(self) -> int:
        """The total value of the hand."""
        return self.get_value()

    @property
    def num_cards(self) -> int:
        """The number of cards in the hand."""
        return len(self.cards)

    @property
    def third_card(self) -> Card | None:
        """The third card in the hand, if any.

        :return: The third card in the hand, or None if there is no third card
        """
        if self.num_cards < 3:
            return None

        return self.cards[2]

    @property
    def is_natural(self) -> bool:
        """Whether the hand is a natural win.
        A natural win is when the first two cards total 8 or 9.

        :return: True if the hand is a natural win, otherwise False
        """
        return self.num_cards == 2 and self.total in [8, 9]

    def add_card(self, card: Card) -> None:
        """Add a card to the hand.

        :param card: The card to add
        """
        self.cards.append(card)

    def get_value(self) -> int:
        """Get the value of the hand.
        An ace is worth 1, face cards are worth 0, and all other cards are worth their pip value.
        A hand's value is the sum of the values of its cards, modulo 10
        (i.e., the maximum value of a hand is 9).

        :return: The value of the hand
        """
        return sum(get_baccarat_value(card) for card in self.cards) % 10

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(total={self.get_value()}, cards={self.cards})"


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

        if amount > self.bankroll:
            raise NotEnoughMoneyError("Player does not have enough money to make bet")

        self.bankroll -= amount
        return Bet(amount, result)

    def win_bet(self, amount: int) -> None:
        """Win a bet - add the amount to the bankroll.

        :param amount: The amount won
        """

        self.bankroll += amount


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
        self.shoe = Shoe(num_decks)
        self.shoe.shuffle()
        logging.info(f"Shoe shuffled with {self.shoe.num_cards} cards")

        self.player = None
        self.bets = deque()
        self.player_hand = None
        self.banker_hand = None
        self.results = []

    @property
    def num_games(self) -> int:
        """The number of games played."""
        return len(self.results)

    @property
    def result_counts(self) -> dict[BetResult, int]:
        """The number of times each bet type has won."""
        return Counter(self.results)

    def seat_player(self, player: Player) -> None:
        """Seat a player at the table.

        :param player: The player to seat
        """
        self.player = player
        logging.info(f"Player seated with ${player.bankroll:.02f}")

    def place_bet(self, amount: int, result: BetResult) -> None:
        """Place a bet.

        :param amount: The amount to bet
        :param result: The bet type
        :raises ValueError: If the bet amount is greater than the player's bankroll
        """

        if self.player is None:
            raise ValueError("Player is not set")

        bet = self.player.make_bet(amount, result)
        self.bets.append(bet)
        logging.info(f"Player bets ${bet.amount:.02f} on '{bet.result.value}'")

    def play(self) -> None:
        """Play a game of baccarat."""
        if len(self.bets) == 0:
            raise ValueError("No bets have been placed")

        if self.shoe.num_cards < 6:
            self.shoe.reset()
            logging.info(f"Shoe reset with {self.shoe.num_cards} cards")

        # Set up the game - deal 2 cards to the player and banker
        logging.info(f"Starting new deal with {self.shoe.num_cards} cards")
        self._deal()

        # Play the game - draw as needed, and determine the result
        result = self._play()
        logging.info(f"The result is '{result.value}'")
        self.results.append(result)

        # Settle the bets - pay out winnings, if any
        self._settle_bets(result)

        if self.player is None:
            raise ValueError("Player is not set")

        logging.info(f"Player's bankroll is now ${self.player.bankroll:.02f}")

    def _deal(self) -> None:
        """Deal the cards."""

        self.player_hand = BaccaratHand()
        self.banker_hand = BaccaratHand()

        self.player_hand.add_card(self.shoe.deal())
        self.banker_hand.add_card(self.shoe.deal())
        self.player_hand.add_card(self.shoe.deal())
        self.banker_hand.add_card(self.shoe.deal())

        logging.info(f"Player has {self.player_hand}")
        logging.info(f"Banker has {self.banker_hand}")

    def _play(self) -> BetResult:
        """Play the game."""

        if self.player_hand is None or self.banker_hand is None:
            raise ValueError("Hands have not been dealt")

        natural_win = check_natural(self.player_hand, self.banker_hand)

        if natural_win:
            logging.info(f"Natual! Result is '{natural_win.value}'")
            return natural_win

        do_player_draw(self.player_hand, self.shoe)
        BaccaratTable._log_draw("Player", self.player_hand)

        do_banker_draw(self.banker_hand, self.player_hand, self.shoe)
        BaccaratTable._log_draw("Banker", self.banker_hand)

        return get_result(self.player_hand, self.banker_hand)

    def _settle_bets(self, result: BetResult) -> None:
        if self.player is None:
            raise ValueError("Player is not set")

        while self.bets:
            bet = self.bets.popleft()
            amount = settle_bet(bet, result)

            if amount == 0:
                logging.info(f"Player loses ${bet.amount:.02f}")
            if amount > 0:
                logging.info(f"Player wins ${amount:.02f}")

            self.player.win_bet(amount)

        if len(self.bets) != 0:
            raise ValueError("Not all bets have been settled")

    @classmethod
    def _log_draw(cls, who: str, hand: BaccaratHand) -> None:
        if hand.num_cards == 3:
            logging.info(f"{who} draws {hand.third_card} - new total is {hand.total}")
        else:
            logging.info(f"{who} stands with {hand.total}")


def get_baccarat_value(card: Card) -> int:
    """Get the value of a card for baccarat

    :param card: A playing card
    :return: The baccarat value of the card as an integer
    """

    if card.value in [Value.TEN, Value.JACK, Value.QUEEN, Value.KING]:
        return 0
    elif card.value is Value.ACE:
        return 1
    else:
        return int(card.value.value)


def does_player_draw(player_total: int) -> bool:
    """Determine if the player should draw a third card.

    :param player_total: The player's total
    :return: True if the player should draw a third card, otherwise False
    """

    return player_total <= 5


def does_banker_draw(banker_total: int, player_third_card_value: int | None) -> bool:
    """Determine if the banker should draw a third card.

    :param banker_total: The banker's total
    :param player_third_card_value: The value of the player's third card, if any
    :return: True if the banker should draw a third card, otherwise False
    """
    if player_third_card_value is None:
        return banker_total <= 5

    return (
        (banker_total <= 2)
        or (banker_total == 3 and player_third_card_value != 8)
        or (banker_total == 4 and player_third_card_value in range(2, 7 + 1))
        or (banker_total == 5 and player_third_card_value in range(4, 7 + 1))
        or (banker_total == 6 and player_third_card_value in range(6, 7 + 1))
    )


def do_player_draw(player_hand: BaccaratHand, shoe: Shoe) -> None:
    """Draw a card for the player if needed.

    :param player_hand: The player's hand
    :param shoe: The shoe of cards
    :return: The player's hand
    """

    if does_player_draw(player_hand.get_value()):
        player_hand.add_card(shoe.deal())


def do_banker_draw(banker_hand: BaccaratHand, player_hand: BaccaratHand, shoe: Shoe) -> None:
    """Draw a card for the banker if needed.

    :param banker_hand: The banker's hand
    :param player_hand: The player's hand
    :param shoe: The shoe of cards
    :return: The banker's hand
    """

    if player_hand.third_card is None:
        player_third_card_value: int | None = None
    else:
        player_third_card_value = get_baccarat_value(player_hand.third_card)

    if does_banker_draw(banker_hand.get_value(), player_third_card_value):
        banker_hand.add_card(shoe.deal())


def check_natural(player_hand: BaccaratHand, banker_hand: BaccaratHand) -> BetResult | None:
    """Check for a natural win.

    :param player_hand: The player's hand
    :param banker_hand: The banker's hand
    :return: The bet type if a natural win, otherwise False
    """

    if player_hand.is_natural and banker_hand.is_natural:
        return BetResult.TIE
    elif player_hand.is_natural:
        return BetResult.PLAYER
    elif banker_hand.is_natural:
        return BetResult.BANKER
    else:
        return None


def get_result(player_hand: BaccaratHand, banker_hand: BaccaratHand) -> BetResult:
    """Get the result of a game of baccarat.

    :param player_hand: The player's hand
    :param banker_hand: The banker's hand
    :return: The result of the game
    """

    if player_hand.total > banker_hand.total:
        return BetResult.PLAYER
    elif player_hand.total < banker_hand.total:
        return BetResult.BANKER
    else:
        return BetResult.TIE


def settle_bet(bet: Bet, result: BetResult) -> int:
    """Settle a bet.

    :param bet: the bet
    :param result: the result of the game
    :return: the amount to pay out (0 if the bet loses)
    """
    if result is BetResult.PLAYER and bet.result == result:
        return bet.amount * 2
    elif result is BetResult.BANKER and bet.result == result:
        return math.floor(bet.amount * 1.95)  # 5% commission
    elif bet.result == BetResult.TIE and result == BetResult.TIE:
        return bet.amount * 8
    else:
        return 0
