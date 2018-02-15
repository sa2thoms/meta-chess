from pieces.MovementRule import MovementRule
from RuleSet import RuleSet
from Game import Game
from GameRepl import GameRepl

def main():
    knight = MovementRule(vert=False, horiz=False, diag=False, jumps=[[2, 1]])
    bishop = MovementRule(vert=False, horiz=False, diag=True)
    rook = MovementRule(vert=True, horiz=True, diag=False)
    queen = MovementRule(vert=True, horiz=True, diag=True)
    
    rules = RuleSet(rook, knight, bishop, queen)

    game = Game(rules)

    gameRepl = GameRepl(game)
    gameRepl.run()

if __name__ == '__main__':
    main()