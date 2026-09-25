import csv
import csv
import gzip
import json
import tempfile
import unittest
from pathlib import Path

from tools.matchid_dic import (
    MatchIDExportError,
    audit_dat_rows,
    inspect_dat_file,
    merge_exported_frame,
    parse_matchid_dat,
    read_matchid_export,
)
from tools.merge_matchid_exports import merge_experiment_exports
from tools.check_pa12_environment import inspect_environment
from tools.audit_matchid_dic import _force_status, build_closure_status, write_closure_outputs
from tools.matchid_prepare import build_matchid_preparation


FIELD_MAP = {
    "x": "X",
    "y": "Y",
    "u": "U",
    "v": "V",
    "exx": "exx",
    "eyy": "eyy",
    "exy": "exy",
}

UNITS = {
    "x": "mm",
    "y": "mm",
    "u": "mm",
    "v": "mm",
    "exx": "dimensionless",
    "eyy": "dimensionless",
    "exy": "dimensionless",
}


class MatchIDDicTests(unittest.TestCase):
    def test_dat_point_count_gate_rejects_a_dramatically_small_frame(self):
        from tools.matchid_dic import classify_dat_point_count_anomalies

        audits = [
            {
                "照片": "000001.jpg",
                "status": "DIC_FIELDS_AVAILABLE",
                "point_count": 100_000,
            },
            {
                "照片": "000002.jpg",
                "status": "DIC_FIELDS_AVAILABLE",
                "point_count": 99_800,
            },
            {
                "照片": "000003.jpg",
                "status": "DIC_FIELDS_AVAILABLE",
                "point_count": 5_000,
            },
        ]

        result = classify_dat_point_count_anomalies(audits, min_fraction=0.2)

        self.assertEqual(result[0]["status"], "DIC_FIELDS_AVAILABLE")
        self.assertEqual(result[1]["status"], "DIC_FIELDS_AVAILABLE")
        self.assertEqual(result[2]["status"], "DAT_POINT_COUNT_ANOMALY")
        self.assertEqual(result[2]["point_count_reference"], 99_800)

    def test_visual_fracture_without_force_drop_has_explicit_force_missing_status(self):
        self.assertEqual(
            _force_status(
                {
                    "status": "DATA_LIMITED",
                    "visual_fracture_confirmed": True,
                    "force_missing_at_visual_fracture": True,
                }
            ),
            "FORCE_SYNC_VISUAL_FRACTURE_FORCE_MISSING",
        )

    def test_closure_report_keeps_rotated_boundary_mapping(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            config_path = root / "config.json"
            config_path.write_text(
                '{"output_root": "' + str(root).replace('\\', '/') + '", "experiments": [{"experiment_id": "S1"}]}',
                encoding="utf-8",
            )
            record_root = root / "Agents" / "PA12实验数据处理" / "处理记录"
            prep_root = root / "Agents" / "PA12实验数据处理" / "MatchID_VFM准备"
            record_root.mkdir(parents=True)
            prep_root.mkdir(parents=True)
            (record_root / "PA12批量处理清单.json").write_text(
                '[{"experiment_id":"S1","status":"VFM_READY","vfm_allowed":true}]',
                encoding="utf-8",
            )
            (prep_root / "PA12_DIC_DAT质量审计.json").write_text(
                '[{"实验编号":"S1","照片":"000001.jpg","status":"DIC_FIELDS_AVAILABLE"}]',
                encoding="utf-8",
            )
            merged_status_dir = prep_root / "S1"
            merged_status_dir.mkdir()
            (merged_status_dir / "S1_DIC全场—力状态.json").write_text(
                '{"status":"MATCHID_VFM_INPUT_READY","frame_count":1}',
                encoding="utf-8",
            )

            result = write_closure_outputs(config_path)
            report = Path(result["markdown"]).read_text(encoding="utf-8")

            self.assertIn("顶部=`X2`、底部=`X1`、左侧=`Y2`、右侧=`Y1`", report)
            self.assertIn("双轴使用 X 顶/底、Y 左/右", report)
            self.assertIn("单轴只使用受力方向两边", report)
            self.assertIn("用户确认外围机器力传感器读数直接作为 ROI 边界合力", report)
            self.assertIn("所有当前双轴均为等双轴", report)
            self.assertNotIn("力臂仍需确认", report)

    def _write_reconstructable_dat(self, path: Path, *, invalid_second: bool = False):
        second_valid = "False" if invalid_second else "True"
        second_strain = "NaN;NaN;NaN;NaN;NaN;NaN" if invalid_second else "2;3;4;5;6;7"
        payload = (
            "<11>=<0.5>"
            "<18>=<0;100;200;0;0;3;4;1;2;0;0;0;0;0.9;0.1;0;1;0>"
            "<53>=<0;True;1;2;3;4;5;6;0.9;1;2;3>"
            "<18>=<1;110;210;0;0;5;6;7;8;0;0;0;0;0.8;0.2;0;1;0>"
            f"<53>=<1;{second_valid};{second_strain};0;0;0;0>"
        ).encode("latin1")
        with gzip.open(path, "wb") as handle:
            handle.write(payload)

    def test_parse_matchid_dat_maps_fields_and_excludes_invalid_strain_points(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "000001.jpg.dat"
            payload = (
                "<11>=<0.5>"
                "<18>=<0;100;200;0;0;3;4;1;2;0;0;0;0;0.9;0.1;0;1;0>"
                "<53>=<0;True;1;2;3;4;5;6;0.9;1;2;3>"
                "<18>=<1;100;200;0;0;5;6;7;8;0;0;0;0;0.8;0.2;0;1;0>"
                "<53>=<1;False;NaN;NaN;NaN;NaN;NaN;NaN;0;0;0;0>"
            ).encode("latin1")
            with gzip.open(path, "wb") as handle:
                handle.write(payload)

            result = parse_matchid_dat(path)

            self.assertEqual(result["point_count"], 2)
            self.assertEqual(result["excluded_invalid_count"], 1)
            self.assertEqual(len(result["rows"]), 1)
            self.assertAlmostEqual(result["rows"][0]["x"], 51.5)
            self.assertAlmostEqual(result["rows"][0]["y"], 102.0)
            self.assertAlmostEqual(result["rows"][0]["u"], 0.5)
            self.assertAlmostEqual(result["rows"][0]["v"], 1.0)
            self.assertEqual(result["rows"][0]["exx"], 1.0)
            self.assertEqual(result["rows"][0]["eyy"], 2.0)
            self.assertEqual(result["rows"][0]["exy"], 3.0)

    def test_dat_quality_distinguishes_missing_strain_records(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "000001.jpg.dat"
            with gzip.open(path, "wt", encoding="latin1") as handle:
                handle.write(
                    "\x1e***MatchID 2D-Version 19.2.2.0"
                    "<11>=<0.087464><55>=<3>"
                    "<18>=<0;a;b><18>=<1;a;b>"
                )

            quality = inspect_dat_file(path)

            self.assertEqual(quality["record_counts"], {"18": 2, "53": 0})
            self.assertEqual(quality["status"], "NO_STRAIN_RECORDS")

    def test_dat_quality_ignores_matchid_binary_tail_after_valid_gzip_stream(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "000001.jpg.dat"
            payload = "<55>=<2><18>=<0;a;b><53>=<0;a;b>".encode("latin1")
            with gzip.open(path, "wb") as handle:
                handle.write(payload)
            with path.open("ab") as handle:
                handle.write(b"\\x93\\xd5matchid-binary-tail")

            quality = inspect_dat_file(path)

            self.assertEqual(quality["status"], "DIC_FIELDS_AVAILABLE")
            self.assertEqual(quality["record_counts"], {"18": 1, "53": 1})

    def test_matchid_export_requires_explicit_field_mapping(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "000001.csv"
            path.write_text(
                "X,Y,U,V,exx,eyy,exy\n1,2,0.1,0.2,0.01,0.02,0.03\n",
                encoding="utf-8-sig",
            )

            with self.assertRaises(MatchIDExportError):
                read_matchid_export(path, {})

    def test_merge_exported_frame_attaches_one_frame_force_and_time_to_each_point(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "000001.csv"
            path.write_text(
                "X,Y,U,V,exx,eyy,exy\n1,2,0.1,0.2,0.01,0.02,0.03\n"
                "3,4,0.3,0.4,0.04,0.05,0.06\n",
                encoding="utf-8-sig",
            )

            merged = merge_exported_frame(
                {"照片": "000001.jpg", "时间/s": "1.25", "X向力/N": "10", "Y向力/N": "20"},
                path,
                FIELD_MAP,
                UNITS,
            )

            self.assertEqual(len(merged), 2)
            self.assertEqual(merged[0]["照片"], "000001.jpg")
            self.assertEqual(merged[0]["时间/s"], "1.25")
            self.assertEqual(merged[0]["X向力/N"], "10")
            self.assertEqual(merged[0]["Y向力/N"], "20")
            self.assertEqual(merged[1]["exy"], "0.06")

    def test_matchid_export_rejects_non_numeric_values(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "000001.csv"
            path.write_text(
                "X,Y,U,V,exx,eyy,exy\n1,2,not-a-number,0.2,0.01,0.02,0.03\n",
                encoding="utf-8-sig",
            )

            with self.assertRaises(MatchIDExportError):
                read_matchid_export(path, FIELD_MAP)

    def test_audit_dat_rows_reports_missing_and_unusable_dat_separately(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            folder = Path(temporary_directory)
            with gzip.open(folder / "000001.jpg.dat", "wt", encoding="latin1") as handle:
                handle.write("<55>=<2><18>=<0;a;b>")
            with gzip.open(folder / "000002.jpg.dat", "wt", encoding="latin1") as handle:
                handle.write("<55>=<2><18>=<0;a;b><53>=<0;a;b>")

            rows = audit_dat_rows(
                folder,
                [
                    {"照片": "000000.jpg"},
                    {"照片": "000001.jpg"},
                    {"照片": "000002.jpg"},
                ],
            )

            self.assertEqual([row["status"] for row in rows], [
                "MISSING_DAT",
                "NO_STRAIN_RECORDS",
                "DIC_FIELDS_AVAILABLE",
            ])

    def test_merge_experiment_exports_requires_every_frame_before_formal_output(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            index_path = root / "frame-index.csv"
            with index_path.open("w", newline="", encoding="utf-8-sig") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=["照片", "DAT", "时间/s", "X向力/N", "Y向力/N"],
                )
                writer.writeheader()
                writer.writerows(
                    [
                        {"照片": "000001.jpg", "DAT": "000001.jpg.dat", "时间/s": "1", "X向力/N": "10", "Y向力/N": "20"},
                        {"照片": "000002.jpg", "DAT": "000002.jpg.dat", "时间/s": "2", "X向力/N": "11", "Y向力/N": "21"},
                    ]
                )
            export_root = root / "exports"
            export_root.mkdir()
            for stem, offset in (("000001", 0), ("000002", 1)):
                (export_root / f"{stem}.csv").write_text(
                    "X,Y,U,V,exx,eyy,exy\n1,2,0.1,0.2,0.01,0.02,0.03\n"
                    f"{3 + offset},4,0.3,0.4,0.04,0.05,0.06\n",
                    encoding="utf-8-sig",
                )

            result = merge_experiment_exports(
                "demo",
                index_path,
                export_root,
                root / "output",
                FIELD_MAP,
                UNITS,
            )

            self.assertEqual(result["status"], "MATCHID_VFM_INPUT_READY")
            self.assertEqual(result["frame_count"], 2)
            self.assertEqual(len(list((root / "output" / "merged").glob("*.csv"))), 2)

    def test_merge_experiment_exports_reports_missing_frame_without_formal_output(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            index_path = root / "frame-index.csv"
            index_path.write_text(
                "照片,DAT,时间/s,X向力/N,Y向力/N\n"
                "000001.jpg,000001.jpg.dat,1,10,20\n",
                encoding="utf-8-sig",
            )
            result = merge_experiment_exports(
                "demo",
                index_path,
                root / "exports",
                root / "output",
                FIELD_MAP,
                UNITS,
            )

            self.assertEqual(result["status"], "EXPORT_REQUIRED")
            self.assertFalse((root / "output" / "demo_DIC全场—力索引.csv").exists())

    def test_merge_experiment_exports_reports_invalid_frame_without_formal_output(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            index_path = root / "frame-index.csv"
            index_path.write_text(
                "照片,DAT,时间/s,X向力/N,Y向力/N\n"
                "000001.jpg,000001.jpg.dat,1,10,20\n",
                encoding="utf-8-sig",
            )
            export_root = root / "exports"
            export_root.mkdir()
            (export_root / "000001.csv").write_text(
                "X,Y,U,V,exx,eyy,exy\n"
                "1,2,0.1,0.2,NaN,0.02,0.03\n",
                encoding="utf-8-sig",
            )

            result = merge_experiment_exports(
                "demo",
                index_path,
                export_root,
                root / "output",
                FIELD_MAP,
                UNITS,
            )

            self.assertEqual(result["status"], "EXPORT_INVALID")
            self.assertEqual(result["invalid_export"], str(export_root / "000001.csv"))
            self.assertFalse((root / "output" / "demo_DIC全场—力索引.csv").exists())

    def test_merge_experiment_exports_reconstructs_missing_csv_from_dat(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            dat_path = root / "000001.jpg.dat"
            self._write_reconstructable_dat(dat_path)
            index_path = root / "frame-index.csv"
            index_path.write_text(
                "照片,DAT,时间/s,X向力/N,Y向力/N\n"
                f"000001.jpg,{dat_path},1,10,20\n",
                encoding="utf-8-sig",
            )

            result = merge_experiment_exports(
                "demo",
                index_path,
                root / "exports",
                root / "output",
                FIELD_MAP,
                UNITS,
            )

            self.assertEqual(result["status"], "MATCHID_VFM_INPUT_READY")
            self.assertEqual(result["source_counts"], {"DAT_RECONSTRUCTED": 1})
            self.assertEqual(result["reconstructed_frame_count"], 1)
            with (root / "output" / "demo_DIC全场—力索引.csv").open(
                encoding="utf-8-sig", newline=""
            ) as handle:
                index_rows = list(csv.DictReader(handle))
            self.assertEqual(index_rows[0]["DIC数据来源"], "DAT_RECONSTRUCTED")
            with (root / "output" / "merged" / "000001_DIC全场—力.csv").open(
                encoding="utf-8-sig", newline=""
            ) as handle:
                merged_rows = list(csv.DictReader(handle))
            self.assertEqual(len(merged_rows), 2)

    def test_merge_experiment_exports_reconstructs_nan_csv_and_reports_excluded_dat_points(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            dat_path = root / "000001.jpg.dat"
            self._write_reconstructable_dat(dat_path, invalid_second=True)
            index_path = root / "frame-index.csv"
            index_path.write_text(
                "照片,DAT,时间/s,X向力/N,Y向力/N\n"
                f"000001.jpg,{dat_path},1,10,20\n",
                encoding="utf-8-sig",
            )
            export_root = root / "exports"
            export_root.mkdir()
            (export_root / "000001.csv").write_text(
                "X,Y,U,V,exx,eyy,exy\n"
                "1,2,0.1,0.2,NaN,0.02,0.03\n",
                encoding="utf-8-sig",
            )

            result = merge_experiment_exports(
                "demo",
                index_path,
                export_root,
                root / "output",
                FIELD_MAP,
                UNITS,
            )

            self.assertEqual(result["status"], "MATCHID_VFM_INPUT_READY")
            self.assertEqual(result["source_counts"], {"DAT_RECONSTRUCTED": 1})
            self.assertEqual(result["excluded_invalid_point_count"], 1)
            with (root / "output" / "demo_DIC全场—力索引.csv").open(
                encoding="utf-8-sig", newline=""
            ) as handle:
                index_rows = list(csv.DictReader(handle))
            self.assertEqual(index_rows[0]["排除无效点数"], "1")

    def test_merge_experiment_exports_reconstructs_when_csv_point_count_differs_from_dat(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            dat_path = root / "000001.jpg.dat"
            self._write_reconstructable_dat(dat_path)
            index_path = root / "frame-index.csv"
            index_path.write_text(
                "照片,DAT,时间/s,X向力/N,Y向力/N\n"
                f"000001.jpg,{dat_path},1,10,20\n",
                encoding="utf-8-sig",
            )
            export_root = root / "exports"
            export_root.mkdir()
            (export_root / "000001.csv").write_text(
                "X,Y,U,V,exx,eyy,exy\n"
                "1,2,0.1,0.2,0.01,0.02,0.03\n",
                encoding="utf-8-sig",
            )

            result = merge_experiment_exports(
                "demo",
                index_path,
                export_root,
                root / "output",
                FIELD_MAP,
                UNITS,
            )

            self.assertEqual(result["status"], "MATCHID_VFM_INPUT_READY")
            self.assertEqual(result["source_counts"], {"DAT_RECONSTRUCTED": 1})
            with (root / "output" / "merged" / "000001_DIC全场—力.csv").open(
                encoding="utf-8-sig", newline=""
            ) as handle:
                merged_rows = list(csv.DictReader(handle))
            self.assertEqual(len(merged_rows), 2)

    def test_merge_experiment_exports_blocks_when_dat_reconstruction_has_no_strain_records(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            dat_path = root / "000001.jpg.dat"
            with gzip.open(dat_path, "wt", encoding="latin1") as handle:
                handle.write("<11>=<0.5><18>=<0;100;200;0;0;3;4;1;2>")
            index_path = root / "frame-index.csv"
            index_path.write_text(
                "照片,DAT,时间/s,X向力/N,Y向力/N\n"
                f"000001.jpg,{dat_path},1,10,20\n",
                encoding="utf-8-sig",
            )

            result = merge_experiment_exports(
                "demo",
                index_path,
                root / "exports",
                root / "output",
                FIELD_MAP,
                UNITS,
            )

            self.assertEqual(result["status"], "EXPORT_REQUIRED")
            self.assertEqual(result["reconstruction_failed_frame"], "000001.jpg")
            self.assertIn("完整的 <18>/<53>", result["reconstruction_error"])
            self.assertFalse((root / "output" / "demo_DIC全场—力索引.csv").exists())

    def test_environment_report_separates_python_and_matchid_availability(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            config_path = root / "config.json"
            config_path.write_text(
                '{"output_root": "' + str(root).replace('\\', '/') + '", "experiments": []}',
                encoding="utf-8",
            )

            report = inspect_environment(
                config_path,
                matchid_executable=root / "missing-matchid.exe",
            )

            self.assertTrue(report["python_dependencies_ok"])
            self.assertEqual(report["matchid"]["status"], "NOT_DETECTED")
            self.assertEqual(report["overall_status"], "READY_FOR_SELF_VFM")
            self.assertEqual(report["matchid_export_status"], "OPTIONAL_MATCHID_UNAVAILABLE")

    def test_matchid_preparation_instructions_keep_validated_mapping_as_completed(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            image_folder = root / "images"
            image_folder.mkdir()
            (image_folder / "000001.jpg").write_bytes(b"jpg")
            with gzip.open(image_folder / "000001.jpg.dat", "wt", encoding="latin1") as handle:
                handle.write(
                    "<11>=<0.5><55>=<1>"
                    "<18>=<0;100;200;0;0;3;4;1;2;0;0;0;0;0.9;0.1;0;1;0>"
                    "<53>=<0;True;1;2;3;4;5;6;0.9;1;2;3>"
                )
            (image_folder / "Job.m2inp").write_text(
                "<Reference$image>=<000001.jpg>\n"
                "<Deformed$image>=<000001.jpg;3;0;0;None>\n"
                "<Conversion>=<0.5>\n"
                "<Export$unit>=<1>\n",
                encoding="utf-8",
            )
            agent_root = root / "Agents" / "PA12实验数据处理"
            record_root = agent_root / "处理记录"
            match_root = agent_root / "照片力匹配"
            record_root.mkdir(parents=True)
            match_root.mkdir()
            (record_root / "PA12批量处理清单.json").write_text(
                '[{"experiment_id":"S1","status":"VFM_READY","vfm_allowed":true,"photo_count":1}]',
                encoding="utf-8",
            )
            (match_root / "S1_照片-力对应表.csv").write_text(
                "照片,时间/s,X向力/N,Y向力/N\n000001.jpg,0,0,0\n",
                encoding="utf-8-sig",
            )
            config_path = root / "config.json"
            config_path.write_text(
                json.dumps(
                    {
                        "output_root": str(root),
                        "experiments": [
                            {
                                "experiment_id": "S1",
                                "image_folder": str(image_folder),
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            result = build_matchid_preparation(config_path)
            instructions = Path(result["instructions"]).read_text(encoding="utf-8")

            self.assertIn("当前版本本地同帧交叉验证", instructions)
            self.assertIn("顶部=`X2`、底部=`X1`、左侧=`Y2`、右侧=`Y1`", instructions)
            self.assertIn("双轴使用 X 顶/底、Y 左/右", instructions)
            self.assertIn("raw/assets/PA12原始方向与旋转标定方向.jpg", instructions)
            self.assertIn("外围机器力按用户确认直接作为 ROI 边界合力输入 MatchID 自带 VFM", instructions)
            self.assertIn("按 `0.2、2、20 mm/s` 分速率识别", instructions)
            self.assertNotIn("载荷分布、力臂仍需确认", instructions)
            self.assertNotIn("字段映射已由本地同版本 MatchID", instructions.split("## 尚未确认", 1)[1])

    def test_closure_status_keeps_force_and_dic_gates_separate(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            config_path = root / "config.json"
            config_path.write_text(
                '{"output_root": "' + str(root).replace('\\', '/') + '", "experiments": [{"experiment_id": "S1"}]}',
                encoding="utf-8",
            )
            record_root = root / "Agents" / "PA12实验数据处理" / "处理记录"
            prep_root = root / "Agents" / "PA12实验数据处理" / "MatchID_VFM准备"
            record_root.mkdir(parents=True)
            prep_root.mkdir(parents=True)
            (record_root / "PA12批量处理清单.json").write_text(
                '[{"experiment_id":"S1","status":"VFM_READY","vfm_allowed":true}]',
                encoding="utf-8",
            )
            (prep_root / "PA12_DIC_DAT质量审计.json").write_text(
                '[{"实验编号":"S1","照片":"000001.jpg","status":"DIC_FIELDS_AVAILABLE"}]',
                encoding="utf-8",
            )

            status = build_closure_status(config_path)

            self.assertEqual(status["experiments"][0]["force_status"], "FORCE_SYNC_READY")
            self.assertEqual(status["experiments"][0]["dic_status"], "DIC_DAT_READY")
            self.assertEqual(status["experiments"][0]["overall_status"], "EXPORT_REQUIRED")

    def test_closure_status_classifies_preload_release_as_non_vfm_record(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            config_path = root / "config.json"
            config_path.write_text(
                '{"output_root": "' + str(root).replace('\\', '/') + '", "experiments": [{"experiment_id": "S24"}]}',
                encoding="utf-8",
            )
            record_root = root / "Agents" / "PA12实验数据处理" / "处理记录"
            prep_root = root / "Agents" / "PA12实验数据处理" / "MatchID_VFM准备"
            record_root.mkdir(parents=True)
            prep_root.mkdir(parents=True)
            (record_root / "PA12批量处理清单.json").write_text(
                '[{"experiment_id":"S24","status":"PRELOAD_RELEASE_ONLY","vfm_allowed":false}]',
                encoding="utf-8",
            )
            (prep_root / "PA12_DIC_DAT质量审计.json").write_text("[]", encoding="utf-8")

            status = build_closure_status(config_path)

            self.assertEqual(
                status["experiments"][0]["force_status"],
                "FORCE_SYNC_PRELOAD_RELEASE_ONLY",
            )
            self.assertEqual(status["experiments"][0]["overall_status"], "PRELOAD_RELEASE_ONLY")

    def test_job_missing_frame_does_not_block_when_selected_dat_is_usable(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            config_path = root / "config.json"
            config_path.write_text(
                '{"output_root": "' + str(root).replace('\\', '/') + '", "experiments": [{"experiment_id": "S1"}]}',
                encoding="utf-8",
            )
            record_root = root / "Agents" / "PA12实验数据处理" / "处理记录"
            prep_root = root / "Agents" / "PA12实验数据处理" / "MatchID_VFM准备"
            record_root.mkdir(parents=True)
            prep_root.mkdir(parents=True)
            (record_root / "PA12批量处理清单.json").write_text(
                '[{"experiment_id":"S1","status":"VFM_READY","vfm_allowed":true}]',
                encoding="utf-8",
            )
            (prep_root / "PA12_DIC_DAT质量审计.json").write_text(
                '[{"实验编号":"S1","照片":"000001.jpg","status":"DIC_FIELDS_AVAILABLE"}]',
                encoding="utf-8",
            )
            (prep_root / "PA12_MatchID_VFM实验级索引.csv").write_text(
                "实验编号,Job缺少有效帧数\nS1,1\n",
                encoding="utf-8-sig",
            )

            status = build_closure_status(config_path)

            self.assertEqual(status["experiments"][0]["job_status"], "JOB_COVERAGE_REVIEW_REQUIRED")
            self.assertEqual(status["experiments"][0]["overall_status"], "EXPORT_REQUIRED")

    def test_closure_status_promotes_an_experiment_after_dic_force_merge(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            config_path = root / "config.json"
            config_path.write_text(
                '{"output_root": "' + str(root).replace('\\', '/') + '", "experiments": [{"experiment_id": "S1"}]}',
                encoding="utf-8",
            )
            record_root = root / "Agents" / "PA12实验数据处理" / "处理记录"
            prep_root = root / "Agents" / "PA12实验数据处理" / "MatchID_VFM准备"
            record_root.mkdir(parents=True)
            prep_root.mkdir(parents=True)
            (record_root / "PA12批量处理清单.json").write_text(
                '[{"experiment_id":"S1","status":"VFM_READY","vfm_allowed":true}]',
                encoding="utf-8",
            )
            (prep_root / "PA12_DIC_DAT质量审计.json").write_text(
                '[{"实验编号":"S1","照片":"000001.jpg","status":"DIC_FIELDS_AVAILABLE"}]',
                encoding="utf-8",
            )
            merged_status_dir = prep_root / "S1"
            merged_status_dir.mkdir()
            (merged_status_dir / "S1_DIC全场—力状态.json").write_text(
                '{"status":"MATCHID_VFM_INPUT_READY","frame_count":1}',
                encoding="utf-8",
            )

            status = build_closure_status(config_path)

            self.assertEqual(status["experiments"][0]["overall_status"], "MATCHID_VFM_INPUT_READY")

    def test_closure_status_uses_formal_merged_frame_count_after_exclusion(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            config_path = root / "config.json"
            config_path.write_text(
                '{"output_root": "' + str(root).replace('\\', '/') + '", "experiments": [{"experiment_id": "S15"}]}',
                encoding="utf-8",
            )
            record_root = root / "Agents" / "PA12实验数据处理" / "处理记录"
            prep_root = root / "Agents" / "PA12实验数据处理" / "MatchID_VFM准备"
            record_root.mkdir(parents=True)
            prep_root.mkdir(parents=True)
            (record_root / "PA12批量处理清单.json").write_text(
                '[{"experiment_id":"S15","status":"VFM_READY","vfm_allowed":true}]',
                encoding="utf-8",
            )
            (prep_root / "PA12_DIC_DAT质量审计.json").write_text(
                '[{"实验编号":"S15","照片":"000001.jpg","status":"DIC_FIELDS_AVAILABLE"},'
                '{"实验编号":"S15","照片":"000002.jpg","status":"DIC_FIELDS_AVAILABLE"}]',
                encoding="utf-8",
            )
            merged_status_dir = prep_root / "S15"
            merged_status_dir.mkdir()
            (merged_status_dir / "S15_DIC全场—力状态.json").write_text(
                '{"status":"MATCHID_VFM_INPUT_READY","frame_count":1,"source_counts":{"DAT_RECONSTRUCTED":1}}',
                encoding="utf-8",
            )

            status = build_closure_status(config_path)

            row = status["experiments"][0]
            self.assertEqual(row["selected_frame_count"], 1)
            self.assertEqual(row["dic_usable_frame_count"], 1)
            self.assertEqual(row["dic_unusable_frame_count"], 0)

    def test_closure_status_exposes_invalid_matchid_export(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            config_path = root / "config.json"
            config_path.write_text(
                '{"output_root": "' + str(root).replace('\\', '/') + '", "experiments": [{"experiment_id": "S1"}]}',
                encoding="utf-8",
            )
            record_root = root / "Agents" / "PA12实验数据处理" / "处理记录"
            prep_root = root / "Agents" / "PA12实验数据处理" / "MatchID_VFM准备"
            record_root.mkdir(parents=True)
            prep_root.mkdir(parents=True)
            (record_root / "PA12批量处理清单.json").write_text(
                '[{"experiment_id":"S1","status":"VFM_READY","vfm_allowed":true}]',
                encoding="utf-8",
            )
            (prep_root / "PA12_DIC_DAT质量审计.json").write_text(
                '[{"实验编号":"S1","照片":"000001.jpg","status":"DIC_FIELDS_AVAILABLE"}]',
                encoding="utf-8",
            )
            merged_status_dir = prep_root / "S1"
            merged_status_dir.mkdir()
            (merged_status_dir / "S1_DIC全场—力状态.json").write_text(
                '{"status":"EXPORT_INVALID","invalid_export":"000001.jpg.csv"}',
                encoding="utf-8",
            )

            status = build_closure_status(config_path)

            self.assertEqual(status["experiments"][0]["overall_status"], "EXPORT_INVALID")


if __name__ == "__main__":
    unittest.main()
