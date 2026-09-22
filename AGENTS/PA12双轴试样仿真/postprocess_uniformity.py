# -*- coding: utf-8 -*-
"""Extract center-region uniformity metrics from one Abaqus ODB."""

from __future__ import print_function

import csv
import json
import math
import os
import sys

from odbAccess import openOdb


def _metric(values):
    if not values:
        raise RuntimeError("field region has no values")
    mean = sum(values) / float(len(values))
    variance = sum((value - mean) ** 2 for value in values) / float(len(values))
    standard_deviation = math.sqrt(variance)
    denominator = abs(mean)
    cv = standard_deviation / denominator if denominator > 1.0e-12 else None
    return {"n": len(values), "mean": mean, "std": standard_deviation, "cv": cv}


def _component(value, index):
    return float(value.data[index])


def main():
    if len(sys.argv) < 2:
        raise RuntimeError("usage: abaqus python postprocess_uniformity.py <job.odb>")
    odb_path = os.path.abspath(sys.argv[1])
    output_path = os.path.splitext(odb_path)[0] + "_uniformity.json"
    odb = openOdb(path=odb_path, readOnly=True)
    step = odb.steps[sorted(odb.steps.keys())[-1]]
    frame = step.frames[-1]
    instance = odb.rootAssembly.instances[sorted(odb.rootAssembly.instances.keys())[0]]
    center = instance.elementSets["CENTER_REGION"]

    stress = frame.fieldOutputs["S"].getSubset(region=center).values
    strain_name = "E" if "E" in frame.fieldOutputs else "LE"
    strain = frame.fieldOutputs[strain_name].getSubset(region=center).values

    result = {
        "odb": odb_path,
        "step": step.name,
        "frame_value": frame.frameValue,
        "strain_field": strain_name,
        "S11": _metric([_component(value, 0) for value in stress]),
        "S22": _metric([_component(value, 1) for value in stress]),
        "E11": _metric([_component(value, 0) for value in strain]),
        "E22": _metric([_component(value, 1) for value in strain]),
    }
    e11 = result["E11"]["mean"]
    e22 = result["E22"]["mean"]
    denominator = abs(e11) + abs(e22)
    result["K_ratio"] = abs(e11 - e22) / denominator if denominator > 1.0e-12 else None
    result["primary_score"] = sum(
        result[name]["cv"] for name in ("S11", "S22", "E11", "E22")
        if result[name]["cv"] is not None
    )

    with open(output_path, "w") as handle:
        json.dump(result, handle, indent=2)
    with open(os.path.splitext(output_path)[0] + ".csv", "w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["metric", "mean", "std", "cv"])
        for name in ("S11", "S22", "E11", "E22"):
            item = result[name]
            writer.writerow([name, item["mean"], item["std"], item["cv"]])
        writer.writerow(["K_ratio", result["K_ratio"], "", ""])
        writer.writerow(["primary_score", result["primary_score"], "", ""])
    odb.close()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
