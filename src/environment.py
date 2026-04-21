import random as rd
import pygame as pg
from collections import deque
from display import draw
from interpreter import get_state


DIRS: dict[str, tuple[int, int]] = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
}
REWARDS: dict[str, int | float] = {
    "G": 10,
    "R": -10,
    "W": -100,
    "0": -0.1
}


class Board:
    def __init__(self):
        self.grid: list[list[str]] = [["0"] * 12 for _ in range(12)]
        self.snake: deque[tuple[int, int]] = deque()
        self.length = 3
        self.place_snake()
        self.generate_apple(1)
        self.generate_apple(1)
        self.generate_apple(-1)
        self.place_walls()

    def generate_apple(self, type: int):
        while True:
            x = rd.randint(1, 10)
            y = rd.randint(1, 10)
            if self.grid[x][y] == "0":
                self.grid[x][y] = "G" if type == 1 else "R"
                break

    def place_walls(self):
        self.grid[0] = ["W"] * 12
        self.grid[11] = ["W"] * 12
        for row in self.grid:
            row[0] = "W"
            row[11] = "W"

    def place_snake(self):
        x = rd.randint(1, 10)
        y = rd.randint(1, 10)

        if y > 2:
            dx, dy = 0, -1
        elif x > 2:
            dx, dy = -1, 0
        elif y < 9:
            dx, dy = 0, 1
        else:
            dx, dy = 1, 0

        for i, label in enumerate(["H", "S", "S"]):
            self.grid[x + dx * i][y + dy * i] = label
            if i != 0:
                self.snake.append((x + dx * i, y + dy * i))

        self.snake_x = x
        self.snake_y = y

    def move_snake(self, x: int, y: int, length: int):
        if length == -1 and self.length == 1:
            return 1
        self.grid[x][y] = "H"
        self.grid[self.snake_x][self.snake_y] = "S"
        self.snake.appendleft((self.snake_x, self.snake_y))
        if length == 1:
            self.length += 1
            self.generate_apple(1)
        elif length == -1:
            tx, ty = self.snake.pop()
            self.grid[tx][ty] = "0"
            tx, ty = self.snake.pop()
            self.grid[tx][ty] = "0"
            self.length -= 1
            self.generate_apple(-1)
        else:
            tx, ty = self.snake.pop()
            self.grid[tx][ty] = "0"
        self.snake_x = x
        self.snake_y = y
        return 0

    def step(self, dir: str):
        dx, dy = DIRS[dir]
        nx, ny = self.snake_x + dx, self.snake_y + dy
        cell = self.grid[nx][ny]
        if self.length > 1 and (nx, ny) == self.snake[0]:
            return 0
        elif cell in ("W", "S"):
            return REWARDS["W"]
        print(dir)
        reward = REWARDS[cell]
        self.move_snake(nx, ny, {"G": 1, "R": -1}.get(cell, 0))
        return reward


def print_state(state):
    up, down, left, right = state
    pad = " " * len(left)
    for cell in reversed(up):
        print(pad + cell)
    print("".join(reversed(left)) + "H" + "".join(right))
    for cell in down:
        print(pad + cell)


snake = Board()

pg.init()
screen = pg.display.set_mode((600, 600))
pg.event.clear()
running = True
score = 0
reward = 0
draw(screen, snake.grid)
print_state(get_state(snake))
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                reward = snake.step("UP")
            elif event.key == pg.K_DOWN:
                reward = snake.step("DOWN")
            elif event.key == pg.K_LEFT:
                reward = snake.step("LEFT")
            elif event.key == pg.K_RIGHT:
                reward = snake.step("RIGHT")
            score += reward
            print(f"score: {score}")
            if reward == -100:
                exit("You died!")
            draw(screen, snake.grid)
            print_state(get_state(snake))
