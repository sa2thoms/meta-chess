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
        return self._getBestMoveAtDepth(self.searchDepth, game).move

    class BestCaseMove:
        def __init__(self, move, differential):
            self.move = move
            self.differential = differential
        
        def __lt__(self, other):
            return self.differential < other.differential

        def __gt__(self, other):
            return self.differential > other.differential

    def _getBestMoveAtDepth(self, depth, game):
        moves = game.allLegalMoves()
        if len(moves):
            bestScore = Ai.BestCaseMove(move[0], -100000000.0)
            for move in moves:
                game.move(move)
                score = self._worstDifferential(bestScore.differential, depth, game)
                if score > bestScore.differential:
                    bestScore.move = move
                    bestScore.differential = score
                game.undoLastMove()
            return bestScore

    def _worstDifferential(self, bestScoreSoFar, depth, game):
        if depth == 1:
            moves = game.allLegalMoves()
            if len(moves):
                worstScore = Ai.BestCaseMove(moves[0], 100000000000.0)
                for move in moves:
                    game.move(move)
                    score = -game.positionDifferential()
                    if score < worstScore.differential:
                        worstScore.move = move
                        worstScore.differential = score
                    game.undoLastMove()
                    if score < bestScoreSoFar:
                        break
                return worstScore
        else:
            moves = game.allLegalMoves()
            if len(moves):
                worstScore = Ai.BestCaseMove(move[0], 1000000000000.0)
                for move in moves:
                    game.move(move)
                    score = self._getBestMoveAtDepth(depth - 1, game).differential
                    if score < worstScore.differential:
                        worstScore.move = move
                        worstScore.differential = score
                    game.undoLastMove()
                    if score < bestScoreSoFar:
                        break
                return worstScore