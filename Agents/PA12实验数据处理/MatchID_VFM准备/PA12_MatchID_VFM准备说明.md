# PA12 MatchID VFM 准备包

## 用户意图

后续把同一有效照片帧的 DIC 位移/应变场、同步的 X/Y 力、试样几何和边界载荷接入 MatchID VFM 模块，继续识别材料参数。当前包只完成输入索引和元数据核对，不宣称已经完成 VFM 识别。

## 已生成

- 实验级索引：`D:\2026.9.21_finally\Agents\PA12实验数据处理\MatchID_VFM准备\PA12_MatchID_VFM实验级索引.csv`。
- 逐帧 DAT 质量审计：`D:\2026.9.21_finally\Agents\PA12实验数据处理\MatchID_VFM准备\PA12_DIC_DAT质量审计.md`、`D:\2026.9.21_finally\Agents\PA12实验数据处理\MatchID_VFM准备\PA12_DIC_DAT质量审计.csv`、`D:\2026.9.21_finally\Agents\PA12实验数据处理\MatchID_VFM准备\PA12_DIC_DAT质量审计.json`。
- 环境检查：`MatchID_VFM准备/PA12_环境检查.md` 和 `PA12_环境检查.json`。
- 闭环状态：`MatchID_VFM准备/PA12_MatchID_VFM闭环状态.md` 和 `PA12_MatchID_VFM闭环状态.json`。
- 每个实验的 DIC 元数据 JSON：包含 Job 标定、ROI、DAT 点数、记录计数和输入路径。
- 每个已完成同步实验的帧—力—时间索引：同一照片名对应同名 DAT、X/Y 力和同步时间。
- 已增加 Job 覆盖和 DAT 逐帧有效性检查；Job 不覆盖或 DAT 没有 `<53>` 记录的帧不能直接当作已完成 DIC 全场输入。
- 已用同版本 Results Viewer 交叉验证 DAT 字段映射；`valid=False` 的 `<53>` 点被明确排除，绝不填零或插值。

## 原始方向与旋转后边界映射

- 方向证据图片：`raw/assets/PA12原始方向与旋转标定方向.jpg`；可复用边界配置：`configs/pa12_vfm_boundary.json`；审计结果：`MatchID_VFM准备/PA12_VFM边界载荷审计.json`。
- 原始机器右上/左下为 `Y1/Y2`，右下/左上为 `X1/X2`；正式旋转 DIC 的边界映射为：顶部=`X2`、底部=`X1`、左侧=`Y2`、右侧=`Y1`。
- MatchID Boundary 顺序固定为 `0=顶部、1=左侧、2=右侧、3=底部`；双轴使用 X 顶/底、Y 左/右，单轴只使用受力方向两边；拉伸力为正。
- 外围夹持/加载结构厚度记录为 `3 mm`；中心 ROI 必须完全位于 `1 mm` 减薄区，MatchID 工程厚度使用 `1 mm`；完整 S16 `.vfm` 只作为格式/方向证据。
- 所有当前双轴试验均为等双轴；外围机器力按用户确认直接作为 ROI 边界合力输入 MatchID 自带 VFM；按 `0.2、2、20 mm/s` 分速率识别。
- 参数策略：阶段 1 固定 `ν=0.375` 识别 `E`；阶段 2 固定该 `E、ν` 识别屈服 `Y` 和硬化 `H`。没有运行输出的参数写未识别/未计算。
- 当前检查结果：`MatchID_VFM准备/PA12等双轴VFM当前检查结果.md/.csv`；记录 ROI/力同步/帧数及当前识别状态。

## 已确认规则

- 正式 DIC 来源只使用 `vertical_all_45°/PAPER`；不使用 `CHECK` 或 `orginal_all`。
- `Press` 是力；等双轴默认 X/Y 各自取两条同向通道平均。
- X/Y 力使用同一组有效照片时间轴插值。
- DAT 原始文件保持不变；MatchID 可直接读取原 DAT。
- 当前 Python 依赖和原始输入路径均可用；环境检查已发现 MatchID 2D 19.2.2.0，DAT 字段映射和标准导出列已完成当前版本本地同帧交叉验证；各实验仍需按闭环状态完成导出/重构。

## 尚未确认

- S15 正式 DIC/VFM 使用 `000001–000284.jpg`；`000285.jpg` 是视觉断裂帧，其 DAT 点数异常，不进入有效场；原始 JPG/DAT 保留。S22 有 8 个没有 `<53>` 的 DAT 帧，已排除出有效全场。
- 需要逐步核验 ROI 在中心减薄区内的位置、1 mm MatchID 厚度、旋转后 XY 方向、参考帧/零力映射和逐帧力序列；用户已确认机器力直接作为 ROI 边界合力，不恢复四边牵引分布。
- 厚度 3 mm、宽度 30 mm、标距 30 mm 当前只是名义应力—应变审核的工作参数。
- 当前选定 DAT 逐帧审计结果必须先读 `PA12_DIC_DAT质量审计.md`；S22 的 8 个 `NO_STRAIN_RECORDS` 帧不能直接进入 DIC 全场合并。

## 下一步操作顺序

1. 保持所有实验使用与 S16 相同的 MatchID 2D 版本、导出列和单位；换版本时重新做同帧交叉验证。
2. 对导出缺失、含 NaN 或点数与 DAT 不一致的帧，运行 `python tools/merge_matchid_exports.py`，程序会在 DAT 映射可用时重构并标记 `DAT_RECONSTRUCTED`。
3. DAT 无 `<53>`、无法解析或缺失时，程序保持阻断并写出具体帧，不填零、不插值、不静默删点。
4. 对等双轴各速度按当前检查结果核对 ROI、厚度、XY 方向、同步、首帧、末帧和数量，再使用 MatchID 自带 VFM；非等双轴数据不是前置要求。
5. 每个速度分开运行参数识别，并记录内外虚功、残差、参数边界、收敛及识别区间。
6. 每次继续工作前先运行 `python tools/audit_matchid_dic.py --config configs/pa12_rotated_batch.json`，以闭环状态 JSON 为机器判断入口。

## 可复现命令

```powershell
python tools/matchid_prepare.py --config configs/pa12_rotated_batch.json
```
