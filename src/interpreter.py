from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from environment import Board

State = tuple[tuple[str, ...], ...]


def get_state(board: Board) -> State:
    x, y = board.snake_x, board.snake_y
    grid = board.grid
    return (
        tuple(grid[i][y] for i in range(x - 1, -1, -1)),
        tuple(grid[i][y] for i in range(x + 1, 12)),
        tuple(grid[x][0:y][::-1]),
        tuple(grid[x][y + 1:]),
    )


def interpret(board: Board, action: str) -> tuple[State, int | float]:
    reward = board.step(action)
    return get_state(board), reward


def print_state(state: State) -> None:
    up, down, left, right = state
    pad = " " * len(left)
    for cell in reversed(up):
        print(pad + cell)
    print("".join(reversed(left)) + "H" + "".join(right))
    for cell in down:
        print(pad + cell)
