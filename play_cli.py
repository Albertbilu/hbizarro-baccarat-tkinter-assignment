from baccarat import BaccaratTable
from baccarat import BetResult
from baccarat import NotEnoughMoneyError
from baccarat import Player


BET_CHOICES = {
    "P": BetResult.PLAYER,
    "B": BetResult.BANKER,
    "T": BetResult.TIE,
}


def main(argv: list[str] | None = None) -> int:
    player = Player(1000)

    table = BaccaratTable(num_decks=8)
    table.seat_player(player)

    while player.bankroll < 2000:
        bet_choice = input("Place a bet on Player (P), Banker (B), or Tie (T): ")
        bet_choice = bet_choice.upper()

        if bet_choice not in BET_CHOICES:
            print("Invalid choice.")
            continue

        bet_choice_ = BET_CHOICES[bet_choice]

        try:
            table.place_bet(200, bet_choice_)
        except NotEnoughMoneyError:
            print(f"Not enough money to place bet. Lasted {table.num_games} games.")
            return 1

        table.play()

    print(f"Player has doubled their money to ${player.bankroll} after {table.num_games} games.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
