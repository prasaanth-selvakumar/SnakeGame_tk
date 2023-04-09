import random


class Food:
    """
    Assign a new food object every time the snake eats the food
    Or everytime a new game starts
    """

    def __init__(self, board):
        x_pos, y_pos = random.randint(0, board.board_size-1), \
            random.randint(0, board.board_size-1)

        while board.arr[x_pos][y_pos] != 0:
            x_pos, y_pos = random.randint(0, board.board_size-1), \
                random.randint(0, board.board_size-1)
        board.add_food(x_pos, y_pos)
