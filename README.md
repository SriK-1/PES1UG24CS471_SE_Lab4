# Real-Time Flappy Bird Clone

A small Flappy Bird-style game built with Python and Pygame. This version completes the four lab tasks: accurate collision detection, an on-screen Game Over state, replay with three difficulty levels, and sound feedback.

Chat link: https://chatgpt.com/share/6aca6122-1ef0-83e8-a43d-bce22da27c28

## Requirements

- Python 3.10 or newer
- Pygame (installed from `requirements.txt`)

## Run the game

From the project root, run:

```bash
python -m pip install -r requirements.txt
python main.py
```

## Controls

- **Space** or **left mouse click**: flap upward during gameplay
- **1**: restart on Easy after Game Over
- **2**: restart on Medium after Game Over
- **3**: restart on Hard after Game Over
- **Q** or **Esc**: quit from the Game Over screen

## Completed tasks

1. **Collision detection:** circle-versus-rectangle checks test the bird's visible circular body against both pipe rectangles. Ground and ceiling collisions also end the round.
2. **Game Over screen:** a translucent overlay displays the final score and controls. Gameplay updates stop after death, and gameplay input is ignored until restart or quit.
3. **Difficulty and replay:** Easy, Medium, and Hard configure pipe speed, gap size, and spawn interval. Medium is the default. Restarting resets the bird, pipes, timer, score, and game-over state.
4. **Sound effects:** flap, score, and death effects are generated as PCM tones at startup. If `assets/flap.wav`, `assets/score.wav`, or `assets/hit.wav` is present and readable, that file is used for the corresponding effect; otherwise a generated tone is used. Audio initialization failure is handled gracefully so the game can still run silently.

### Difficulty settings

| Level | Pipe speed (pixels/frame) | Gap height (pixels) | Spawn interval (frames) |
|---|---:|---:|---:|
| Easy | 3 | 200 | 120 |
| Medium | 4 | 160 | 90 |
| Hard | 6 | 130 | 60 |

The settings are a practical starting point, not a claim that every player will find each level equally balanced. Pipe positions and gaps are randomized.

## Project structure

```text
40_flappy-bird-main/
├── main.py
├── requirements.txt
├── README.md
├── REPORT.md
└── game/
    ├── __init__.py
    ├── bird.py
    ├── pipe.py
    ├── game_engine.py
    └── sounds.py
```

## Validation notes

The Python files can be syntax-checked with `python -m compileall .`. Run the game locally to verify visuals, collisions, controls, and actual sound output before recording the final demo. In particular, confirm sound on the computer used for the demonstration; audio hardware and Pygame mixer configuration vary between systems.


