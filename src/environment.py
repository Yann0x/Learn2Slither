import random as rd
from collections import deque


DIRS: dict[str, tuple[int, int]] = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
}
REWARDS: dict[str, int | float] = {"G": 10, "R": -10, "W": -100, "0": 0}


class Board:
    __slots__ = ("grid", "snake", "length", "direction", "snake_x", "snake_y")

    def __init__(self):
        self.grid: list[list[str]] = [["0"] * 12 for _ in range(12)]
        self.snake: deque[tuple[int, int]] = deque()
        self.length = 3
        self.direction = ""
        self.place_snake()
        self.generate_apple(1)
        self.generate_apple(1)
        self.generate_apple(-1)
        self.place_walls()

    def generate_apple(self, type: int) -> None:
        while True:
            x = rd.randint(1, 10)
            y = rd.randint(1, 10)
            if self.grid[x][y] == "0":
                self.grid[x][y] = "G" if type == 1 else "R"
                break

    def place_walls(self) -> None:
        self.grid[0] = ["W"] * 12
        self.grid[11] = ["W"] * 12
        for row in self.grid:
            row[0] = "W"
            row[11] = "W"

    def place_snake(self) -> None:
        x = rd.randint(1, 10)
        y = rd.randint(1, 10)

        dirs = [("LEFT", 0, -1), ("UP", -1, 0), ("RIGHT", 0, 1), ("DOWN", 1, 0)]
        conds = [y > 2, x > 2, y < 9, True]
        self.direction, dx, dy = next(d for d, c in zip(dirs, conds) if c)

        for i, label in enumerate(["H", "S", "S"]):
            self.grid[x + dx * i][y + dy * i] = label
            if i:
                self.snake.append((x + dx * i, y + dy * i))

        self.snake_x = x
        self.snake_y = y

    def move_snake(self, x: int, y: int, length: int) -> int:
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

    def step(self, dir: str) -> int | float:
        dx, dy = DIRS[dir]
        nx, ny = self.snake_x + dx, self.snake_y + dy
        cell = self.grid[nx][ny]
        if cell in ("W", "S"):
            return REWARDS["W"]
        self.direction = dir
        reward: int | float = REWARDS[cell] + 0.01 * self.length
        self.move_snake(nx, ny, {"G": 1, "R": -1}.get(cell, 0))
        return reward
