from RuleSet import RuleSet
from pieces.MovementRule import MovementRule

rookMovement = MovementRule(vert=True, horiz=True, diag=False, jumps=[[2, 2]])
knightMovement = MovementRule(vert=False, horiz=False, diag=False, jumps=[[2, 1], [2, 2]])
bishopMovement = MovementRule(vert=False, horiz=False, diag=True, jumps=[[1, 0]])
queenMovement = MovementRule(vert=True, horiz=True, diag=True, jumps=[[2, 1]])

ruleSet = RuleSet(rookMovement, knightMovement, bishopMovement, queenMovement)
