"""
Quick Test - Verify Setup Before Full Experiment
Run this first to ensure everything works (5 minutes)
"""

import anthropic
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import json
from pathlib import Path

print("\n" + "="*60)
print("SETUP VERIFICATION TEST")
print("="*60 + "\n")

# Test 1: Dependencies
print("1. Checking dependencies...")
dependencies = {
    'anthropic': anthropic,
    'numpy': np,
    'matplotlib': plt,
    'seaborn': sns,
    'scipy': stats,
    'json': json,
    'pathlib': Path
}

all_ok = True
for name, module in dependencies.items():
    try:
        print(f"   ✓ {name}: {module.__version__ if hasattr(module, '__version__') else 'OK'}")
    except Exception as e:
        print(f"   ✗ {name}: FAILED - {e}")
        all_ok = False

if not all_ok:
    print("\n⚠ Some dependencies missing. Install with:")
    print("   pip install anthropic numpy matplotlib seaborn scipy")
    exit(1)

# Test 2: API Key
print("\n2. Checking API key...")
try:
    client = anthropic.Anthropic(api_key=" API KEY ")
    print("   ✓ API key found")
except Exception as e:
    print(f"   ✗ API key not found")
    print("   Set it with: export ANTHROPIC_API_KEY='your-key-here'")
    print("   Or edit line 23 in experiment_extended_validation.py")
    exit(1)

# Test 3: Quick API call
print("\n3. Testing API connection (1 quick call)...")
try:
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=50,
        messages=[{"role": "user", "content": "Say 'test successful' and nothing else."}]
    )
    response = message.content[0].text
    print(f"   ✓ API response: {response[:50]}...")
except Exception as e:
    print(f"   ✗ API call failed: {e}")
    exit(1)

# Test 4: Output directory
print("\n4. Checking output directory...")
output_dir = Path("results")
try:
    output_dir.mkdir(exist_ok=True)
    test_file = output_dir / "test.txt"
    test_file.write_text("test")
    test_file.unlink()
    print(f"   ✓ Can write to {output_dir}/")
except Exception as e:
    print(f"   ✗ Cannot write to output directory: {e}")
    exit(1)

# Test 5: Mini experiment (2 iterations)
print("\n5. Running mini experiment (2 iterations, 1 seed)...")
print("   This tests the full pipeline in ~60 seconds...")

from collections import Counter

def lempel_ziv_complexity(s):
    if not s:
        return 0
    i, c = 0, 1
    u, v, w = 0, 1, 1
    s_len = len(s)
    
    while u + v <= s_len:
        if s[i + v - 1] == s[u + v - 1]:
            v += 1
        else:
            c += 1
            i = 0
            u += w
            v = 1
            w = u
    if v != 1:
        c += 1
    
    return c / (len(s) / np.log2(len(s)))

def shannon_entropy(s):
    if not s:
        return 0
    counts = Counter(s)
    probs = [count / len(s) for count in counts.values()]
    return -sum(p * np.log2(p) for p in probs)

def compute_metrics(text):
    return {
        'lz': lempel_ziv_complexity(text),
        'shannon': shannon_entropy(text)
    }

# Mini test
prompt = "Explain the concept of emergence."
results_test = []

for i in range(2):
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        temperature=0.8,
        messages=[{"role": "user", "content": prompt}]
    )
    response = message.content[0].text
    metrics = compute_metrics(response)
    results_test.append(metrics)
    prompt = response[:200]  # Self-reference for next iteration
    print(f"   Iteration {i+1}: LZ={metrics['lz']:.3f}, Shannon={metrics['shannon']:.3f}")

print("\n   ✓ Pipeline functional")

# Summary
print("\n" + "="*60)
print("✓ ALL CHECKS PASSED")
print("="*60)
print("\nYou're ready to run the full experiment:")
print("  python experiment_extended_validation.py")
print("\nEstimated:")
print("  - Runtime: 2-3 hours")
print("  - API calls: 2000 (100 iterations × 10 seeds × 2 conditions)")
print("  - Cost: ~$15-25 (depending on pricing)")
print("\nPress Ctrl+C to cancel at any time. Progress is saved after each seed.")
print("\n")
