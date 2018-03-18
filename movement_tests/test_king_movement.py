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

def test_that_king_moves_forward():
    ruleSet = RuleSet(None, None, None, None)
    game = Game(ruleSet)
    game.load()
    game.move('E2 to E4')
    game.move('D7 to D5')
    game.move('E1 to E2')
    assert isinstance(game.getPiece([4, 1]), King)
    assert game.getPiece([4, 0]) == None

def test_that_king_takes():
    ruleSet = RuleSet(None, None, None, None)
    game = Game(ruleSet)
    game.load()
    game.move('E2 to E4')
    game.move('D7 to D5')
    game.move('A2 to A4')
    game.move('D5 to E4')
    game.move('A4 to A5')
    game.move('E4 to E3')
    game.move('A5 to A6')
    game.move('E3 to D2')
    game.move('E1 to D2')
    assert isinstance(game.getPiece([3, 1]), King)
    assert game.getPiece([4, 0]) == None

