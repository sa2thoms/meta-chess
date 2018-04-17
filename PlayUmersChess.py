from pieces.MovementRule import MovementRule
from RuleSet import RuleSet
from Game import Game
from GameRepl import GameRepl

import UmersChessConfig

def main():
    rules = UmersChessConfig.ruleSet

    gameRepl = GameRepl(rules)
    gameRepl.run()

if __name__ == '__main__':
    main()