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

def test_that_move_throws_exception_for_invalid_move_string():
    ruleSet = RuleSet(None, None, None, None)
    game = Game(ruleSet)
    game.load()
    with pytest.raises(InvalidMoveStringException):
        game.move('NotAValid MoveString to Duh')

def test_that_isValidMove_returns_true_for_a_valid_move():
    ruleSet = RuleSet(None, None, None, None)
    game = Game(ruleSet)
    game.load()
    assert game.isValidMove('D2 to D4') == True
    assert game.isValidMove(Move(Square(0, 1), Square(0, 3))) == True

def test_that_isValidMove_returns_false_for_an_invalid_move():
    ruleSet = RuleSet(None, None, None, None)
    game = Game(ruleSet)
    game.load()
    assert game.isValidMove('D2 to E3') == False
    assert game.isValidMove(Move(Square(4, 0), Square(4, 1))) == False

def test_that_isAttacking_returns_true_when_piece_attacking():
    ruleSet = RuleSet(None, None, None, None)
    game = Game(ruleSet)
    game.load()
    game.move('E2 to E4')
    game.move('D7 to D5')
    assert game.isAttacking('E4 to D5') == True
    assert game.isAttacking(Move(Square(3, 4), Square(4, 3))) == True
    assert game.isAttacking(Move(Square(4, 0), Square(3, 1))) == True
    

def test_that_isAttacking_returns_false_when_piece_not_attacking():
    ruleSet = RuleSet(None, None, None, None)
    game = Game(ruleSet)
    game.load()
    assert game.isAttacking('E4 to D5') == False
    assert game.isAttacking(Move(Square(0, 1), Square(1, 2))) == False
    assert game.isAttacking(Move(Square(4, 7), Square(4, 5))) == False
    
def test_that_isKingAttacked_returns_true_when_the_king_is_attacked():
    ruleSet = NormalChessConfig.ruleSet
    game = Game(ruleSet)
    game.load()
    game.move('D2 to D4')
    game.move('E7 to E5')
    game.move('D4 to E5')
    game.move('A7 to A5')
    game.move('E5 to E6')
    assert game.isKingAttacked(game.COLOR_BLACK) == False
    game.move('A5 to A4')
    game.move('E6 to D7')
    assert game.isKingAttacked(game.COLOR_BLACK) == True

def test_that_isKingAttacked_returns_false_when_the_king_is_not_attacked():
    ruleSet = NormalChessConfig.ruleSet
    game = Game(ruleSet)
    game.load()
    game.isKingAttacked(game.COLOR_WHITE) == False