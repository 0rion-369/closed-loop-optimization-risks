import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_data(path, model_name, condition):
    if not os.path.exists(path): return pd.DataFrame()
    with open(path, 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['model_label'] = model_name
    df['unique_ratio'] = df['text'].apply(lambda x: len(set(x.lower().split())) / len(x.lower().split()) if x.lower().split() else 0)
    return df

# Load all 3 datasets
grok_df = load_data('results/grok_extended_validation.json', 'Grok-4-1 (Explosion)', 'closed_loop')
v3_df = load_data('results/deepseek_deepseek_chat_validation.json', 'DeepSeek-V3 (Attractor)', 'closed_loop')
r1_df = load_data('results/deepseek_r1_reasoner_validation.json', 'DeepSeek-R1 (Implosion)', 'closed_loop')

# Combine and Filter only closed-loop
full_df = pd.concat([grok_df, v3_df, r1_df])
full_df = full_df[full_df['condition'] == 'closed_loop']

# Plotting
plt.figure(figsize=(14, 8))
sns.set_theme(style="darkgrid")
sns.lineplot(data=full_df, x='iteration', y='unique_ratio', hue='model_label', linewidth=2.5)

plt.title('The Hybrid Axis: Triple Divergence Analysis (0rion-369)', fontsize=18)
plt.xlabel('Recursive Iterations', fontsize=14)
plt.ylabel('Lexical Richness (Unique Word Ratio)', fontsize=14)
plt.xlim(0, 50)
plt.ylim(0.4, 0.8)
plt.legend(title='AI Architecture')

plt.savefig('results/triple_divergence_comparison.png')
print("✅ Final comparison chart generated: results/triple_divergence_comparison.png")
