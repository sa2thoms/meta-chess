from RuleSet import RuleSet
from pieces.MovementRule import MovementRule

rookMovement = MovementRule(True, True, False, [])
knightMovement = MovementRule(False, False, False, [[2, 1]])
bishopMovement = MovementRule(False, False, True, [])
queenMovement = MovementRule(True, True, True, [])

ruleSet = RuleSet(rookMovement, knightMovement, bishopMovement, queenMovement)
