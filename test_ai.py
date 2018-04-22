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

from Ai import Ai

import NormalChessConfig

def test_that_ai_makes_correct_choice_for_one_move_depth():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('E2 to E4')
    game.move('E7 to E5')
    game.move('D1 to F3')
    game.move('D8 to F6')
    game.move('F3 to F5')

    ai = Ai(2)
    assert ai.bestMove(game) == Move(Square(5, 5), Square(5, 4))

def test_that_ai_makes_good_move_playing_as_white():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('E2 to E4')
    game.move('E7 to E5')
    game.move('G1 to F3')
    game.move('D8 to H4')

    ai = Ai(2)
    assert ai.bestMove(game) == Move(Square(5, 2), Square(7, 3))

def test_that_ai_does_checkmate():
    ruleSet = NormalChessConfig.ruleSet
    def promotionCallback():
        return 'q'
    game = Game(ruleSet, promotionCallback)
    game.load()
    game.move('F2 to F3')
    game.move('E7 to E5')
    game.move('G2 to G4')
    
    ai = Ai(3)
    assert ai.bestMove(game) == Move(Square(3, 7), Square(7, 3))