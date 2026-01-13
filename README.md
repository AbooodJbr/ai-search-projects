# CS50 AI - Search Projects

This folder contains three small search-based projects from CS50 AI. Each subfolder is self-contained.

## Structure
- `degrees/` — Graph search for degrees of separation between actors using movie/people CSVs.
- `maze/` — Grid maze solver with DFS/BFS (and hooks for other strategies); reads ASCII maze files.
- `tic-tac-toe/` — Minimax-powered Tic Tac Toe with a Tkinter GUI.

## Prerequisites
- Python 3.x
- Standard library only (Tkinter ships with most Python installs). No external dependencies required.

## How to run
### Degrees
From `degrees/`:
1) Choose dataset: `small/` (fast) or `large/` (full). Files: `people.csv`, `movies.csv`, `stars.csv`.
2) Run: `python degrees.py`
3) Enter two actor names; program prints the shortest co-starring chain.

### Maze
From `maze/`:
1) Pick a maze file (e.g., `maze1.txt`, `maze2.txt`, `maze3.txt`).
2) Run: `python search.py maze2.txt`
3) Output shows the maze with a solution path and search statistics.

### Tic Tac Toe
From `tic-tac-toe/` in a GUI-capable environment:
1) Open `tictactoe.ipynb` (or import the module) and execute the logic + GUI cells.
2) Call `start_ui()` to launch the Tkinter window.
3) Pick X or O, click New Game, and play; the AI uses minimax.

## Notes
- Data files can be large; prefer `small/` for quick testing in `degrees/`.
- Tkinter windows may not display on headless servers without a display backend.
- No tests are included; run scripts directly to verify behavior.
