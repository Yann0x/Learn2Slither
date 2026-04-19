import random as rd
import pygame as pg
from display import draw


class Board:
    def __init__(self):
        self.grid: list[list[str]] = [["0"] * 12 for _ in range(12)]
        self.snake: list[int] = []
        self.length = 3
        self.place_snake()
        for i in range(3):
            self.generate_apple(i)
        self.place_walls()

    def generate_apple(self, type: int):
        while True:
            x = rd.randint(1, 10)
            y = rd.randint(1, 10)
            if self.grid[x][y] == "0":
                self.grid[x][y] = "R" if type == 1 else "G"
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
                self.snake.append((x + dx * i) * 100 + (y + dy * i))

        self.snake_x = x
        self.snake_y = y

    def move_snake(self, x: int, y: int, length: int):
        if length == -1 and self.length == 1:
            return 1
        oldelem = self.snake_x * 100 + self.snake_y
        self.grid[x][y] = "H"
        i = 0
        for elem in self.snake:
            self.grid[oldelem // 100][oldelem % 100] = "S"
            tmp = oldelem
            oldelem = elem
            self.snake[i] = tmp
            i += 1
        self.grid[oldelem // 100][oldelem % 100] = "0"
        if length == 1:
            self.grid[oldelem // 100][oldelem % 100] = "S"
            self.length += 1
            self.snake.append(oldelem)
        elif length == -1:
            pos = self.snake.pop()
            self.grid[pos // 100][pos % 100] = "0"
            self.length -= 1
        if length != 0:
            self.generate_apple(length * -1)
        self.snake_x = x
        self.snake_y = y
        return 0

    def step(self, dir: str):
        if dir == "UP":
            newpos_x = self.snake_x - 1
            newpos_y = self.snake_y
        elif dir == "DOWN":
            newpos_x = self.snake_x + 1
            newpos_y = self.snake_y
        elif dir == "LEFT":
            newpos_x = self.snake_x
            newpos_y = self.snake_y - 1
        else:
            newpos_x = self.snake_x
            newpos_y = self.snake_y + 1
        if self.grid[newpos_x][newpos_y] == "W":
            return 1
        elif self.grid[newpos_x][newpos_y] == "G":
            self.move_snake(newpos_x, newpos_y, 1)
        elif self.grid[newpos_x][newpos_y] == "R":
            return self.move_snake(newpos_x, newpos_y, -1)
        elif self.grid[newpos_x][newpos_y] == "S":
            return 1
        else:
            self.move_snake(newpos_x, newpos_y, 0)
        return 0


snake = Board()

pg.init()
screen = pg.display.set_mode((600, 600))
pg.event.clear()
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                if snake.step("UP"):
                    exit("you died!")
            elif event.key == pg.K_DOWN:
                if snake.step("DOWN"):
                    exit("you died!")
            elif event.key == pg.K_LEFT:
                if snake.step("LEFT"):
                    exit("you died!")
            elif event.key == pg.K_RIGHT:
                if snake.step("RIGHT"):
                    exit("you died!")
            draw(screen, snake.grid)
