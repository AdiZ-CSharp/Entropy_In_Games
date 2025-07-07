import itertools
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import Counter
import concurrent.futures
import os

# --- 1. Word list ---
TARGETS = [
"the", "and", "for", "are", "you", "was", "not", "but", "all", "can",
"had", "his", "her", "one", "out", "has", "who", "she", "how", "now",
"see", "him", "new", "any", "way", "our", "may", "get", "too", "two",
"man", "did", "old", "big", "say", "boy", "use", "off", "let", "top",
"end", "red", "its", "war", "run", "day", "god", "try", "yet", "set",
"car", "dog", "eat", "sun", "win", "job", "law", "key", "bad", "fun",
"pay", "act", "bed", "low", "sea", "hot", "yes", "box", "bar", "bag",
"gas", "cut", "sit", "arm", "mom", "dad", "leg", "die", "dry", "cat",
"cup", "net", "far", "toe", "ten", "aid", "age", "air", "aim", "art",
"ask", "bit", "bow", "buy", "cap", "cry", "dig", "dot", "fan", "fat",
"fit", "fix", "fly", "fun", "gap", "gun", "hit", "hop", "ice", "jam",
"jar", "kit", "lay", "lie", "lip", "mad", "man", "map", "mat", "mix",
"mud", "nap", "net", "nod", "off", "oil", "pad", "pan", "pen", "pet",
"pit", "pop", "pot", "rag", "rat", "rip", "rob", "rod", "row", "rub",
"run", "sad", "saw", "say", "see", "set", "shy", "sip", "sit", "ski",
"sky", "son", "spy", "tag", "tap", "tax", "tea", "tip", "toe", "top",
"toy", "try", "tug", "use", "van", "vet", "war", "wax", "way", "web",
"wet", "who", "why", "wig", "win", "wow", "yes", "yet", "zip", "zoo",
"ash", "ate", "ban", "bay", "bee", "beg", "bet", "bin", "bob", "bug",
"bus", "cab", "cam", "can", "cap", "cop", "cow", "cub", "cue", "dam",
"den", "dew", "dim", "dip", "don", "dub", "dug", "ear", "eel", "egg",
"elf", "elk", "elm", "emo", "emu", "era", "eve", "fan", "fee", "fig",
"fin", "fir", "foe", "fog", "fry", "fur", "gem", "get", "gig", "gin",
"gnu", "goa", "gum", "gut", "gym", "hen", "hip", "hog", "hop", "ice",
"ill", "inn", "ion", "irk", "ivy", "jab", "jog", "jot", "joy", "jug",
"ken", "kin", "kit", "lab", "lad", "lag", "lap", "law", "lay", "lee",
"leg", "let", "lid", "log", "lot", "mad", "man", "map", "mat", "max",
"men", "met", "mob", "mod", "mom", "mop", "mud", "nag", "net", "nip",
"nod", "nun", "oak", "oar", "odd", "off", "oil", "one", "opt", "orb",
"ore", "owl", "pad", "pal", "pan", "par", "pat", "paw", "pay", "pea",
"pen", "pet", "pie", "pig", "pin", "pit", "pod", "pop", "pot", "pro",
"pub", "pun", "pus", "put", "rag", "ram", "ran", "rap", "rat", "raw",
"ray", "red", "rib", "rid", "rig", "rim", "rip", "rob", "rod", "row",
"rub", "rug", "rum", "run", "rye", "sad", "sag", "sap", "sat", "saw",
"say", "sea", "see", "set", "sew", "she", "shy", "sin", "sip", "sir",
"sit", "ski", "sky", "sly", "sob", "son", "sow", "soy", "spa", "spy",
"sub", "sue", "sum", "sun", "tab", "tag", "tan", "tap", "tar", "tax",
"tea", "ten", "the", "thy", "tie", "tip", "toe", "ton", "top", "toy",
"try", "tub", "tug", "urn", "use", "van", "vet", "vow", "war", "was",
"wax", "way", "web", "wed", "wee", "wet", "who", "why", "wig", "win",
"wit", "woe", "won", "wow", "yak", "yam", "yap", "yaw", "yay", "yep",
"yes", "yet", "yew", "yup", "zap", "zen", "zip", "zit", "zoo"
]
GUESSES = TARGETS.copy()

