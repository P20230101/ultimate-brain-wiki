# PA12 MatchID VFM 闭环设计

## 目标

在现有照片—力同步结果之上，增加一层不猜测 DAT 字段的 MatchID 接入流程：审计每个有效照片对应的 `.jpg.dat` 是否含有可用 DIC 记录，接收 MatchID Results Viewer 明确导出的标准 CSV，按同一照片名合并同步时间与 X/Y 力，并为后续 VFM 建立机器可读门禁。

## 边界与取舍

- 原始 JPG、DAT、XLS 和原始 `Job.m2inp` 只读；所有审计、索引和合并结果写入当前 Vault 的 `Agents/PA12实验数据处理/MatchID_VFM准备/`。
- “Job 是否列出某帧”和“该帧 DAT 是否含有 DIC 记录”分开判断。Job 少列但 DAT 有记录的帧不因 Job 清单单独被判定为无效；DAT 缺少 `<53>` 记录的帧不能进入需要应变场的 VFM 阶段。
- 不从 `<18>`、`<53>` 的原始位置猜测 `U/V/exx/eyy/exy`。只有用户用 Results Viewer 导出并在配置中声明字段名、单位后，才允许合并。
- 当前同步力 CSV 保持不变。DIC 字段审计是独立门禁，不为了满足力值数量而删改原始照片。

## 数据流

1. `matchid_prepare.py` 读取已有照片—力索引和同名 DAT。
2. 流式读取 DAT 压缩文本，记录版本、标定、点数以及 `<18>/<53>` 记录数，生成逐帧质量审计。
3. 用户在 MatchID Results Viewer 对一个正式实验导出一帧 CSV，配置显式列映射与单位。
4. `merge_matchid_exports.py` 只接受声明过的列映射，逐帧读取导出 CSV，检查必需字段、数值完整性、点数和坐标列，再把时间、X/Y 力附加到 DIC 全场表。
5. 合并结果只在所有目标帧有对应导出、字段完整、单位已声明时标记为 `MATCHID_VFM_INPUT_READY`；否则只生成缺口报告。

## 输出

- `PA12_DIC_DAT质量审计.csv/json/md`：逐实验、逐照片的 DAT 记录可用性。
- `<实验编号>_DIC全场—力索引.csv`：每帧导出文件、照片时间、X/Y 力、点数和字段状态。
- `<实验编号>/merged/<照片名>_DIC全场—力.csv`：每个导出帧的 DIC 字段加同步力列。
- `PA12_MatchID_VFM闭环状态.md/json`：区分 `FORCE_SYNC_READY`、`DIC_DAT_READY`、`EXPORT_REQUIRED`、`MATCHID_VFM_INPUT_READY`。
- `PA12_环境检查.md/json`：记录 Python 依赖、原始目录、MatchID 可调用性和缺少的人工步骤。

## 成功标准

- DAT 审计能复现 S22 的无 `<53>` 帧，并能识别 S15 的末帧 DAT 虽未列入 Job 但包含记录。
- 未声明字段映射或未声明单位时，合并命令失败并给出具体缺口，不生成正式合并结果。
- 合并后每个 DIC 点的 `时间/s`、`X向力/N`、`Y向力/N` 都来自同一照片索引；所有必需字段无 NaN。
- 现有 29 个同步测试继续通过，并新增针对上述门禁的测试。

## 尚未自动化的外部步骤

本机当前没有可调用的 MatchID Results Viewer 自动化窗口，且 MatchID 不是可由本仓库安全安装的开源依赖。因此“打开 Results Viewer 导出一帧标准 CSV”仍需用户在本机完成；程序会在环境报告和 GPT 交接文档中明确该动作及其输入位置。
