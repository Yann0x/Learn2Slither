from collections import defaultdict
import random as rd

State = tuple[tuple[str, ...], ...]
QTable = defaultdict[State, list[float]]

lr: float = 0.1
gamma: float = 0.9
DECISIONS: dict[int, str] = {0: "UP", 1: "DOWN", 2: "LEFT", 3: "RIGHT"}
DECISIONSINT: dict[str, int] = {"UP": 0, "DOWN": 1, "LEFT": 2, "RIGHT": 3}
OPPOSITE_IDX: dict[str, int] = {"UP": 1, "DOWN": 0, "LEFT": 3, "RIGHT": 2}


def make_decision(
    q_table: QTable,
    state: State,
    dir: str,
    epsilon: float,
) -> int:
    immediate = [state[0][0], state[1][0], state[2][0], state[3][0]]
    opposite = OPPOSITE_IDX[dir]
    safe = [i for i in range(4) if i != opposite and immediate[i] not in ("S", "W")]
    if not safe:
        safe = [i for i in range(4) if i != opposite]
    if rd.random() <= epsilon:
        return rd.choice(safe)
    q = q_table[state]
    return max(safe, key=lambda i: q[i])


def update_Q(
    pre_state: State,
    decision: int,
    reward: int | float,
    new_state: State,
    q_table: QTable,
) -> None:
    q_table[pre_state][decision] = q_table[pre_state][decision] + lr * (
        reward + gamma * max(q_table[new_state]) - q_table[pre_state][decision]
    )
