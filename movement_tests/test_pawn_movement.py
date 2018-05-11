import pytest
from RuleSet import RuleSet
from Game import Game

from color import WHITE, BLACK

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

def test_that_move_moves_pawn_two_forward():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('D2 to D4')
    assert isinstance(game.getPiece(Square(3, 3)), Pawn)
    assert game.getPiece(Square(3, 1)) == None

def test_that_move_moves_pawn_one_forward():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('D2 to D3')
    assert isinstance(game.getPiece(Square(3, 2)), Pawn)
    assert game.getPiece(Square(3, 1)) == None

def test_that_pawn_takes_diagonally():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('D2 to D4')
    game.move('E7 to E5')
    game.move('D4 to E5')
    assert isinstance(game.getPiece(Square(4, 4)), Pawn)
    assert game.getPiece(Square(4, 4)).color == WHITE
    assert game.getPiece(Square(3, 3)) == None

def test_that_blocked_pawn_does_not_move_two_spaces():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('D2 to D4')
    game.move('E7 to E5')
    game.move('D4 to D5')
    game.move('E5 to E4')
    game.move('D5 to D6')
    with pytest.raises(IllegalMoveException):
        game.move('D7 to D5')
    assert isinstance(game.getPiece(Square(3, 6)), Pawn)
    assert game.getPiece(Square(3, 4)) == None

def test_that_pawn_does_not_take_forward():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('D2 to D4')
    game.move('D7 to D5')
    with pytest.raises(IllegalMoveException):
        game.move('D4 to D5')
    assert isinstance(game.getPiece(Square(3, 3)), Pawn)
    assert isinstance(game.getPiece(Square(3, 4)), Pawn)
    
def test_that_pawn_does_not_move_two_forward_from_wrong_row():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('D2 to D4')
    game.move('A7 to A5')
    with pytest.raises(IllegalMoveException):
        game.move('D4 to D6')
    assert isinstance(game.getPiece(Square(3, 3)), Pawn)
    assert game.getPiece(Square(3, 5)) == None

def test_that_pawn_takes_en_passant():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('D2 to D4')
    game.move('A7 to A5')
    game.move('D4 to D5')
    game.move('E7 to E5')
    game.move('D5 to E6')
    assert isinstance(game.getPiece(Square(4, 5)), Pawn)
    assert game.getPiece(Square(4, 5)).color == WHITE
    assert game.getPiece(Square(4, 4)) == None

def test_that_black_pawn_takes_en_passant():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('D2 to D4')
    game.move('A7 to A5')
    game.move('D4 to D5')
    game.move('A5 to A4')
    game.move('B2 to B4')
    game.move('A4 to B3')
    assert isinstance(game.getPiece(Square(1, 2)), Pawn)
    assert game.getPiece(Square(1, 2)).color == BLACK
    assert game.getPiece(Square(1, 3)) == None

def test_that_pawn_promotes_to_queen():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('H2 to H4')
    game.move('A7 to A5')
    game.move('H4 to H5')
    game.move('A5 to A4')
    game.move('H5 to H6')
    game.move('B7 to B5')
    game.move('H6 to G7')
    game.move('B5 to B4')
    assert game.move('G7 to F8') == 'check'
    assert isinstance(game.getPiece(Square(5, 7)), Queen)

def test_that_black_pawn_promotes():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('H2 to H4')
    game.move('A7 to A5')
    game.move('H4 to H5')
    game.move('A5 to A4')
    game.move('H5 to H6')
    game.move('A4 to A3')
    game.move('G2 to G3')
    game.move('A3 to B2')
    game.move('G3 to G4')
    assert game.move('B2 to C1') == 'success'
    assert isinstance(game.getPiece(Square(2, 0)), Queen)