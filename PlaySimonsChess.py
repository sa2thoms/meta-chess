from pieces.MovementRule import MovementRule
from RuleSet import RuleSet
from Game import Game
from GameRepl import GameRepl

import SimonsChessConfig

def main():
    rules = SimonsChessConfig.ruleSet

    gameRepl = GameRepl(rules)
    gameRepl.run()

if __name__ == '__main__':
    main()