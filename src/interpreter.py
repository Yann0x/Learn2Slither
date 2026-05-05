from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from environment import Board

State = tuple[tuple[str, ...], ...]
CELL_TO_IDX = {'0': 0, 'W': 1, 'S': 2, 'G': 3, 'R': 4}


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


def encode_state(state: State) -> np.ndarray:
    result: list[int] = []
    for ray in state:
        ray = ray[:10]
        ray = ray + ('W',) * (10 - len(ray))
        for elem in ray:
            onehot = [0] * 5
            onehot[CELL_TO_IDX[elem]] = 1
            result.extend(onehot)
    return np.array(result, dtype=np.float32)
