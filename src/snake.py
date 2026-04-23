import pygame as pg
from collections import defaultdict

from environment import Board
from interpreter import get_state, interpret, print_state
from agent import make_decision, update_Q, DECISIONS, QTable, State
from display import draw

def train(q_table: QTable, nb_sessions: int) -> None:
    epsilon: float = 0.9
    for _ in range(nb_sessions):
        snake: Board = Board()
        state: State = get_state(snake)
        steps_no_food: int = 0
        running: bool = True
        while running:
            decision: int = make_decision(q_table, state, snake.direction, epsilon)
            new_state, reward = interpret(snake, DECISIONS[decision])
            steps_no_food = 0 if reward >= 10 else steps_no_food + 1
            if reward <= -100 or steps_no_food >= 100 + snake.length * 10:
                update_Q(state, decision, -100, new_state, q_table)
                running = False
            else:
                update_Q(state, decision, reward, new_state, q_table)
            state = new_state
        epsilon = max(0.01, epsilon * 0.9995)


def play(q_table: QTable) -> None:
    pg.init()
    screen: pg.Surface = pg.display.set_mode((600, 600))
    pg.event.clear()
    snake: Board = Board()
    state: State = get_state(snake)
    clock: pg.time.Clock = pg.time.Clock()
    last_step: int = 0
    running: bool = True
    while running:
        clock.tick(60)
        now: int = pg.time.get_ticks()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        if now - last_step > 250:
            last_step = now
            decision: int = make_decision(q_table, state, snake.direction, 0.05)
            new_state, reward = interpret(snake, DECISIONS[decision])
            update_Q(state, decision, reward, new_state, q_table)
            state = new_state
            print_state(state)
            if reward == -100:
                print("Game over!")
                running = False
        draw(screen, snake.grid)
    pg.quit()


def main() -> None:
    q_table: QTable = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
    train(q_table, 100000)
    play(q_table)


if __name__ == "__main__":
    main()
