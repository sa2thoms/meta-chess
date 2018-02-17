import pytest
from RuleSet import RuleSet
from Game import Game

def test_that_constructor_sets_ruleset():
    ruleSet = RuleSet(None, None, None, None)
    game = Game(ruleSet)
    assert game.ruleSet is ruleSet, 'The ruleset was not set in the game instance'

def test_that_constructor_reads_in_board_template():
    ruleSet = RuleSet(None, None, None, None)
    game = Game(ruleSet)
    with open('./board.txt', 'r') as boardFile:
        assert game.boardTemplate == boardFile.read()
