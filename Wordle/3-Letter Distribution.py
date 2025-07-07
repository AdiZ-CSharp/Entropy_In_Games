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

import matplotlib.pyplot as plt
from collections import Counter

# Flatten all letters from all words into a single list
all_letters = [letter for word in TARGETS for letter in word]

# Count frequency of each letter
letter_counts = Counter(all_letters)

# Sort letters alphabetically for the plot
letters = sorted(letter_counts)
frequencies = [letter_counts[letter] for letter in letters]

# Plot
plt.figure(figsize=(12, 6))
plt.bar(letters, frequencies, color='skyblue')
plt.xlabel('Letter')
plt.ylabel('Frequency')
plt.title('Letter Distribution in 3-Letter Word Dataset')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()