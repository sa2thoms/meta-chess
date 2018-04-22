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
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('E2 to E4')
    game.move('D7 to D5')
    game.move('E1 to E2')
    assert isinstance(game.getPiece(Square(4, 1)), King)
    assert game.getPiece(Square(4, 0)) == None

def test_that_king_takes():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('E2 to E4')
    game.move('D7 to D5')
    game.move('A2 to A4')
    game.move('D5 to E4')
    game.move('A4 to A5')
    game.move('E4 to E3')
    game.move('F1 to D3')
    game.move('E3 to D2')
    game.move('E1 to D2')
    assert isinstance(game.getPiece(Square(3, 1)), King)
    assert game.getPiece(Square(4, 0)) == None

def test_that_castling_works_under_normal_conditions():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('E2 to E4')
    game.move('E7 to E5')
    game.move('F1 to C4')
    game.move('D7 to D5')
    game.move('G1 to F3')
    game.move('A7 to A5')
    assert game.move('E1 to G1') == 'success'
    assert game.getPiece(Square(4, 0)) == None
    assert isinstance(game.getPiece(Square(5, 0)), Rook)
    assert isinstance(game.getPiece(Square(6, 0)), King)
    assert game.getPiece(Square(7, 0)) == None

def test_that_castling_works_under_normal_conditions_for_black():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('E2 to E4')
    game.move('E7 to E5')
    game.move('F1 to C4')
    game.move('F8 to C5')
    game.move('G1 to F3')
    game.move('G8 to F6')
    game.move('E1 to G1')
    assert game.move('E8 to G8') == 'success'
    assert game.getPiece(Square(4, 7)) == None
    assert isinstance(game.getPiece(Square(5, 7)), Rook)
    assert isinstance(game.getPiece(Square(6, 7)), King)
    assert game.getPiece(Square(7, 7)) == None

def test_that_queenside_castling_works():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('E2 to E4')
    game.move('E7 to E5')
    game.move('D2 to D4')
    game.move('D7 to D5')
    game.move('D1 to E2')
    game.move('D8 to E7')
    game.move('C1 to D2')
    game.move('C8 to D7')
    game.move('B1 to C3')
    game.move('B8 to C6')
    assert game.move('E1 to C1') == 'success'
    assert game.getPiece(Square(4, 0)) == None
    assert isinstance(game.getPiece(Square(3, 0)), Rook)
    assert isinstance(game.getPiece(Square(2, 0)), King)
    assert game.getPiece(Square(1, 0)) == None
    assert game.getPiece(Square(0, 0)) == None

def test_that_queenside_castling_works_for_black():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('E2 to E4')
    game.move('E7 to E5')
    game.move('D2 to D4')
    game.move('D7 to D5')
    game.move('D1 to E2')
    game.move('D8 to E7')
    game.move('C1 to D2')
    game.move('C8 to D7')
    game.move('B1 to C3')
    game.move('B8 to C6')
    game.move('E1 to C1')
    assert game.move('E8 to C8') == 'success'
    assert game.getPiece(Square(4, 7)) == None
    assert isinstance(game.getPiece(Square(3, 7)), Rook)
    assert isinstance(game.getPiece(Square(2, 7)), King)
    assert game.getPiece(Square(1, 7)) == None
    assert game.getPiece(Square(0, 7)) == None
