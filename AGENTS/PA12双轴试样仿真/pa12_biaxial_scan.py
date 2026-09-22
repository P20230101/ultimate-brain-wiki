# -*- coding: utf-8 -*-
"""Build one PA12 cruciform STEP model for Abaqus.

This script is intentionally a pipeline verifier first. The default material
card is marked provisional and must not be used as a scientific result.
"""

from __future__ import print_function

import json
import os
import sys

from abaqus import *
from abaqusConstants import *
from part import *
from interaction import *
from step import *
from load import *
import mesh
import regionToolset


PROVISIONAL_MATERIAL = {
    "E1": 1800.0,
    "E2": 1800.0,
    "E3": 1500.0,
    "nu12": 0.35,
    "nu13": 0.35,
    "nu23": 0.35,
    "G12": 666.7,
    "G13": 555.6,
    "G23": 555.6,
    "status": "PROVISIONAL_ONLY_NOT_FOR_PAPER",
}


def _value(args, name, default=None, required=False):
    if name in args:
        index = args.index(name)
        if index + 1 >= len(args):
            raise RuntimeError("missing value for %s" % name)
        return args[index + 1]
    if required:
        raise RuntimeError("missing required argument %s" % name)
    return default


def _args():
    raw = list(sys.argv)
    if "--" in raw:
        raw = raw[raw.index("--") + 1:]
    step_path = _value(raw, "--step", required=True)
    out_dir = os.path.abspath(_value(raw, "--out", required=True))
    return {
        "step": os.path.abspath(step_path),
        "out": out_dir,
        "dx": float(_value(raw, "--dx", "0.5")),
        "dy": float(_value(raw, "--dy", "0.5")),
        "mesh": float(_value(raw, "--mesh", "1.0")),
        "submit": "--submit" in raw,
        "job": _value(raw, "--job", None),
    }


