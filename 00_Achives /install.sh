#!/bin/bash

# Installation Script for Extended Validation Experiment
# This sets up everything in your ASI directory

echo "========================================"
echo "Extended Validation - Installation"
echo "========================================"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Installing from: $SCRIPT_DIR"
echo ""

# Ask for target directory
echo "Where do you want to install? (Press Enter for current directory)"
read -p "Target directory [$(pwd)]: " TARGET_DIR
TARGET_DIR=${TARGET_DIR:-$(pwd)}

echo ""
echo "Installing to: $TARGET_DIR"
echo ""

# Create directory structure
echo "1. Creating directory structure..."
mkdir -p "$TARGET_DIR/experiments"
mkdir -p "$TARGET_DIR/results"
echo "   ✓ Created experiments/ and results/"

# Copy files
echo ""
echo "2. Copying experiment files..."
cp "$SCRIPT_DIR/experiment_extended_validation.py" "$TARGET_DIR/experiments/" 2>/dev/null || \
   cp "$SCRIPT_DIR"/../experiment_extended_validation.py "$TARGET_DIR/experiments/" || \
   echo "   ⚠ Could not find experiment_extended_validation.py"

cp "$SCRIPT_DIR/test_setup.py" "$TARGET_DIR/experiments/" 2>/dev/null || \
   cp "$SCRIPT_DIR"/../test_setup.py "$TARGET_DIR/experiments/" || \
   echo "   ⚠ Could not find test_setup.py"

cp "$SCRIPT_DIR/compare_experiments.py" "$TARGET_DIR/experiments/" 2>/dev/null || \
   cp "$SCRIPT_DIR"/../compare_experiments.py "$TARGET_DIR/experiments/" || \
   echo "   ⚠ Could not find compare_experiments.py"

echo "   ✓ Copied experiment scripts"

# Copy documentation
echo ""
echo "3. Copying documentation..."
cp "$SCRIPT_DIR/EXPERIMENT_EXTENDED_README.md" "$TARGET_DIR/experiments/" 2>/dev/null || \
   cp "$SCRIPT_DIR"/../EXPERIMENT_EXTENDED_README.md "$TARGET_DIR/experiments/" || \
   echo "   ⚠ Could not find EXPERIMENT_EXTENDED_README.md"

cp "$SCRIPT_DIR/GITHUB_INTEGRATION_GUIDE.md" "$TARGET_DIR/" 2>/dev/null || \
   cp "$SCRIPT_DIR"/../GITHUB_INTEGRATION_GUIDE.md "$TARGET_DIR/" || \
   echo "   ⚠ Could not find GITHUB_INTEGRATION_GUIDE.md"

cp "$SCRIPT_DIR/DELIVERY_SUMMARY.md" "$TARGET_DIR/" 2>/dev/null || \
   cp "$SCRIPT_DIR"/../DELIVERY_SUMMARY.md "$TARGET_DIR/" || \
   echo "   ⚠ Could not find DELIVERY_SUMMARY.md"

echo "   ✓ Copied documentation"

# Check for original results
echo ""
echo "4. Looking for original compressibility_divergence.pdf..."
if [ -f "$SCRIPT_DIR/compressibility_divergence.pdf" ]; then
    cp "$SCRIPT_DIR/compressibility_divergence.pdf" "$TARGET_DIR/results/"
    echo "   ✓ Copied original PDF to results/"
elif [ -f "$SCRIPT_DIR"/../compressibility_divergence.pdf ]; then
    cp "$SCRIPT_DIR"/../compressibility_divergence.pdf "$TARGET_DIR/results/"
    echo "   ✓ Copied original PDF to results/"
else
    echo "   ⚠ Original PDF not found (you can add it later)"
fi

# Check Python dependencies
echo ""
echo "5. Checking Python dependencies..."
python3 -c "import anthropic" 2>/dev/null && echo "   ✓ anthropic" || echo "   ✗ anthropic (pip install anthropic)"
python3 -c "import numpy" 2>/dev/null && echo "   ✓ numpy" || echo "   ✗ numpy (pip install numpy)"
python3 -c "import matplotlib" 2>/dev/null && echo "   ✓ matplotlib" || echo "   ✗ matplotlib (pip install matplotlib)"
python3 -c "import seaborn" 2>/dev/null && echo "   ✓ seaborn" || echo "   ✗ seaborn (pip install seaborn)"
python3 -c "import scipy" 2>/dev/null && echo "   ✓ scipy" || echo "   ✗ scipy (pip install scipy)"

# Check API key
echo ""
echo "6. Checking API key..."
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "   ✗ ANTHROPIC_API_KEY not set"
    echo "   Set it with: export ANTHROPIC_API_KEY='your-key-here'"
    echo "   Or add to ~/.zshrc for persistence"
else
    echo "   ✓ ANTHROPIC_API_KEY is set"
fi

# Summary
echo ""
echo "========================================"
echo "✓ Installation Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Install missing dependencies (if any):"
echo "   pip install anthropic numpy matplotlib seaborn scipy"
echo ""
echo "2. Set your API key (if not already set):"
echo "   export ANTHROPIC_API_KEY='your-key-here'"
echo ""
echo "3. Test your setup:"
echo "   cd $TARGET_DIR/experiments"
echo "   python3 test_setup.py"
echo ""
echo "4. Run the experiment:"
echo "   python3 experiment_extended_validation.py"
echo ""
echo "Files installed at:"
echo "   $TARGET_DIR/experiments/"
echo "   $TARGET_DIR/results/"
echo ""
