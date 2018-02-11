import MovementRule

class Piece:
    position
    idNumber
    color

    def __init__(self, position = None, idNumber, color):
        self.position = position
        self.idNumber = idNumber
        self.color = color