from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
from pathlib import Path


REQUIRED_MODULES = {
    "numpy": "numpy",
    "pandas": "pandas",
    "matplotlib": "matplotlib",
    "Pillow": "PIL",
    "openpyxl": "openpyxl",
}


def _module_status() -> dict[str, bool]:
    return {
        display_name: importlib.util.find_spec(module_name) is not None
        for display_name, module_name in REQUIRED_MODULES.items()
    }


def _matchid_status(executable: Path | None) -> dict[str, str | None]:
    if executable is not None:
        if executable.is_file():
            return {"status": "AVAILABLE", "path": str(executable)}
        return {"status": "NOT_DETECTED", "path": str(executable)}
    command = shutil.which("matchid.exe")
    if command:
        return {"status": "AVAILABLE", "path": command}
    return {
        "status": "NOT_DETECTED",
        "path": None,
        "reason": "本机未发现可调用的 matchid.exe；需要用户在 Results Viewer 中完成导出。",
    }


def inspect_environment(config_path: Path, *, matchid_executable: Path | None = None) -> dict:
    batch = json.loads(config_path.read_text(encoding="utf-8"))
    dependency_status = _module_status()
    path_rows = []
    for entry in batch["experiments"]:
        image_folder = Path(entry["image_folder"])
        force_file = Path(entry["force_file"]) if entry.get("force_file") else None
        job_value = entry.get("dic_job_file")
        job_path = Path(job_value) if job_value else image_folder / "Job.m2inp"
        path_rows.append(
            {
                "experiment_id": entry["experiment_id"],
                "image_folder": str(image_folder),
                "image_folder_exists": image_folder.is_dir(),
                "force_file": str(force_file) if force_file else None,
                "force_file_exists": force_file.is_file() if force_file else False,
                "job_file": str(job_path),
                "job_file_exists": job_path.is_file(),
            }
        )
    inputs_ok = all(
        row["image_folder_exists"] and row["force_file_exists"] and row["job_file_exists"]
        for row in path_rows
    )
    dependencies_ok = all(dependency_status.values())
    configured_matchid = batch.get("matchid_executable")
    selected_matchid = matchid_executable
    if selected_matchid is None and configured_matchid:
        selected_matchid = Path(configured_matchid)
    matchid = _matchid_status(selected_matchid)
    if not dependencies_ok:
        overall_status = "PYTHON_DEPENDENCIES_INCOMPLETE"
    elif not inputs_ok:
        overall_status = "INPUT_PATHS_INCOMPLETE"
    else:
        overall_status = "READY_FOR_SELF_VFM"
    matchid_export_status = (
        "READY_FOR_MATCHID_EXPORT"
        if matchid["status"] == "AVAILABLE"
        else "OPTIONAL_MATCHID_UNAVAILABLE"
    )
    return {
        "config": str(config_path),
        "python_dependencies": dependency_status,
        "python_dependencies_ok": dependencies_ok,
        "input_paths": path_rows,
        "input_paths_ok": inputs_ok,
        "matchid": matchid,
        "matchid_export_status": matchid_export_status,
        "overall_status": overall_status,
    }


def _write_report(path: Path, report: dict) -> None:
    lines = [
        "# PA12 处理环境检查",
        "",
        f"- 总体状态：`{report['overall_status']}`",
        "- 自建 VFM：可继续运行；MatchID 不可用不会阻断虚功和参数候选计算。",
        f"- Python 依赖：`{'可用' if report['python_dependencies_ok'] else '不完整'}`",
        f"- 原始输入路径：`{'可用' if report['input_paths_ok'] else '不完整'}`",
        f"- MatchID：`{report['matchid']['status']}`",
        "",
        "## Python 依赖",
        "",
    ]
    lines.extend(
        f"- `{name}`：`{'可用' if available else '缺失'}`"
        for name, available in report["python_dependencies"].items()
    )
    lines += ["", "## MatchID", ""]
    if report["matchid"]["status"] == "AVAILABLE":
        lines.append(f"- 可调用路径：`{report['matchid']['path']}`")
    else:
        lines.append("- 未发现可调用的 `matchid.exe`；当前环境不能自动打开 Results Viewer 或自动导出字段。")
        lines.append("- 这只影响 MatchID 导出；自建 VFM 不依赖 MatchID，可直接使用已合并的 DIC—Press 数据继续分析。")
    lines += ["", "## 原始输入", ""]
    for row in report["input_paths"]:
        lines.append(
            f"- `{row['experiment_id']}`：照片目录={'可用' if row['image_folder_exists'] else '缺失'}；力文件={'可用' if row['force_file_exists'] else '缺失'}；Job={'可用' if row['job_file_exists'] else '缺失'}。"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="检查 PA12 MatchID VFM 处理环境")
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--matchid-executable", type=Path)
    args = parser.parse_args()
    report = inspect_environment(args.config, matchid_executable=args.matchid_executable)
    output_root = args.output_root / "Agents" / "PA12实验数据处理" / "MatchID_VFM准备"
    json_path = output_root / "PA12_环境检查.json"
    markdown_path = output_root / "PA12_环境检查.md"
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_report(markdown_path, report)
    print(json.dumps({"json": str(json_path), "markdown": str(markdown_path), **report}, ensure_ascii=False, indent=2))
    return 0 if report["overall_status"] == "READY_FOR_SELF_VFM" else 2


if __name__ == "__main__":
    raise SystemExit(main())
