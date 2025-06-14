import builtins
from expect_player.game import Game
from expect_player.data import players


def test_game_filters_players(monkeypatch):
    inputs = iter(['y', 'n', 'n', 'y'])

    def mock_input(prompt):
        return next(inputs)

    monkeypatch.setattr(builtins, 'input', mock_input)
    game = Game(players[:3])  # use a subset for predictable test
    result = game.play()
    assert result
    assert 'name' in result
