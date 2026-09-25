from __future__ import annotations

import argparse
import json
from pathlib import Path

if __package__:
    from .vfm_boundary import (
        load_vfm_boundary_config,
        parse_matchid_vfm_metadata,
        validate_vfm_boundary_config,
    )
else:
    from vfm_boundary import (
        load_vfm_boundary_config,
        parse_matchid_vfm_metadata,
        validate_vfm_boundary_config,
    )


def build_boundary_audit(config_path: Path) -> dict:
    config = load_vfm_boundary_config(config_path)
    failures: list[str] = []
    try:
        validate_vfm_boundary_config(config)
    except ValueError as error:
        failures.append(str(error))

    vfm_path = Path(config["source"]["vfm_format_evidence"])
    metadata = parse_matchid_vfm_metadata(vfm_path)
    expected_order = config["matchid_boundary_order"]
    mapping = config["rotated_boundary_mapping"]
    boundary_ids = metadata["boundary_ids"]
    if boundary_ids != list(range(len(expected_order))):
        failures.append(f"Boundary 编号不是连续顺序：{boundary_ids}")
    if metadata["boundary_count"] != len(expected_order):
        failures.append(
            f"Boundary 数量不一致：实际={metadata['boundary_count']}，配置={len(expected_order)}"
        )
    if metadata["force_series_count"] != metadata["boundary_count"]:
        failures.append(
            "Forces 组数与 Boundary 数量不一致："
            f"{metadata['force_series_count']} != {metadata['boundary_count']}"
        )
    if len(metadata["force_frame_counts"]) != 1:
        failures.append(f"各边界 Forces 帧数不一致：{metadata['force_frame_counts']}")
    if metadata["thickness_mm"] != float(config["geometry"]["center_roi_thickness_mm"]):
        failures.append(
            "VFM 厚度与中心 ROI 厚度不一致："
            f"实际={metadata['thickness_mm']}，配置={config['geometry']['center_roi_thickness_mm']}"
        )
    if not metadata["all_force_values_nonnegative"]:
        failures.append("VFM Forces 中存在负值")
    if not metadata["first_force_samples_zero"]:
        failures.append("VFM Forces 首帧没有全部归零")
    if not metadata["later_force_values_positive"]:
        failures.append("VFM Forces 首帧之后存在非正拉伸力")

    boundary_mapping = []
    for boundary_id, side in enumerate(expected_order):
        axis = next(
            axis for axis, sides in config["loading_modes"]["双轴"]["positive_sides"].items()
            if side in sides
        )
        boundary_mapping.append(
            {
                "boundary_id": boundary_id,
                "side": side,
                "machine_channel": mapping[side],
                "force_axis": axis,
            }
        )

    return {
        "config": str(config_path),
        "vfm_path": str(vfm_path),
        "audit_passed": not failures,
        "failures": failures,
        "center_roi_thickness_mm": float(config["geometry"]["center_roi_thickness_mm"]),
        "overall_thickness_mm": float(config["geometry"]["overall_thickness_mm"]),
        "boundary_count": metadata["boundary_count"],
        "force_series_count": metadata["force_series_count"],
        "force_frame_counts": metadata["force_frame_counts"],
        "force_values_nonnegative": metadata["all_force_values_nonnegative"],
        "first_force_samples_zero": metadata["first_force_samples_zero"],
        "later_force_values_positive": metadata["later_force_values_positive"],
        "boundary_mapping": boundary_mapping,
        "metadata": {
            "thickness_mm": metadata["thickness_mm"],
            "conversion_mm_per_pixel": metadata["conversion_mm_per_pixel"],
            "boundary_ids": boundary_ids,
        },
    }


def _write_markdown(path: Path, audit: dict) -> None:
    lines = [
        "# PA12 VFM 边界载荷方向审计",
        "",
        "本审计固定旋转后的 DIC 坐标、原机器通道和历史 MatchID `.vfm` 四边顺序；当前计算主路径为自建 VFM。该方向/格式审计不等于已经完成材料参数识别。",
        "",
        "## 审计结果",
        "",
        f"- 结果：**{'通过' if audit['audit_passed'] else '存在失败项'}**",
        f"- `.vfm` 证据：`{audit['vfm_path']}`",
        f"- 中心 ROI 厚度：`{audit['center_roi_thickness_mm']} mm`。",
        f"- 整体厚度记录：`{audit['overall_thickness_mm']} mm`。",
        f"- Boundary 数量：`{audit['boundary_count']}`；Forces 组数：`{audit['force_series_count']}`。",
        f"- 每组 Forces 帧数：`{audit['force_frame_counts']}`。",
        f"- Forces 全部为非负值：**{'是' if audit['force_values_nonnegative'] else '否'}**。",
        f"- Forces 首帧全部归零：**{'是' if audit['first_force_samples_zero'] else '否'}**；后续力值全部为正：**{'是' if audit['later_force_values_positive'] else '否'}**。",
        "",
        "## 旋转后边界映射",
        "",
        "| MatchID Boundary ID | 旋转后边界 | 原机器通道 | 力方向 |",
        "| ---: | --- | --- | --- |",
    ]
    lines.extend(
        f"| {row['boundary_id']} | {row['side']} | {row['machine_channel']} | {row['force_axis']} |"
        for row in audit["boundary_mapping"]
    )
    lines += [
        "",
        "## 使用规则",
        "",
        "- 双轴：X 使用顶部/底部两条边，Y 使用左侧/右侧两条边。",
        "- 单轴 X：只使用顶部/底部两条边；单轴 Y：只使用左侧/右侧两条边。",
        "- 拉伸力统一按正值记录；`Press` 的工程单位为 N。",
        "- 外围夹持/加载结构整体厚度为 3 mm；中心 ROI 必须完全位于 1 mm 减薄区，MatchID 工程厚度使用 1 mm。",
        "- 自建 VFM 主路径和 MatchID 对照均按用户确认：机器力传感器读数直接作为 ROI 边界合力；本项目不自行恢复四边牵引分布或假设均布边界应力。该输入约定不代表逐帧内外虚功闭合或材料参数识别通过。",
        "- 所有当前双轴试验均为等双轴；按 0.2、2、20 mm/s 分速率识别，不要求非等双轴路径。",
        "- 每个速度先固定 ν=0.375 识别 E，再固定该 E 和 ν 识别屈服 Y 与硬化 H；当前文件审计不代表已得到这些参数。",
    ]
    if audit["failures"]:
        lines += ["", "## 失败项", ""]
        lines.extend(f"- {failure}" for failure in audit["failures"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_boundary_audit(config_path: Path, output_root: Path | None = None) -> dict:
    audit = build_boundary_audit(config_path)
    root = output_root or Path(
        load_vfm_boundary_config(config_path).get("output_root", config_path.parents[1])
    )
    output_dir = root / "Agents" / "PA12实验数据处理" / "MatchID_VFM准备"
    json_path = output_dir / "PA12_VFM边界载荷审计.json"
    markdown_path = output_dir / "PA12_VFM边界载荷说明.md"
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_markdown(markdown_path, audit)
    return {"json": str(json_path), "markdown": str(markdown_path), **audit}


def main() -> int:
    parser = argparse.ArgumentParser(description="审计 PA12 MatchID VFM 边界方向和格式")
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output-root", type=Path)
    args = parser.parse_args()
    result = write_boundary_audit(args.config, args.output_root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["audit_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
