"""Command line interface for the Expect Player game."""

from .game import Game
from .data import players


def main() -> None:
    game = Game(players)
    game.play()


if __name__ == "__main__":
    main()
