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

def test_that_move_moves_pawn_two_forward():
    ruleSet = RuleSet(None, None, None, None)
    game = Game(ruleSet)
    game.load()
    game.move('D2 to D4')
    assert isinstance(game.getPiece([3, 3]), Pawn)
    assert game.getPiece([3, 1]) == None

def test_that_move_moves_pawn_one_forward():
    ruleSet = RuleSet(None, None, None, None)
    game = Game(ruleSet)
    game.load()
    game.move('D2 to D3')
    assert isinstance(game.getPiece([3, 2]), Pawn)
    assert game.getPiece([3, 1]) == None

def test_that_pawn_takes_diagonally():
    ruleSet = RuleSet(None, None, None, None)
    game = Game(ruleSet)
    game.load()
    game.move('D2 to D4')
    game.move('E7 to E5')
    game.move('D4 to E5')
    assert isinstance(game.getPiece([4, 4]), Pawn)
    assert game.getPiece([4, 4]).color == game.COLOR_WHITE
    assert game.getPiece([3, 3]) == None

def test_that_blocked_pawn_does_not_move_two_spaces():
    ruleSet = RuleSet(None, None, None, None)
    game = Game(ruleSet)
    game.load()
    game.move('D2 to D4')
    game.move('E7 to E5')
    game.move('D4 to D5')
    game.move('E5 to E4')
    game.move('D5 to D6')
    with pytest.raises(IllegalMoveException):
        game.move('D7 to D5')
    assert isinstance(game.getPiece([3, 6]), Pawn)
    assert game.getPiece([3, 4]) == None