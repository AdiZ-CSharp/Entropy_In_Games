import random
import math
import itertools

# --- Config ---
GRID_SIZE = 6
SHIP_SIZES = [3, 2]  # Example: one ship of length 3, one of length 2

# --- Board Representation ---
def empty_board():
    return [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def print_board(board, reveal=False):
    print("  " + " ".join(str(i) for i in range(GRID_SIZE)))
    for r in range(GRID_SIZE):
        row = []
        for c in range(GRID_SIZE):
            v = board[r][c]
            if v == 0:
                row.append(".")
            elif v == 1:
                row.append("O" if reveal else ".")
            elif v == 2:
                row.append("X")
            elif v == 3:
                row.append("M")
        print(f"{r} " + " ".join(row))
    print()

# --- Ship Placement ---
def place_ships_randomly():
    board = empty_board()
    ships = []
    for size in SHIP_SIZES:
        placed = False
        while not placed:
            orient = random.choice(['H', 'V'])
            if orient == 'H':
                r = random.randint(0, GRID_SIZE-1)
                c = random.randint(0, GRID_SIZE-size)
                if all(board[r][c+i] == 0 for i in range(size)):
                    for i in range(size):
                        board[r][c+i] = 1
                    ships.append([(r, c+i) for i in range(size)])
                    placed = True
            else:
                r = random.randint(0, GRID_SIZE-size)
                c = random.randint(0, GRID_SIZE-1)
                if all(board[r+i][c] == 0 for i in range(size)):
                    for i in range(size):
                        board[r+i][c] = 1
                    ships.append([(r+i, c) for i in range(size)])
                    placed = True
    return board, ships

# --- Entropy Calculation ---
def all_possible_ship_placements(hits, misses):
    # Generate all possible non-overlapping placements for the ships, given hits/misses
    positions = []
    for size in SHIP_SIZES:
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE-size+1):
                pos = [(r, c+i) for i in range(size)]
                if all((r, c+i) not in misses for i in range(size)):
                    positions.append(pos)
        for r in range(GRID_SIZE-size+1):
            for c in range(GRID_SIZE):
                pos = [(r+i, c) for i in range(size)]
                if all((r+i, c) not in misses for i in range(size)):
                    positions.append(pos)
    # Now, generate all combinations of ship placements (no overlap, all hits covered)
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
        # All hits must be covered by some ship
        if all(any(hit in ship for ship in combo) for hit in hits):
            all_combos.append(combo)
    return all_combos

def board_entropy(hits, misses):
    # For each cell, compute probability of being occupied by a ship
    combos = all_possible_ship_placements(hits, misses)
    if not combos:
        return 0.0, [[0.0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    cell_probs = [[0.0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for combo in combos:
        occupied = set(cell for ship in combo for cell in ship)
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if (r, c) in occupied:
                    cell_probs[r][c] += 1
    total = len(combos)
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            cell_probs[r][c] /= total
    # Entropy per cell
    entropy = 0.0
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            p = cell_probs[r][c]
            if p > 0 and p < 1:
                entropy -= p * math.log2(p) + (1-p) * math.log2(1-p)
    return entropy, cell_probs

# --- Game Simulation ---
def simulate_battleship():
    # Place ships for both player and opponent
    player_board, player_ships = place_ships_randomly()
    opp_board, opp_ships = place_ships_randomly()
    # Knowledge: hits/misses for both
    player_hits, player_misses = set(), set()
    opp_hits, opp_misses = set(), set()
    # Simulate a few moves
    moves = [(2,2), (0,0), (3,3), (5,5), (1,4)]
    print("Player's Board (ships revealed):")
    print_board(player_board, reveal=True)
    print("Opponent's Board (ships revealed):")
    print_board(opp_board, reveal=True)
    print("--- Simulating moves against opponent ---")
    for move in moves:
        r, c = move
        if opp_board[r][c] == 1:
            print(f"Hit at {move}!")
            player_hits.add(move)
            opp_board[r][c] = 2
        else:
            print(f"Miss at {move}.")
            player_misses.add(move)
            opp_board[r][c] = 3
        entropy, cell_probs = board_entropy(player_hits, player_misses)
        print(f"Entropy after move: {entropy:.3f} bits")
        print("Probability board (probability each cell contains a ship):")
        for row in cell_probs:
            print(" ".join(f"{p:.2f}" for p in row))
        print()
    # You can add similar simulation for the opponent's guesses

if __name__ == "__main__":
    simulate_battleship()