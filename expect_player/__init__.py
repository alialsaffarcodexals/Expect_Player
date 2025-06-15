"""Expect Player package."""

from .game import Game
from .data import players

try:  # optional dependency for GUI
    from .gui import GameGUI
except Exception:  # pragma: no cover - GUI requirements may be missing
    GameGUI = None  # type: ignore

__all__ = ["Game", "GameGUI", "players"]
