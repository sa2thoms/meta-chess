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
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    assert game.ruleSet is ruleSet, 'The ruleset was not set in the game instance'

def test_that_constructor_reads_in_board_template():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    with open('./board.txt', 'r') as boardFile:
        assert game.boardTemplate == boardFile.read()

def test_that_load_throws_error_if_already_loaded():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    with pytest.raises(Exception):
        game.load()

def test_that_load_loads_pieces():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    assert len(game.whitePieces) == 16
    assert len(game.blackPieces) == 16
    assert isinstance(game.whitePieces[0], Pawn)

def test_that_move_throws_exception_for_invalid_move_string():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    with pytest.raises(InvalidMoveStringException):
        game.move('NotAValid MoveString to Duh')

def test_that_isValidMove_returns_true_for_a_valid_move():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    assert game.isValidMove('D2 to D4') == True
    assert game.isValidMove(Move(Square(0, 1), Square(0, 3))) == True

def test_that_isValidMove_returns_false_for_an_invalid_move():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    assert game.isValidMove('D2 to E3') == False
    assert game.isValidMove(Move(Square(4, 0), Square(4, 1))) == False

def test_that_isAttacking_returns_true_when_piece_attacking():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('E2 to E4')
    game.move('D7 to D5')
    assert game.isAttacking('E4 to D5') == True
    assert game.isAttacking(Move(Square(3, 4), Square(4, 3))) == True
    assert game.isAttacking(Move(Square(4, 0), Square(3, 1))) == True
    

def test_that_isAttacking_returns_false_when_piece_not_attacking():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    assert game.isAttacking('E4 to D5') == False
    assert game.isAttacking(Move(Square(0, 1), Square(1, 2))) == False
    assert game.isAttacking(Move(Square(4, 7), Square(4, 5))) == False
    
def test_that_isKingAttacked_returns_true_when_the_king_is_attacked():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
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

def test_that_checking_returns_check_from_move():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('D2 to D4')
    game.move('E7 to E5')
    game.move('D4 to E5')
    game.move('A7 to A5')
    game.move('E5 to E6')
    game.move('A5 to A4')
    assert game.move('E6 to D7') == 'check'

def test_that_move_returns_success_when_not_check_or_mate():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    assert game.move('D2 to D4') == 'success'

def test_that_isKingAttacked_returns_false_when_the_king_is_not_attacked():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    assert game.isKingAttacked(game.COLOR_WHITE) == False

def test_that_moving_so_that_king_attacked_is_not_allowed():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('E2 to E4')
    game.move('E7 to E5')
    game.move('D2 to D4')
    game.move('D7 to D5')
    game.move('A2 to A4')
    game.move('E5 to D4')
    game.move('A4 to A5')
    game.move('D8 to E7')
    with pytest.raises(IllegalMoveException):
        game.move('E4 to D5')

def test_that_checkmate_results_in_a_mate_return():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('E2 to E4')
    game.move('E7 to E5')
    game.move('D1 to F3')
    game.move('A7 to A5')
    game.move('F1 to C4')
    game.move('B7 to B5')
    assert game.move('F3 to F7') == 'mate'

def test_that_undoLastMove_undoes_a_move():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('E2 to E4')
    game.move('E7 to E5')
    assert game.getPiece(Square(4, 6)) == None
    assert len(game.moveHistory) == 2
    game.undoLastMove()
    assert game.getPiece(Square(4, 4)) == None
    assert isinstance(game.getPiece(Square(4, 6)), Pawn)
    assert len(game.moveHistory) == 1

def test_that_a_piece_is_untaken_during_undoLastMove():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('E2 to E4')
    game.move('D7 to D5')
    game.move('E4 to D5')
    game.undoLastMove()
    assert isinstance(game.getPiece(Square(3, 4)), Pawn)
    assert game.getPiece(Square(3, 4)).color == game.COLOR_BLACK
    assert isinstance(game.getPiece(Square(4, 3)), Pawn)

def test_that_a_piece_is_unpromoted_if_undoLastMove_undoes_its_promotion():
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
    game.undoLastMove()
    assert isinstance(game.getPiece(Square(6, 6)), Pawn)
    assert isinstance(game.getPiece(Square(5, 7)), Bishop)

def test_that_undo_returns_false_when_no_moves_have_been_made_and_true_otherwise():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    assert game.undoLastMove() == False
    game.move('E2 to E4')
    assert game.undoLastMove() == True
    assert game.undoLastMove() == False