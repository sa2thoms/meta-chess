class Square:

    def __init__(self, file, rank):
        assert file < 8
        assert file >= 0
        assert rank < 8
        assert rank >= 0

        self.file = file
        self.rank = rank

    def fullCopy(self):
        return Square(self.file, self.rank)

    def __eq__(self, other):
        return self.file == other.file and self.rank == other.rank
        
    def __str__(self):
        return  str(chr(ord('A') + self.file) + chr(ord('1') + self.rank))