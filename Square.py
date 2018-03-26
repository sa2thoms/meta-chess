class Square:

    def __init__(self, file, rank):
        assert file < 8
        assert file >= 0
        assert rank < 8
        assert rank >= 0

        self.file = file
        self.rank = rank