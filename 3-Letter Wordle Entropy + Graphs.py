import itertools
import math
import matplotlib.pyplot as plt
from collections import Counter, defaultdict

# --- 1. Word list ---
TARGETS = ['cat', 'dog', 'pig', 'cow', 'bug', 'sun', 'fun', 'run', 'pan', 'man']
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

# --- 4. Find best first guess ---
entropies = {g: expected_entropy(g, TARGETS) for g in GUESSES}
best_start = max(entropies, key=entropies.get)

print(f"Best first guess: {best_start} (entropy = {entropies[best_start]:.3f} bits)")
print("Top 5 starting guesses:")
for g, e in sorted(entropies.items(), key=lambda x: -x[1])[:5]:
    print(f"  {g}: {e:.3f}")

# --- 5. Game simulation with entropy tracking ---
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

# --- 6. Run all simulations ---
guess_counts = []
entropy_logs = []
for word in TARGETS:
    history, entropies = simulate_game(word)
    guess_counts.append(len(history))
    entropy_logs.append(entropies)

avg_guesses = sum(guess_counts) / len(guess_counts)
print(f"\n📊 Average number of guesses to solve: {avg_guesses:.2f}")
for w, n in zip(TARGETS, guess_counts):
    print(f"  Secret: {w}, Guesses: {n}")

# --- 7. Plotting ---

# a) Average entropy per turn
max_turns = max(len(e) for e in entropy_logs)
avg_entropy_by_turn = []
for i in range(max_turns):
    turn_vals = [e[i] for e in entropy_logs if i < len(e)]
    avg_entropy_by_turn.append(sum(turn_vals) / len(turn_vals))

plt.figure(figsize=(10,5))
plt.plot(range(1, len(avg_entropy_by_turn)+1), avg_entropy_by_turn, marker='o')
plt.title("📈 Average Entropy per Turn")
plt.xlabel("Turn")
plt.ylabel("Expected Entropy (bits)")
plt.grid(True)
plt.show()

# b) Number of guesses required per word
plt.figure(figsize=(10,5))
plt.bar(TARGETS, guess_counts)
plt.title("🔢 Number of Guesses per Secret Word")
plt.xlabel("Secret Word")
plt.ylabel("Guesses Required")
plt.grid(True)
plt.show()

# --- 8. Specific Examples ---
print("\n🔍 Example Guess Feedbacks:")
examples = [('cat', 'dog'), ('dog', 'dog'), ('bug', 'sun'), ('man', 'pan')]
for guess, target in examples:
    fb = score_feedback(guess, target)
    print(f"  Guess: {guess}, Target: {target}, Feedback: {fb}")