import itertools
import math
from collections import Counter, defaultdict

# --- 1. Word list ---
# Example small 3-letter word list; expand as needed
TARGETS = ['cat','dog','pig','cow','bug','sun','fun','run','pan','man']
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

# Simulate all possible secrets
results = {secret: len(simulate_game(secret)) 
           for secret in TARGETS}
avg_steps = sum(results.values()) / len(results)
print(f"Average guesses to solve 3‑letter Wordle: {avg_steps:.2f}")
for w, steps in results.items():
    print(f"  Secret={w}, guesses={steps}")