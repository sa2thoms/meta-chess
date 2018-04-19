from Game import Game

from Square import Square
from Move import Move

class Ai:

    def __init__(self, searchDepth):
        self.searchDepth = searchDepth
        self.promoteTo = 'q'

    def setPromotionPiece(self, game):
        return 'q'

    def promotionCallback(self):
        return self.promoteTo

    def bestMove(self, game):
        return self._getBestMoveAtDepth(self.searchDepth, game)

    def _getBestMoveAtDepth(self, depth, game):
        if depth == 1:
            moves = game.allLegalMoves()
            if len(moves):
                bestMove = moves[0]
                bestWorstCase = -10000000000.0
                for move in moves:
                    game.move(move)
                    worstCase = self._worstDifferential(bestWorstCase, game)
                    if worstCase > bestWorstCase:
                        bestWorstCase = worstCase
                        bestMove = move
                    game.undoLastMove()
                return bestMove

    def _worstDifferential(self, bestWorstCase, game):
        