from RuleSet import RuleSet
from pieces.Piece import Piece
from pieces.Pawn import Pawn
from pieces.King import King
from pieces.Queen import Queen
from pieces.Rook import Rook
from pieces.Knight import Knight
from pieces.Bishop import Bishop
from NoRuleException import NoRuleException
from IllegalMoveException import IllegalMoveException
from InvalidMoveStringException import InvalidMoveStringException
import re

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
    ruleSet = None
    whitePieces = []
    blackPieces = []

    COLOR_WHITE = 0
    COLOR_BLACK = 1

    turn = 0 # white starts

    def __init__(self, ruleSet = None):
        self.ruleSet = ruleSet

    def isLoaded(self):
        return len(self.whitePieces) > 0 or len(self.blackPieces) > 0

    def load(self):
        if (self.ruleSet == None):
            raise NoRuleException('There is no rule set from which to load the game')

        if (len(self.whitePieces) != 0 or len(self.blackPieces) != 0):
            raise Exception('Game is already loaded')

        for i in range(0, 8):
            self.whitePieces.append(Pawn(position=[i, 1], idNumber=i, color=self.COLOR_WHITE))
            self.blackPieces.append(Pawn(position=[i, 6], idNumber=i, color=self.COLOR_BLACK))

        self._loadPowerPieces(self.COLOR_WHITE)
        self._loadPowerPieces(self.COLOR_BLACK)

        self.turn = self.COLOR_WHITE

    def printBoard(self):
        BOARD_FILE = './board.txt'
        with open(BOARD_FILE, 'r') as boardFile:
            template = boardFile.read()
        for row in range(0, 8):
            for col in range(0, 8):
                pieceAtLocation = self._getPiece([col, row])
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
            spaceString.strip()
        
        spaceCodes = []
        for spaceString in spaceStrings:
            col = ord(spaceString[0]) - ord('A')
            row = ord(spaceString[1]) - ord('1')
            spaceCodes.append([col, row])

        pieceForMove = self._getPiece(spaceCodes[0])
        if (pieceForMove == None):
            raise IllegalMoveException('There is no piece at the starting location')
        if (pieceForMove.color != self.turn):
            raise IllegalMoveException('Wrong colored piece')
        
        if (isinstance(pieceForMove, Pawn)):
            # Pawn case
            if (self.turn == self.COLOR_WHITE):
                if (spaceCodes[1] == [spaceCodes[0][0], spaceCodes[0][1] + 1]):
                    if (self._getPiece(spaceCodes[1]) != None):
                        raise IllegalMoveException('There is a piece blocking the pawn from moving forward')
                    else:
                        pieceForMove.position = spaceCodes[1]
                        self._switchTurn()
                elif (spaceCodes[1] == [spaceCodes[0][0], spaceCodes[0][1] + 2]):
                    if (spaceCodes[0][1] != 1):
                        raise IllegalMoveException('A pawn may only move two spaces on its first move of the game')
                    if (self._getPiece(spaceCodes[1]) != None):
                        raise IllegalMoveException('A pawn may not take a piece directly in front of it')
                    if (self._getPiece([spaceCodes[0][0], spaceCodes[0][1] + 1]) != None):
                        raise IllegalMoveException('There is a piece blocking the pawn from moving forward')
                    else:
                        pieceForMove.position = spaceCodes[1]
                        self._switchTurn()
                
                
        # TODO: define cases for standard pieces and special pieces
                
    def _switchTurn(self):
        if (self.turn == self.COLOR_WHITE):
            self.turn = self.COLOR_BLACK
        else:
            self.turn = self.COLOR_WHITE
    
    def _getPiece(self, position):
        assert(len(position) == 2)
        for piece in self.whitePieces:
            if piece.position == position:
                return piece
        for piece in self.blackPieces:
            if piece.position == position:
                return piece
        return None

    def _loadPowerPieces(self, color):
        row = color * 7
        teamList = self.whitePieces
        if color == self.COLOR_BLACK:
            teamList = self.blackPieces

        teamList.append(Rook(position=[0, row], idNumber=8, color=color, movementRule=self.ruleSet.rookMovement))
        teamList.append(Knight(position=[1, row], idNumber=9, color=color, movementRule=self.ruleSet.knightMovement))
        teamList.append(Bishop(position=[2, row], idNumber=10, color=color, movementRule=self.ruleSet.bishopMovement))
        teamList.append(Queen(position=[3, row], idNumber=11, color=color, movementRule=self.ruleSet.queenMovement))
        teamList.append(King(position=[4, row], idNumber=12, color=color))
        teamList.append(Bishop(position=[5, row], idNumber=13, color=color, movementRule=self.ruleSet.bishopMovement))
        teamList.append(Knight(position=[6, row], idNumber=14, color=color, movementRule=self.ruleSet.knightMovement))
        teamList.append(Rook(position=[7, row], idNumber=15, color=color, movementRule=self.ruleSet.rookMovement))

        