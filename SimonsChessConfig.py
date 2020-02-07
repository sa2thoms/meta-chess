from RuleSet import RuleSet
from pieces.MovementRule import MovementRule

rookMovement = MovementRule(vert=True, horiz=True, diag=True, jumps=[])
knightMovement = MovementRule(vert=True, horiz=True, diag=True, jumps=[])
bishopMovement = MovementRule(vert=True, horiz=True, diag=True, jumps=[])
queenMovement = MovementRule(vert=True, horiz=True, diag=True, jumps=[])

ruleSet = RuleSet(rookMovement, knightMovement, bishopMovement, queenMovement)
