"""Core game logic for the Expect Player guessing game."""

from typing import List, Dict


def unique_values(players: List[Dict], attr: str) -> List[str]:
    """Return unique attribute values preserving dataset order."""
    seen = set()
    values = []
    for player in players:
        value = player.get(attr)
        if value not in seen:
            seen.add(value)
            values.append(value)
    return values


class Game:
    """Interactive guessing game."""

    def __init__(self, players: List[Dict]):
        """Initialize game with a list of player dictionaries."""
        self.possible_players = players[:]
        # ask questions about these attributes
        self.attributes = ["nationality", "club", "position"]

    def ask(self, attr: str, value: str) -> bool:
        """Prompt user with a yes/no question about an attribute."""
        while True:
            answer = input(f"Is your player's {attr} {value}? (y/n): ").strip().lower()
            if answer in {"y", "n"}:
                return answer == "y"
            print("Please answer with 'y' or 'n'.")

    def filter_players(self, attr: str, value: str, keep: bool) -> None:
        """Filter ``possible_players`` according to the user's answer."""
        if keep:
            self.possible_players = [p for p in self.possible_players if p.get(attr) == value]
        else:
            self.possible_players = [p for p in self.possible_players if p.get(attr) != value]

    def play(self) -> Dict:
        """Run the interactive guessing loop and return the guessed player."""
        print("Think of one of these players:")
        for p in self.possible_players:
            print(" -", p["name"])
        print("\nAnswer the following questions with 'y' or 'n'.\n")

        for attr in self.attributes:
            values = unique_values(self.possible_players, attr)
            for value in values:
                keep = self.ask(attr, value)
                self.filter_players(attr, value, keep)
                if len(self.possible_players) == 1:
                    break
            if len(self.possible_players) == 1:
                break

        if self.possible_players:
            player = self.possible_players[0]
            print(f"\nYour player is {player['name']}!")
            print(f"Photo URL: {player['photo']}")
            return player
        else:
            print("\nI couldn't guess your player.")
            return {}