# --- 2. Feedback function (green=2, yellow=1, gray=0) ---
def score_feedback(guess, target):
    fb = [0]*3
    used = [False]*3
    for i in range(3):
        if guess[i] == target[i]:
            fb[i] = 2
            used[i] = True
    for i in range(3):
        if fb[i] == 0:
            for j in range(3):
                if not used[j] and guess[i] == target[j]:
                    fb[i] = 1
                    used[j] = True
                    break
    return tuple(fb)

# --- 3. Entropy calculation ---
def expected_entropy(guess, candidates):
    patterns = Counter(score_feedback(guess, target) for target in candidates)
    total = len(candidates)
    ent = 0.0
    for count in patterns.values():
        p = count / total
        ent -= p * math.log2(p)
    return ent

# --- 4. Game simulation with entropy tracking ---
def simulate_game(secret):
    candidates = TARGETS.copy()
    history = []
    entropy_trace = []
    while True:
        guess = max(candidates, key=lambda g: expected_entropy(g, candidates))
        fb = score_feedback(guess, secret)
        ent = expected_entropy(guess, candidates)
        entropy_trace.append(ent)
        history.append((guess, fb))
        if fb == (2, 2, 2):
            return history, entropy_trace
        candidates = [w for w in candidates if score_feedback(guess, w) == fb]


# --- 5. Simulate all games and record entropy paths (parallelized) ---
def simulate_game_entropy(word):
    _, entropies = simulate_game(word)
    return entropies

if __name__ == "__main__":
    with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        entropy_logs = list(executor.map(simulate_game_entropy, TARGETS))


# --- 6. Compute average entropy per turn ---
    max_turns = max(len(log) for log in entropy_logs)
    avg_entropy_by_turn = []
    for i in range(max_turns):
        turn_vals = [log[i] for log in entropy_logs if i < len(log)]
        avg_entropy_by_turn.append(sum(turn_vals) / len(turn_vals))


    # --- 7a. Animate average entropy drop ---
    fig1, ax1 = plt.subplots(figsize=(8,5))
    ax1.set_xlim(0.5, len(avg_entropy_by_turn) + 0.5)
    ax1.set_ylim(0, max(avg_entropy_by_turn) + 0.5)
    line, = ax1.plot([], [], marker='o', color='blue')
    ax1.set_title("Entropy Drop While Solving 3-Letter Wordle (Average)")
    ax1.set_xlabel("Turn")
    ax1.set_ylabel("Expected Entropy (bits)")
    ax1.grid(True)

    xdata, ydata = [], []

    """
    def init():
        line.set_data([], [])
        return line,

    def update(frame):
        xdata.append(frame + 1)
        ydata.append(avg_entropy_by_turn[frame])
        line.set_data(xdata, ydata)
        return line,

    ani = animation.FuncAnimation(
        fig1, update, frames=len(avg_entropy_by_turn),
        init_func=init, blit=True, interval=700, repeat=False
    )
    """

    lines = []
    avg_line, = ax1.plot([], [], lw=3, color='blue', label='Average Entropy')

    def init():
        return lines + [avg_line]

    def update(frame):
        if frame < len(entropy_logs):
            trace = entropy_logs[frame]
            x = list(range(1, len(trace)+1))
            y = trace
            line, = ax1.plot(x, y, color='gray', alpha=0.2)
            lines.append(line)
        x_avg = list(range(1, len(avg_entropy_by_turn)+1))
        y_avg = avg_entropy_by_turn
        avg_line.set_data(x_avg, y_avg)
        return lines + [avg_line]

    ani = animation.FuncAnimation(
        fig1, update, frames=len(entropy_logs),
        init_func=init, blit=True, interval=10, repeat=False
    )

    
    # --- 7b. Plot all entropy traces for all games ---
    fig2, ax2 = plt.subplots(figsize=(8,5))
    for trace in entropy_logs:
        ax2.plot(range(1, len(trace)+1), trace, color='gray', alpha=0.2)
    ax2.plot(range(1, len(avg_entropy_by_turn)+1), avg_entropy_by_turn, color='blue', label='Average')
    ax2.set_title("Entropy Traces for All Games (3-Letter Wordle)")
    ax2.set_xlabel("Turn")
    ax2.set_ylabel("Expected Entropy (bits)")
    ax2.grid(True)
    ax2.legend()

    # Show both figures simultaneously
    fig1.show()
    fig2.show()
    import time
    # Give time for both windows to appear before script exits
    plt.pause(0.1)
    input("Press Enter to close plots...")