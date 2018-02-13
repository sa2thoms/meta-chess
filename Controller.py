from Game import Game
from RuleSet import RuleSet

def main():
    ruleSet = RuleSet(rookMovement=None, knightMovement=None, bishopMovement=None, queenMovement=None)
    game = Game(ruleSet)
    game.loadPieces()
    game.fullPrint()

if __name__ == '__main__':
    main()