def _ensure_directory(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def _reference_region(assembly, reference_point):
    return regionToolset.Region(
        referencePoints=(assembly.referencePoints[reference_point.id],)
    )


def _end_face_region(instance, axis, value, epsilon):
    bounds = {}
    bounds[axis + "Min"] = value - epsilon
    bounds[axis + "Max"] = value + epsilon
    faces = instance.faces.getByBoundingBox(**bounds)
    if not faces:
        raise RuntimeError("no end face found for %s=%g" % (axis, value))
    return regionToolset.Region(side1Faces=faces), len(faces)


def build_model(options):
    if not os.path.isfile(options["step"]):
        raise RuntimeError("STEP file not found: %s" % options["step"])
    _ensure_directory(options["out"])
    os.chdir(options["out"])

    model_name = "PA12_Biaxial"
    if model_name in mdb.models:
        del mdb.models[model_name]
    model = mdb.Model(name=model_name)

    step_geometry = mdb.openStep(fileName=options["step"], scaleFromFile=OFF)
    part = model.PartFromGeometryFile(
        name="Cruciform",
        geometryFile=step_geometry,
        combine=False,
        dimensionality=THREE_D,
        type=DEFORMABLE_BODY,
    )

    bbox = part.vertices.getBoundingBox()
    low = bbox["low"]
    high = bbox["high"]
    cx = 0.5 * (low[0] + high[0])
    cy = 0.5 * (low[1] + high[1])
    cz = 0.5 * (low[2] + high[2])
    epsilon = max(1.0e-4, 1.0e-5 * max(high[0] - low[0], high[1] - low[1]))

    material = model.Material(name="PA12_PROVISIONAL")
    material.Elastic(
        type=ENGINEERING_CONSTANTS,
        table=((PROVISIONAL_MATERIAL["E1"], PROVISIONAL_MATERIAL["E2"],
                PROVISIONAL_MATERIAL["E3"], PROVISIONAL_MATERIAL["nu12"],
                PROVISIONAL_MATERIAL["nu13"], PROVISIONAL_MATERIAL["nu23"],
                PROVISIONAL_MATERIAL["G12"], PROVISIONAL_MATERIAL["G13"],
                PROVISIONAL_MATERIAL["G23"]),),
    )
    section = model.HomogeneousSolidSection(
        name="PA12_SECTION", material=material.name, thickness=None
    )
    part.SectionAssignment(
        region=regionToolset.Region(cells=part.cells), sectionName=section.name
    )
    part.MaterialOrientation(
        region=regionToolset.Region(cells=part.cells),
        orientationType=GLOBAL,
        axis=AXIS_1,
        additionalRotationType=ROTATION_NONE,
        stackDirection=STACK_3,
    )

    part.setMeshControls(regions=part.cells, elemShape=TET, technique=FREE)
    elem_type = mesh.ElemType(elemCode=C3D10, elemLibrary=STANDARD)
    part.setElementType(regions=(part.cells,), elemTypes=(elem_type,))
    part.seedPart(size=options["mesh"], deviationFactor=0.1, minSizeFactor=0.1)
    part.generateMesh()
    center_elements = part.elements.getByBoundingBox(
        xMin=cx - 14.0, xMax=cx + 14.0,
        yMin=cy - 14.0, yMax=cy + 14.0,
        zMin=low[2] - epsilon, zMax=high[2] + epsilon,
    )
    if not center_elements:
        raise RuntimeError("center region contains no mesh elements")
    part.Set(name="CENTER_REGION", elements=center_elements)

    assembly = model.rootAssembly
    instance = assembly.Instance(name="Cruciform-1", part=part, dependent=ON)

    rp_xmin = assembly.ReferencePoint(point=(low[0], cy, cz))
    rp_xmax = assembly.ReferencePoint(point=(high[0], cy, cz))
    rp_ymin = assembly.ReferencePoint(point=(cx, low[1], cz))
    rp_ymax = assembly.ReferencePoint(point=(cx, high[1], cz))

    face_xmin, n_xmin = _end_face_region(instance, "x", low[0], epsilon)
    face_xmax, n_xmax = _end_face_region(instance, "x", high[0], epsilon)
    face_ymin, n_ymin = _end_face_region(instance, "y", low[1], epsilon)
    face_ymax, n_ymax = _end_face_region(instance, "y", high[1], epsilon)

    for name, rp, face_region in (
        ("XMIN", rp_xmin, face_xmin), ("XMAX", rp_xmax, face_xmax),
        ("YMIN", rp_ymin, face_ymin), ("YMAX", rp_ymax, face_ymax),
    ):
        model.Coupling(
            name="COUPLE_" + name,
            controlPoint=_reference_region(assembly, rp),
            surface=face_region,
            influenceRadius=WHOLE_SURFACE,
            couplingType=KINEMATIC,
            u1=ON, u2=ON, u3=ON,
            ur1=ON, ur2=ON, ur3=ON,
        )

    model.StaticStep(name="Load", previous="Initial", nlgeom=ON)
    model.fieldOutputRequests["F-Output-1"].setValues(
        variables=("S", "E", "LE", "U", "RF")
    )

    model.DisplacementBC(
        name="BC_XMIN", createStepName="Initial",
        region=_reference_region(assembly, rp_xmin), u1=0.0, u2=0.0, u3=0.0,
    )
    model.DisplacementBC(
        name="BC_YMIN", createStepName="Initial",
        region=_reference_region(assembly, rp_ymin), u2=0.0,
    )
    model.DisplacementBC(
        name="BC_XMAX", createStepName="Load",
        region=_reference_region(assembly, rp_xmax), u1=options["dx"],
    )
    model.DisplacementBC(
        name="BC_YMAX", createStepName="Load",
        region=_reference_region(assembly, rp_ymax), u2=options["dy"],
    )

    job_name = options["job"] or "pa12_%s" % os.path.splitext(os.path.basename(options["step"]))[0]
    job_name = job_name.replace("-", "_").replace(".", "_")[:80]
    job = mdb.Job(
        name=job_name,
        model=model_name,
        type=ANALYSIS,
        description="PA12 cruciform geometry scan; material card is provisional.",
        memory=90,
        memoryUnits=PERCENTAGE,
    )
    job.writeInput(consistencyChecking=OFF)
    mdb.saveAs(pathName=os.path.join(options["out"], job_name + ".cae"))

    manifest = {
        "status": "input_written",
        "step": options["step"],
        "output_directory": options["out"],
        "job": job_name,
        "bbox_low_mm": list(low),
        "bbox_high_mm": list(high),
        "center": [cx, cy, cz],
        "center_region_mm": [28.0, 28.0],
        "mesh_size_mm": options["mesh"],
        "displacement_mm": {"dx": options["dx"], "dy": options["dy"]},
        "end_face_counts": {
            "xmin": n_xmin, "xmax": n_xmax,
            "ymin": n_ymin, "ymax": n_ymax,
        },
        "material": PROVISIONAL_MATERIAL,
    }

    if options["submit"]:
        job.submit(consistencyChecking=OFF)
        job.waitForCompletion()
        manifest["status"] = "job_completed"

    with open(os.path.join(options["out"], "run_manifest.json"), "w") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    build_model(_args())
