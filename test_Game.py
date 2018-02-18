import pytest
from RuleSet import RuleSet
from Game import Game

from pieces.Piece import Piece
from pieces.Pawn import Pawn
from pieces.King import King
from pieces.Queen import Queen
from pieces.Rook import Rook
from pieces.Knight import Knight
from pieces.Bishop import Bishop

from NoRuleException import NoRuleException
from IllegalMoveException import IllegalMoveException
from InvalidMoveStringException import InvalidMoveStringException

def test_that_constructor_sets_ruleset():
    ruleSet = RuleSet(None, None, None, None)
    game = Game(ruleSet)
    assert game.ruleSet is ruleSet, 'The ruleset was not set in the game instance'

def test_that_constructor_reads_in_board_template():
    ruleSet = RuleSet(None, None, None, None)
    game = Game(ruleSet)
    with open('./board.txt', 'r') as boardFile:
        assert game.boardTemplate == boardFile.read()

def test_that_load_throws_error_if_no_ruleset():
    game = Game(None)
    with pytest.raises(NoRuleException):
        game.load()

def test_that_load_throws_error_if_already_loaded():
    ruleSet = RuleSet(None, None, None, None)
    game = Game(ruleSet)
    print(game.isLoaded())
    game.load()
    print(game.isLoaded())
    with pytest.raises(Exception):
        game.load()

def test_that_load_loads_pieces():
    ruleSet = RuleSet(None, None, None, None)
    game = Game(ruleSet)
    game.load()
    assert len(game.whitePieces) == 16
    assert len(game.blackPieces) == 16
    assert isinstance(game.whitePieces[0], Pawn)
