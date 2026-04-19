import random as rd


class Board:
    def __init__(self):
        self.grid: list[list[str]] = [["0"] * 12 for _ in range(12)]
        self.lenght = 3
        self.place_snake()
        self.place_apples()
        self.place_walls()
        for row in self.grid:
            print(row)

    def place_walls(self):
        self.grid[0] = ["W"] * 12
        self.grid[11] = ["W"] * 12
        for row in self.grid:
            row[0] = "W"
            row[11] = "W"

    def place_snake(self):
        x: int = rd.randint(1, 10)
        y: int = rd.randint(1, 10)
        if y > 2:
            self.grid[x][y] = "H"
            self.grid[x][y - 1] = "S"
            self.grid[x][y - 2] = "S"
        elif x > 2:
            self.grid[x][y] = "H"
            self.grid[x - 1][y] = "S"
            self.grid[x - 2][y] = "S"
        elif y < 9:
            self.grid[x][y] = "H"
            self.grid[x][y + 1] = "S"
            self.grid[x][y + 2] = "S"
        elif x < 9:
            self.grid[x][y] = "H"
            self.grid[x + 1][y] = "S"
            self.grid[x + 2][y] = "S"
        self.snake_x = x
        self.snake_y = y

    def place_apples(self):
        count = 0
        while count < 3:
            x: int = rd.randint(1, 10)
            y: int = rd.randint(1, 10)
            if count < 2 and self.grid[x][y] == "0":
                self.grid[x][y] = "G"
                count += 1
            elif self.grid[x][y] == "0":
                self.grid[x][y] = "R"
                count += 1

    def find_body(self):
        

    def move_snake(self,x: int, y: int, lenght: int):
        

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
        if self.grid[newpos_x][newpos_y] == 'G':
            
            

Board()
