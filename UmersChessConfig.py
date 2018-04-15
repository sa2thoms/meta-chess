from RuleSet import RuleSet
from pieces.MovementRule import MovementRule

rookMovement = MovementRule(False, False, False, [])
knightMovement = MovementRule(False, False, False, [])
bishopMovement = MovementRule(False, False, False, [])
queenMovement = MovementRule(False, False, False, [])

ruleSet = RuleSet(rookMovement, knightMovement, bishopMovement, queenMovement)
