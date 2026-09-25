from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path


def audit(path: Path, train_fraction: float = 0.75) -> dict[str, float | int]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = [row for row in csv.DictReader(handle) if row["等效塑性应变"] and float(row["等效塑性应变"]) >= 0.001]
    split = int(len(rows) * train_fraction)
    train, test = rows[:split], rows[split:]
    x = [float(row["等效塑性应变"]) for row in train]
    y = [float(row["等效应力/MPa"]) for row in train]
    xbar, ybar = sum(x) / len(x), sum(y) / len(y)
    hardening = sum((a - xbar) * (b - ybar) for a, b in zip(x, y)) / sum((a - xbar) ** 2 for a in x)
    yield_stress = ybar - hardening * xbar
    residuals = [yield_stress + hardening * float(row["等效塑性应变"]) - float(row["等效应力/MPa"]) for row in test]
    return {"train_points": len(train), "test_points": len(test), "Y_MPa": yield_stress, "H_MPa": hardening, "test_rmse_MPa": math.sqrt(sum(value * value for value in residuals) / len(residuals))}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    args = parser.parse_args()
    print(audit(args.csv))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
