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

    def fullCopy(self):
        position_copy = None if self.position == None else self.position.fullCopy()
        movementRule_copy = None if self.movementRule == None else self.movementRule.fullCopy()
        return Piece(position_copy, self.color, self.symbol, movementRule_copy)

    def isAttacking(self, square, game):
        assert isinstance(square, Square)
        if self.taken or square == self.position:
            return False
        else:
            return self.movementRule.isAttacking(Move(self.position, square), game)

    def allAttackingMoves(self, game):
        if self.taken:
            return []
        else:
            return self.movementRule.allAttackingMoves(self.position, game)

    def pointValue(self):
        return self.movementRule.pointValue(self.position)