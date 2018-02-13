import MovementRule

class Piece:
    position
    idNumber
    color
    symbol

    def __init__(self, position = None, idNumber, color, symbol):
        self.position = position
        self.idNumber = idNumber
        self.color = color