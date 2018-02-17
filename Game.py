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
            self.whitePieces.append(Pawn(position=[i, 1], color=self.COLOR_WHITE))
            self.blackPieces.append(Pawn(position=[i, 6], color=self.COLOR_BLACK))

        self._loadPowerPieces(self.COLOR_WHITE)
        self._loadPowerPieces(self.COLOR_BLACK)

        self.turn = self.COLOR_WHITE

    def printBoard(self):
        template = self.boardTemplate
        for row in range(0, 8):
            for col in range(0, 8):
                pieceAtLocation = self.getPiece([col, row])
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

    def move(self, moveString):
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

        startPosition = spaceCodes[0]
        endPosition = spaceCodes[1]
        pieceForMove = self.getPiece(startPosition)
        if (pieceForMove == None):
            raise IllegalMoveException('There is no piece at the starting location')
        if (pieceForMove.color != self.turn):
            raise IllegalMoveException('Wrong colored piece')
        
        if (isinstance(pieceForMove, Pawn)):
            self._pawnMove(pieceForMove, startPosition, endPosition)



                
    def _switchTurn(self):
        if (self.turn == self.COLOR_WHITE):
            self.turn = self.COLOR_BLACK
        else:
            self.turn = self.COLOR_WHITE
    
    def getPiece(self, position):
        assert(len(position) == 2)
        for piece in self.whitePieces:
            if piece.position == position and piece.taken == False:
                return piece
        for piece in self.blackPieces:
            if piece.position == position and piece.taken == False:
                return piece
        return None

    def _loadPowerPieces(self, color):
        row = color * 7
        teamList = self.whitePieces
        if color == self.COLOR_BLACK:
            teamList = self.blackPieces

        teamList.append(Rook(position=[0, row], color=color, movementRule=self.ruleSet.rookMovement))
        teamList.append(Knight(position=[1, row], color=color, movementRule=self.ruleSet.knightMovement))
        teamList.append(Bishop(position=[2, row], color=color, movementRule=self.ruleSet.bishopMovement))
        teamList.append(Queen(position=[3, row], color=color, movementRule=self.ruleSet.queenMovement))
        teamList.append(King(position=[4, row], color=color))
        teamList.append(Bishop(position=[5, row], color=color, movementRule=self.ruleSet.bishopMovement))
        teamList.append(Knight(position=[6, row], color=color, movementRule=self.ruleSet.knightMovement))
        teamList.append(Rook(position=[7, row], color=color, movementRule=self.ruleSet.rookMovement))

    def _pawnMove(self, pieceForMove, startPosition, endPosition):
        assert(isinstance(pieceForMove, Pawn))
        if (self.turn == self.COLOR_WHITE):
            if (endPosition == [startPosition[0], startPosition[1] + 1]):
                if (self.getPiece(endPosition) != None):
                    raise IllegalMoveException('There is a piece blocking the pawn from moving forward')
                else:
                    pieceForMove.position = endPosition
                    self._switchTurn()
                    record = MoveRecord(startPosition, endPosition, pieceForMove)
                    self.moveHistory.append(record)
            elif (endPosition == [startPosition[0], startPosition[1] + 2]):
                if (startPosition[1] != 1):
                    raise IllegalMoveException('A pawn may only move two spaces on its first move of the game')
                if (self.getPiece(endPosition) != None):
                    raise IllegalMoveException('A pawn may not take a piece directly in front of it')
                if (self.getPiece([startPosition[0], startPosition[1] + 1]) != None):
                    raise IllegalMoveException('There is a piece blocking the pawn from moving forward')
                else:
                    pieceForMove.position = endPosition
                    self._switchTurn()
                    record = MoveRecord(startPosition, endPosition, pieceForMove)
                    self.moveHistory.append(record)
            elif (startPosition[1] + 1 == endPosition[1] and abs(startPosition[0] - endPosition[0]) == 1):
                if (self.getPiece(endPosition) == None):
                    raise IllegalMoveException('Pawns can only move diagonally to take')
                if (self.getPiece(endPosition).color == self.COLOR_WHITE):
                    raise IllegalMoveException('You may not take your own piece')
                else:
                    takenPiece = self.getPiece(endPosition)
                    takenPiece.taken = True
                    pieceForMove.position = endPosition
                    self._switchTurn()
                    record = MoveRecord(startPosition, endPosition, pieceForMove, takenPiece)
                    self.moveHistory.append(record)
        if (self.turn == self.COLOR_BLACK):
            if (endPosition == [startPosition[0], startPosition[1] - 1]):
                if (self.getPiece(endPosition) != None):
                    raise IllegalMoveException('There is a piece blocking the pawn from moving forward')
                else:
                    pieceForMove.position = endPosition
                    self._switchTurn()
                    record = MoveRecord(startPosition, endPosition, pieceForMove)
                    self.moveHistory.append(record)
            elif (endPosition == [startPosition[0], startPosition[1] - 2]):
                if (startPosition[1] != 6):
                    raise IllegalMoveException('A pawn may only move two spaces on its first move of the game')
                if (self.getPiece(endPosition) != None):
                    raise IllegalMoveException('A pawn may not take a piece directly in front of it')
                if (self.getPiece([startPosition[0], startPosition[1] - 1]) != None):
                    raise IllegalMoveException('There is a piece blocking the pawn from moving forward')
                else:
                    pieceForMove.position = endPosition
                    self._switchTurn()
                    record = MoveRecord(startPosition, endPosition, pieceForMove)
                    self.moveHistory.append(record)
            elif (startPosition[1] - 1 == endPosition[1] and abs(startPosition[0] - endPosition[0]) == 1):
                if (self.getPiece(endPosition) == None):
                    raise IllegalMoveException('Pawns can only move diagonally to take')
                if (self.getPiece(endPosition).color == self.COLOR_BLACK):
                    raise IllegalMoveException('You may not take your own piece')
                else:
                    takenPiece = self.getPiece(endPosition)
                    takenPiece.taken = True
                    pieceForMove.position = endPosition
                    self._switchTurn()
                    record = MoveRecord(startPosition, endPosition, pieceForMove, takenPiece)
                    self.moveHistory.append(record)