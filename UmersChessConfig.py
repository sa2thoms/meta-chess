from RuleSet import RuleSet
from pieces.MovementRule import MovementRule

rookMovement = MovementRule(vert=False, horiz=False, diag=False, jumps=[[3, 0], [3, 3]])
knightMovement = MovementRule(vert=False, horiz=False, diag=False, jumps=[[2, 1]])
bishopMovement = MovementRule(vert=False, horiz=False, diag=True, jumps=[])
queenMovement = MovementRule(vert=True, horiz=True, diag=True, jumps=[])

ruleSet = RuleSet(rookMovement, knightMovement, bishopMovement, queenMovement)
