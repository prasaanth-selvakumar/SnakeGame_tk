"""
Author - Prasaanth
Date - 08/04/2023

Idea create a snake game using tkinter and train a re-inforncement learning model to learn to play it
"""
# Python packages
import tkinter as tk


# Created Classes
from game_constants import *
from Snake import Snake
from Food import Food


class Board:
    def __init__(self, board_size):
        self.board_size = board_size
        self.arr = [[0] * self.board_size for i in range(self.board_size)]
        self.h_block = (WINDOW_HEIGHT // self.board_size)
        self.w_block = (WINDOW_WIDTH // self.board_size)
        self.food = Food(self)
        self.snake = Snake(self)


    def add_food(self, x_pos, y_pos):
        self.arr[x_pos][y_pos] = 1
        canvas.create_oval(x_pos * self.h_block,
                           y_pos * self.w_block,
                           (1 + x_pos) * self.h_block,
                           (1 + y_pos) * self.w_block,
                           fill=FOOD_COLOUR, tags="food")

    def initialize_snake(self, snake):

        for i in range(snake.length):
            x, y = snake.coordinates[i]
            self.arr[x][y] = 10
            square = canvas.create_rectangle(x * self.h_block,
                                             y * self.w_block,
                                             (x + 1) * self.h_block,
                                             (y + 1) * self.w_block,
                                             fill=SNAKE_COLOUR, tags="snake_body")
            snake.squares.append(square)

    def update_snake_pos(self, head):
        global score
        skip_pop = False
        self.snake.coordinates.insert(0, head)
        x1, y1 = self.snake.coordinates.pop()
        x, y = head
        square = canvas.create_rectangle(x * self.h_block,
                                         y * self.w_block,
                                         (x + 1) * self.h_block,
                                         (y + 1) * self.w_block,
                                         fill=SNAKE_COLOUR, tags=f"snake_body")
        self.snake.squares.insert(0, square)
        if self.arr[x][y] == 10:
            self.game_over()
            return False
        elif self.arr[x][y] == 1:
            canvas.delete("food")
            self.food = Food(self)
            self.snake.length += 1
            skip_pop = True
            self.snake.coordinates.append([x1, y1])
            score += 1
            label.config(text=f"Score: {score}")

        # Removing the last element from the snake
        if not skip_pop:
            canvas.delete(self.snake.squares[-1])
            self.snake.squares.pop()
            self.arr[x1][y1] = 0
        self.arr[x][y] = 10

        return True

    def game_over(self):
        global game_status
        game_status = 0
        canvas.delete("snake_body")
        canvas.delete("food")
        canvas.create_text(window.winfo_width() // 2,
                           window.winfo_height() // 2,
                           text=f"Game Over\nScore: {score}", fill="#770000", font=("consolas", 30), tags="game_over")


def next_turn(board):
    x, y = board.snake.coordinates[0]
    if cur_dir == "up":
        y -= 1
    elif cur_dir == "down":
        y += 1
    elif cur_dir == "left":
        x -= 1
    else:
        x += 1
    # updating condition to make boundaries as walls
    if x >= BOARD_SIZE or y >= BOARD_SIZE or x<0 or y<0:
        update_turn = False
        board.game_over()
    else:
        update_turn = board.update_snake_pos([x, y])
    if update_turn:
        window.after(GAME_SPEED, next_turn, board)


def change_direction(new_direction):
    global cur_dir
    if new_direction != cur_dir:
        if new_direction == 'left' and cur_dir != 'right':
            cur_dir = new_direction
        elif new_direction == 'right' and cur_dir != 'left':
            cur_dir = new_direction
        elif new_direction == 'up' and cur_dir != 'down':
            cur_dir = new_direction
        elif new_direction == 'down' and cur_dir != 'up':
            cur_dir = new_direction
        else:
            pass


def reset_game(arg):
    global game_status, cur_dir, score
    if(game_status==0):
        game_status = 1
        score = 0
        label.config(text=f"Score: {score}")
        canvas.delete("game_over")
        board = Board(BOARD_SIZE)
        cur_dir = "down"
        next_turn(board)



cur_dir = "down"
window = tk.Tk()
window.title("Snake Game - Trial1")
# Track scores throughout the game
score = 0
game_status = 0

label = tk.Label(window, text=f"Score: {score}",
                 font=("consolas", 30))
label.pack()

canvas = tk.Canvas(window, background=BACKGROUND_COLOUR,
                   height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
canvas.pack()

window.update()
window.bind("<Left>", lambda x: change_direction('left'))
window.bind("<Right>", lambda x: change_direction('right'))
window.bind("<Up>", lambda x: change_direction('up'))
window.bind("<Down>", lambda x: change_direction('down'))
window.bind("<Return>", reset_game)

reset_game("")
window.mainloop()
