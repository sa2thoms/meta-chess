import pieces.MovementRule

class Piece:

    def __init__(self, position = None, color = None, symbol = None):
        self.position = position
        self.color = color
        self.symbol = symbol
        self.taken = False