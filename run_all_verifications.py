#!/usr/bin/env python3
"""
run_all_verifications.py
========================
Unified single-entry-point verification runner for repository
"AdjustedRedundancyIndex_Non-Linear (EigenFlow)" — Harids Irawan (2026).

Executes the full suite of deterministic tests:
  1. Gate 1: Mathematical Verification of Non-Linear Woodbury / Sherman-Morrison Solver & Elasto-Plastic Pushover (Eqs. 4.13d–4.13g)
  2. Gate 2: Branched Pipeline Verification (ARI Linear Gatekeeper -> EigenFlow Non-Linear Woodbury Transparency & Prescriptive Advisor)

How to run from repository root:
    python3 run_all_verifications.py
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
EXAMPLES_DIR = ROOT_DIR / "examples"

SUITE = [
    ("1. Gate 1: Non-Linear Woodbury Solver & Elasto-Plastic Pushover (M1–M4)", "test_woodbury_solver.py"),
    ("2. Gate 2: Branched Pipeline ARI Linear -> Non-Linear & Prescriptive Recommendations", "test_branching_pipeline.py"),
]


def main() -> int:
    print("=" * 88)
    print("UNIFIED VERIFICATION SUITE — ADJUSTED REDUNDANCY INDEX NON-LINEAR (EIGENFLOW)")
    print("=" * 88)

    results = []
    t0_all = time.perf_counter()

    for label, script_name in SUITE:
        script_path = EXAMPLES_DIR / script_name
        print(f"\n>>> Running {label} ({script_name})...")
        t0 = time.perf_counter()
        proc = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(EXAMPLES_DIR),
            capture_output=True,
            text=True,
        )
        dt = time.perf_counter() - t0
        passed = proc.returncode == 0
        print(proc.stdout.strip())
        if not passed and proc.stderr:
            print(proc.stderr.strip(), file=sys.stderr)
        results.append((label, passed, dt))

    total_dt = time.perf_counter() - t0_all
    n_pass = sum(1 for _, ok, _ in results if ok)
    n_total = len(results)

    print("\n" + "=" * 88)
    print("VERIFICATION RESULTS SUMMARY — ARI NON-LINEAR REPOSITORY (EIGENFLOW)")
    print("=" * 88)
    print(f"{'Verification Stage':<64} | {'Status':<8} | {'Time':>8}")
    print("-" * 88)
    for label, ok, dt in results:
        print(f"{label:<64} | {'PASSED' if ok else 'FAILED':<8} | {dt:>6.2f} s")
    print("-" * 88)
    print(f"Total Passed Stages: {n_pass}/{n_total} | Total Execution Time: {total_dt:.2f} seconds")
    print("=" * 88)
    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    raise SystemExit(main())
