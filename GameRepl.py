from Game import Game
from IllegalMoveException import IllegalMoveException
from InvalidMoveStringException import InvalidMoveStringException

class GameRepl:
    game = None

    def __init__(self, game = None):
        if not game is Game:
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
            moveString = input()
            try:
                self.game.move(moveString)
            except IllegalMoveException:
                print('\nThat move is not legal. Try again: ', end="")
                continue
            except InvalidMoveStringException:
                helpString = 'the requested move could not be understood. Make sure you give coordinates in the following format: A4 to B2\n\ntype \'/\' to preface any command, such as \'print\', which reprints the game\'s board\n\nPlease enter a new move: '
                print(helpString, end="")
                continue