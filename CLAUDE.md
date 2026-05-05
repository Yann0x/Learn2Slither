# Learn2Slither — Claude Context

## Project Overview

42Paris reinforcement learning project. A snake agent learns via Q-learning to maximize its length on a board. The agent sees only what's in the 4 directions from its head (snake vision) and picks UP/DOWN/LEFT/RIGHT each step.

**Goal:** snake reaches length 10+ and stays alive as long as possible.

## Architecture (4 modules, required by subject)

```
ENVIRONMENT  →  INTERPRETER  →  AGENT
     ↑               ↓             ↓
     └─────── ACTION ──────────────┘
                  REWARD ──────────┘
```

| File | Role |
|------|------|
| [src/environment.py](src/environment.py) | `Board` class — grid, snake, apples, physics |
| [src/interpreter.py](src/interpreter.py) | `get_state()` — converts board → snake vision state |
| [src/agent.py](src/agent.py) | Q-table, `make_decision()`, `update_Q()` |
| [src/display.py](src/display.py) | pygame rendering |
| [src/snake.py](src/snake.py) | `train()`, `play()`, `main()` — entry point |

## Board / Environment Rules

- Grid is **12×12** internally (10×10 playable + 1-cell wall border)
- Cell symbols: `'0'`=empty, `'W'`=wall, `'H'`=snake head, `'S'`=snake body, `'G'`=green apple, `'R'`=red apple
- Start: snake length 3, placed randomly with direction chosen by position constraints
- **2 green apples** and **1 red apple** on board at all times
- Green apple eaten → length +1, new green apple spawns
- Red apple eaten → length -1, new red apple spawns
- Game over triggers: hit wall (`W`), hit own body (`S`), length drops to 0

## State Representation

`get_state()` in [src/interpreter.py](src/interpreter.py) returns a `tuple[tuple[str, ...], ...]` of 4 rays:

```python
state = (
    up,    # state[0]: cells above head, nearest first
    down,  # state[1]: cells below head, nearest first
    left,  # state[2]: cells left of head, nearest first
    right, # state[3]: cells right of head, nearest first
)
```

**Critical constraint (subject penalty -42):** the agent may ONLY receive information visible from the snake's head in 4 directions. No board coordinates, no absolute positions, nothing else.

`print_state()` renders the vision as a cross in the terminal, which is also displayed during play.

## Agent / Q-Learning

File: [src/agent.py](src/agent.py)

- `QTable = defaultdict[State, list[float]]` — 4 Q-values per state (one per action)
- Actions: `{0: "UP", 1: "DOWN", 2: "LEFT", 3: "RIGHT"}`
- **Opposite direction filtering**: agent never selects the direct opposite of current direction (avoids instant self-collision)
- `make_decision(q_table, state, dir, epsilon)` — epsilon-greedy, only among safe moves
- `update_Q()` — standard Bellman update: `Q(s,a) += lr * (r + γ * max Q(s') - Q(s,a))`
- Hyperparameters: `lr=0.1`, `gamma=0.9`
- Epsilon decay in `train()`: starts 0.9, multiplied by 0.9995 each session, floored at 0.01

**Known issue (see git log):** the full-ray state representation creates ~68 billion unique states — Q-table approach doesn't scale. Next step: replace with a **Deep Q-Network (DQN / Neural Network)**. The subject explicitly allows either Q-table or Neural Network.

## Rewards (current values)

Defined in [src/environment.py](src/environment.py) `REWARDS` dict and `step()`:

| Event | Reward |
|-------|--------|
| Green apple | `+10` |
| Red apple | `-10` |
| Wall / self (`W`/`S`) | `-100` (also triggers game over) |
| Empty move | `0` |
| Survival bonus | `+0.01 * snake.length` (added each step) |

Game-over in `train()` always sends `-100` to `update_Q` regardless of step() return value.

## Training Loop ([src/snake.py](src/snake.py))

```python
train(q_table, nb_sessions=100_000)
play(q_table)          # pygame window, 250ms per step, epsilon=0.05
```

Episode termination condition: `reward <= -100` OR `steps_no_food >= 100 + snake.length * 10` (stall guard).

## What's Still Missing (subject requirements not yet implemented)

These must be added before submission:

1. **CLI argument parsing** — subject specifies these flags:
   - `-sessions N` — number of training sessions
   - `-save <file>` — export model after training
   - `-load <file>` — import model before running
   - `-visual on/off` — toggle pygame display (off = faster training)
   - `-dontlearn` — disable Q updates (evaluation mode)
   - `-step-by-step` — pause after each agent decision
   
2. **Model save/load** — serialize and deserialize the Q-table (or NN weights) to a file

3. **`models/` folder** — must contain at least 3 pre-trained models:
   - `models/1sess.txt` (1 training session)
   - `models/10sess.txt` (10 training sessions)
   - `models/100sess.txt` (100 training sessions)

4. **DQN replacement** — Q-table state explosion makes learning impractical; need neural network

5. **Display speed config** — at least one human-readable speed + step-by-step mode

## Running the Project

```bash
# Setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run (current — no CLI args yet)
cd src && python snake.py

# Lint (norm check)
flake8 src/
```

## Subject Constraints Summary

- Model type: **Q-table or Neural Network only** — any other model = score 0
- State input: **snake vision only** — extra board info = penalty -42
- Language: Python (flake8 norm enforced)
- Must submit: board + agent code + trained model files in git repo
- Bonuses (only if mandatory is complete): length 15/20/25/30/35, better UI, configurable board size
