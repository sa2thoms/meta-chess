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

def test_that_queen_moves_correctly():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move(Move(Square(4, 1), Square(4, 3)))
    game.move('E7 to E5')
    game.move('D1 to H5')
    assert isinstance(game.getPiece(Square(7, 4)), Queen)
    game.move('D7 to D5')
    game.move('H5 to E5')
    assert isinstance(game.getPiece(Square(4, 4)), Queen)
    game.move('F8 to E7')
    game.move('E5 to C7')
    assert isinstance(game.getPiece(Square(2, 6)), Queen)

def test_that_queen_does_not_move_illegally():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move(Move(Square(4, 1), Square(4, 3)))
    game.move('E7 to E5')
    with pytest.raises(IllegalMoveException):
        game.move('D1 to D5')
    with pytest.raises(IllegalMoveException):
        game.move('D1 to E5')
    with pytest.raises(IllegalMoveException):
        game.move('D1 to C2')
    with pytest.raises(IllegalMoveException):
        game.move('D1 to A4')

def test_that_knight_moves_correctly():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
         return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('E2 to E4')
    game.move('B8 to C6')
    assert isinstance(game.getPiece(Square(2, 5)), Knight)

def test_that_knight_does_not_move_illegally():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    with pytest.raises(IllegalMoveException):
        game.move('B1 to D2')
    with pytest.raises(IllegalMoveException):
        game.move('B1 to B3')

def test_that_knight_does_not_move_diagonally():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('E2 to E4')
    game.move('E7 to E5')
    game.move('D1 to F3')
    game.move('A7 to A5')
    game.move('F3 to F7')
    with pytest.raises(IllegalMoveException):
        game.move('G8 to F7')

def test_that_multiple_jump_moves_work():
    ruleSet = NormalChessConfig.ruleSet
    ruleSet.knightMovement.jumpRules.append([3, 3])
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('B1 to C3')
    game.move('B8 to C6')
    game.move('A2 to A4')
    assert game.move('C6 to B4') == 'mate'