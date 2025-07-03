import numpy as np
import matplotlib.pyplot as plt

def entropy(p):
    p = np.clip(p, 1e-12, 1 - 1e-12)
    return - (p * np.log2(p) + (1 - p) * np.log2(1 - p))

def update_belief_given_bet(prior, bluff_rate=1/3):
    p_bet = prior * 1 + (1 - prior) * bluff_rate
    return (prior * 1) / p_bet

# Initial prior
prior = 0.5
bluff_rate = 1/3

# Step 0: Before any action
H0 = entropy(prior)

# Step 1: Player 1 acts (always bets with King, 1/3 with Queen)
# Prob(P1 bets) = 0.5 * 1 + 0.5 * 1/3 = 2/3
# Prob(P1 folds) = 1 - 2/3 = 1/3

# If P1 folds → belief unchanged ⇒ H1_fold = H0
# If P1 bets → update belief
belief_after_bet = update_belief_given_bet(prior, bluff_rate)
H1_bet = entropy(belief_after_bet)
H1_fold = H0  # no update

# Expected entropy at Turn 1
H1_expected = (2/3)*H1_bet + (1/3)*H1_fold

# Step 2: No further information in this game structure — entropy stays the same
H2 = H1_expected

# Plot entropy trajectory
turns = ['Initial', 'After P1 Action', 'After P2 Observes']
entropy_vals = [H0, H1_expected, H2]

plt.figure(figsize=(8, 5))
plt.plot(turns, entropy_vals, marker='o', color='purple')
plt.title("Entropy Trajectory in Stripped-Down Poker")
plt.ylabel("Entropy (bits)")
plt.ylim(0, 1.05)
plt.grid(True)
plt.show()

# Print entropy values
print(f"Turn 0: {H0:.3f} bits")
print(f"Turn 1 (expected): {H1_expected:.3f} bits")
print(f"Turn 2: {H2:.3f} bits (same as Turn 1)")
