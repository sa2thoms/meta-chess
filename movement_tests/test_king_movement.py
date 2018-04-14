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

from Square import Square
from Move import Move

from NoRuleException import NoRuleException
from IllegalMoveException import IllegalMoveException
from InvalidMoveStringException import InvalidMoveStringException

import NormalChessConfig

def test_that_king_moves_forward():
    ruleSet = NormalChessConfig.ruleSet
    game = Game(ruleSet)
    game.load()
    game.move('E2 to E4')
    game.move('D7 to D5')
    game.move('E1 to E2')
    assert isinstance(game.getPiece(Square(4, 1)), King)
    assert game.getPiece(Square(4, 0)) == None

def test_that_king_takes():
    ruleSet = NormalChessConfig.ruleSet
    game = Game(ruleSet)
    game.load()
    game.move('E2 to E4')
    game.move('D7 to D5')
    game.move('A2 to A4')
    game.move('D5 to E4')
    game.move('A4 to A5')
    game.move('E4 to E3')
    game.move('F1 to D3')
    game.printBoard()
    game.move('E3 to D2')
    game.printBoard()
    game.move('E1 to D2')
    assert isinstance(game.getPiece(Square(3, 1)), King)
    assert game.getPiece(Square(4, 0)) == None

