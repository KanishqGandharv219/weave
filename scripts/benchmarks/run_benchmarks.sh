#!/bin/bash
# Benchmark runner — compares Weave against baselines
# Usage: ./run_benchmarks.sh [weave|local|saladcloud|replicate]

set -euo pipefail

echo "Weave Benchmark Suite"
echo "====================="
echo "Phase 0: Scaffolding only — real benchmarks start Phase 1"
echo ""
echo "Baselines to compare:"
echo "  1. Local single-device (llama.cpp)"
echo "  2. SaladCloud API"
echo "  3. Replicate API"
echo "  4. Weave (two-node WAN)"
echo ""
echo "Metrics:"
echo "  - Time to first token (TTFT)"
echo "  - Total generation time"
echo "  - Tokens per second"
echo "  - Cost per 1K tokens"
echo "  - Job success rate"
echo "  - P2P overhead vs local"
