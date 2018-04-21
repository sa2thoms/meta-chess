from Game import Game

from Square import Square
from Move import Move

class Ai:

    def __init__(self, searchDepth):
        self.searchDepth = searchDepth
        self.promoteTo = 'q'

    def setPromotionPiece(self, game):
        bestScore = 0.0
        if game.ruleSet.queenMovement.pointValue(Square(7, 7)) > bestScore:
            bestScore = game.ruleSet.queenMovement.pointValue(Square(7, 7))
            self.promoteTo = 'q'
        if game.ruleSet.bishopMovement.pointValue(Square(7, 7)) > bestScore:
            bestScore = game.ruleSet.bishopMovement.pointValue(Square(7, 7))
            self.promoteTo = 'b'
        if game.ruleSet.knightMovement.pointValue(Square(7, 7)) > bestScore:
            bestScore = game.ruleSet.knightMovement.pointValue(Square(7, 7))
            self.promoteTo = 'k'
        if game.ruleSet.rookMovement.pointValue(Square(7, 7)) > bestScore:
            bestScore = game.ruleSet.rookMovement.pointValue(Square(7, 7))
            self.promoteTo = 'r'

    def promotionCallback(self):
        return self.promoteTo

    def bestMove(self, game):
        bestScoreEver = 10000000000.0
        if game.turn == Game.COLOR_BLACK:
            bestScoreEver = -10000000000.0
        return self._getBestMoveAtDepth(bestScoreEver, self.searchDepth, game).move

    class BestCaseMove:
        def __init__(self, move, differential):
            self.move = move
            self.differential = differential
        
        def __lt__(self, other):
            return self.differential < other.differential

        def __gt__(self, other):
            return self.differential > other.differential

    def _getBestMoveAtDepth(self, bestScoreSoFar, depth, game):
        worstScoreEver = 10000000000.0
        if game.turn == Game.COLOR_WHITE:
            worstScoreEver = -10000000000.0
        isBetterThan = lambda a, b: a < b
        if game.turn == Game.COLOR_WHITE:
            isBetterThan = lambda a, b: a > b

        if depth <= 1:
            moves = list(game.allLegalMoves())
            if len(moves):
                bestScore = Ai.BestCaseMove(moves[0], worstScoreEver)
                for move in moves:
                    game.move(move, knownValid=True)
                    score = game.positionDifferential()
                    if isBetterThan(score, bestScore.differential):
                        bestScore.move = move
                        bestScore.differential = score
                    game.undoLastMove()
                    if isBetterThan(score, bestScoreSoFar):
                        break
                return bestScore
        else:
            moves = list(game.allLegalMoves())
            if len(moves):
                bestScore = Ai.BestCaseMove(moves[0], worstScoreEver)
                for move in moves:
                    game.move(move, knownValid=True)
                    score = self._getBestMoveAtDepth(bestScore.differential, depth - 1, game).differential
                    if isBetterThan(score, bestScore.differential):
                        bestScore.move = move
                        bestScore.differential = score
                    game.undoLastMove()
                    if isBetterThan(score, bestScoreSoFar):
                        break
                return bestScore
