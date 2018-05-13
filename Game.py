import re
from functools import reduce

from color import modchar, BLACK, WHITE

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

class Game:

    def __init__(self, ruleSet, promotionCallback):
        self.ruleSet = ruleSet
        self.promotionCallback = promotionCallback

        self.whitePieces = []
        self.blackPieces = []

        self.gameTable = [[None for i in range(0, 8)] for j in range(0, 8)]

        self.turn = WHITE

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
            whiteSquare = Square(i, 1)
            whitePawn = Pawn(position=whiteSquare, color=WHITE)
            self.whitePieces.append(whitePawn)
            self.gameTable[whiteSquare.file][whiteSquare.rank] = whitePawn

            blackSquare = Square(i, 6)
            blackPawn = Pawn(position=blackSquare, color=BLACK)
            self.blackPieces.append(blackPawn)
            self.gameTable[blackSquare.file][blackSquare.rank] = blackPawn

        self._loadPowerPieces(WHITE)
        self._loadPowerPieces(BLACK)

        self.turn = WHITE

    def printBoard(self):
        template = self.boardTemplate
        for row in range(0, 8):
            for col in range(0, 8):
                square = Square(col, row)
                pieceAtLocation = self.getPiece(square)
                symb = '  '
                if pieceAtLocation != None:
                    colorCode = modchar.BLUE
                    if pieceAtLocation.color == WHITE:
                        colorCode = modchar.PINK
                    elif pieceAtLocation.color == BLACK:
                        colorCode = modchar.GREEN
                    symb = colorCode + pieceAtLocation.symbol + modchar.ENDC
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
        if color == BLACK:
            return WHITE
        elif color == WHITE:
            return BLACK
        else:
            raise Exception('Not a valid color')
    
    def move(self, moveIn, knownValid = False):
        move = moveIn
        if (isinstance(move, str)):
            move = self._moveFromMoveString(moveIn)

        pieceForMove = self.getPiece(move.start)
        if not knownValid:
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
            castleMove = None
            if isinstance(pieceForMove, King) and abs(move.start.file - move.end.file) == 2:
                castleInMotion = self.getPiece(Square(0, pieceForMove.position.rank))
                castleStart = None
                if castleInMotion:
                    castleStart = castleInMotion.position
                castleEnd = Square(3, pieceForMove.position.rank)
                if move.end.file > move.start.file:
                    castleInMotion = self.getPiece(Square(7, pieceForMove.position.rank))
                    castleStart = castleInMotion.position
                    castleEnd = Square(5, pieceForMove.position.rank)
                castleMove = MoveRecord(Move(castleStart, castleEnd), castleInMotion)
                castleInMotion.position = castleEnd
                self.gameTable[castleStart.file][castleStart.rank] = None
                self.gameTable[castleEnd.file][castleEnd.rank] = castleInMotion
            pieceForMove.position = move.end
            self.gameTable[move.start.file][move.start.rank] = None
            self.gameTable[move.end.file][move.end.rank] = pieceForMove
            self._switchTurn()
            record = MoveRecord(move, pieceForMove, takenPiece, castleMove=castleMove)
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
        self.gameTable[record.move.end.file][record.move.end.rank] = None
        if record.pieceTaken:
            record.pieceTaken.taken = False
            self.gameTable[record.move.end.file][record.move.end.rank] = record.pieceTaken
        if record.piecePromotedTo:
            record.pieceInMotion.taken = False
            self.whitePieces.remove(record.piecePromotedTo)
        if record.castleMove:
            castle = record.castleMove.pieceInMotion
            m = record.castleMove.move
            castle.position = m.start
            self.gameTable[m.start.file][m.start.rank] = castle
            self.gameTable[m.end.file][m.end.rank] = None
        self.gameTable[record.move.start.file][record.move.start.rank] = record.pieceInMotion
        self._switchTurn()
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

    def isAttacked(self, square, color):
        if color == WHITE:
            for piece in self.whitePieces:
                if piece.isAttacking(square, self):
                    return True
        elif color == BLACK:
            for piece in self.blackPieces:
                if piece.isAttacking(square, self):
                    return True

    def _getKing(self, color):
        if (color == WHITE):
            for piece in self.whitePieces:
                if isinstance(piece, King):
                    return piece
        elif (color == BLACK):
            for piece in self.blackPieces:
                if isinstance(piece, King):
                    return piece

    def isKingAttacked(self, color):
        king = self._getKing(color)
        if (color == WHITE):
            for piece in self.blackPieces:
                if (not piece.taken) and self.isAttacking(Move(piece.position, king.position)):
                    return True
            return False
        elif (color == BLACK):
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

        if isinstance(pieceForMove, King) and abs(move.end.file - move.start.file) == 2:
            # Checking if this is a valid castling move
            if move.end.rank != move.start.rank:
                return False
            elif self.isKingAttacked(pieceForMove.color):
                return False
            else:
                if move.end.file == 2:
                    if self.isAttacked(Square(3, move.start.rank), self.oppositeColor(pieceForMove.color)):
                        return False
                    elif self.isAttacked(Square(2, move.start.rank), self.oppositeColor(pieceForMove.color)):
                        return False
                    elif self.getPiece(Square(3, move.start.rank)) or self.getPiece(Square(2, move.start.rank)) or self.getPiece(Square(1, move.start.rank)):
                        return False
                    else:
                        castle = self.getPiece(Square(0, move.start.rank))
                        if castle == None or not isinstance(castle, Rook):
                            return False
                        for record in self.moveHistory:
                            if record.pieceInMotion == castle or record.pieceInMotion == pieceForMove:
                                return False
                elif move.end.file == 6:
                    if self.isAttacked(Square(5, move.start.rank), self.oppositeColor(pieceForMove.color)):
                        return False
                    elif self.isAttacked(Square(6, move.start.rank), self.oppositeColor(pieceForMove.color)):
                        return False
                    elif self.getPiece(Square(5, move.start.rank)) or self.getPiece(Square(6, move.start.rank)):
                        return False
                    else:
                        castle = self.getPiece(Square(7, move.start.rank))
                        if castle == None or not isinstance(castle, Rook):
                            return False
                        for record in self.moveHistory:
                            if record.pieceInMotion == castle or record.pieceInMotion == pieceForMove:
                                return False
                return True

        takenPiece = self.getPiece(move.end)
        pieceForMove.position = move.end
        self.gameTable[move.end.file][move.end.rank] = pieceForMove
        self.gameTable[move.start.file][move.start.rank] = None
        if takenPiece:
            takenPiece.taken = True
        if self.isKingAttacked(pieceForMove.color):
            pieceForMove.position = move.start
            self.gameTable[move.start.file][move.start.rank] = pieceForMove
            self.gameTable[move.end.file][move.end.rank] = None
            if takenPiece:
                takenPiece.taken = False
                self.gameTable[move.end.file][move.end.rank] = takenPiece
            return False
        pieceForMove.position = move.start
        self.gameTable[move.start.file][move.start.rank] = pieceForMove
        self.gameTable[move.end.file][move.end.rank] = None
        if takenPiece:
            takenPiece.taken = False
            self.gameTable[move.end.file][move.end.rank] = takenPiece

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
        if (self.turn == WHITE):
            self.turn = BLACK
        else:
            self.turn = WHITE
    
    def getPiece(self, position):
        return self.gameTable[position.file][position.rank]

    def positionDifferential(self):
        whiteTotal = 0.0
        blackTotal = 0.0

        for piece in self.whitePieces:
            if not piece.taken:
                whiteTotal += piece.pointValue()
        for piece in self.blackPieces:
            if not piece.taken:
                blackTotal += piece.pointValue()

        return whiteTotal - blackTotal

    def allLegalMoves(self):
        def addAttacksToList(listOfMoves, piece):
            return listOfMoves + list(piece.allAttackingMoves(self))
        
        if self.turn == WHITE:
            attackingMoves = reduce(addAttacksToList, self.whitePieces, [])
            validMoves = filter((lambda move: self.isValidMove(move)), attackingMoves)
            return validMoves
        elif self.turn == BLACK:
            attackingMoves = reduce(addAttacksToList, self.blackPieces, [])
            validMoves = filter((lambda move: self.isValidMove(move)), attackingMoves)
            return validMoves

    def _loadPowerPieces(self, color):
        rank = color * 7
        teamList = self.whitePieces
        if color == BLACK:
            teamList = self.blackPieces

        newPieces = [
            Rook(position = Square(0, rank), color=color, movementRule=self.ruleSet.rookMovement),
            Knight(position = Square(1, rank), color=color, movementRule=self.ruleSet.knightMovement),
            Bishop(position = Square(2, rank), color=color, movementRule=self.ruleSet.bishopMovement),
            Queen(position = Square(3, rank), color=color, movementRule=self.ruleSet.queenMovement),
            King(position = Square(4, rank), color=color),
            Bishop(position = Square(5, rank), color=color, movementRule=self.ruleSet.bishopMovement),
            Knight(position = Square(6, rank), color=color, movementRule=self.ruleSet.knightMovement),
            Rook(position = Square(7, rank), color=color, movementRule=self.ruleSet.rookMovement)
        ]

        fileAt = 0
        for piece in newPieces:
            teamList.append(piece)
            self.gameTable[fileAt][rank] = piece
            fileAt += 1

    def _checkPawnValidity(self, move):
        pieceForMove = self.getPiece(move.start)

        forward = 1
        startRank = 1
        endRank = 7
        lessInRank = lambda a, b: a < b
        if pieceForMove.color == BLACK:
            forward = -1
            startRank = 6
            endRank = 0
            lessInRank = lambda a, b: a > b
        
        oneForward = None
        if lessInRank(move.start.rank, endRank):
            oneForward = Square(move.start.file, move.start.rank + forward)
        twoForward = None
        if lessInRank(move.start.rank + forward, endRank):
            twoForward = Square(move.start.file, move.start.rank + forward * 2)
        if oneForward and (move.end == oneForward):
            if (self.getPiece(move.end) != None):
                return False
            else:
                return True
        elif twoForward and (move.end == twoForward):
            if (move.start.rank != startRank):
                return False
            elif (self.getPiece(move.end) != None):
                return False
            elif (self.getPiece(oneForward) != None):
                return False
            else:
                return True
        elif (move.start.rank + forward == move.end.rank and abs(move.start.file - move.end.file) == 1):
            if (self.getPiece(move.end) == None):
                if (len(self.moveHistory) == 0):
                    return False
                previousMove = self.moveHistory[-1]
                if (move.start.rank == (startRank + forward * 3) and previousMove.move.start == Square(move.end.file, (startRank + forward * 5)) and previousMove.move.end == Square(move.end.file, (startRank + forward * 3)) and isinstance(previousMove.pieceInMotion, Pawn)):
                    # This is where the pawn takes en passant
                    return True
                else:
                    return False
            elif (self.getPiece(move.end).color == pieceForMove.color):
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
        forward = 1
        startRank = 1
        endRank = 7
        lessInRank = lambda a, b: a < b
        if pieceForMove.color == BLACK:
            forward = -1
            startRank = 6
            endRank = 0
            lessInRank = lambda a, b: a > b

        assert(isinstance(pieceForMove, Pawn))
        oneForward = None
        if lessInRank(move.start.rank, endRank):
            oneForward = Square(move.start.file, move.start.rank + forward)
        twoForward = None
        if lessInRank(move.start.rank + forward, endRank):
            twoForward = Square(move.start.file, move.start.rank + forward * 2)
        if move.end == oneForward:
            if (self.getPiece(move.end) != None):
                raise IllegalMoveException('There is a piece blocking the pawn from moving forward')
            else:
                pieceForMove.position = move.end
                self.gameTable[move.end.file][move.end.rank] = pieceForMove
                self.gameTable[move.start.file][move.start.rank] = None
                piecePromotedTo = None
                if pieceForMove.position.rank == endRank:
                    piecePromotedTo = self.getPromotionPiece(pieceForMove)
                    self.whitePieces.append(piecePromotedTo)
                    self.gameTable[move.end.file][move.end.rank] = piecePromotedTo
                    pieceForMove.taken = True
                self._switchTurn()
                record = MoveRecord(move, pieceForMove, piecePromotedTo=piecePromotedTo)
                self.moveHistory.append(record)
        elif twoForward and (move.end == twoForward):
            if (move.start.rank != startRank):
                raise IllegalMoveException('A pawn may only move two spaces on its first move of the game')
            elif (self.getPiece(move.end) != None):
                raise IllegalMoveException('A pawn may not take a piece directly in front of it')
            elif (self.getPiece(oneForward) != None):
                raise IllegalMoveException('There is a piece blocking the pawn from moving forward')
            else:
                pieceForMove.position = move.end
                self.gameTable[move.end.file][move.end.rank] = pieceForMove
                self.gameTable[move.start.file][move.start.rank] = None
                piecePromotedTo = None
                if pieceForMove.position.rank == endRank:
                    piecePromotedTo = self.getPromotionPiece(pieceForMove)
                    self.whitePieces.append(piecePromotedTo)
                    self.gameTable[move.end.file][move.end.rank] = piecePromotedTo
                    pieceForMove.taken = True
                self._switchTurn()
                record = MoveRecord(move, pieceForMove, piecePromotedTo=piecePromotedTo)
                self.moveHistory.append(record)
        elif (move.start.rank + forward == move.end.rank and abs(move.start.file - move.end.file) == 1):
            if (self.getPiece(move.end) == None):
                if (len(self.moveHistory) == 0):
                    raise IllegalMoveException('You cannot move a pawn diagonally except to take')
                previousMove = self.moveHistory[-1]
                if (move.start.rank == (startRank + forward * 3) and previousMove.move.start == Square(move.end.file, (startRank + forward * 5)) and previousMove.move.end == Square(move.end.file, (startRank + forward * 3)) and isinstance(previousMove.pieceInMotion, Pawn)):
                    # This is where the pawn takes en passant
                    takenPiece = previousMove.pieceInMotion
                    self.gameTable[takenPiece.position.file][takenPiece.position.rank] = None
                    takenPiece.taken = True
                    pieceForMove.position = move.end
                    self.gameTable[move.end.file][move.end.rank] = pieceForMove
                    self.gameTable[move.start.file][move.start.rank] = None
                    self._switchTurn()
                    record = MoveRecord(move, pieceForMove, takenPiece)
                    self.moveHistory.append(record)
                else:
                    raise IllegalMoveException('Pawns can only move diagonally to take')
            elif (self.getPiece(move.end).color == pieceForMove.color):
                raise IllegalMoveException('You may not take your own piece')
            else:
                takenPiece = self.getPiece(move.end)
                takenPiece.taken = True
                pieceForMove.position = move.end
                self.gameTable[move.end.file][move.end.rank] = pieceForMove
                self.gameTable[move.start.file][move.start.rank] = None
                piecePromotedTo = None
                if pieceForMove.position.rank == endRank:
                    piecePromotedTo = self.getPromotionPiece(pieceForMove)
                    self.whitePieces.append(piecePromotedTo)
                    self.gameTable[move.end.file][move.end.rank] = piecePromotedTo
                    pieceForMove.taken = True
                self._switchTurn()
                record = MoveRecord(move, pieceForMove, pieceTaken=takenPiece, piecePromotedTo=piecePromotedTo)
                self.moveHistory.append(record)

