import pygame as pg

CELL: int = 50

COLORS: dict[str, tuple[int, int, int]] = {
    "0": (200, 200, 200),
    "W": (50, 50, 50),
    "H": (0, 0, 255),
    "S": (0, 100, 255),
    "G": (0, 255, 0),
    "R": (255, 0, 0),
}


def draw(screen: pg.Surface, grid: list[list[str]]) -> None:
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            color = COLORS.get(cell, (0, 0, 0))
            pg.draw.rect(screen, color, (y * CELL, x * CELL, CELL, CELL))
    pg.display.flip()
