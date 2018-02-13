import pieces.MovementRule

class Piece:
    position = None
    idNumber = None
    color = None
    symbol = None

    def __init__(self, position, idNumber, color, symbol):
        self.position = position
        self.idNumber = idNumber
        self.color = color
        self.symbol = symbol