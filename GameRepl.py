from Game import Game
from IllegalMoveException import IllegalMoveException
from InvalidMoveStringException import InvalidMoveStringException

class GameRepl:

    def __init__(self, game = None):
        if not isinstance(game, Game):
            raise TypeError('game must be of type Game')
        self.game = game

    def run(self):
        if self.game == None:
            raise Exception('No game to run')
        if not self.game.isLoaded():
            self.game.load()
        
        message = 'Enter move (Eg. \'D2 to D4\'): '

        self.game.printBoard()
        print('\n' + message, end="")
        while True:
            moveString = input().strip()
            if moveString[0] == '/':
                self._executeCommands(moveString.lstrip('/'))
                continue
            try:
                self.game.move(moveString)
            except IllegalMoveException as e:
                print('\nThat move is not legal: ' + e.message + '. Try again: ', end="")
                continue
            except InvalidMoveStringException:
                helpString = 'the requested move could not be understood. Make sure you give coordinates in the following format: A4 to B2\n\ntype \'/\' to preface any command, such as \'print\', which reprints the game\'s board\n\nPlease enter a new move: '
                print(helpString, end="")
                continue
            
            self.game.printBoard()
            print(message, end="")

    def _executeCommands(self, command):
        if command == 'exit' or command == 'quit':
            exit()
        else:
            print('Command not recognized. Please try again or enter your next move: ', end="")
