import time
import tkinter as tk
from tkinter import ttk

from baccarat.game import BaccaratTable
from baccarat.game import BetResult
from baccarat.game import get_baccarat_value
from baccarat.game import Player


class Window(tk.Tk):
    table: BaccaratTable

    def __init__(self):
        super().__init__()

        self.table = BaccaratTable()

        self.title("Tkinter Baccarat")
        self.minsize(400, 200)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.player_sit_panel = PlayerSitPanel(self)
        self.game_panel = GamePanel(self)
        self.bet_panel = BetPanel(self)

        self.player_sit_panel.grid(row=0, column=0, sticky="NSEW")
        self.game_panel.grid(row=0, column=0, sticky="NSEW")
        self.bet_panel.grid(row=1, column=0, sticky="NSEW")

        self.game_panel.grid_remove()
        self.bet_panel.grid_remove()

    def sit_player(self, player: Player):
        self.table.seat_player(player)
        self.player_sit_panel.grid_remove()
        self.game_panel.grid()
        self.bet_panel.grid()

    def deal(self, bet: int, bet_type: str):
        self.table.place_bet(bet, BetResult(bet_type))
        self.table.play()

        self.bet_panel.update_bankroll(self.table.player.bankroll)
        self.game_panel.player_cards.clear()
        self.game_panel.banker_cards.clear()
        self.update()

        player_card1 = self.table.player_hand.cards[0]
        self.game_panel.player_cards.add_card(str(player_card1), get_baccarat_value(player_card1))
        self._deal_card_delay()

        banker_card1 = self.table.banker_hand.cards[0]
        self.game_panel.banker_cards.add_card(str(banker_card1), get_baccarat_value(banker_card1))
        self._deal_card_delay()

        player_card2 = self.table.player_hand.cards[1]
        self.game_panel.player_cards.add_card(str(player_card2), get_baccarat_value(player_card2))
        self._deal_card_delay()

        banker_card2 = self.table.banker_hand.cards[1]
        self.game_panel.banker_cards.add_card(str(banker_card2), get_baccarat_value(banker_card2))
        self._deal_card_delay()

        player_has_drawn = self.table.player_hand.num_cards == 3
        banker_has_drawn = self.table.banker_hand.num_cards == 3

        if player_has_drawn:
            player_card3 = self.table.player_hand.cards[2]
            self.game_panel.player_cards.add_card(
                str(player_card3), get_baccarat_value(player_card3)
            )
            self._deal_card_delay()

        if banker_has_drawn:
            banker_card3 = self.table.banker_hand.cards[2]
            self.game_panel.banker_cards.add_card(
                str(banker_card3), get_baccarat_value(banker_card3)
            )
            self._deal_card_delay()

        self.game_panel.update_winner(self.table.results[-1].value)
        self.bet_panel.update_bankroll(self.table.player.bankroll)

    def _deal_card_delay(self):
        time.sleep(0.2)
        self.update()


class PlayerSitPanel(ttk.Frame):
    """Ask the player to sit at the table and enter their bankroll."""

    master: Window

    def __init__(self, container):
        super().__init__(container)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.sit_label = ttk.Label(self, text="Sit at the table")
        self.bankroll_label = ttk.Label(self, text="Bankroll")
        self.sit_button = ttk.Button(self, text="Sit", command=self.sit_player)

        self.bankroll_entry = ttk.Entry(self)
        self.bankroll_entry.insert(0, "1000")

        self.sit_label.grid(row=0, column=0, columnspan=2)
        self.bankroll_label.grid(row=1, column=0, sticky="W")
        self.bankroll_entry.grid(row=1, column=1, sticky="EW")
        self.sit_button.grid(row=2, column=0, columnspan=2, sticky="EW")

    def sit_player(self):
        bankroll = int(self.bankroll_entry.get())
        player = Player(bankroll)
        self.master.sit_player(player)
        self.master.bet_panel.update_bankroll(bankroll)


