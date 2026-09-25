# PA12 照片—力同步、应力—应变与 MatchID VFM 准备

## 目标

以有效 DIC JPG/DAT 配对帧为主索引，将 `Press` 力数据按同一照片时间轴插值，生成正拉伸力 CSV、名义应力—应变审核结果和 MatchID VFM 输入索引。原始 JPG、DAT、XLS 保持不变。

最终目标是把同一有效帧的 DIC 全场位移/应变、同步 X/Y 力、几何和边界载荷接入 MatchID VFM，再进行材料参数识别。当前结果属于 VFM 前置数据，不等于已经完成 VFM。

## 正式来源与程序

- 正式旋转 DIC 来源：`D:\C盘迁移\Desktop\yuan\data\XY\picture-20250529\vertical_all_45°\PAPER`
- 力数据：`D:\C盘迁移\Desktop\yuan\data\XY\data-20250529\20250529`
- 输出 Vault：`D:\2026.9.21_finally\Agents\PA12实验数据处理`
- 批量配置：`configs/pa12_rotated_batch.json`
- 同步入口：`tools/run_pa12_batch.py`
- MatchID 索引入口：`tools/matchid_prepare.py`
- 输出审计入口：`tools/audit_pa12_outputs.py`
- DAT 质量审计入口：`tools/matchid_prepare.py`（生成逐帧审计）
- MatchID 导出合并入口：`tools/merge_matchid_exports.py`
- MatchID 闭环状态入口：`tools/audit_matchid_dic.py`

`CHECK` 和早期 `orginal_all` 不作为当前 DIC/VFM 正式输入。

## 力值和同步规则

- `Press` 按力使用，当前按 N 处理。
- 等双轴默认 `X=(X1_Press+X2_Press)/2`，`Y=(Y1_Press+Y2_Press)/2`；通道差异只作诊断。
- 零点用加载前基线均值，当前拉伸输出公式为 `F_corrected=-(F_raw-F_baseline)`，第一行强制归零。
- X/Y 使用完全相同的照片时间点分别插值，不按照片序号直接抽取力数据。
- 主索引是同名 JPG+DAT 配对帧。缺 DAT 的 JPG 不删除、不补造。
- 无可靠 EXIF 时，将有效力区间映射到配对帧号；实际照片频率按有效帧号差除以有效实验时间计算。稀疏 DAT 的帧号间隔不会被误报为连续采样。
- 正式同步力值门禁：照片数 = X CSV 行数 = Y CSV 行数、时间严格递增、无 NaN、首行归零、主动方向后续力值为正、终点已确定。

## 当前批处理状态

| 状态 | 实验 |
| --- | --- |
| 同步力值 `VFM_READY` | S15_XY_0.2、S16_XY_0.2、S17_XY_20、S18_XY_2、S19_X_0.2、S20_X_2、S21_X_20、S22_Y_0.2 |
| 数据受限 | S23_Y_2：力文件末尾未记录明显掉载，仅保留诊断结果 |
| 未完成 | S24_Y_20：文件开头已有约 1555 N 预载，当前无法估计加载前基线 |

`VFM_READY` 只表示单列同步力值 CSV 通过本程序的数量和数值门禁。当前已有 8 组实验完成 DIC 全场—同步力合并；S15 的 `000285.jpg.dat` 虽未列入 Job，但已直接用有记录的 DAT 重构并标记来源。S22 的 8 个无 `<53>` 帧已排除，不能把它们当作完整应变场。

## 输出

- 实验概览：`Agents/PA12实验数据处理/实验概览/`
- 照片—力表：`Agents/PA12实验数据处理/照片力匹配/`
- X/Y 单列力值：`Agents/PA12实验数据处理/VFM专用力值/`
- 检查图：`Agents/PA12实验数据处理/检查图/`
- 名义应力—应变：`Agents/PA12实验数据处理/应力应变/`
- 批量清单、报告、审计：`Agents/PA12实验数据处理/处理记录/`
- MatchID 元数据和帧—力—时间索引：`Agents/PA12实验数据处理/MatchID_VFM准备/`
- DAT 逐帧质量审计：`Agents/PA12实验数据处理/MatchID_VFM准备/PA12_DIC_DAT质量审计.md`
- MatchID 闭环状态：`Agents/PA12实验数据处理/MatchID_VFM准备/PA12_MatchID_VFM闭环状态.md`
- 环境检查：`Agents/PA12实验数据处理/MatchID_VFM准备/PA12_环境检查.md`

汇总概览按配置顺序包含十组实验。S24 已占位，已知速度和设置频率保留，其余未知字段写 `UNKNOWN`。

## 名义应力—应变工作口径

- 中心有效宽度：30 mm。
- 中心测量区厚度：1 mm。
- 总厚度：3 mm，仅作几何记录。
- 标距：30 mm。
- 当前名义截面积：30 mm²。
- 工程应变：加载方向两侧相对位移之和除以标距。

当前工作几何固定为中心 ROI 厚度 `1 mm`、整体大厚度 `3 mm`、有效宽度 `30 mm`、标距 `30 mm`；仍需在 MatchID 中确认的是坐标原点、坐标变换和边界载荷施加方式。论文中的 `E=1800 MPa`、`ν=0.375`、初始屈服强度 `21 MPa`、硬化模量 `180 MPa` 只是试样优化阶段的 Abaqus 工作参数，不是本实验已识别参数。

## MatchID 下一步

1. 审核检查图、应力—应变图和审计 JSON。
2. 保持 MatchID 2D 19.2.2.0 和已确认的分号/mm/无量纲字段设置；换版本或导出设置时重新做同帧验证。
3. 对 S22 处理 8 个 `NO_STRAIN_RECORDS` 帧，不能用别的帧替代；S23/S24 先人工确认力事件和预载基线。
4. 确认边界力方向、载荷分布、力臂/有效宽度、坐标变换、厚度和单位后，再进入 MatchID VFM。
5. 最后才做材料参数识别。

## 可复现命令

```powershell
python -m unittest discover -s tests -v
python tools/run_pa12_batch.py --config configs/pa12_rotated_batch.json
python tools/matchid_prepare.py --config configs/pa12_rotated_batch.json
python tools/check_pa12_environment.py --config configs/pa12_rotated_batch.json --output-root D:\2026.9.21_finally
python tools/audit_matchid_dic.py --config configs/pa12_rotated_batch.json
python tools/audit_pa12_outputs.py --config configs/pa12_rotated_batch.json
```
