from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from environment import Board


def get_state(board: Board) -> tuple[tuple[str, ...], ...]:
    x, y = board.snake_x, board.snake_y
    state: list[list[str]] = []
    state.append([board.grid[i][y] for i in range(x - 1, -1, -1)])
    state.append([board.grid[i][y] for i in range(x + 1, 12)])
    state.append(board.grid[x][0:y][::-1])
    state.append(board.grid[x][y + 1:])
    return tuple(tuple(ray) for ray in state)