class GamePanel(ttk.Frame):
    """The main game panel."""

    master: Window

    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.player_card = ttk.Label(self, text="Player")
        self.player_cards = HandPanel(self)
        self.banker_card = ttk.Label(self, text="Banker")
        self.banker_cards = HandPanel(self)
        self.winner_label = ttk.Label(self, text="")
        self.deal_button = ttk.Button(self, text="Deal", command=self.deal)

        self.player_card.grid(row=3, column=0)
        self.player_cards.grid(row=4, column=0)
        self.banker_card.grid(row=3, column=1)
        self.banker_cards.grid(row=4, column=1)
        self.winner_label.grid(row=5, column=0, columnspan=2)
        self.deal_button.grid(row=6, column=0, columnspan=2, sticky="EW")

    def deal(self):
        self.winner_label["text"] = ""
        bet = int(self.master.bet_panel.bet_entry.get())
        bet_type = self.master.bet_panel.bet_type.get()

        self.master.deal(bet, bet_type)

    def update_winner(self, winner: str):
        if winner == BetResult.TIE.value:
            self.winner_label["text"] = "It's a tie!"
        else:
            self.winner_label["text"] = f"{winner} wins!"


class BetPanel(ttk.Frame):
    bankroll: int

    def __init__(self, container):
        super().__init__(container)
        self.bankroll = 0

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Bet amount
        self.bet_label = ttk.Label(self, text="Bet")
        self.bet_type_label = ttk.Label(self, text="Bet Type")
        self.bankroll_label = ttk.Label(self, text=f"Bankroll: ${self.bankroll:,.2f}")

        self.bet_entry = ttk.Entry(self)
        self.bet_entry.insert(0, "200")

        self.bet_type = tk.StringVar()
        self.bet_type.set("Player")
        self.bet_type_combobox = ttk.Combobox(
            self,
            textvariable=self.bet_type,
            values=["Player", "Banker", "Tie"],
            state="readonly",
        )

        self.bet_label.grid(row=0, column=0, sticky="W")
        self.bet_entry.grid(row=0, column=1, sticky="EW")
        self.bet_type_label.grid(row=1, column=0, sticky="W")
        self.bet_type_combobox.grid(row=1, column=1, sticky="EW")
        self.bankroll_label.grid(row=2, column=0, sticky="W")

    def update_bankroll(self, bankroll: int):
        self.bankroll = bankroll
        self.bankroll_label["text"] = f"Bankroll: {self.bankroll}"


class HandPanel(ttk.Frame):
    """A layout for 3 cards, 2 next to each other and 1 above."""

    cards: list[str]
    total: int

    def __init__(self, container) -> None:
        super().__init__(container)
        self.cards = []
        self.total = 0

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.card1 = ttk.Label(self, text="", width=10)
        self.card2 = ttk.Label(self, text="")
        self.card3 = ttk.Label(self, text="")
        self.total_label = ttk.Label(self, text="")

        self.card1.grid(row=0, column=0)
        self.card2.grid(row=0, column=1)
        self.card3.grid(row=1, column=0, columnspan=2)
        self.total_label.grid(row=2, column=0, columnspan=2)

    def clear(self) -> None:
        """Clear the cards and total."""

        self.cards = []
        self.total = 0

        self.card1["text"] = ""
        self.card2["text"] = ""
        self.card3["text"] = ""
        self.total_label["text"] = ""

    def add_card(self, card: str, card_value: int) -> None:
        """Add a card to the hand and update the total."""

        self.cards.append(card)
        if len(self.cards) >= 1:
            self.card1["text"] = self.cards[0]

        if len(self.cards) >= 2:
            self.card2["text"] = self.cards[1]

        if len(self.cards) >= 3:
            self.card3["text"] = self.cards[2]

        self.total += card_value
        self.total = self.total % 10

        self.total_label["text"] = str(self.total)


if __name__ == "__main__":
    window = Window()
    window.mainloop()
