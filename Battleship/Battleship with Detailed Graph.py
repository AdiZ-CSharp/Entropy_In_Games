import random
import math
import itertools
import matplotlib.pyplot as plt
import numpy as np
import time

# --- Config ---
GRID_SIZE = 6
SHIP_SIZES = [3, 2]
NUM_GAMES = 500
MAX_MOVES = 50  # Safety cap, but most games will end sooner

# --- Board Representation ---
def empty_board():
    return [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# --- Ship Placement ---
def place_ships_randomly():
    board = empty_board()
    ships = []
    for size in SHIP_SIZES:
        placed = False
        while not placed:
            orient = random.choice(['H', 'V'])
            if orient == 'H':
                r = random.randint(0, GRID_SIZE - 1)
                c = random.randint(0, GRID_SIZE - size)
                if all(board[r][c + i] == 0 for i in range(size)):
                    for i in range(size):
                        board[r][c + i] = 1
                    ships.append([(r, c + i) for i in range(size)])
                    placed = True
            else:
                r = random.randint(0, GRID_SIZE - size)
                c = random.randint(0, GRID_SIZE - 1)
                if all(board[r + i][c] == 0 for i in range(size)):
                    for i in range(size):
                        board[r + i][c] = 1
                    ships.append([(r + i, c) for i in range(size)])
                    placed = True
    return board, ships

# --- Entropy Calculation ---
def all_possible_ship_placements(hits, misses):
    positions = []
    for size in SHIP_SIZES:
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE - size + 1):
                pos = [(r, c + i) for i in range(size)]
                if all((r, c + i) not in misses for i in range(size)):
                    positions.append(pos)
        for r in range(GRID_SIZE - size + 1):
            for c in range(GRID_SIZE):
                pos = [(r + i, c) for i in range(size)]
                if all((r + i, c) not in misses for i in range(size)):
                    positions.append(pos)
    all_combos = []
    for combo in itertools.combinations(positions, len(SHIP_SIZES)):
        cells = set()
        valid = True
        for ship in combo:
            for cell in ship:
                if cell in cells:
                    valid = False
                    break
                cells.add(cell)
            if not valid:
                break
        if not valid:
            continue
        if all(any(hit in ship for ship in combo) for hit in hits):
            all_combos.append(combo)
    return all_combos

def board_entropy(hits, misses):
    combos = all_possible_ship_placements(hits, misses)
    if not combos:
        return 0.0
    total = len(combos)
    cell_probs = [[0.0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for combo in combos:
        occupied = set(cell for ship in combo for cell in ship)
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if (r, c) in occupied:
                    cell_probs[r][c] += 1
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            cell_probs[r][c] /= total
    entropy = 0.0
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            p = cell_probs[r][c]
            if 0 < p < 1:
                entropy -= p * math.log2(p) + (1 - p) * math.log2(1 - p)
    return entropy

# --- Simulation ---
def simulate_entropy_trace():
    board, ships = place_ships_randomly()
    hits = set()
    misses = set()
    all_moves = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)]
    random.shuffle(all_moves)
    entropies = []
    ship_cells = set(cell for ship in ships for cell in ship)
    for move_num, move in enumerate(all_moves):
        r, c = move
        if board[r][c] == 1:
            hits.add((r, c))
        else:
            misses.add((r, c))
        ent = board_entropy(hits, misses)
        entropies.append(ent)
        # If all ship cells have been hit, entropy is zero, game is solved
        if ship_cells.issubset(hits):
            break
        if move_num + 1 >= MAX_MOVES:
            break
    return entropies

start_time = time.time()

# --- Run Simulations ---
all_entropy_traces = []
max_length = 0
for _ in range(NUM_GAMES):
    trace = simulate_entropy_trace()
    all_entropy_traces.append(trace)
    if len(trace) > max_length:
        max_length = len(trace)

# Pad shorter games with zeros (entropy is zero after solved)
for trace in all_entropy_traces:
    if len(trace) < max_length:
        last_val = trace[-1] if trace else 0.0
        # If last entropy is not zero, pad with zeros (game solved)
        pad_val = 0.0
        trace.extend([pad_val] * (max_length - len(trace)))

# Average entropy per move
avg_entropy = np.mean(all_entropy_traces, axis=0)

# --- Plot ---
plt.figure(figsize=(10, 6))

# Plot individual entropy traces (faint gray lines)
for trace in all_entropy_traces:
    plt.plot(trace, color='gray', alpha=0.1, linewidth=1)

# Plot average entropy (bold line)
plt.plot(avg_entropy, color='blue', linewidth=2.5, label="Average Entropy")

end_time = time.time()
print(f"Total runtime: {end_time - start_time:.2f} seconds")

# Labels and formatting
plt.xlabel("Move Number")
plt.ylabel("Entropy (bits)")
plt.title(f"Entropy Over Time in {NUM_GAMES} Simulated Battleship Games")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()