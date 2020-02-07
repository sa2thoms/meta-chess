from Game import Game

from color import WHITE, BLACK

from Square import Square
from Move import Move

import random
import threading

def coinToss():
    return bool(random.getrandbits(1))

def aiThreadTask(game, searchDepth, assigned_moves, best_move, best_move_sem):

    assert len(best_move) == 1
    worstScoreEver = 10000000000.0
    if game.turn == WHITE:
        worstScoreEver = -10000000000.0
    isBetterThan = lambda a, b: a < b
    if game.turn == WHITE:
        isBetterThan = lambda a, b: a > b

    if len(assigned_moves):
        bestScore = Ai.BestCaseMove(assigned_moves[0], worstScoreEver)
        for move in assigned_moves:
            result = game.move(move, knownValid=True)
            score = 0
            if result == 'mate':
                # multiply by depth so that earlier mates are prefered
                score = -worstScoreEver * searchDepth
            else:
                score = singleThreadBestMove(bestScore.differential, searchDepth - 1, game).differential
            if isBetterThan(score, bestScore.differential):
                bestScore.move = move
                bestScore.differential = score
            elif score == bestScore.differential and coinToss():
                bestScore.move = move
                bestScore.differential = score
            game.undoLastMove()
        best_move_sem.acquire()
        if (best_move[0] == None):
            best_move[0] = bestScore
        elif (isBetterThan(bestScore.differential, best_move[0].differential)):
            best_move[0] = bestScore
        best_move_sem.release()


def singleThreadBestMove(differential, searchDepth, game):
    ai = Ai(searchDepth, 1)
    return ai._getBestMoveAtDepth(differential, searchDepth, game)

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
        if (self.thread_count == 1 or self.searchDepth < 3):
            return self._getBestMoveAtDepth(bestScoreEver, self.searchDepth, game).move
        else:
            return self._bestMoveUsingThreads(bestScoreEver, self.searchDepth, game, self.thread_count)

    def _bestMoveUsingThreads(self, bestScoreSoFar, depth, game, n_threads):
        moves = list(game.allLegalMoves())
        move_assignments = []
        for i in range(0, n_threads):
            move_assignments.append([])
        for i in range(0, len(moves)):
            assignee = i % n_threads
            move_assignments[assignee].append(moves[i])
        threads = []
        best_move = [None] # this will be written to by threads
        best_move_sem = threading.Semaphore(1)

        for i in range(0, n_threads):
            game_copy = game.fullCopy()
            thread = threading.Thread(target=aiThreadTask, args=(game_copy, depth, move_assignments[i], best_move, best_move_sem))
            threads.append((thread, game_copy))
            thread.start()
        for thread_tuple in threads:
            thread = thread_tuple[0]
            thread.join()
        return None if (best_move[0] == None) else best_move[0].move
            

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
