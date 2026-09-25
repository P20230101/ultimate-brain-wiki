"""对已生成的自建 VFM CSV 做固定窗口稳定性审计；不重算或修改主结果。"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path


def _f(row: dict[str, str], key: str) -> float:
    return float(row[key])


def _fit_zero_intercept(xs: list[float], ys: list[float]) -> float:
    return sum(x * y for x, y in zip(xs, ys)) / sum(x * x for x in xs)


def audit(path: Path, windows: int = 4) -> list[dict[str, object]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    output: list[dict[str, object]] = []
    for number in range(windows):
        start = number * len(rows) // windows
        end = (number + 1) * len(rows) // windows
        block = rows[start:end]
        elastic = [
            row for row in block
            if max(abs(_f(row, "平均exx")), abs(_f(row, "平均eyy"))) <= 0.005
            and (_f(row, "X向力/N") > 5 or _f(row, "Y向力/N") > 5)
        ]
        coefficients = []
        forces = []
        for row in elastic:
            for coefficient, force in (("X虚场系数/N每MPa", "X向力/N"), ("Y虚场系数/N每MPa", "Y向力/N")):
                if _f(row, coefficient) != 0 and _f(row, force) > 5:
                    coefficients.append(_f(row, coefficient))
                    forces.append(_f(row, force))
        e = _fit_zero_intercept(coefficients, forces) if len(coefficients) >= 2 else None
        plastic = [row for row in block if _f(row, "等效塑性应变") >= 0.001 and _f(row, "等效应力/MPa") > 0]
        y = h = None
        if len(plastic) >= 2:
            x = [_f(row, "等效塑性应变") for row in plastic]
            stress = [_f(row, "等效应力/MPa") for row in plastic]
            xbar = sum(x) / len(x)
            ybar = sum(stress) / len(stress)
            slope = sum((a - xbar) * (b - ybar) for a, b in zip(x, stress)) / sum((a - xbar) ** 2 for a in x)
            h = slope
            y = ybar - slope * xbar
        output.append({"window": number + 1, "first_photo": block[0]["照片"], "last_photo": block[-1]["照片"], "rows": len(block), "elastic_points": len(elastic), "E_MPa": e, "plastic_points": len(plastic), "Y_MPa": y, "H_MPa": h})
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    parser.add_argument("--windows", type=int, default=4)
    args = parser.parse_args()
    for row in audit(args.csv, args.windows):
        print(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
