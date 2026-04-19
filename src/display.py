import pygame as pg
CELL = 50  # taille d'une cellule en pixels

COLORS = {
    "0": (200, 200, 200),
    "W": (50, 50, 50),
    "H": (0, 0, 255),
    "S": (0, 100, 255),
    "G": (0, 255, 0),
    "R": (255, 0, 0),
}


def draw(screen, grid):
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            color = COLORS.get(cell, (0, 0, 0))
            pg.draw.rect(screen, color, (y * CELL, x * CELL, CELL, CELL))
    pg.display.flip()
