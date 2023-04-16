from game_constants import *


class Snake:

    def __init__(self, board):
        self.coordinates = []
        self.length = INITIAL_SNAKE_SIZE
        self.squares = []
        for i in range(self.length-1, -1, -1):
            self.coordinates.append([0, i])
        board.initialize_snake(self)

