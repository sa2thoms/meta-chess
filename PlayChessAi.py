from pieces.MovementRule import MovementRule
from RuleSet import RuleSet
from Game import Game
from AiRepl import AiRepl

from color import WHITE, BLACK

import NormalChessConfig

def main():
    rules = NormalChessConfig.ruleSet

    searchDepth = 4
    aiRepl = AiRepl(rules, searchDepth, BLACK)
    aiRepl.run()

if __name__ == '__main__':
    main()