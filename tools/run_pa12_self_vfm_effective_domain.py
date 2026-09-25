from __future__ import annotations

import argparse
import json
from pathlib import Path

from run_pa12_self_vfm import (
    _effective_dicom_geometry,
    _geometry,
    _read_index,
    _read_frame_arrays,
    _write_csv,
    _write_json,
    process_experiment,
)


def run(batch_config_path: Path, self_config_path: Path) -> dict:
    batch = json.loads(batch_config_path.read_text(encoding="utf-8"))
    self_config = json.loads(self_config_path.read_text(encoding="utf-8"))
    output_root = Path(batch["output_root"])
    results = []
    for entry in batch["experiments"]:
        if entry.get("loading_mode") != "双轴" or not entry.get("formal_vfm_allowed", False):
            continue
        experiment_id = entry["experiment_id"]
        preparation_dir = output_root / "Agents" / "PA12实验数据处理" / "MatchID_VFM准备" / experiment_id
        index_path = preparation_dir / f"{experiment_id}_DIC全场—力索引.csv"
        merged_dir = preparation_dir / "merged"
        index_rows = _read_index(index_path)
        first_frame = _read_frame_arrays(merged_dir / f"{Path(index_rows[0]['照片']).stem}_DIC全场—力.csv")
        points = [{"x": float(x), "y": float(y)} for x, y in zip(first_frame["x"], first_frame["y"])]
        effective_geometry = _effective_dicom_geometry(points, _geometry(Path(entry["dic_job_file"])))
        result_dir = output_root / self_config["output_directory"] / "敏感性分析" / experiment_id
        results.append(
            process_experiment(
                entry,
                batch,
                self_config,
                geometry_override=effective_geometry,
                result_directory=result_dir,
                analysis_label="DIC subset内缩有效域敏感性分析",
            )
        )
    summary_dir = output_root / self_config["output_directory"] / "敏感性分析"
    _write_csv(summary_dir / "PA12自建VFM有效域敏感性结果.csv", results, ["实验编号", "状态", "帧数", "E/MPa", "Y/MPa", "H/MPa", "虚功文件"])
    _write_json(summary_dir / "PA12自建VFM有效域敏感性结果.json", {"状态": "独立有效域敏感性分析；不覆盖完整 Job ROI 主结果", "结果": results})
    lines = [
        "# PA12 自建 VFM 有效域敏感性分析",
        "",
        "本目录使用 DIC subset 中心有效点外接框作为独立数值积分域；完整 Job ROI 主结果不被覆盖。",
        "",
        "| 实验编号 | 状态 | 帧数 | E/MPa | Y/MPa | H/MPa |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in results:
        lines.append(f"| {row['实验编号']} | {row['状态']} | {row['帧数']} | {row['E/MPa']} | {row['Y/MPa']} | {row['H/MPa']} |")
    lines += [
        "",
        "## 限制",
        "",
        "有效 DIC 域不自动等同于试样物理 VFM 边界；本目录只用于积分域口径敏感性比较，不生成最终材料参数。",
    ]
    (summary_dir / "PA12自建VFM有效域敏感性分析.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"output_directory": str(summary_dir), "results": results}


def main() -> int:
    parser = argparse.ArgumentParser(description="运行 PA12 自建 VFM DIC 有效域敏感性分析")
    parser.add_argument("--batch-config", type=Path, default=Path("configs/pa12_rotated_batch.json"))
    parser.add_argument("--config", type=Path, default=Path("configs/pa12_self_vfm.json"))
    args = parser.parse_args()
    print(json.dumps(run(args.batch_config, args.config), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
