from pieces.Piece import Piece

class Knight(Piece):

    def __init__(self, position, color, symbol='kn', movementRule = None):
        Piece.__init__(self, position, color, symbol, movementRule)

    def fullCopy(self):
        position_copy = None if self.position == None else self.position.fullCopy()
        movementRule_copy = None if self.movementRule == None else self.movementRule.fullCopy()
        return Knight(position_copy, self.color, self.symbol, movementRule_copy)
