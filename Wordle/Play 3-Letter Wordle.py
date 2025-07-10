import math
import matplotlib.pyplot as plt
from collections import Counter
import random

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

# --- 4. Playable game loop ---
def play_wordle():
    secret = random.choice(TARGETS)
    candidates = TARGETS.copy()
    entropy_trace = []
    print("Welcome to 3-Letter Wordle!")
    # Uncomment below to debug with a known word
    # print(f"[DEBUG] Secret word: {secret}")
    moves = 0
    while True:
        guess = input(f"\nEnter your guess #{moves+1} (3-letter word): ").lower().strip()
        if len(guess) != 3 or guess not in GUESSES:
            print("Invalid guess. Please enter a valid 3-letter word from the allowed list.")
            continue
        fb = score_feedback(guess, secret)
        moves += 1
        # Print feedback in Wordle style
        fb_str = ''.join(['🟩' if x==2 else '🟨' if x==1 else '⬜' for x in fb])
        print(f"Feedback: {fb_str}")
        ent = expected_entropy(guess, candidates)
        entropy_trace.append(ent)
        if fb == (2,2,2):
            print(f"Congratulations! You solved it in {moves} moves. The word was '{secret}'.")
            break
        # Filter candidates
        candidates = [w for w in candidates if score_feedback(guess, w) == fb]
        print(f"Possible words remaining: {len(candidates)}")
    # Plot entropy trace
    plt.figure(figsize=(7,4))
    plt.plot(range(1, len(entropy_trace)+1), entropy_trace, marker='o', color='blue')
    plt.title("Entropy After Each Move (3-Letter Wordle)")
    plt.xlabel("Move Number")
    plt.ylabel("Expected Entropy (bits)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    play_wordle()
