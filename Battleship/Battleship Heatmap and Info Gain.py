import random
import math
import itertools
import matplotlib.pyplot as plt
import numpy as np
import time

# --- Config ---
GRID_SIZE = 10
SHIP_SIZES = [3, 2]

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
    return entropy, cell_probs

# --- Information Gain Calculation ---
def expected_information_gain(hits, misses):
    combos = all_possible_ship_placements(hits, misses)
    if not combos:
        return np.zeros((GRID_SIZE, GRID_SIZE))
    total = len(combos)
    cell_probs = np.zeros((GRID_SIZE, GRID_SIZE))
    for combo in combos:
        occupied = set(cell for ship in combo for cell in ship)
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if (r, c) in occupied:
                    cell_probs[r][c] += 1
    cell_probs /= total
    info_gain = np.zeros((GRID_SIZE, GRID_SIZE))
    base_entropy, _ = board_entropy(hits, misses)
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if (r, c) in hits or (r, c) in misses:
                info_gain[r][c] = 0.0
                continue
            # Probability of hit/miss
            p_hit = cell_probs[r][c]
            p_miss = 1 - p_hit
            # Entropy if hit
            new_hits = set(hits)
            new_hits.add((r, c))
            ent_hit, _ = board_entropy(new_hits, misses)
            # Entropy if miss
            new_misses = set(misses)
            new_misses.add((r, c))
            ent_miss, _ = board_entropy(hits, new_misses)
            # Expected entropy after move
            exp_entropy = p_hit * ent_hit + p_miss * ent_miss
            info_gain[r][c] = base_entropy - exp_entropy
    return info_gain

# --- Main Visualization ---
def plot_heatmap_and_info_gain():
    hits = set()
    misses = set()
    _, cell_probs = board_entropy(hits, misses)
    info_gain = expected_information_gain(hits, misses)

    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    # Heatmap of ship probabilities
    im0 = axs[0].imshow(cell_probs, cmap='YlOrRd', origin='upper')
    axs[0].set_title('First Move: Probability Heatmap of Ship Locations')
    axs[0].set_xlabel('Column')
    axs[0].set_ylabel('Row')
    fig.colorbar(im0, ax=axs[0], fraction=0.046, pad=0.04)

    # Heatmap of expected information gain
    im1 = axs[1].imshow(info_gain, cmap='Blues', origin='upper')
    axs[1].set_title('Expected Information Gain per Square (First Move)')
    axs[1].set_xlabel('Column')
    axs[1].set_ylabel('Row')
    fig.colorbar(im1, ax=axs[1], fraction=0.046, pad=0.04)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_heatmap_and_info_gain()
