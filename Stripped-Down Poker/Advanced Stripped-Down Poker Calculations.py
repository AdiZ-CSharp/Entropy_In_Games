import numpy as np
import matplotlib.pyplot as plt

# ---------- Core Functions ----------

def entropy(p):
    p = np.clip(p, 1e-12, 1 - p + 1e-12)  # avoid log(0)
    return - (p * np.log2(p) + (1 - p) * np.log2(1 - p))

def update_belief_given_bet(prior, bluff_rate):
    # Bayes' rule: P(K | bet) = P(bet | K) * P(K) / P(bet)
    # P(bet | K) = 1, P(bet | Q) = bluff_rate
    p_bet = prior * 1 + (1 - prior) * bluff_rate
    return (prior * 1) / p_bet

def simulate_game(prior=0.5, bluff_rate=1/3):
    # Randomly deal a card to Player 1
    card = np.random.choice(['K', 'Q'], p=[prior, 1 - prior])

    # Player 1's action based on strategy
    if card == 'K':
        action1 = 'bet'
    else:
        action1 = 'bet' if np.random.rand() < bluff_rate else 'fold'

    # Entropy calculations
    H0 = entropy(prior)

    if action1 == 'fold':
        # No information revealed
        H1 = H0
        H2 = H1
    else:
        # Bet observed → Bayesian update
        belief_after_bet = update_belief_given_bet(prior, bluff_rate)
        H1 = entropy(belief_after_bet)
        H2 = H1  # no additional info in this simplified model

    return H0, H1, H2

def run_trials(num_trials=10000, bluff_rate=1/3):
    H0_vals, H1_vals, H2_vals = [], [], []
    for _ in range(num_trials):
        H0, H1, H2 = simulate_game(bluff_rate=bluff_rate)
        H0_vals.append(H0)
        H1_vals.append(H1)
        H2_vals.append(H2)
    return np.mean(H0_vals), np.mean(H1_vals), np.mean(H2_vals)

# ---------- Run Simulations Across Bluff Rates ----------

bluff_rates = np.linspace(0, 1, 11)
H0s, H1s, H2s = [], [], []

print("Bluff rate → Expected entropy after P1's action (Turn 1):")
for rate in bluff_rates:
    H0, H1, H2 = run_trials(5000, bluff_rate=rate)
    H0s.append(H0)
    H1s.append(H1)
    H2s.append(H2)
    print(f"  {rate:.2f} → {H1:.4f} bits")

# ---------- Plot Results ----------

plt.figure(figsize=(10,6))
plt.plot(bluff_rates, H0s, label='Turn 0 (Initial)', linestyle='--', color='gray')
plt.plot(bluff_rates, H1s, label='Turn 1 (After Bet/Fold)', marker='o')
plt.plot(bluff_rates, H2s, label='Turn 2 (After P2 observes)', marker='x')
plt.title("Entropy vs Bluffing Rate in Stripped-Down Poker")
plt.xlabel("Bluffing Probability (P(bet | Queen))")
plt.ylabel("Expected Entropy (bits)")
plt.legend()
plt.grid(True)
plt.ylim(0.7, 1.02)
plt.show()