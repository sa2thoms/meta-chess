from Game import Game
from IllegalMoveException import IllegalMoveException
from InvalidMoveStringException import InvalidMoveStringException

class GameRepl:

    def __init__(self, ruleSet):
        def promoCallback():
            return self.promotionCallback()
        self.game = Game(ruleSet, promoCallback)
        self.state = 'normal'

    def promotionCallback(self):
        while True:
            i = input('Enter piece to promote to (\'Queen\', \'Rook\', \'Bishop\', \'Knight\'): ').strip()

            if i[0] == '/':
                self._executeCommands(i.lstrip('/'))
                continue

            i = i.lower()

            if i == 'queen':
                return 'q'
            elif i == 'bishop':
                return 'b'
            elif i == 'knight':
                return 'k'
            elif i == 'rook':
                return 'r'


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
            if moveString[0] == '/':
                self._executeCommands(moveString.lstrip('/'))
                continue
            try:
                result = self.game.move(moveString)
                if result == 'check':
                    print("Check!")
                    self.state = result
                elif result == 'mate':
                    winning = 'White'
                    if (self.game.turn == self.game.COLOR_WHITE):
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
        else:
            print('Command not recognized. Please try again or enter your next move: ', end="")
