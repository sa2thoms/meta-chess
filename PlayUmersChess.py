from pieces.MovementRule import MovementRule
from RuleSet import RuleSet
from Game import Game
from GameRepl import GameRepl

import UmersChessConfig

def main():
    rules = UmersChessConfig.ruleSet

    game = Game(rules)

    gameRepl = GameRepl(game)
    gameRepl.run()

if __name__ == '__main__':
    main()