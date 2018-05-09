from pieces.MovementRule import MovementRule
from RuleSet import RuleSet
from Game import Game
from Ai import Ai

from color import WHITE, BLACK

import NormalChessConfig

def main():
    def promoCallback():
        return 'q'
    game = Game(NormalChessConfig.ruleSet, promoCallback)
    game.load()

    ai = Ai(4)
    gameOver = False
    while not gameOver:
        result = game.move(ai.bestMove(game))
        game.printBoard()
        print(result)
        if result == 'mate':
            gameOver = True


if __name__ == '__main__':
    main()