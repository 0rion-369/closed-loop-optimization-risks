import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load data
DATA_PATH = 'results/grok_extended_validation.json'
if not os.path.exists(DATA_PATH):
    print(f"Error: {DATA_PATH} not found.")
    exit()

with open(DATA_PATH, 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Calculate Lexical Richness
def unique_ratio(text):
    words = text.lower().split()
    return len(set(words)) / len(words) if words else 0

df['unique_ratio'] = df['text'].apply(unique_ratio)

# Plotting
plt.figure(figsize=(14, 7))
sns.set_theme(style="whitegrid")

sns.lineplot(data=df, x='iteration', y='unique_ratio', hue='condition', palette=['#E63946', '#2A9D8F'])

plt.title('Lexical Richness Divergence: Closed-Loop vs Exogenous', fontsize=16)
plt.xlabel('Iteration Step', fontsize=12)
plt.ylabel('Unique Word Ratio', fontsize=12)
plt.legend(title='Condition')

# Save to results
plt.savefig('results/grok_divergence_chart.png')
print("✅ Visualization generated: results/grok_divergence_chart.png")
