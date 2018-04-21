from Game import Game
from IllegalMoveException import IllegalMoveException
from InvalidMoveStringException import InvalidMoveStringException

from color import WHITE, BLACK

class GameRepl:

    COMMAND_NOT_RECOGNIZED = 'commandNotRecognized'
    COMMAND_NOT_PERMITTED = 'commandNotPermitted'

    def __init__(self, ruleSet):
        def promoCallback():
            return self.promotionCallback()
        self.game = Game(ruleSet, promoCallback)
        self.state = 'normal'
        self.promoting = False

    def promotionCallback(self):
        self.promoting = True
        ret = None
        while True:
            i = input('Enter piece to promote to (\'Queen\', \'Rook\', \'Bishop\', \'Knight\'): ').strip()
            if not len(i):
                continue
            if i[0] == '/':
                status = self._executeCommands(i.lstrip('/'))
                if status == GameRepl.COMMAND_NOT_RECOGNIZED:
                    print('Command not recognized: Try again, or')
                if status == GameRepl.COMMAND_NOT_PERMITTED:
                    print('Command not permitted at this time. Try again, or')
                continue

            i = i.lower()

            if i == 'queen':
                ret = 'q'
                break
            elif i == 'bishop':
                ret = 'b'
                break
            elif i == 'knight':
                ret = 'k'
                break
            elif i == 'rook':
                ret = 'r'
                break
        self.promoting = False
        return ret



    def run(self):
        if self.game == None:
            raise Exception('No game to run')
        if not self.game.isLoaded():
            self.game.load()
        
        MESSAGE = 'Enter move (Eg. \'D2 to D4\'): '

        self.game.printBoard()
        print('\n' + MESSAGE, end="")
        while True:
            moveString = input().strip()
            if not len(moveString):
                continue
            if moveString[0] == '/':
                status = self._executeCommands(moveString.lstrip('/'))
                if status == GameRepl.COMMAND_NOT_RECOGNIZED:
                    print('Command not recognized. Please try again or enter your next move: ', end="")
                elif status == GameRepl.COMMAND_NOT_PERMITTED:
                    print('Command not permitted at this time. Please try again or enter your next move: ', end="")
                elif status == 'undone':
                    self.game.printBoard()
                    print('\n' + MESSAGE, end="")
                elif status == 'not undone':
                    print('\nCould not undo: No moves have been made. Enter a move or a command: ', end="")
                else:
                    print('\n' + MESSAGE, end="")
                continue
            try:
                result = self.game.move(moveString)
                if result == 'check':
                    print("Check!")
                    self.state = result
                elif result == 'mate':
                    winning = 'White'
                    if (self.game.turn == self.WHITE):
                        winning = 'Black'
                    print("Checkmate! " + winning + " has won by checkmate.")
                    self.runPostGame()
                elif result == 'success':
                    self.state = 'normal'

            except IllegalMoveException as e:
                print('\nThat move is not legal: ' + str(e) + '. Try again: ', end="")
                continue
            except InvalidMoveStringException:
                helpString = 'the requested move could not be understood. Make sure you give coordinates in the following format: A4 to B2\n\ntype \'/\' to preface any command, such as \'print\', which reprints the game\'s board\n\nPlease enter a new move: '
                print(helpString, end="")
                continue
            
            self.game.printBoard()
            if self.state == 'check':
                print('Check!')
            print(MESSAGE, end="")

    def runPostGame(self):
        print('Game will now exit. Thanks for playing!')
        exit()

    def _executeCommands(self, command):
        if command == 'exit' or command == 'quit':
            exit()
        elif command == 'undo':
            if not self.promoting:
                resp = self.game.undoLastMove()
                if resp:
                    return 'undone'
                else:
                    return 'not undone'
            else:
                return GameRepl.COMMAND_NOT_PERMITTED
        else:
            return GameRepl.COMMAND_NOT_RECOGNIZED
            
