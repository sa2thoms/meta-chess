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

    def __init__(self, ruleSet = None):
        self.ruleSet = ruleSet

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
        
        if (isinstance(pieceForMove, Pawn)):
            self._pawnMove(pieceForMove, move)
        elif (isinstance(pieceForMove, King)):
            self._kingMove(pieceForMove, move)

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

    def _checkMoveValidity(self, move):
        pieceForMove = self.getPiece(move.start)
        if (pieceForMove == None):
            return False
        elif (pieceForMove.color != self.turn):
            return False
        elif (move.start == move.end):
            return False

        elif (isinstance(pieceForMove, Pawn)):
            return self._checkPawnValidity(pieceForMove, move)
        elif (isinstance(pieceForMove, King)):
            return self._checkKingValidity(pieceForMove, move)

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

    def _checkPawnValidity(self, pieceForMove, move):

        if (self.turn == self.COLOR_WHITE):
            oneForward = Square(move.start.file, move.start.rank + 1)
            twoForward = Square(move.start.file, move.start.rank + 2)
            if (move.end == oneForward):
                if (self.getPiece(move.end) != None):
                    return False
                else:
                    return True
            elif (move.end == twoForward):
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
            oneForward = Square(move.start.file, move.start.rank - 1)
            twoForward = Square(move.start.file, move.start.rank - 2)
            if (move.end == oneForward):
                if (self.getPiece(move.end) != None):
                    return False
                else:
                    return True
            elif (move.end == twoForward):
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


    def _pawnMove(self, pieceForMove, move):
        assert(isinstance(pieceForMove, Pawn))
        if (self.turn == self.COLOR_WHITE):
            oneForward = Square(move.start.file, move.start.rank + 1)
            twoForward = Square(move.start.file, move.start.rank + 2)
            if (move.end == oneForward):
                if (self.getPiece(move.end) != None):
                    raise IllegalMoveException('There is a piece blocking the pawn from moving forward')
                else:
                    pieceForMove.position = move.end
                    self._switchTurn()
                    record = MoveRecord(move, pieceForMove)
                    self.moveHistory.append(record)
            elif (move.end == twoForward):
                if (move.start.rank != 1):
                    raise IllegalMoveException('A pawn may only move two spaces on its first move of the game')
                elif (self.getPiece(move.end) != None):
                    raise IllegalMoveException('A pawn may not take a piece directly in front of it')
                elif (self.getPiece(oneForward) != None):
                    raise IllegalMoveException('There is a piece blocking the pawn from moving forward')
                else:
                    pieceForMove.position = move.end
                    self._switchTurn()
                    record = MoveRecord(move, pieceForMove)
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
                    self._switchTurn()
                    record = MoveRecord(move, pieceForMove, takenPiece)
                    self.moveHistory.append(record)
        elif (self.turn == self.COLOR_BLACK):
            oneForward = Square(move.start.file, move.start.rank - 1)
            twoForward = Square(move.start.file, move.start.rank - 2)
            if (move.end == oneForward):
                if (self.getPiece(move.end) != None):
                    raise IllegalMoveException('There is a piece blocking the pawn from moving forward')
                else:
                    pieceForMove.position = move.end
                    self._switchTurn()
                    record = MoveRecord(move, pieceForMove)
                    self.moveHistory.append(record)
            elif (move.end == twoForward):
                if (move.start.rank != 6):
                    raise IllegalMoveException('A pawn may only move two spaces on its first move of the game')
                elif (self.getPiece(move.end) != None):
                    raise IllegalMoveException('A pawn may not take a piece directly in front of it')
                elif (self.getPiece(oneForward) != None):
                    raise IllegalMoveException('There is a piece blocking the pawn from moving forward')
                else:
                    pieceForMove.position = move.end
                    self._switchTurn()
                    record = MoveRecord(move, pieceForMove)
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
                    self._switchTurn()
                    record = MoveRecord(move, pieceForMove, takenPiece)
                    self.moveHistory.append(record)

    def _checkKingValidity(self, move):
        if (self.turn == self.COLOR_WHITE):
            if (abs(move.end.file - move.start.file) <= 1 and abs(move.end.rank - move.start.rank) <= 1):
                if (self.getPiece(move.end) != None and self.getPiece(move.end).color == self.COLOR_WHITE):
                    return False
                else:
                    return True
            else:
                return False
        elif (self.turn == self.COLOR_BLACK):
            if (abs(move.end.file - move.start.file) <= 1 and abs(move.end.rank - move.start.rank) <= 1):
                if (self.getPiece(move.end).color == self.COLOR_BLACK):
                    return False
                else:
                    return True
            else:
                return False

    def _kingMove(self, pieceForMove, move):
        if (self.turn == self.COLOR_WHITE):
            if (abs(move.end.file - move.start.file) <= 1 and abs(move.end.rank - move.start.rank) <= 1):
                if (self.getPiece(move.end) != None and self.getPiece(move.end).color == self.COLOR_WHITE):
                    raise IllegalMoveException('You may not take your own piece')
                else:
                    takenPiece = self.getPiece(move.end)
                    if (takenPiece != None):
                        takenPiece.taken = True
                    pieceForMove.position = move.end
                    self._switchTurn()
                    record = MoveRecord(move, pieceForMove, takenPiece)
                    self.moveHistory.append(record)
            else:
                raise IllegalMoveException('A king may only move one square in any direction')
        elif (self.turn == self.COLOR_BLACK):
            if (abs(move.end.file - move.start.file) <= 1 and abs(move.end.rank - move.start.rank) <= 1):
                if (self.getPiece(move.end).color == self.COLOR_BLACK):
                    raise IllegalMoveException('You may not take your own piece')
                else:
                    takenPiece = self.getPiece(move.end)
                    if (takenPiece != None):
                        takenPiece.taken = True
                    pieceForMove.position = move.end
                    self._switchTurn()
                    record = MoveRecord(move, pieceForMove, takenPiece)
                    self.moveHistory.append(record)
            else:
                raise IllegalMoveException('A king may only move one square in any direction')
