import re

from pieces.Piece import Piece
from pieces.Pawn import Pawn
from pieces.King import King
from pieces.Queen import Queen
from pieces.Rook import Rook
from pieces.Knight import Knight
from pieces.Bishop import Bishop

from RuleSet import RuleSet
from MoveRecord import MoveRecord
from Square import Square
from Move import Move

from NoRuleException import NoRuleException
from IllegalMoveException import IllegalMoveException
from InvalidMoveStringException import InvalidMoveStringException

class bcolors:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Game:

    def __init__(self, ruleSet, promotionCallback):
        self.ruleSet = ruleSet
        self.promotionCallback = promotionCallback

        self.whitePieces = []
        self.blackPieces = []

        self.COLOR_WHITE = 0
        self.COLOR_BLACK = 1
        self.turn = self.COLOR_WHITE

        self.moveHistory = []

        BOARD_FILE = './board.txt'
        with open(BOARD_FILE, 'r') as boardFile:
            self.boardTemplate = boardFile.read()

    def isLoaded(self):
        return len(self.whitePieces) > 0 or len(self.blackPieces) > 0

    def load(self):
        if (self.ruleSet == None):
            raise NoRuleException('There is no rule set from which to load the game')

        if (len(self.whitePieces) != 0 or len(self.blackPieces) != 0):
            raise Exception('Game is already loaded')

        for i in range(0, 8):
            self.whitePieces.append(Pawn(position=Square(i, 1), color=self.COLOR_WHITE))
            self.blackPieces.append(Pawn(position=Square(i, 6), color=self.COLOR_BLACK))

        self._loadPowerPieces(self.COLOR_WHITE)
        self._loadPowerPieces(self.COLOR_BLACK)

        self.turn = self.COLOR_WHITE

    def printBoard(self):
        template = self.boardTemplate
        for row in range(0, 8):
            for col in range(0, 8):
                square = Square(col, row)
                pieceAtLocation = self.getPiece(square)
                symb = '  '
                if pieceAtLocation != None:
                    colorCode = bcolors.BLUE
                    if pieceAtLocation.color == self.COLOR_WHITE:
                        colorCode = bcolors.PINK
                    elif pieceAtLocation.color == self.COLOR_BLACK:
                        colorCode = bcolors.GREEN
                    symb = colorCode + pieceAtLocation.symbol + bcolors.ENDC
                locationCode = chr(ord('A') + col) + chr(ord('0') + row)
                template = template.replace(locationCode, symb)
        print(template)

    def _moveFromMoveString(self, moveString):
        assert isinstance(moveString, str)
        validMs = re.compile(r'^\s*[A-H][1-8] +to +[A-H][1-8]\s*$')
        if validMs.fullmatch(moveString) == None:
            raise InvalidMoveStringException('Move string not valid')

        spaceStrings = moveString.split(" to ")
        for spaceString in spaceStrings:
            spaceString = spaceString.strip()
        
        spaceCodes = []
        for spaceString in spaceStrings:
            col = ord(spaceString[0]) - ord('A')
            row = ord(spaceString[1]) - ord('1')
            spaceCodes.append([col, row])
        startSquare = Square(spaceCodes[0][0], spaceCodes[0][1])
        endSquare = Square(spaceCodes[1][0], spaceCodes[1][1])

        return Move(startSquare, endSquare)

    def oppositeColor(self, color):
        if color == self.COLOR_BLACK:
            return self.COLOR_WHITE
        elif color == self.COLOR_WHITE:
            return self.COLOR_BLACK
        else:
            raise Exception('Not a valid color')
    
    def move(self, moveIn):
        move = moveIn
        if (isinstance(move, str)):
            move = self._moveFromMoveString(moveIn)

        pieceForMove = self.getPiece(move.start)
        if (pieceForMove == None):
            raise IllegalMoveException('There is no piece at the starting location')
        elif (pieceForMove.color != self.turn):
            raise IllegalMoveException('Wrong colored piece')
        elif (move.start == move.end):
            raise IllegalMoveException('The piece cannot move to where it already was')
        elif not self.isValidMove(move):
            raise IllegalMoveException('That move is not allowed')

        if (isinstance(pieceForMove, Pawn)):
            self._pawnMove(pieceForMove, move)
        else:
            takenPiece = None
            if self.getPiece(move.end):
                takenPiece = self.getPiece(move.end)
                takenPiece.taken = True
            pieceForMove.position = move.end
            self._switchTurn()
            record = MoveRecord(move, pieceForMove, takenPiece)
            self.moveHistory.append(record)

        if self.isKingAttacked(self.oppositeColor(pieceForMove.color)):
            if self.checkForMate(self.oppositeColor(pieceForMove.color)):
                return 'mate'
            else:
                return 'check'
        else:
            return 'success'

    def undoLastMove(self):
        if len(self.moveHistory) == 0:
            return False
        record = self.moveHistory.pop()
        record.pieceInMotion.position = record.move.start
        if record.pieceTaken:
            record.pieceTaken.taken = False
        if record.piecePromotedTo:
            record.pieceInMotion.taken = False
            self.whitePieces.remove(record.piecePromotedTo)
        return True

    def isValidMove(self, move):
        if (isinstance(move, str)):
            return self._checkMoveValidity(self._moveFromMoveString(move))
        else:
            return self._checkMoveValidity(move)

    def isAttacking(self, move):
        moveArray = move
        if (isinstance(move, str)):
            moveArray = self._moveFromMoveString(move)
        
        pieceForMove = self.getPiece(moveArray.start)
        if (pieceForMove):
            return pieceForMove.isAttacking(moveArray.end, self)
        else:
            return False

    def _getKing(self, color):
        if (color == self.COLOR_WHITE):
            for piece in self.whitePieces:
                if isinstance(piece, King):
                    return piece
        elif (color == self.COLOR_BLACK):
            for piece in self.blackPieces:
                if isinstance(piece, King):
                    return piece

    def isKingAttacked(self, color):
        king = self._getKing(color)
        if (color == self.COLOR_WHITE):
            for piece in self.blackPieces:
                if (not piece.taken) and self.isAttacking(Move(piece.position, king.position)):
                    return True
            return False
        elif (color == self.COLOR_BLACK):
            for piece in self.whitePieces:
                if (not piece.taken) and self.isAttacking(Move(piece.position, king.position)):
                    return True
            return False

    def checkForMate(self, color):
        if not self.isKingAttacked(color):
            return False
        else:
            #check moves the king can make
            king = self._getKing(color)
            fstart = king.position.file - 1
            if fstart < 0:
                fstart = 0
            rstart = king.position.rank - 1
            if rstart < 0:
                rstart = 0
            fend = king.position.file + 1
            if fend > 7:
                fend = 7
            rend = king.position.rank + 1
            if rend > 7:
                rend = 7
            for fcount in range(fstart, fend + 1):
                for rcount in range(rstart, rend + 1):
                    square = Square(fcount, rcount)
                    if square != king.position:
                        if self.isValidMove(Move(king.position, square)):
                            return False
            
            #TODO: now check moves ending on the checking piece (for performance)

            # now check all moves (4096 combinations)
            for fstart in range(0, 8):
                for rstart in range(0, 8):
                    startSquare = Square(fstart, rstart)
                    for fend in range(0, 8):
                        for rend in range(0, 8):
                            endSquare = Square(fend, rend)
                            if startSquare != endSquare:
                                if self.isValidMove(Move(startSquare, endSquare)):
                                    return False
            
            return True


    def _checkMoveValidity(self, move):
        assert isinstance(move, Move)
        pieceForMove = self.getPiece(move.start)
        if (pieceForMove == None):
            return False
        elif (pieceForMove.color != self.turn):
            return False
        elif (move.start == move.end):
            return False

        takenPiece = self.getPiece(move.end)
        pieceForMove.position = move.end
        if takenPiece:
            takenPiece.taken = True
        if self.isKingAttacked(pieceForMove.color):
            pieceForMove.position = move.start
            if takenPiece:
                takenPiece.taken = False
            return False
        pieceForMove.position = move.start
        if takenPiece:
            takenPiece.taken = False

        if (isinstance(pieceForMove, Pawn)):
            return self._checkPawnValidity(move)
        else:
            if pieceForMove.isAttacking(move.end, self):
                if self.getPiece(move.end) and self.getPiece(move.end).color == pieceForMove.color:
                    return False
                else:
                    return True
            else:
                return False

    def _switchTurn(self):
        if (self.turn == self.COLOR_WHITE):
            self.turn = self.COLOR_BLACK
        else:
            self.turn = self.COLOR_WHITE
    
    def getPiece(self, position):
        assert(isinstance(position, Square))
        for piece in self.whitePieces:
            if piece.position == position and piece.taken == False:
                return piece
        for piece in self.blackPieces:
            if piece.position == position and piece.taken == False:
                return piece
        return None

    def _loadPowerPieces(self, color):
        rank = color * 7
        teamList = self.whitePieces
        if color == self.COLOR_BLACK:
            teamList = self.blackPieces

        teamList.append(Rook(position = Square(0, rank), color=color, movementRule=self.ruleSet.rookMovement))
        teamList.append(Knight(position = Square(1, rank), color=color, movementRule=self.ruleSet.knightMovement))
        teamList.append(Bishop(position = Square(2, rank), color=color, movementRule=self.ruleSet.bishopMovement))
        teamList.append(Queen(position = Square(3, rank), color=color, movementRule=self.ruleSet.queenMovement))
        teamList.append(King(position = Square(4, rank), color=color))
        teamList.append(Bishop(position = Square(5, rank), color=color, movementRule=self.ruleSet.bishopMovement))
        teamList.append(Knight(position = Square(6, rank), color=color, movementRule=self.ruleSet.knightMovement))
        teamList.append(Rook(position = Square(7, rank), color=color, movementRule=self.ruleSet.rookMovement))

    def _checkPawnValidity(self, move):

        if (self.turn == self.COLOR_WHITE):
            oneForward = None
            if move.start.rank + 1 < 8:
                oneForward = Square(move.start.file, move.start.rank + 1)
            twoForward = None
            if move.start.rank + 2 < 8:
                twoForward = Square(move.start.file, move.start.rank + 2)
            if oneForward and (move.end == oneForward):
                if (self.getPiece(move.end) != None):
                    return False
                else:
                    return True
            elif twoForward and (move.end == twoForward):
                if (move.start.rank != 1):
                    return False
                elif (self.getPiece(move.end) != None):
                    return False
                elif (self.getPiece(oneForward) != None):
                    return False
                else:
                    return True
            elif (move.start.rank + 1 == move.end.rank and abs(move.start.file - move.end.file) == 1):
                if (self.getPiece(move.end) == None):
                    if (len(self.moveHistory) == 0):
                        return False
                    previousMove = self.moveHistory[-1]
                    if (move.start.rank == 4 and previousMove.move.start == Square(move.end.file, 6) and previousMove.move.end == Square(move.end.file, 4) and isinstance(previousMove.pieceInMotion, Pawn)):
                        # This is where the pawn takes en passant
                        return True
                    else:
                        return False
                elif (self.getPiece(move.end).color == self.COLOR_WHITE):
                    return False
                else:
                    return True
        elif (self.turn == self.COLOR_BLACK):
            oneForward = None
            if move.start.rank - 1 >= 0:
                oneForward = Square(move.start.file, move.start.rank - 1)
            twoForward = None
            if move.start.rank - 2 >= 0:
                twoForward = Square(move.start.file, move.start.rank - 2)
            if oneForward and (move.end == oneForward):
                if (self.getPiece(move.end) != None):
                    return False
                else:
                    return True
            elif twoForward and (move.end == twoForward):
                if (move.start.rank != 6):
                    return False
                elif (self.getPiece(move.end) != None):
                    return False
                elif (self.getPiece(oneForward) != None):
                    return False
                else:
                    return True
            elif (move.start.rank - 1 == move.end.rank and abs(move.start.file - move.end.file) == 1):
                if (self.getPiece(move.end) == None):
                    if (len(self.moveHistory) == 0):
                        return False
                    previousMove = self.moveHistory[-1]
                    if (move.start.rank == 3 and previousMove.move.start == Square(move.end.file, 1) and previousMove.move.end == Square(move.end.file, 3) and isinstance(previousMove.pieceInMotion, Pawn)):
                        # This is where the pawn takes en passant
                        return True
                    else:
                        return False
                elif (self.getPiece(move.end).color == self.COLOR_BLACK):
                    return False
                else:
                    return True

    def getPromotionPiece(self, pawn):
        choice = self.promotionCallback()
        if choice == 'q':
            return Queen(pawn.position, pawn.color, movementRule=self.ruleSet.queenMovement)
        elif choice == 'b':
            return Bishop(pawn.position, pawn.color, movementRule=self.ruleSet.bishopMovement)
        elif choice == 'k':
            return Knight(pawn.position, pawn.color, movementRule=self.ruleSet.knightMovement)
        elif choice == 'r':
            return Rook(pawn.position, pawn.color, movementRule=self.ruleSet.rookMovement)
        else:
            raise Exception('The promotion callback did not return an expected piece letter')

    def _pawnMove(self, pieceForMove, move):
        assert(isinstance(pieceForMove, Pawn))
        if (self.turn == self.COLOR_WHITE):
            oneForward = None
            if move.start.rank + 1 < 8:
                oneForward = Square(move.start.file, move.start.rank + 1)
            twoForward = None
            if move.start.rank + 2 < 8:
                twoForward = Square(move.start.file, move.start.rank + 2)
            if oneForward and (move.end == oneForward):
                if (self.getPiece(move.end) != None):
                    raise IllegalMoveException('There is a piece blocking the pawn from moving forward')
                else:
                    pieceForMove.position = move.end
                    piecePromotedTo = None
                    if pieceForMove.position.rank == 7:
                        piecePromotedTo = self.getPromotionPiece(pieceForMove)
                        self.whitePieces.append(piecePromotedTo)
                        pieceForMove.taken = True
                    self._switchTurn()
                    record = MoveRecord(move, pieceForMove, piecePromotedTo=piecePromotedTo)
                    self.moveHistory.append(record)
            elif twoForward and (move.end == twoForward):
                if (move.start.rank != 1):
                    raise IllegalMoveException('A pawn may only move two spaces on its first move of the game')
                elif (self.getPiece(move.end) != None):
                    raise IllegalMoveException('A pawn may not take a piece directly in front of it')
                elif (self.getPiece(oneForward) != None):
                    raise IllegalMoveException('There is a piece blocking the pawn from moving forward')
                else:
                    pieceForMove.position = move.end
                    piecePromotedTo = None
                    if pieceForMove.position.rank == 7:
                        piecePromotedTo = self.getPromotionPiece(pieceForMove)
                        self.whitePieces.append(piecePromotedTo)
                        pieceForMove.taken = True
                    self._switchTurn()
                    record = MoveRecord(move, pieceForMove, piecePromotedTo=piecePromotedTo)
                    self.moveHistory.append(record)
            elif (move.start.rank + 1 == move.end.rank and abs(move.start.file - move.end.file) == 1):
                if (self.getPiece(move.end) == None):
                    if (len(self.moveHistory) == 0):
                        raise IllegalMoveException('You cannot move a pawn diagonally except to take')
                    previousMove = self.moveHistory[-1]
                    if (move.start.rank == 4 and previousMove.move.start == Square(move.end.file, 6) and previousMove.move.end == Square(move.end.file, 4) and isinstance(previousMove.pieceInMotion, Pawn)):
                        # This is where the pawn takes en passant
                        takenPiece = previousMove.pieceInMotion
                        takenPiece.taken = True
                        pieceForMove.position = move.end
                        self._switchTurn()
                        record = MoveRecord(move, pieceForMove, takenPiece)
                        self.moveHistory.append(record)
                    else:
                        raise IllegalMoveException('Pawns can only move diagonally to take')
                elif (self.getPiece(move.end).color == self.COLOR_WHITE):
                    raise IllegalMoveException('You may not take your own piece')
                else:
                    takenPiece = self.getPiece(move.end)
                    takenPiece.taken = True
                    pieceForMove.position = move.end
                    piecePromotedTo = None
                    if pieceForMove.position.rank == 7:
                        piecePromotedTo = self.getPromotionPiece(pieceForMove)
                        self.whitePieces.append(piecePromotedTo)
                        pieceForMove.taken = True
                    self._switchTurn()
                    record = MoveRecord(move, pieceForMove, pieceTaken=takenPiece, piecePromotedTo=piecePromotedTo)
                    self.moveHistory.append(record)
        elif (self.turn == self.COLOR_BLACK):
            oneForward = None
            if move.start.rank - 1 >= 0:
                oneForward = Square(move.start.file, move.start.rank - 1)
            twoForward = None
            if move.start.rank - 2 >= 0:
                twoForward = Square(move.start.file, move.start.rank - 2)
            if oneForward and (move.end == oneForward):
                if (self.getPiece(move.end) != None):
                    raise IllegalMoveException('There is a piece blocking the pawn from moving forward')
                else:
                    pieceForMove.position = move.end
                    piecePromotedTo = None
                    if pieceForMove.position.rank == 0:
                        piecePromotedTo = self.getPromotionPiece(pieceForMove)
                        self.blackPieces.append(piecePromotedTo)
                        pieceForMove.taken = True
                    self._switchTurn()
                    record = MoveRecord(move, pieceForMove, piecePromotedTo=piecePromotedTo)
                    self.moveHistory.append(record)
            elif twoForward and (move.end == twoForward):
                if (move.start.rank != 6):
                    raise IllegalMoveException('A pawn may only move two spaces on its first move of the game')
                elif (self.getPiece(move.end) != None):
                    raise IllegalMoveException('A pawn may not take a piece directly in front of it')
                elif (self.getPiece(oneForward) != None):
                    raise IllegalMoveException('There is a piece blocking the pawn from moving forward')
                else:
                    pieceForMove.position = move.end
                    piecePromotedTo = None
                    if pieceForMove.position.rank == 0:
                        piecePromotedTo = self.getPromotionPiece(pieceForMove)
                        self.blackPieces.append(piecePromotedTo)
                        pieceForMove.taken = True
                    self._switchTurn()
                    record = MoveRecord(move, pieceForMove, piecePromotedTo=piecePromotedTo)
                    self.moveHistory.append(record)
            elif (move.start.rank - 1 == move.end.rank and abs(move.start.file - move.end.file) == 1):
                if (self.getPiece(move.end) == None):
                    if (len(self.moveHistory) == 0):
                        raise IllegalMoveException('A pawn cannot move diagonally except to take')
                    previousMove = self.moveHistory[-1]
                    if (move.start.rank == 3 and previousMove.move.start == Square(move.end.file, 1) and previousMove.move.end == Square(move.end.file, 3) and isinstance(previousMove.pieceInMotion, Pawn)):
                        # This is where the pawn takes en passant
                        takenPiece = previousMove.pieceInMotion
                        takenPiece.taken = True
                        pieceForMove.position = move.end
                        self._switchTurn()
                        record = MoveRecord(move, pieceForMove, takenPiece)
                        self.moveHistory.append(record)
                    else:
                        raise IllegalMoveException('Pawns can only move diagonally to take')
                elif (self.getPiece(move.end).color == self.COLOR_BLACK):
                    raise IllegalMoveException('You may not take your own piece')
                else:
                    takenPiece = self.getPiece(move.end)
                    takenPiece.taken = True
                    pieceForMove.position = move.end
                    piecePromotedTo = None
                    if pieceForMove.position.rank == 0:
                        piecePromotedTo = self.getPromotionPiece(pieceForMove)
                        self.blackPieces.append(piecePromotedTo)
                        pieceForMove.taken = True
                    self._switchTurn()
                    record = MoveRecord(move, pieceForMove, pieceTaken=takenPiece, piecePromotedTo=piecePromotedTo)
                    self.moveHistory.append(record)

