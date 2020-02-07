from Game import Game

from color import WHITE, BLACK

from Square import Square
from Move import Move

import random
import threading

def singleThreadBestMove(game, searchDepth):
    ai = Ai(searchDepth, 1)
    return ai.bestMove(game)

class Ai:

    def __init__(self, searchDepth, thread_count = 1):
        self.searchDepth = searchDepth
        self.thread_count = thread_count
        self.promoteTo = 'q'
        random.seed()

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
        if game.turn == BLACK:
            bestScoreEver = -10000000000.0
        if (self.thread_count == 1):
            return self._getBestMoveAtDepth(bestScoreEver, self.searchDepth, game).move
        else:
            return Ai._bestMoveUsingThreads(bestScoreEver, self.searchDepth, game, self.thread_count)

    def _bestMoveUsingThreads(bestScoreSoFar, depth, game, n_threads):
        moves = list(game.allLegalMoves())
        move_assignments = []
        for i in range(0, n_threads):
            move_assignments.push([])
        for i in range(0, len(moves)):
            assignee = i % n_threads
            move_assignments[assignee].push(moves[i])
        threads = []
        for i in range(0, n_threads):
            game_copy = game.fullCopy()
            thread = threading.Thread(target=singleThreadBestMove, args=(game_copy, self.searchDepth - 1))
            threads.push()

    class BestCaseMove:
        def __init__(self, move, differential):
            self.move = move
            self.differential = differential
        
        def __lt__(self, other):
            return self.differential < other.differential

        def __gt__(self, other):
            return self.differential > other.differential

    def _coinToss(self):
        return bool(random.getrandbits(1))

    def _getBestMoveAtDepth(self, bestScoreSoFar, depth, game):
        worstScoreEver = 10000000000.0
        if game.turn == WHITE:
            worstScoreEver = -10000000000.0
        isBetterThan = lambda a, b: a < b
        if game.turn == WHITE:
            isBetterThan = lambda a, b: a > b

        if depth <= 1:
            moves = list(game.allLegalMoves())
            if len(moves):
                bestScore = Ai.BestCaseMove(moves[0], worstScoreEver)
                for move in moves:
                    result = game.move(move, knownValid=True)
                    score = 0
                    if result == 'mate':
                        score = -worstScoreEver
                    else:
                        score = game.positionDifferential()
                    if isBetterThan(score, bestScore.differential):
                        bestScore.move = move
                        bestScore.differential = score
                    elif score == bestScore.differential and self._coinToss():
                        bestScore.move = move
                        bestScore.differential = score
                    game.undoLastMove()
                    if isBetterThan(score, bestScoreSoFar):
                        break
                return bestScore
            else:
                return Ai.BestCaseMove(None, worstScoreEver)
        else:
            moves = list(game.allLegalMoves())
            if len(moves):
                bestScore = Ai.BestCaseMove(moves[0], worstScoreEver)
                for move in moves:
                    result = game.move(move, knownValid=True)
                    score = 0
                    if result == 'mate':
                        # multiply by depth so that earlier mates are prefered
                        score = -worstScoreEver * depth
                    else:
                        score = self._getBestMoveAtDepth(bestScore.differential, depth - 1, game).differential
                    if isBetterThan(score, bestScore.differential):
                        bestScore.move = move
                        bestScore.differential = score
                    elif score == bestScore.differential and self._coinToss():
                        bestScore.move = move
                        bestScore.differential = score
                    game.undoLastMove()
                    if isBetterThan(score, bestScoreSoFar):
                        break
                return bestScore
            else:
                return Ai.BestCaseMove(None, worstScoreEver)
