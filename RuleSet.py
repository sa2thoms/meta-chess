import pieces.MovementRule

class RuleSet:

    def __init__(self, rookMovement, knightMovement, bishopMovement, queenMovement):
        self.rookMovement = rookMovement
        self.knightMovement = knightMovement
        self.bishopMovement = bishopMovement
        self.queenMovement = queenMovement
