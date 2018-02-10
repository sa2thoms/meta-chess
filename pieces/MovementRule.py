

class MovementRule:
    allowsVerticalCartesian = False
    allowsHorizontalCartesian = False
    allowsDiagonal = False
    jumpRules = []

    def __init__(self, vert = False, horiz = False, diag = False, jumps = []):
        self.allowsVerticalCartesian = vert
        self.allowsHorizontalCartesian = horiz
        self.allowsDiagonal = diag
        self.jumpRules.append(jumps)
    