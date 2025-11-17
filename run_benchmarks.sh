#!/bin/bash
# run_benchmarks.sh - One-Click Benchmark Execution
# 
# This script runs all benchmarks for the Hope Genome supplementary material
# and generates publication-ready results.

set -e  # Exit on error

echo "========================================================================"
echo "HOPE GENOME - AUTOMATED BENCHMARK SUITE"
echo "========================================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}[1/7] Checking Python version...${NC}"
python --version
if ! python -c 'import sys; assert sys.version_info >= (3, 10)' 2>/dev/null; then
    echo "ERROR: Python 3.10+ required"
    exit 1
fi
echo -e "${GREEN}✓ Python version OK${NC}"
echo ""

# Install dependencies
echo -e "${BLUE}[2/7] Installing dependencies...${NC}"
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Create results directory
mkdir -p results

# Run integrity benchmarks
echo -e "${BLUE}[3/7] Running Integrity Verification Benchmarks...${NC}"
python benchmark.py --test integrity
echo -e "${GREEN}✓ Integrity benchmarks complete${NC}"
echo ""

# Run collective benchmarks
echo -e "${BLUE}[4/7] Running Collective Resonance Benchmarks...${NC}"
python benchmark.py --test collective
echo -e "${GREEN}✓ Collective benchmarks complete${NC}"
echo ""

# Run memory benchmarks
echo -e "${BLUE}[5/7] Running Memory Usage Benchmarks...${NC}"
python benchmark.py --test memory
echo -e "${GREEN}✓ Memory benchmarks complete${NC}"
echo ""

# Run robustness tests
echo -e "${BLUE}[6/7] Running Robustness Tests...${NC}"
if [ -d "tests" ]; then
    pytest tests/test_robustness.py -v --tb=short
else
    echo "Note: tests/ directory not found, skipping pytest"
fi
echo -e "${GREEN}✓ Robustness tests complete${NC}"
echo ""

# Generate plots
echo -e "${BLUE}[7/7] Generating plots...${NC}"
python benchmark.py --generate-plots
echo -e "${GREEN}✓ Plots generated${NC}"
echo ""

# Summary
echo "========================================================================"
echo "BENCHMARK SUITE COMPLETE"
echo "========================================================================"
echo ""
echo "Results saved to:"
echo "  - results/benchmark_results.json (raw data)"
echo "  - results/integrity_latency.png (figure)"
echo "  - results/collective_scaling.png (figure)"
echo "  - results/memory_usage.png (figure)"
echo ""
echo "To view results:"
echo "  cat results/benchmark_results.json | python -m json.tool"
echo "  open results/*.png  # macOS"
echo "  xdg-open results/*.png  # Linux"
echo ""
echo "These results are ready for inclusion in the supplementary material."
echo ""
