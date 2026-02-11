# Quick Start Guide - Mac Setup

## What Happened

You downloaded the files to your Downloads folder, but you're trying to run them from `/Users/marko77/Desktop/ASI`. Python can't find the scripts because they're not in your current directory.

---

## Solution 1: Automatic Installation (Recommended)

### Step 1: Make the installer executable
```bash
cd ~/Downloads
chmod +x install.sh
```

### Step 2: Run the installer
```bash
./install.sh
```

When prompted, enter: `/Users/marko77/Desktop/ASI`

This will:
- Copy all scripts to `ASI/experiments/`
- Create `ASI/results/` directory
- Check your Python dependencies
- Verify your API key

---

## Solution 2: Manual Installation (If installer doesn't work)

### Step 1: Copy files manually
```bash
cd /Users/marko77/Desktop/ASI

# Create directories
mkdir -p experiments
mkdir -p results

# Copy from Downloads
cp ~/Downloads/experiment_extended_validation.py experiments/
cp ~/Downloads/test_setup.py experiments/
cp ~/Downloads/compare_experiments.py experiments/
cp ~/Downloads/EXPERIMENT_EXTENDED_README.md experiments/
cp ~/Downloads/compressibility_divergence.pdf results/
cp ~/Downloads/GITHUB_INTEGRATION_GUIDE.md .
cp ~/Downloads/DELIVERY_SUMMARY.md .
```

### Step 2: Verify files are there
```bash
ls experiments/
# Should show: experiment_extended_validation.py, test_setup.py, compare_experiments.py
```

---

## After Installation

### 1. Install Python dependencies
```bash
pip3 install anthropic numpy matplotlib seaborn scipy
```

Or if you prefer conda:
```bash
conda install numpy matplotlib seaborn scipy
pip install anthropic
```

### 2. Set your API key

**Temporary (just for this session):**
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

**Permanent (persists across sessions):**
```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### 3. Test setup
```bash
cd /Users/marko77/Desktop/ASI/experiments
python3 test_setup.py
```

Expected output:
```
✓ All dependencies OK
✓ API key found
✓ API connection successful
✓ Pipeline functional
```

### 4. Run the experiment
```bash
python3 experiment_extended_validation.py
```

---

## Troubleshooting

### "command not found: python"
- Try `python3` instead of `python`
- Or check with: `which python3`

### "ModuleNotFoundError: No module named 'anthropic'"
```bash
pip3 install anthropic
# or
python3 -m pip install anthropic
```

### "Permission denied"
```bash
chmod +x install.sh
```

### "API key not found"
```bash
# Check if it's set:
echo $ANTHROPIC_API_KEY

# If empty, set it:
export ANTHROPIC_API_KEY="your-key-here"
```

---

## Your Current Directory Structure

After installation, you should have:

```
/Users/marko77/Desktop/ASI/
├── experiments/
│   ├── experiment_extended_validation.py
│   ├── test_setup.py
│   ├── compare_experiments.py
│   └── EXPERIMENT_EXTENDED_README.md
├── results/
│   └── compressibility_divergence.pdf
├── docs/
│   └── (your existing docs)
├── notes/
│   └── (your existing notes)
├── GITHUB_INTEGRATION_GUIDE.md
├── DELIVERY_SUMMARY.md
└── README.md
```

---

## Quick Commands Reference

```bash
# Navigate to experiments
cd /Users/marko77/Desktop/ASI/experiments

# Test setup (5 minutes)
python3 test_setup.py

# Run full experiment (2-3 hours)
python3 experiment_extended_validation.py

# Compare with original (after experiment)
python3 compare_experiments.py

# Check results
ls ../results/
```

---

## What Each Script Does

**`test_setup.py`** (5 min)
- Checks dependencies
- Verifies API key
- Runs mini 2-iteration test
- **Run this first**

**`experiment_extended_validation.py`** (2-3 hours)
- Main experiment
- 100 iterations × 10 seeds × 2 conditions
- Generates 4 output files in `results/`
- Costs ~$15-25 in API calls

**`compare_experiments.py`** (5 min)
- Compares original 30-iter with extended 100-iter
- Statistical analysis
- Generates comparison plots

---

## Ready to Start?

```bash
# 1. Install everything
cd ~/Downloads
chmod +x install.sh
./install.sh

# 2. Follow the on-screen instructions

# 3. Test
cd /Users/marko77/Desktop/ASI/experiments
python3 test_setup.py

# 4. If test passes → run experiment
python3 experiment_extended_validation.py
```

---

## Need Help?

The installer will check everything and tell you what's missing. If you see any ✗ marks, follow the suggestions provided.
