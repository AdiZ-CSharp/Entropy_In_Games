import itertools
import math
from collections import Counter, defaultdict
import concurrent.futures
import os

# --- 1. Word list ---
# Example small 3-letter word list; expand as needed
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
GUESSES = TARGETS.copy()  # restrict guesses to possible answers

# --- 2. Scoring function (Mastermind-style) ---
def score_feedback(guess, target):
    # returns tuple of 3 ints: 2=green,1=yellow,0=gray
    fb = [0]*3
    used = [False]*3
    # green pass
    for i,(g,t) in enumerate(zip(guess,target)):
        if g == t:
            fb[i] = 2
            used[i] = True
    # yellow pass
    for i,g in enumerate(guess):
        if fb[i] == 0:
            for j,t in enumerate(target):
                if not used[j] and g == t:
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

# --- 4. Compute best starting word ---
entropies = {g: expected_entropy(g, TARGETS) for g in GUESSES}
best_start = max(entropies, key=entropies.get)
print(f"Best first guess: {best_start} (entropy = {entropies[best_start]:.3f} bits)")

# Display top 5
print("Top 5 starting guesses:")
for g, e in sorted(entropies.items(), key=lambda x: -x[1])[:5]:
    print(f"  {g}: {e:.3f}")

# --- 5. Simulation of play using entropy-optimal guesses ---
def simulate_game(secret):
    candidates = TARGETS.copy()
    history = []
    while True:
        guess = max(candidates, key=lambda g: expected_entropy(g, candidates))
        fb = score_feedback(guess, secret)
        history.append((guess, fb))
        if fb == (2,2,2):
            return history
        # filter candidates
        candidates = [w for w in candidates if score_feedback(guess,w)==fb]


# Simulate all possible secrets (parallelized)
def simulate_game_length(secret):
    return secret, len(simulate_game(secret))

if __name__ == "__main__":
    with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        results_list = list(executor.map(simulate_game_length, TARGETS))
    results = dict(results_list)
    avg_steps = sum(results.values()) / len(results)
    print(f"Average guesses to solve 3‑letter Wordle: {avg_steps:.2f}")
    for w, steps in results.items():
        print(f"  Secret={w}, guesses={steps}")