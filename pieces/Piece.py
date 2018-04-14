from pieces.MovementRule import MovementRule

from Square import Square
from Move import Move

class Piece:

    def __init__(self, position = None, color = None, symbol = None, movementRule = None):
        self.position = position
        self.color = color
        self.symbol = symbol
        self.taken = False
        self.movementRule = movementRule

    def isAttacking(self, square, game):
        assert isinstance(square, Square)
        return self.movementRule.isAttacking(Move(self.position, square), game)