from pieces.MovementRule import MovementRule
from RuleSet import RuleSet
from Game import Game
from AiRepl import AiRepl

import NormalChessConfig

def main():
    rules = NormalChessConfig.ruleSet

    aiRepl = AiRepl(rules, 1, Game.COLOR_BLACK)
    aiRepl.run()

if __name__ == '__main__':
    main()