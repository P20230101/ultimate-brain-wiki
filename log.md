# 工作日志

本文件只追加，不改写旧记录。每条记录使用一致标题，便于搜索和脚本处理。

## [2026-09-21] init | 终极大脑 Wiki 初始化

- 来源：[Karpathy LLM Wiki gist](raw/karpathy-llm-wiki.md)
- 更新：`AGENTS.md`, `index.md`, `log.md`, `README.md`, `raw/`, `wiki/`, `schema/`
- 结论：采用 Raw sources / The wiki / The schema 三层架构，保留最小核心层级。
- 待验证：GitHub Pages 启用后确认首页可访问。

## [2026-09-21] policy | Obsidian Second Brain 工作区约定

- 来源：用户指令
- 更新：`AGENTS.md`, `README.md`, `log.md`
- 结论：当前仓库即 Obsidian 连接的 Second Brain 文件夹；后续所有构建都在此目录内进行。
- 待验证：暂无。

## [2026-09-21] config | Obsidian 框架初始化

- 来源：用户指令
- 更新：`.obsidian/`, `schema/obsidian-templates/`, `AGENTS.md`, `README.md`, `index.md`, `schema/README.md`, `log.md`
- 结论：Obsidian vault 已配置默认笔记目录、附件目录、模板目录和核心插件；后续可直接在 Second Brain 中使用模板维护 wiki。
- 待验证：打开 Obsidian 后确认模板插件识别 `schema/obsidian-templates/`。

## [2026-09-22] ingest | PA12 单轴/双轴拉伸项目第一阶段盘点

- 来源：`D:\C盘迁移\Desktop\yuan`
- 更新：`D:\C盘迁移\Desktop\yuan\PA12_biaxial_project\05_output\manifests\`, `D:\C盘迁移\Desktop\yuan\PA12_biaxial_project\05_output\reports\data_inventory_report.md`, `wiki/PA12双轴拉伸项目_第一阶段盘点.md`
- 结论：建立了结构化副本和第一阶段索引；12 个正式状态导出可读但未发现直接 force/load 列；DIC 数据存在缺 DAT、孤立 DAT 或非连续编号，图片与力文件尚未同步。
- 待验证：试样编号与状态导出映射、相机/控制器触发关系、真实力通道和缺失 DAT 的来源。

## [2026-09-22] experiment | PA12 XY-0.1-02 照片—力同步与 VFM

- 来源：`D:\C盘迁移\Desktop\yuan\data\XY\picture-20250529\orginal_all\XY-0.1-02\Test1\33061_1_16`、`D:\C盘迁移\Desktop\yuan\data\XY\data-20250529\20250529\xy-2-0.1_state_20250529104919_20250529104947.xls`
- 更新：`wiki/PA12照片力同步与VFM生成.md`、`wiki/PA12双轴拉伸项目_第一阶段盘点.md`；结果写入 `D:\C盘迁移\Desktop\yuan\second brain\AGENTS\PA12实验数据处理`
- 结论：确认 `Press` 为力；自动确定力起点、峰值和掉载点；选取 258 张有效照片；X/Y 插值时间轴一致；两份正式 VFM CSV 均为 258 行。
- 待验证：无可靠 EXIF 时相机时间轴为估计值；原始 Press 符号按数据保留，后续 VFM 约定若需要正值需显式设置 `force_sign`。

## [2026-09-22] experiment | PA12 旋转序列照片—力同步闭环

- 来源：`D:\C盘迁移\Desktop\yuan\data\XY\picture-20250529\vertical_all_45°\PAPER`、`D:\C盘迁移\Desktop\yuan\data\XY\data-20250529\20250529`
- 更新：`configs/pa12_rotated_batch.json`、`tools/pa12_sync.py`、`tools/run_pa12_batch.py`、`tests/test_pa12_sync.py`、`Agents/PA12实验数据处理/`、`wiki/PA12照片力同步与VFM生成.md`、`wiki/PA12双轴拉伸项目_第一阶段盘点.md`
- 结论：固定十组旋转序列—力文件映射；配对帧成为照片主索引；支持 S22–S24 稀疏 DAT；生成 S15、S16、S18 三组正式 VFM 力值 CSV，其他实验保留诊断或未完成状态。
- 待验证：Press 工程单位、相机触发/实际设定频率、旋转目录速度与力文件速度冲突、单轴非加载方向力规则、DAT 全场位移导出、MatchID VFM 边界力与材料参数输入。

## [2026-09-22] experiment | PA12 闭环补齐位移、应力—应变和 MatchID 准备包

- 来源：`D:\C盘迁移\Desktop\yuan\data\XY\picture-20250529\vertical_all_45°\PAPER`、`D:\C盘迁移\Desktop\yuan\data\XY\data-20250529\20250529`
- 更新：`tools/pa12_sync.py`, `tools/pa12_mechanics.py`, `tools/matchid_prepare.py`, `tools/run_pa12_batch.py`, `configs/pa12_rotated_batch.json`, `tests/test_pa12_sync.py`, `Agents/PA12实验数据处理/`, `wiki/`, `index.md`
- 结论：设备位移改为加载方向两侧增量之和；S15、S16、S18 仍通过正式 VFM 力值门禁；S15—S22 已生成名义应力—应变审核结果；10 组 Job/DAT 元数据和 8 组帧—力—时间索引已写入 MatchID 准备包。
- 待验证：S23/S24 人工事件索引；DAT `<18>/<53>` 逐点字段真实导出列名；Press 工程单位、厚度/标距和 VFM 边界力定义。

## [2026-09-22] audit | PA12 批量结果与 GPT/MatchID 交接收尾

- 来源：`configs/pa12_rotated_batch.json`、`Agents/PA12实验数据处理/处理记录/PA12批量处理清单.json`
- 更新：`tools/audit_pa12_outputs.py`、`tools/run_pa12_batch.py`、`Agents/PA12实验数据处理/处理记录/`、`Agents/PA12实验数据处理/MatchID_VFM准备/`、`wiki/`、`index.md`
- 结论：新增可重复的批量输出审计；概览按配置顺序保留 10 行并为 S24 写入已知速度/设置频率和未知结果；8 组同步力值通过正式 CSV 门禁，S23 数据受限，S24 未解决。
- 待验证：S15/S22 Job 缺帧、S23/S24 人工事件、DAT 字段正式导出、VFM 边界力和几何/单位确认。

## [2026-09-23] experiment | PA12 MatchID DAT 质量审计与 VFM 接入门禁

- 来源：`D:\C盘迁移\Desktop\yuan\data\XY\picture-20250529\vertical_all_45°\PAPER`、`configs/pa12_rotated_batch.json`
- 更新：`tools/matchid_dic.py`、`tools/matchid_prepare.py`、`tools/merge_matchid_exports.py`、`tools/audit_matchid_dic.py`、`tools/check_pa12_environment.py`、`configs/matchid_export_example.json`、`tests/test_matchid_dic.py`、`Agents/PA12实验数据处理/MatchID_VFM准备/`、`Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md`、`wiki/`、`index.md`
- 结论：完成 1327 个选定 DAT 的逐帧记录审计；1319 个含 `<18>/<53>`，S22 有 8 个 `NO_STRAIN_RECORDS`；S15 `000285.jpg.dat` 有记录但当前 Job 未列出。新增声明式 MatchID CSV 合并入口，未声明字段/单位或缺帧时阻断正式合并。
- 待验证：需用户在本机 MatchID Results Viewer 导出一帧标准 CSV，确认真实列名、单位、坐标和应变约定；随后才能批量合并 DIC 全场并进入 VFM。

## [2026-09-23] environment | PA12 MatchID 本机环境确认

- 来源：本机程序目录 `D:\DIC\MATCH_DIC\2019\MatchID 2D\MatchID.exe`
- 更新：`configs/pa12_rotated_batch.json`、`Agents/PA12实验数据处理/MatchID_VFM准备/PA12_环境检查.md`、`Agents/PA12实验数据处理/MatchID_VFM准备/PA12_环境检查.json`
- 结论：发现 MatchID 2D 19.2.2.0；Python 依赖和十组原始输入路径均可用，环境状态为 `READY_FOR_MATCHID_EXPORT`。
- 待验证：Results Viewer 的标准 CSV 字段、单位、坐标和应变约定仍需实际导出确认。

## [2026-09-23] experiment | PA12 MatchID 导出合并与闭环审计

- 来源：`_matchid_export/`、`configs/matchid_export_example.json`、`configs/pa12_rotated_batch.json`
- 更新：`tools/merge_matchid_exports.py`、`tools/audit_matchid_dic.py`、`tests/test_matchid_dic.py`、`Agents/PA12实验数据处理/MatchID_VFM准备/`、`Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md`、`Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json`、`index.md`
- 结论：S16（257 帧）、S17（12 帧）、S19（126 帧）完成 DIC 全场—同步力合并；S15 缺 `000285.jpg.csv`；S18/S20/S21 的导出含非有限应变字段并被 `EXPORT_INVALID` 阻断；S22、S23、S24 的既有 DAT/力值问题保持阻断。新增 43 项回归测试全部通过。
- 待验证：S15/S18/S20/S21 的 MatchID 导出修复，S22 的无 `<53>` 帧，S23/S24 的人工力事件，几何和 VFM 边界载荷定义。

## [2026-09-23] ingest | PA12 实验总体流程图与防跑偏协议

- 来源：用户提供流程图 `Agents/PA12实验数据处理/处理记录/PA12实验总体流程图_用户提供.png`
- 更新：`Agents/PA12实验数据处理/处理记录/PA12实验总体方法与防跑偏协议.md`、`index.md`
- 结论：将总体方法固定为“真实实验数据 → MatchID DIC 处理 → 坐标/位移/应变导出 → 时间同步（force.csv: time/Fx/Fy）→ 正式分析输入 → 单轴/双轴 VFM 分支 → J2 参数拟合 → 实验—模型自洽性验证 → 边界力/载荷场策略 → 数据集整理分层 → 参数稳定性判断 → 人工复核；不稳定时再考虑材料数据整合和 AI 代理模型”。
- 待验证：流程图右侧少数节点文字因原图分辨率不足，保留为待人工复核，不作为自动处理规则。

## [2026-09-23] experiment | PA12 DAT 重构与 MatchID 合并闭环更新

- 来源：`_matchid_export/`、`D:\C盘迁移\Desktop\yuan\data\XY\picture-20250529\vertical_all_45°\PAPER`、`configs/matchid_export_example.json`
- 更新：`tools/matchid_dic.py`、`tools/merge_matchid_exports.py`、`tools/matchid_prepare.py`、`tools/audit_matchid_dic.py`、`tests/test_matchid_dic.py`、`tests/test_pa12_sync.py`、`Agents/PA12实验数据处理/MatchID_VFM准备/`、`Agents/PA12实验数据处理/处理记录/`
- 结论：S15（285）、S16（257）、S17（12）、S18（126）、S19（126）、S20（63）、S21（36）帧已生成 DIC 全场—同步力合并；S15/S18/S20/S21 的异常导出按同版本 Results Viewer 交叉验证的 DAT 映射重构，分别排除 570/252/126/72 个 `valid=False` 点。
- 待验证：S22 的 8 个无 `<53>` DAT 帧、S23 的断裂终点、S24 的预载/基线；VFM 边界载荷、几何、坐标变换和单位仍未确认。闭环 `formal_matchid_vfm_ready=false`，不进入 J2 参数识别。

## [2026-09-23] audit | PA12 总体方法入口与 MatchID 交接状态复核

- 来源：用户提供的实验路径/方法流程图、`configs/pa12_rotated_batch.json`、当前 Agent 交接文件和 MatchID 闭环结果。
- 更新：`Agents/PA12实验数据处理/处理记录/PA12实验总体方法与防跑偏协议.md`、`Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md`、`Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json`、MatchID/批量报告模板与对应派生报告。
- 结论：总体方法固定为“真实实验数据 → MatchID DIC → 坐标/位移/应变 → 同步 X/Y 力 → 单轴/双轴 VFM → 边界载荷确认 → J2 参数识别 → 实验—模型验证 → 稳定性判断 → 人工复核”；当前版本 MatchID 2D 19.2.2.0 的字段映射和导出单位已完成本地同帧交叉验证。`Press` 仍按力处理，默认 `X=(X1_Press+X2_Press)/2`、`Y=(Y1_Press+Y2_Press)/2`。
- 验证：`53/53` 单元测试通过；`compileall` 通过；力值/概览审计通过；MatchID 闭环为 7 组 `MATCHID_VFM_INPUT_READY`、S22 `DIC_DAT_REVIEW_REQUIRED`、S23/S24 `FORCE_REVIEW_REQUIRED`，因此 `formal_matchid_vfm_ready=false`。
- 下一步：先处理 S22/S23/S24 阻断，再确认几何、坐标变换和边界载荷场；在这些条件确认前不进入 J2 参数拟合。

## [2026-09-23] ingest | PA12 实验路径与总体方法 Agent 记录复核

- 来源：用户提供的实验流程图；`D:\C盘迁移\Desktop\yuan`；当前 PA12 Agent 交接状态。
- 更新：`Agents/PA12实验数据处理/处理记录/PA12实验总体方法与防跑偏协议.md`
- 结论：确认流程图、正式 DIC 来源、实验数据路径、`Press` 力定义、默认等双轴规则和 MatchID VFM/J2 总体顺序均已固定；同步修正方法表中的闭环状态，使其与机器状态一致（7 组可进入 MatchID 输入，S22–S24 仍阻断）。
- 待验证：S22 无应变帧、S23 断裂终点、S24 预载/基线，以及 VFM 边界载荷、几何和单位。

## [2026-09-23] audit | PA12 当前批次复核与交接状态更新

- 来源：`configs/pa12_rotated_batch.json`、旋转 `PAPER` JPG/DAT、Press/Pos 文件、`tests/` 和各审计脚本。
- 更新：`Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md`、`Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json`、批量派生结果和 MatchID 闭环状态。
- 结论：60/60 单元测试通过；批处理、编译和输出契约审计通过；8 组为 `MATCHID_VFM_INPUT_READY`，S23 为 `FORCE_REVIEW_REQUIRED`，S24 为 `PRELOAD_RELEASE_ONLY`。VFM 中心 ROI 厚度固定为 1 mm，整体厚度记录为 3 mm，`Press` 按 N 使用，正式 DIC 来源固定为旋转 `vertical_all_45°/PAPER`。
- 待验证：S18/S20/S21 的应变回退需要区分测量噪声与真实位移；S22/S23 的终点事件和所有 VFM 边界载荷/坐标定义仍需人工确认。未对异常曲线静默平滑，未进入 J2 参数识别。

## [2026-09-23] query | 两篇激光烧结 PA12 论文写作蒸馏

- 来源：`C:\Users\Administrator\Desktop\综述\000 文献\DIC-VFM-中心分析\center-FEM\VARIABILITY IN THE MECHANICAL PROPERTIES OF LASER SINTERED PA-12 .pdf`；`C:\Users\Administrator\Desktop\综述\000 文献\DIC-VFM-中心分析\center-FEM\Variability, heterogeneity, and anisotropy in the quasi‐static response of laser sintered PA12 components.pdf`
- 更新：`wiki/methods/PA12论文写作学习_两篇激光烧结PA12论文.md`、`index.md`
- 结论：提炼出“工程问题—过程原因—文献分歧—研究目标—方法分工—定量结果—机制解释—限制与工程含义”的写作链；第二篇比第一篇增加了统计分层、密度/SEM、异质性机制和验证边界。
- 待验证：将该模板应用到当前 PA12 DIC/VFM 论文草稿后，逐项核对结论与全场数据、边界载荷和统计证据是否对应。

## [2026-09-23] config | 安装去 AI 味与非防御性写作 skill

- 来源：[petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop)
- 更新：全局 Codex skill `no-ai-slop`；`wiki/methods/去AI味与非防御性学术写作.md`；`wiki/methods/PA12论文写作学习_两篇激光烧结PA12论文.md`；`index.md`
- 结论：将 `no-ai-slop` 设为后续写作的默认最小编辑 skill；中文学术使用时保留真实不确定性和适用边界，不把去防御性改写成过度断言。
- 待验证：下一次修改真实论文段落时，检查是否同时满足“少套话、少重复免责声明、证据边界具体、原意不变”。

## [2026-09-23] experiment | PA12 原始方向与旋转后 VFM 边界审计

- 来源：用户提供的 `raw/assets/PA12原始方向与旋转标定方向.jpg`；完整 `D:\C盘迁移\Desktop\yuan\data\XY\picture-20250529\vertical_all_45°\PAPER\biaxal\S16_XY_0.2\S16_XY_0.2_258.vfm`。
- 更新：`tools/vfm_boundary.py`、`tools/audit_pa12_vfm_boundary.py`、`configs/pa12_vfm_boundary.json`、`tests/test_vfm_boundary.py`、`tools/audit_matchid_dic.py`、`tests/test_matchid_dic.py`、`tools/pa12_sync.py`、`tests/test_pa12_sync.py`、`Agents/PA12实验数据处理/处理记录/`、`Agents/PA12实验数据处理/MatchID_VFM准备/`、`index.md`。
- 结论：原始机器右上/左下为 `Y1/Y2`、右下/左上为 `X1/X2`；旋转后 ROI 顶部=`X2`、底部=`X1`、左侧=`Y2`、右侧=`Y1`。完整 S16 `.vfm` 含 4 个 Boundary、4 组 Forces、每组 258 帧，中心厚度 1 mm，首帧归零且后续力值为正。X/Y 共用时间轴状态已修正为真实数组比较。
- 已知限制：目录内部分试算 `.vfm` 被只读扫描发现压缩截断或缺少 `Boundary/Forces`，不作为正式格式证据；边界载荷分布、施加长度、力臂、DIC 坐标变换和 MatchID 最终载荷选项仍需 VFM 导入验证。

## [2026-09-23] audit | PA12 等双轴 VFM 当前检查结果

- 来源：用户确认的等双轴加载、中心/外围分区厚度与传感器合力前提；`configs/pa12_rotated_batch.json`；四组 MatchID 元数据、DIC全场—力索引、闭环状态及 S16 VFM 文件。
- 更新：`Agents/PA12实验数据处理/MatchID_VFM准备/PA12等双轴VFM当前检查结果.md`、`wiki/PA12单轴到双轴弹塑性VFM总目标与阶段路线图.md`、`index.md`。
- 结论：S15/S16/S18/S17 的有效 DIC—力索引分别为 284/257/126/12 行，照片与力值数量一致且时间严格递增；起始校正力为零。ROI 厚度按用户确认的中心区 1.0 mm 记录，外围结构总体厚度 3 mm 与中心 ROI 分开。
- 待验证：各 ROI 与实体 1 mm 减薄区边界的空间叠合；S16 完整 VFM 含参考帧 000000，须核对参考帧力序列与 257 个有效变形帧的对应；其余速度当前无可确认的完整 VFM 参数结果。E、Y、H、残差及内外虚功均未识别/计算，不填猜测值。

## [2026-09-23] plan | PA12 单轴到双轴弹塑性 VFM 总路线图

- 来源：用户原始 PA12 项目目标、总体方法与防跑偏协议、GPT 交接文档、MatchID 闭环状态、用户提供的弹塑性模型和结果图截图。
- 更新：wiki/PA12单轴到双轴弹塑性VFM总目标与阶段路线图.md、index.md。
- 结论：完整目标按资料/数据准入、边界与本构定义、多模型单轴弹塑性 VFM、跨单轴验证、双轴 VFM、稳定性与人工复核、最终可复现发布分阶段推进。硬化模型首轮至少包含 Linear、Voce I、Voce II、Ludwik、Swift；公式须核实来源后实现，模型比较使用同一数据和边界条件。每个适用的识别阶段交付模型对比、参数收敛、应力空间和驱动参数四类图及源 CSV。
- 待验证：首个合格单轴数据集、各硬化模型的准确公式与参数可辨识性、截图中应力空间和驱动参数图的精确字段/单位、边界载荷空间定义、S15/S23/S24 当前准入状态。

## [2026-09-23] audit | PA12 MatchID VFM 交接与 S16 试算状态

- 来源：用户确认的 MatchID 自带 VFM 与机器力作为 ROI 边界合力规则；用户报告的 S16 `3try`、`4try_step3` 和第 16 轮 GUI 状态。
- 更新：`Agents/PA12实验数据处理/处理记录/PA12实验总体方法与防跑偏协议.md`、`Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md`、`Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json`、`Agents/PA12实验数据处理/MatchID_VFM准备/PA12_VFM边界载荷说明.md`、`index.md`。
- 结论：固定 MatchID 自带 VFM；外围机器传感器力直接作为 ROI 边界合力，不恢复四边牵引分布。外围整体厚度 `3 mm` 与中心 ROI `1 mm` 分开记录。四组等双轴数据分别拟合，阶段1固定 `ν=0.375` 识别 `E`，阶段2固定 `E、ν` 识别 `Y、H`。S16 `3try` 的 X/Y 力 MAE 为 `26.1206/23.4119 N`、末帧绝对差为 `1452.79/1478.85 N`，不同步；`4try_step3` Forces count 为 `0`；第16轮 GUI 参数仅为中间候选。
- 待验证：S16 时间/力序列和 Forces 输入修正后，重新检查逐帧内外虚功、残差及参数边界。用户并行修改的 `tools/pa12_vfm_check.py`、测试、配置和检查结果文件未在本次改动。

## [2026-09-23] audit | PA12 等双轴 VFM 检查器与报告一致性

- 来源：`tools/pa12_vfm_check.py`、`tests/test_pa12_vfm_check.py`、`configs/pa12_vfm_boundary.json`、现有等双轴检查 Markdown/CSV、S15 照片—力表和 X/Y 单列力 CSV。
- 更新：`Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md`、`Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json`、`index.md`。
- 结论：定向测试 4 项中 3 项通过、1 项因 `residual_label_without_value` 缺失报错；代码、测试夹具与生产配置的屈服/硬化/进度/残差标签字段名不一致。当前 Markdown/CSV 虽各有 4 行，但 S15 视觉断裂帧与最后有效 DIC 帧、S16 预处理同步与 VFM Forces 同步状态，以及多项结论文案未完全一致。S15 `000284.jpg` 同步末行力为 X=`1608.18 N`、Y=`1603.33 N`，与峰值统计应分开表达。
- 已知边界：未修改或重生成并行维护的代码、测试、配置及 Markdown/CSV 结果；先统一字段契约和状态语义，再用同一数据生成、复核两种报告。

## [2026-09-23] audit | 更正 S15 有效 DIC/VFM 帧数交接

- 来源：S15 批量配置、DIC—力状态与索引、照片—力表、X/Y VFM 力 CSV、当前等双轴检查报告。
- 更新：`Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md`、`Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json`。
- 结论：S15 正式照片—力表有 284 条数据记录，X/Y 力 CSV 各 284 行，DIC—力合并状态和索引均为 284 帧，排除无效场点共 568 个。`000285.jpg` 是视觉断裂帧，其 DAT 虽存在但仅约 5,277 点，较前序约 98,000 点完整场不完整，因此排除；`000284.jpg` 为最后有效 DIC/VFM 帧。更正旧机器交接中的 285 帧、570 个排除点及错误的帧保留描述。
- 待处理：检查器修复后，从单一检查结果同步生成 Markdown 与 CSV，并保留“视觉断裂照片”和“最后有效 DIC/VFM 照片”两个独立字段。

## [2026-09-23] audit | PA12 检查器同步状态字段语义

- 来源：`tools/pa12_vfm_check.py` 的 `summarize_check()` 状态流和当前 S16 检查报告。
- 更新：`Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md`、`Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json`、`index.md`。
- 结论：当前 `时间同步` 字段只反映预处理照片—力对应表与 X/Y CSV 的一致性；MatchID `vfm_force_status` 只追加在结论文本，不影响该字段。因此报告中“预处理同步通过”不代表具体 VFM Forces 文件与同步序列一致，应分字段呈现。
- 待处理：代码/配置字段统一后，以同一检查结果生成 Markdown 和 CSV，并保留两级同步状态。

## [2026-09-23] audit | PA12 VFM 检查器配置入口契约

- 来源：`tools/pa12_vfm_check.py`、`configs/pa12_vfm_boundary.json`、`configs/pa12_rotated_batch.json` 的只读构建调用。
- 更新：`Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md`、`Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json`、`index.md`。
- 结论：检查器构建函数要求单个输入同时含 `experiments` 和 `defaults.geometry`，并从同一输入读取 `current_matchid_state_snapshot`、`roi_location_status`。边界配置缺 `experiments`，只读构建报 `KeyError`；批次配置可生成四行基础检查，但缺参数快照/ROI 状态，候选值不会进入结果且使用 ROI 默认文案。结果 writer 会覆盖现有报告，本次未调用。
- 下一步：明确统一的配置传入契约，并用生产配置完成只读构建与测试；字段契约、预处理同步/VFM Forces 同步状态和报告 Markdown/CSV 一致性全部通过后，再由 writer 更新报告。

## [2026-09-23] audit | PA12 VFM 检查器当前版本复测

- 来源：当前 `tools/pa12_vfm_check.py`、`tests/test_pa12_vfm_check.py`、`configs/pa12_rotated_batch.json` 与相邻 `configs/pa12_vfm_boundary.json`。
- 更新：PA12 GPT 交接文档、机器状态和 `index.md`。
- 结论：检查器定向测试 4/4 通过；纯读取 `build_current_check(pa12_rotated_batch.json)` 成功构造 S15/S16/S17/S18 四行，并读取相邻边界配置中的 S16 GUI 候选和 ROI 状态。报告 writer 未调用，既有 Markdown/CSV 仍是旧版。
- 待处理：将预处理同步与 VFM Forces 同步拆成独立状态、区分 S15 视觉断裂帧和末有效 DIC 帧，并确保同次构建同时输出 Markdown 与 CSV。

## [2026-09-24] verification | PA12 VFM 检查器更新版

- 来源：当前 `tools/pa12_vfm_check.py`、`tests/test_pa12_vfm_check.py`、`configs/pa12_rotated_batch.json` 和 `configs/pa12_vfm_boundary.json`。
- 更新：`Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md`、`Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json`、`index.md`。
- 结论：`test_pa12_vfm_check.py` 定向测试 4/4 通过；纯读取批次构建成功返回 S15、S16、S17、S18 四行，并包含 S16 候选参数和 ROI 状态。测试覆盖单元逻辑；纯读取构建验证了配置关联但不覆盖报告文件写入。Windows 默认 GBK 无法直接显示包含 Unicode 下标的完整 JSON，改用 ASCII 转义检查了相同内存结果。报告 writer 未运行，现有 Markdown/CSV 保持原样。
- 待处理：对生成器调用/字段映射增加生产配置级验证；由产物负责人或获授权后统一重生成 Markdown/CSV，并复核视觉断裂与有效帧、预处理同步与 VFM Forces 同步的分字段表达。

## [2026-09-24] verification | PA12 等双轴检查报告与当前 builder 一致

- 来源：现有 `PA12等双轴VFM当前检查结果.md/csv` 与 `build_current_check(configs/pa12_rotated_batch.json)` 的只读结果。
- 验证：Markdown 4 行、CSV 4 行；按 `REPORT_FIELDS` 逐行逐字段比较，差异为 0。S15 视觉断裂帧与末有效 DIC 帧分开；S16 预处理照片—力同步通过与 VFM Forces 未闭合分别表达。
- 结果：确认报告由并行流程更新且与当前 builder 一致；本轮未调用 writer、未改报告文件。

## [2026-09-24] verification | PA12 VFM 当前报告逐字段一致性

- 来源：当前 `PA12等双轴VFM当前检查结果.md/csv`、`tools/pa12_vfm_check.py` 的 `build_current_check()` 内存结果。
- 结果：Markdown 4 行、CSV 4 行；按 `REPORT_FIELDS` 逐行逐字段比较，差异 `0`。S15 视觉断裂/末有效 DIC 帧、S16 预处理/VFM Forces 状态和候选参数文案均与当前 builder 输出一致。
- 限制：本轮只读比对，未调用 writer；一致性不等于 VFM 参数已识别或虚功/残差门槛已通过。

## [2026-09-24] assessment | PA12 单轴 VFM 首试候选

- 来源：S19/S20/S21/S22 的 DIC—力状态、MatchID 合并帧数、应力—应变审核报告和旋转批次配置。
- 更新：`Agents/PA12实验数据处理/处理记录/PA12单轴VFM首试候选评估.md`、`index.md`。
- 结论：暂选 `S19_X_0.2` 作为首个单轴 VFM 数据候选。证据为 `MATCHID_VFM_INPUT_READY`、126 个有效合并帧、未标记 DAT 重构阻断、X 方向线性段 R²=`0.999482`。S20/S21 作为同方向不同速率的后续验证，S22 因 R²=`0.822886`、8 个无应变帧排除和大应变适用性问题暂不作首试。
- 新发现：S19 Job Shape 为 5 控制点 Polygon，外接框 `11.53×65.85 mm`，不能直接当作中心约 `28×28 mm` ROI。Job 参考帧为 `000000.jpg`，同步力表从 `000002.jpg` 起；处理报告的自动掉载索引 `12827` 对应同步表最后照片 `000127.jpg`。ROI 物理位置、参考帧零力对应和终点有效性需人工确认。
- 限制：S19 仍只是数据首选，不是 VFM 准入通过或参数识别结果；ROI/参考帧/终点、应变度量、虚功闭合、本构 H 定义和参数稳定性仍未通过。

## [2026-09-24] audit | S19 单轴 Polygon 与双轴中心 ROI 区分

- 来源：S19/S22 参考图、S19 `Job.m2inp` 的 `<Shape>`、S19 DIC 元数据和照片—力时间索引。
- 结论：S19/S20/S21/S22 参考图均为竖直长条单轴试样；S19 Polygon 为 5 控制点长区域，外接框约 `11.53×65.85 mm`，不能当作双轴中心约 `28×28 mm` ROI。单轴 VFM 还需独立确认 Polygon 的实际积分域、厚度、有效宽度、标距和边界外功。
- 更新：`Agents/PA12实验数据处理/处理记录/PA12单轴VFM首试候选评估.md`、`Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json`、`index.md`。
- 结论状态：S19 保留为单轴数据质量首选，但 ROI/几何/参考帧/终点门槛未通过，不启动参数识别。
- 图像核验：S19/S22 参考图为长条单轴试样，S15 参考图为十字双轴试样；S19 的 Polygon 长区域不能等同双轴中心 ROI。
- 可辨识性限制：高 R² 单轴曲线不自动证明 `Y/H` 可由 VFM 独立识别；需检查全场非均匀性、灵敏度矩阵/秩和帧子集稳定性。若不满足，S19 只用于曲线与 `E` 验证。
- 一手资料支持：MatchID 官方将 VFM 塑性识别与全场 DIC、实验设计及误差/灵敏度评估关联；项目 PA12 论文说明双轴应变状态可激活面内本构参数；弹塑性 VFM 方法论文强调非均匀场、虚场选择和噪声对参数识别的影响。详见候选评估页的链接。

## [2026-09-24] audit | S19 VFM 文件边界载荷缺口

- 来源：S19 目录 `X_0.2.vfm` 的只读 gzip 结构扫描；S19 Job/DIC 元数据。
- 结论：`X_0.2.vfm` 只包含 `Thickness`、`Conversion`、`ReferenceFile`、`DataFile`、网格/子集设置等 DIC 工程标签，不含 `Boundary` 或 `Forces`。它不能证明 S19 单轴 VFM 的机器力边界合力、外虚功或实际厚度；双轴 S16 的四边 `.vfm` 不能替代单轴边界定义。
- 更新：`Agents/PA12实验数据处理/处理记录/PA12单轴几何证据缺口.md`、`Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json`。
- 结论状态：S19 继续作为单轴数据质量首选，但保持 VFM 参数识别锁定；需取得单轴边界/外功定义后再进入 MatchID VFM。

## [2026-09-24] assessment | PA12 双轴 VFM 首试候选

- 来源：四组等双轴当前检查报告、S15–S18 DIC—力状态、旋转批次配置、S16 GUI 试算状态。
- 结论：暂选 `S15_XY_0.2` 作为第一个 MatchID 自带 VFM 输入/内外虚功闭合人工核验对象：284 个有效合并帧、中心 ROI 约 28.78×28.78 mm、中心厚度 1 mm、最后有效帧 000284。该选择不等于开始参数识别。
- 延后：S16 因 3try Forces 不同步/4try_step3 Forces=0 暂不首试；S18 作为 2 mm/s 后续候选；S17 仅 12 帧，不作首轮塑性识别。
- 限制：双轴候选核验不能绕过单轴路线的几何/可辨识性门槛；四组等双轴仍分速率、分实验处理。

## [2026-09-24] audit | S15 参考帧与零力场门槛

- 来源：S15 `000000.jpg.dat`、`000001.jpg.dat`、`000002.jpg.dat`、S15 DIC—力合并文件和照片—力索引。
- 结论：`000000.jpg` 参考 DAT 场约 100491 点且 u/v/应变接近零；`000001.jpg` 同步 X/Y 力为 0，但 `std(Exx)=0.00570515`、`std(Eyy)=0.00564645`、`std(Exy)=0.0039352`；`000002.jpg` 力为 X=`17.18 N`、Y=`17.83 N`。这可能来自 DIC 噪声、起始运动或力/图像延迟，不能直接当真实材料响应。
- 更新：双轴首试候选评估和机器状态。
- 待处理：人工确认 S15 `000000→000001` 参考/零力/时间对应；确认前不把 `000001` 零力场直接用于参数识别。
- 图像诊断补充：中心裁剪 `000000→000001` 相位平移约 `0.005 px`、平均灰度变化约 `−7.86`；`000000→000002` 相位平移约 `0.014 px`、平均灰度变化约 `−3.40`。未见明显整体相机平移，优先排查照明/采集基线与力—图像延迟。
- GUI 核验限制：Virtual Fields Module 当前不是 S15，而是 S16 `3try`；MatchID 2D 窗口报 `000000.jpg: Not a TIFF or MDI file`，因此没有完成 S15 Results Viewer/参考帧人工核验；未保存、导出或运行参数。

## [2026-09-24] update | PA12 总目标计划校正单轴/双轴方法边界

- 来源：用户固定的 MatchID 自带 VFM/外围机器力合力规则；S19/S22 长条单轴参考图；S15 十字双轴参考图；S19 `X_0.2.vfm` 无 Boundary/Forces 审计。
- 更新：`Agents/PA12实验数据处理/处理记录/PA12总目标与阶段计划.md`。
- 结论：总计划不再写“自建 VFM”或把机器力—ROI 合力等价性列为待证明前提；改为 MatchID 自带 VFM、机器力直接作为 ROI 边界合力。同时明确单轴长条几何与双轴中心 ROI 分开定义，S19 单轴积分域/厚度/宽度/标距/外功仍是准入门槛。

## [2026-09-24] analysis | S19 全场应变可辨识性预审

- 来源：S19 `merged/*_DIC全场—力.csv`，共 126 帧、9144 点/帧。
- 方法：逐帧统计 `Exx/Eyy/Exy` 的有限点数、均值、空间标准差、分位数和范围；不计算虚功、不拟合参数。
- 结果：126/126 帧字段有限；全帧平均空间标准差为 `Exx=0.00318806`、`Eyy=0.00172527`、`Exy=0.00162140`。加载后存在空间离散，但初始帧也有明显离散，需区分 DIC 噪声与真实梯度。
- 结论：S19 可进入灵敏度矩阵/秩/条件数和帧子集稳定性分析，但当前不能直接声称 `Y/H` 可辨识；若秩或稳定性不足，只用于曲线与 `E` 验证。
- 更新：`Agents/PA12实验数据处理/处理记录/PA12_S19全场应变预审.md`、`PA12_S19全场应变预审.json`、`index.md`。

## [2026-09-24] measurement | S19 Job Polygon 图像尺寸

- 来源：S19 `000000.jpg`、`Job.m2inp` Polygon 控制点和 `0.084746 mm/pixel` 标定。
- 结果：参考图 `1120×1120 px`；Polygon 外接框 `136×777 px`，图像/Job 推定尺寸约 `11.525×65.848 mm`。
- 限制：该尺寸只描述 DIC Polygon 长条区域，不是单轴厚度、有效标距、材料截面或 VFM 积分域实测值；S19 参数识别仍锁定。

## [2026-09-24] ingest | PA12 单轴试样几何证据缺口

- 来源：S19/S20/S21/S22 参考图、Job.m2inp 的 Polygon、单轴 DIC 元数据、S19 帧—力索引，以及论文第 3.3–3.4 节。
- 更新：`Agents/PA12实验数据处理/处理记录/PA12单轴几何证据缺口.md`、`Agents/PA12实验数据处理/处理记录/PA12单轴VFM首试候选评估.md`、`index.md`。
- 结论：长条单轴试样的 Job Polygon 是长标距/相关区域，不是双轴中心约 28×28 mm ROI；现有资料没有 S19 专属单轴厚度、有效宽度、标距、VFM 积分域和边界外功定义证据。双轴几何工作值不能直接迁移到单轴 VFM。
- 待验证：取得单轴试样图纸/CAD/实测尺寸，确认 Polygon 用途、单轴 VFM 外功边界和参考帧—力时间对应后，才能解锁 S19 参数识别。

## [2026-09-24] verification | PA12 全量回归测试

- 来源：当前仓库 `tests/`。
- 验证命令：`python -m unittest discover -s tests -v`。
- 结果：`75/75` 通过，覆盖同步、DAT/MatchID 合并、应力—应变审计、VFM 边界、检查器更新和现有回归测试；未调用报告 writer。
- 限制：该结果证明代码测试通过，不等于 MatchID GUI 参数识别、虚功数值、边界合力物理等价性或最终报告人工复核已完成。

## [2026-09-24] verification | PA12 闭环状态帧数修复

- 来源：新增 S15 正式合并帧数回归测试；`tools/audit_matchid_dic.py`；S15 DIC—力状态。
- 修复：闭环状态生成器在 `MATCHID_VFM_INPUT_READY` 时使用正式合并状态的 `frame_count`，不再把被排除的 DAT 审计行计入有效帧。
- 验证：新增回归测试通过；`test_matchid_dic.py` 25/25 通过；全量测试 76/76 通过；`compileall` 通过。刷新后的闭环状态为 S15 284 帧/284 个可用 DIC 帧，S23/S24 保持已知阻断。

## [2026-09-24] verification | PA12 Python 编译检查

- 来源：当前 `tools/` 与 `tests/`。
- 验证命令：`python -m compileall -q tools tests`。
- 结果：通过；当前检查器及既有工具/测试无 Python 语法编译错误。
- 限制：未调用报告 writer，未验证 MatchID GUI 运行、虚功数值或最终 Markdown/CSV 产物一致性。

## [2026-09-24] update | PA12 VFM 路线图加入 Linear 符号核验门槛

- 来源：已核对的优化论文原页式 (2.19) 与材料参数页、Abaqus 2025 官方等向塑性说明、当前可查六份几何扫描 `.inp`。
- 更新：`wiki/PA12单轴到双轴弹塑性VFM总目标与阶段路线图.md`、`index.md`。
- 结论：路线图现明确记载论文 `σ_y=σ_y0−H ε̄p`、`H=+180 MPa`、`σ_y0=21 MPa` 的符号冲突、字面软化含义及缺少 `*Plastic` 输入卡的证据限制，并将核对原始卡/作者资料与 MatchID H 定义设为实现或解释 Linear H 前置条件；未修改公式或工作参数。
- 下一步：取得原始 Abaqus 塑性材料卡或作者确认，核实 MatchID 当前模型定义；在此之前不将论文工作参数作为识别值或参数标签。

## [2026-09-24] update | PA12 S16 GUI 中间候选交接状态

- 来源：S16 `3try`/`4try_step3` 试算记录及当前 GUI 截图 `matchid_dialog.png`。
- 更新：`Agents/PA12实验数据处理/处理记录/PA12实验总体方法与防跑偏协议.md`、`Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md`、`Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json`、`Agents/PA12实验数据处理/MatchID_VFM准备/PA12_VFM边界载荷说明.md`、`index.md`。
- 结论：S16 `3try` 仍因 X/Y 载荷与 DIC 时间不同步而排除，`4try_step3` 仍因 Forces count=`0` 而排除。第 16 轮界面显示 `Y=63.93 MPa`、`H=41.55 MPa`、残差栏=`1214`、迭代=`16`、进度约 `70%`；`E`、`ν` 未显示，残差定义/单位未知。上述仅为 GUI 中间候选，不是最终识别结果。
- 待验证：修正/确认 S16 的照片—力序列和 Forces 输入后，再进行内外虚功、残差、参数边界与稳定性检查；不把当前候选值迁移到其他实验。

## [2026-09-24] evidence | PA12 双轴几何尺寸证据补充

- 来源：`D:\C盘迁移\Desktop\yuan\PA12_biaxial_project\04_geometry\drawings\moxing\moxing.pdf`、`简易版.pdf`；MinerU 定位 `doc:7535ee9/tier:standard/page:1` 至 `page:4`、`doc:953d05c/tier:standard/page:1`。
- 更新：`Agents/PA12实验数据处理/处理记录/PA12实验总体方法与防跑偏协议.md`、`Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md`、`Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json`、`Agents/PA12实验数据处理/MatchID_VFM准备/PA12_VFM边界载荷说明.md`、`index.md`。
- 结论：双轴十字试样模型采用总厚 `3.00 mm`（图纸标为比例/截面推定值），中心减薄厚度为 `1.00 mm`，减薄区外边界约 `30×30 mm`，中心平坦测量区约 `28×28 mm`；DAT/照片 ROI 约 `27.64×28.08 mm`。当前 S15 准备记录约 `28.78×28.78 mm`，两种尺寸口径需在 MatchID 中核对。
- 限制：该图纸是双轴十字试样证据，不能补足 S19/S20/S21/S22 单轴长条的厚度、有效宽度、标距或边界外功定义。

## [2026-09-24] verification | PA12 双轴几何证据定位

- 来源：MinerU 4.0.5 对 `moxing.pdf` 和 `简易版.pdf` 的本地缓存解析。
- 验证：`doc:7535ee9/tier:standard/page:4` 可读取厚度证据；`doc:953d05c/tier:standard/page:1` 可读取双轴平面尺寸证据；交接状态 JSON 可解析。
- 结果：面内尺寸/中心厚度/总厚推定值的证据等级已在协议、交接状态和边界说明中分开记录；未修改原始 PDF、STEP、JPG、DAT 或代码。

## [2026-09-23] audit | PA12 优化论文线性塑性公式符号

- 来源：学位论文第 2.3.2 节式 (2.19) 及材料参数页；Abaqus 2025 官方 [Classical Metal Plasticity 文档](https://docs.software.vt.edu/abaqusv2025/English/SIMACAEMATRefMap/simamat-c-metalplastic.htm)；可查的 PA12 几何扫描 `.inp` 文件。
- 更新：`Agents/PA12实验数据处理/处理记录/PA12实验总体方法与防跑偏协议.md`、`Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md`、`Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json`、`index.md`。
- 结论：论文式 (2.19) 为 `σ_y=σ_y0−H ε̄p`，参数页列 `H=+180 MPa`、`σ_y0=21 MPa`；按字面是软化斜率，外推至等效塑性应变约 0.1167 时屈服应力为零。Abaqus 允许等向塑性屈服应力表随塑性应变增加或降低，故需核实是有意软化还是公式/称谓错误。当前可查的六份 PA12 几何扫描 `.inp` 均只有 provisional Elastic 卡，无 `*Plastic` 数据可证实论文实际求解卡。
- 待验证：从作者或原始 Abaqus 材料卡核实式 (2.19) 负号和参数符号；从 MatchID 当前本构模型定义核实 GUI `H` 含义。此前不要将论文工作参数作为实验识别值或代理模型标签。

## [2026-09-24] analysis | S15 Job ROI 与 DAT 有效点范围口径

- 来源：S15 `Job.m2inp` 的 `<Shape>`、`<Conversion>`；REV B 双轴图纸的 DAT/照片尺寸证据。
- 结果：S15 Job 矩形为 `329×329 px`，按 `0.087464 mm/pixel` 换算为 `28.775656×28.775656 mm`，与当前约 `28.78×28.78 mm` 的 MatchID ROI 一致；`27.64×28.08 mm` 是 DAT 有效点外接范围。两者是不同统计对象，不构成 ROI 尺寸冲突。
- 待验证：仍需在 MatchID 中人工核对实际 ROI 边界坐标、中心减薄区叠合和参考帧；该结论只适用于 S15 双轴 ROI，不解锁单轴 VFM。

## [2026-09-24] audit | PA12 论文单轴路径与当前长条试样范围

- 来源：项目论文 `3D打印尼龙材料的双轴拉伸测试方法与力学性能(1).pdf`；MinerU 定位 `doc:b39265e/tier:standard/page:28`、`page:31`、`page:37`、`page:38`；当前 S19–S22 参考图、Job 和配置。
- 结论：论文第 3.3 节包含单轴与等双轴加载，第 4.6 节共同使用单轴/等双轴屈服点，但论文没有给出当前 S19–S22 长条单轴试样的独立几何、积分域或外功边界。因此论文“单轴”暂只能作为加载路径，不能与 S19 长条试样静默合并。
- 结论：论文列出的速率为 `0.1/1/10 mm/s`，当前真实数据标签为 `0.2/2/20 mm/s`；保留两套来源标签，不重命名、不混合拟合。论文第 3.1 节确认四个力传感器位于四个加载方向的夹具与驱动单元之间，但这不替代当前机器力—MatchID ROI 边界合力规则。
- 待验证：取得实验记录或原始采集表，确认论文单轴路径对应的具体试样/文件；在单轴几何、外功边界和路径对应关系确认前，S19 阶段 1 参数识别保持锁定。

## [2026-09-24] verification | PA12 速率标签来源口径

- 来源：`configs/pa12_rotated_batch.json` 各 S15–S24 的 `loading_speed_source`、S19 处理报告的照片/Pos 位移字段，以及项目论文第 3.3 节（MinerU：`doc:b39265e/tier:standard/page:31`）。
- 结果：当前数据内部的 `0.1/1/10`（单个执行通道）与 `0.2/2/20`（两侧相对速度）关系已有配置和位移证据支持；两套标签保留，不重命名、不混合拟合。
- 待验证：论文中的“加载速率”术语是否指单个执行通道速度或两侧相对速度；这不影响当前标签的保存，但在确认前不解锁 S19 阶段 1 参数识别。

## [2026-09-24] audit | S15 ROI 与名义平坦区尺寸筛查

- 来源：S15 `Job.m2inp` 的 Shape/Conversion、S15 `000000.jpg`、REV B 图纸 `doc:7535ee9/tier:standard/page:3`。
- 结果：若 Job ROI 与试样名义中心同心，Job ROI 为 `28.775656×28.775656 mm`；相对名义 `30×30 mm` 减薄区外边界每侧余 `0.612172 mm`，但相对名义 `28×28 mm` 平坦测量区每侧超出 `0.387828 mm`。
- 结论：当前只能判定“同心条件下位于外边界内、相对平坦区存在潜在重叠”；二维参考照片不能证明厚度均匀性，中心偏移和真实厚度边界仍未知，MatchID ROI containment 未通过人工核验，不启动参数识别。

## [2026-09-24] lint | PA12 VFM 状态语义冲突

- 发现：历史 `PA12数据合理性审计结果.json` 的实验级 `formal_vfm_ready:true` 和 `PA12批量处理报告.md` 的“正式 VFM 已完成”，与实际 S15 无 `.vfm`、当前闭环 `formal_matchid_vfm_ready=false` 不一致。
- 判断：这些旧字段表示同步力值/输出契约通过，不表示 MatchID `.vfm`、虚功或参数识别通过。
- 修改：在总体协议、GPT 交接状态/文档和 `index.md` 中登记语义边界；保留历史生成文件不改写。
- 下一步：后续人工复核和最终发布只使用 MatchID 闭环状态、实际 `.vfm` 文件审计及 GUI 虚功证据。

## [2026-09-24] audit | S15 Job 控制点与厚度边界区分

- 来源：S15 `Job.m2inp` 的 `<Shape>`、初始子集和 `<Extensometer>` 记录。
- 结果：ROI 中心 `(559.5,577.5) px`；初始子集 `(531,591) px`；引伸计标记 `(575,483)`、`(573,711) px`。
- 结论：Job 文件没有显式厚度过渡边界坐标；这些控制点不能直接证明实体中心或 1 mm 厚度边界，因此 ROI containment 仍需人工/几何证据核验。

## [2026-09-24] audit | S15 MatchID VFM 工程文件存在性

- 来源：S15 原始实验目录文件清单。
- 结果：目录中存在 `Job.m2inp`、`S15_XY_0.2.mti` 和 JPG/DAT，未发现 `.vfm` 文件；S16 目录另有完整 `.vfm` 和多份试算文件。
- 结论：S15 当前仅完成 DIC Job/同步力输入准备，尚未建立 MatchID VFM 工程；既有 `MATCHID_VFM_INPUT_READY` 不等于 `.vfm` 工程已建立。ROI/参考帧门槛通过后，下一步才是建立 S15 VFM 工程并核对 Boundary/Forces。

## [2026-09-24] audit | S15 mti DIC 元数据与合并帧对应

- 来源：S15 `S15_XY_0.2.mti` 的只读文本审计、S15 DIC—力状态和 Job 文件。
- 结果：`.mti` 记录参考图 `000000.jpg`、`000000–000284.jpg` 共 285 个有效 DIC 条目（含参考帧），`000285.jpg=False`，标定 `0.087464 mm/pixel`，ROI 起点 `(395,413)`、尺寸 `329×329 px`；对应当前 284 个非参考有效合并帧和排除的视觉断裂帧。
- 结论：S15 的 DIC 工程层帧/ROI 元数据与当前合并状态一致；缺口仅是尚未建立 `.vfm` Boundary/Forces 工程，不能据此宣称虚功或参数识别通过。

## [2026-09-24] analysis | S15 原始四通道力与平均 CSV 对应

- 来源：S15 原始 `Press` 表、S15 照片时间轴、现有 X/Y 单列力 CSV；只读重采样。
- 结果：原始表含 `X1_Press/X2_Press/Y1_Press/Y2_Press` 四通道、36,244 个 1 ms 采样点。按配置起始/终止力索引和 50 点基线，在 284 个有效照片时刻重采样后，四通道平均与现有 X/Y CSV 最大差分别为 `4.93×10⁻⁷ N`、`4.79×10⁻⁷ N`。
- 结论：S15 四边 Boundary Forces 的数据层已具备；现有 CSV 只是平均 X/Y 表示，尚未创建 `.vfm` 工程，也未进行虚功或参数识别。

## [2026-09-24] analysis | S15 VFM Boundary Forces 帧契约

- 来源：S15 `.mti` 帧条目、S16 完整 `.vfm` 的参考帧/Forces 结构、S15 原始四通道 Press 重采样结果。
- 结论：S15 每个 Boundary/Forces 序列应包含 `285` 个值：`000000` 参考帧零值、`000001–000284` 四通道同步力；`000285` 排除。四边映射为 Boundary0=X2、Boundary1=Y2、Boundary2=Y1、Boundary3=X1。
- 限制：这只是可追溯输入蓝图，尚未创建 `.vfm` 文件，未验证 MatchID GUI 导入、内外虚功或参数识别。

## [2026-09-24] artifact | S15 四边力蓝图 CSV

- 来源：S15 原始 Press 四通道、现有同步时间轴和 VFM Boundary 映射。
- 输出：`Agents/PA12实验数据处理/MatchID_VFM准备/S15_XY_0.2/S15_XY_0.2_BoundaryForces_blueprint.csv`，285 行（参考帧 + 284 个非参考帧），四个 Boundary 列。
- 验证：帧索引 0–284 连续、无 `000285`；跳过参考帧后，Boundary 平均值与既有 X/Y CSV 最大差约 `5.0×10⁻⁷ N`。
- 限制：这是建立 MatchID `.vfm` 的输入蓝图，不是 `.vfm` 工程，不代表 GUI 导入、虚功或参数识别已通过。

## [2026-09-24] artifact | S15 VFM 输入蓝图 JSON

- 来源：S15 `.mti`、DIC—力合并状态/索引、原始 Press 四通道、S15 四边力蓝图 CSV、REV B 几何证据。
- 输出：`Agents/PA12实验数据处理/MatchID_VFM准备/S15_XY_0.2/S15_XY_0.2_VFM输入蓝图.json`。
- 结论：清单集中记录 285 条含参考帧的 Boundary/Forces 契约、284 个 DIC 非参考帧、字段单位、ROI、厚度和门槛；当前 ROI/参考帧人工复核未通过，`.vfm` 尚未创建，参数识别保持锁定。

## [2026-09-24] audit | S16 完整 VFM Forces 与当前同步力数值

- 来源：S16 完整 `S16_XY_0.2_258.vfm`、S16 原始 Press 表、当前 S16 处理报告的真实起止时间和 257 个有效照片帧。
- 结果：四组 Boundary 的 MAE 约为 `24.65–29.80 N`，末帧差约 `1.43–1.49 kN`；`.vfm` 末帧仍约 `1.60 kN`，当前同步序列末帧约 `0.12–0.18 kN`。
- 结论：该完整 `.vfm` 只能作为格式/Boundary 顺序证据，不能作为当前同步力真值或 S15 Forces 模板；S15 必须使用原始 Press 四通道蓝图重新建立 Forces。

## [2026-09-24] analysis | S16 完整 VFM 终点敏感性

- 来源：同一 S16 完整 `.vfm` 与原始 Press，只改变当前照片时间轴终点假设。
- 结果：掉载终点 `25.834 s` 映射时末帧差为 kN 级；峰值终点 `25.751 s` 映射时各 Boundary 最大差约 `38–67 N`，但仍未完全吻合。
- 结论：旧 `.vfm` 可能采用峰值截断或另一时间映射；该结果是诊断线索，不是同步通过证据，S15 仍使用自己的四通道蓝图。

## [2026-09-24] analysis | S16 共同时间映射拟合限制

- 来源：S16 完整 `.vfm` 四组 Forces、当前原始 Press 四通道；纯 NumPy 网格搜索。
- 结果：四组共用起止时间的最佳拟合约 `0.2044–25.7870 s`，仍有 `16.7–21.5 N` MAE、`39–58 N` 最大偏差。
- 结论：旧 `.vfm` 与当前 Press 的差异不能仅由共同时间起止解释；保留为格式/方向证据，不做进一步拟合校准，也不迁移到 S15。

## [2026-09-25] audit | PA12 名义 STEP 几何证据范围

- 来源：`D:\C盘迁移\Desktop\yuan\PA12_biaxial_project\04_geometry\drawings\moxing\05_a1p1.00mm.step`、同目录 `README_厚度模型顺序.txt`；STEP 只读解析得到 1483 个三维笛卡尔点。
- 结果：STEP 单位为 mm，点坐标包络为 `x/y=-75.2…75.2 mm、z=-5…5 mm`；中心局部平面角点为 `x/y=±14.005 mm、z=±0.5 mm`，对应约 `28.01×28.01 mm` 中心平面和 `1.0 mm` 局部厚度。README 记录总厚度 `3.0 mm`。
- 结论：全局 CAD 坐标包络、中心局部模型和 README 总厚度属于不同证据范围；不能把 `z=-5…5 mm` 当作实际试样整体厚度，也不能用名义 CAD 坐标替代实测厚度。当前 VFM 仍按中心 `1 mm`、外围 `3 mm`，S15 真实厚度过渡边界继续等待独立核验。
- 更新：`PA12实验总体方法与防跑偏协议.md`、`PA12_GPT交接状态.json`、`PA12_GPT交接文档.md`、`PA12_VFM边界载荷说明.md`、`index.md`。
- 下一步：在 MatchID 人工核对 S15 ROI 与真实厚度边界前，不建立参数识别结论；不得因 STEP 全局坐标范围自动改写 VFM 厚度。

## [2026-09-25] audit | PA12 几何验证元数据来源映射

- 来源：两份 `verification.json`、`00_README/known_information.md`、对应目录中的 STEP 文件清单。
- 结果：两份 `verification.json` 内容一致，记录中心厚度 `1.0 mm`、总厚度 `3.0 mm`、过渡半径约 `0.995 mm`、包络 `150.4×150.4×3.0 mm`；但其引用的 `05_PA12_cruciform_center_thickness_a1p0mm.step` 在两目录均不存在，实际找到的是 `05_a1p1.00mm.step`。`known_information.md` 还写明总厚度暂按 3 mm 建模，需实验实测确认。
- 结论：`verification.json` 只能支持名义设计意图，不能直接验证当前 STEP 或实物厚度；来源映射和实际厚度仍是 MatchID ROI containment 的前置核验项。
- 补充检索：在 `D:\C盘迁移\Desktop\yuan` 全原始资料根目录内未找到其引用的长文件名 STEP 或同族长文件名模型；原始资料未修改。

## [2026-09-25] analysis | PA12 短文件名 STEP 实体拓扑复核

- 来源：`D:\C盘迁移\Desktop\yuan\PA12_biaxial_project\04_geometry\drawings\moxing\05_a1p1.00mm.step`；只读解析 STEP 拓扑实体和 `VERTEX_POINT`，不修改原始文件。
- 结果：文件包含 1 个 `MANIFOLD_SOLID_BREP`、1 个 `CLOSED_SHELL`、280 个实体顶点；顶点包络为 `150.4×150.4×3.0 mm`，坐标范围 `x/y=±75.2 mm、z=±1.5 mm`。中心顶点位于 `z=±0.5 mm`、`x/y=±14.005 mm`，中心名义平面约 `28.01×28.01 mm`、厚度 `1.0 mm`；STEP 中存在半径 `0.995 mm` 的圆柱面记录。
- 结论：此前所有 `CARTESIAN_POINT` 得到的 `z=±5 mm` 是几何控制点范围，不是实体厚度。当前短文件名 STEP 的实体拓扑与 `verification.json` 的名义包络、中心厚度和过渡半径相互支持；长文件名映射仍是血缘问题，但不再构成名义几何阻塞。
- 待验证：实际试样是否按该 CAD 制造、S15 ROI 在照片坐标中是否完全位于实际 1 mm 区域；相对直接 STEP 中心平面，S15 `28.775656 mm` ROI 若同心每侧超出约 `0.382828 mm`，仍需 MatchID/实物边界核对。
- 更新：`PA12实验总体方法与防跑偏协议.md`、`PA12_GPT交接状态.json`、`PA12_GPT交接文档.md`、`PA12_VFM边界载荷说明.md`、`index.md`。
- 下一步：先核对长文件名模型是否为当前短文件名模型的重命名/导出版本，再结合实测截面或 MatchID 几何确认 ROI 是否完全处于 1 mm 区域。

## [2026-09-25] audit | PA12 S16 GUI 候选快照一致性

- 来源：用户要求保留的 S16 第 16 轮 GUI 记录；只读检查 `configs/pa12_vfm_boundary.json` 及其当前 Markdown/CSV 报告。
- 发现：交接状态记录第 16 轮 `Y=63.93 MPa`、`H=41.55 MPa`、界面值 `1214`；受保护并行配置/报告另记录第 28 轮 `Y=61.94 MPa`、`H=139.60 MPa`、界面值 `1655`。两者均明确为 GUI 中间候选，均未通过同步、虚功、残差定义和稳定性门槛。
- 处理：在交接状态、总体协议、GPT 交接文档、边界说明和 `index.md` 中登记两份快照的关系；保留第 16 轮作为用户指定的交接主记录，不修改并行维护的配置、检查器、测试或报告。
- 下一步：先统一实际采用的 S16 Forces/照片时间轴，再对唯一选定的输入重新导出内外虚功、残差和参数边界；在此之前不得接受或迁移任一候选参数。

## [2026-09-25] audit | PA12 单轴几何证据扩展检索

- 来源：论文 MinerU 解析稿、PA12 原始资料文件清单、S19 `Job.m2inp` 和参考照片 `000000.jpg`。
- 结果：论文解析稿的几何/实验内容仍只给十字形双轴试样；S19 Job 仅提供 5 控制点 Polygon，范围 `136×777 px`，按 `0.084746 mm/pixel` 约为 `11.525456×65.847642 mm`。
- 结论：该 Polygon 只能作为二维 DIC/Job 分析区域的尺寸证据，不能补足单轴实物厚度、有效宽度、标距、VFM 积分域或外部虚功边界；扩大检索后单轴 VFM 门槛仍未解锁。
- 下一步：取得单轴试样图纸/实测截面/实验记录，或在 MatchID 中确认单轴积分域和边界外功定义；此前不启动 S19 阶段 1 参数识别。

## [2026-09-25] audit | PA12 MatchID GUI 入口复核

- 来源：`D:\DIC\MATCH_DIC\2019\MatchID 2D\MatchID.exe` 及当前 Windows 桌面窗口状态。
- 结果：MatchID 可执行文件存在，窗口进程可以枚举；当前桌面状态捕获接口不可用，未取得新的可信 GUI 画面或控件状态。
- 结论：S15 ROI、参考帧、零力场和内外虚功仍未完成人工核验；没有保存、导出或运行参数识别，旧截图不作为新的 S15 证据。
- 下一步：在可获得稳定 MatchID 画面后，先完成 S15 输入门槛；在此之前保持 `formal_matchid_vfm_ready=false`。

## [2026-09-25] update | PA12 S16 当前 GUI 试算与边界说明口径

- 来源：S16 `3try`/`4try_step3` 试算记录、完整 `S16_XY_0.2_258.vfm` 格式审计及第 16 轮 GUI 截图。
- 更新：`Agents/PA12实验数据处理/MatchID_VFM准备/PA12_VFM边界载荷说明.md`、`index.md`；既有交接状态、总体协议和 GPT 交接文档保持一致。
- 结论：完整 `.vfm` 的“审计通过”仅表示 Boundary/Forces 格式、方向、帧数和数值符号通过；`3try` 仍因 X/Y 载荷不同步排除，`4try_step3` 因 `Forces count=0` 排除。第 16 轮 `Y=63.93 MPa`、`H=41.55 MPa`、残差栏 `1214` 仅为 GUI 中间候选，不是最终识别结果。
- 待验证：修正/确认 S16 照片—力时间序列和 Forces 输入后，再检查内外虚功、残差、参数边界和稳定性；此前不得接受或迁移这些候选参数。

## [2026-09-25] audit | S19 单轴 VFM 文件结构复核

- 来源：`D:\C盘迁移\Desktop\yuan\PA12_biaxial_project\03_DIC\vertical_all_45deg\PAPER\unixal\S19_X_0.2\X_0.2.vfm`；仓库现有 `tools/vfm_boundary.py::parse_matchid_vfm_metadata`，只读解析。
- 结果：原始目录确实存在 `X_0.2.vfm`，但解析未发现 `Boundary` 和 `Forces` 记录。
- 结论：此前“未发现 `.vfm` 文件”修正为“存在文件但不是完整边界输入”；S19 单轴 VFM 的边界输入、几何和外功门槛仍未解锁，不启动阶段 1 `E` 识别。
- 下一步：取得单轴厚度、有效宽度、标距、积分域和外功边界证据，并建立/确认包含 Boundary/Forces 的正式 MatchID 单轴工程。

## [2026-09-25] audit | S19–S22 单轴几何文本检索封口

- 来源：`D:\C盘迁移\Desktop\yuan\PA12_biaxial_project` 内排除 `PAPER/CHECK` 图像目录后的 65 个文本型说明、配置、清单和 MatchID 文本文件；只读关键词检索。
- 结果：仅发现项目级单轴/双轴目标描述和双轴十字试样厚度模型说明；未发现 S19/S20/S21/S22 的独立厚度、有效宽度、标距、VFM 积分域或外功边界。
- 结论：项目说明文件检索范围暂时封口，不再从双轴模型说明推测单轴几何；单轴门槛仍需实验记录、单轴图纸/实测截面或 MatchID 工程证据。
- 下一步：优先取得外部单轴几何/实验记录，并在此基础上建立包含 Boundary/Forces 的正式单轴 VFM 工程。

## [2026-09-25] update | PA12 自建 VFM 阶段 B 单轴 Polygon 复核

- 来源：S19–S22 的 Job Polygon、DIC 全场—力合并数据、`tools/run_pa12_self_vfm.py` 和 Polygon 积分实现。
- 更新：`Agents/PA12实验数据处理/VFM自建/汇总/PA12自建VFM阶段B单轴Polygon复核.md`、`Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json`、`Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md`、`index.md`。
- 结论：S19–S22 已使用真实 Job Polygon 接入自建 VFM，逐点积分不以外接矩形补足缺失场点；四组仍为 `REVIEW_REQUIRED`。S20 原始 E 为负值，未取绝对值或补默认值；S21 E 异常高，S19 的 Y/H 极端，S22 仍需大应变与局部化复核。
- 待验证：单轴实测厚度、有效宽度、标距、Polygon 的物理含义和外部虚功边界；面积比低于 0.95 的原因。上述候选值不得作为最终材料参数或代理模型标签。

## [2026-09-25] audit | PA12 自建 VFM 阶段 C 等双轴虚功与稳定性门槛

- 来源：S15–S18 自建 VFM 结果 JSON 的积分质量、阶段 1 质量和虚功拟合字段。
- 更新：`Agents/PA12实验数据处理/VFM自建/汇总/PA12自建VFM阶段C等双轴虚功与稳定性门槛.md`、`index.md`。
- 结论：S15–S18 的最低面积比均低于 `0.95`；S15 阶段 1 相对 RMSE `0.1121` 超过 `0.10`；S16/S18 可作为稳定性复核候选；S17 阶段 2 点数不足。当前没有一组可发布为正式材料参数。
- 待验证：S16/S18 的加载窗口和帧子集稳定性、跨实验一致性与留出验证；S15 的早期参考响应和面积覆盖问题。

## [2026-09-25] audit | S16/S18 帧子集稳定性初筛

- 来源：S16/S18 `参数收敛.csv`，取逐步扩展窗口的最后约四分之一记录。
- 结果：S16 的 Y 为 `36.76–39.50 MPa`、H 为 `156.40–279.10 MPa`；S18 的 Y 为 `38.83–43.77 MPa`、H 为 `632.27–1570.10 MPa`。阶段 2 拟合 RMSE 分别约为 `7.42–7.70 MPa` 和 `4.59–5.25 MPa`。
- 结论：Y 尚可作候选趋势，H 对加载窗口明显敏感；两组均未达到稳定材料参数发布条件。
- 下一步：固定可比加载窗口，补做独立留出帧验证和模型间比较；不把当前 H 迁移到其他速度或单轴数据。

## [2026-09-25] audit | S16/S18 固定四窗口初筛

- 更新：新增只读脚本 `tools/audit_pa12_self_vfm_stability.py`，未修改主 runner 或原始结果。
- 结果：将既有逐帧 CSV 分成四个不重叠窗口后，S16 的 Y/H 为 `(14.28,4940.98)`、`(33.95,977.24)`、`(52.60,32.49)`、`(65.39,-65.20) MPa`；S18 为窗口 1 塑性点不足，后续窗口 `(28.42,5415.81)`、`(52.21,253.69)`、`(78.49,-1012.34) MPa`。
- 结论：固定窗口下 Y/H 明显不稳定，当前不能宣称参数可辨识；后段窗口也不具备独立 E 识别条件。该结果是稳定性否决证据，不是新的材料参数。
- 限制：审计使用已有 CSV 中的塑性应变，仍需基于原始 DIC 场和严格留出规则完成最终验证。

## [2026-09-25] audit | S16/S18 本构模型描述性比较

- 来源：S16/S18 `模型对比.csv`。
- 结果：S16 的 Linear/Ludwik/Swift/Voce I/Voce II RMSE 为 `7.419/4.363/4.250/1.344/0.237 MPa`；S18 为 `5.248/3.578/4.723/0.795/0.813 MPa`。
- 结论：同组最低模型分别为 Voce II 和 Voce I，但跨实验不一致；这是描述性拟合，不足以选定最终本构模型。

## [2026-09-25] audit | S16/S18 诊断性留出

- 更新：新增只读脚本 `tools/audit_pa12_self_vfm_holdout.py`。
- 结果：前 75% 塑性点拟合 Linear、后 25% 留出评估，S16 的 Y/H=`37.28/249.49 MPa`、留出 RMSE=`17.01 MPa`；S18 的 Y/H=`40.58/1171.96 MPa`、留出 RMSE=`25.93 MPa`。
- 限制：等效塑性应变来自全窗口 E，故这是诊断性而非严格独立验证；不改变当前未通过稳定性门槛的结论。

## [2026-09-25] audit | S16/S18 严格训练段 E 与留出段评估

- 更新：新增 `tools/audit_pa12_self_vfm_strict_holdout.py`。
- 方法：前 75% 原始逐帧数据识别 E，并用训练 E 重新计算全部塑性应变；Y/H 只在训练段拟合，后 25% 仅评估。
- 结果：S16 训练 E/Y/H=`3405.14/36.76/279.10 MPa`，留出 RMSE=`19.05 MPa`；S18=`4606.81/39.04/1517.36 MPa`，留出 RMSE=`29.02 MPa`。
- 结论：严格留出仍显示较大误差和 H 的跨实验差异，正式参数与本构模型验证门槛未通过。

## [2026-09-25] audit | S16/S18 等双轴路径一致性

- 方法：对塑性段计算边界应力比 `σx/σy` 和平均应变比 `εx/εy` 的均值与标准差。
- 结果：S16 应力比 `1.044±0.014`、应变比 `1.048±0.008`；S18 应力比 `1.019±0.021`、应变比 `0.993±0.011`。
- 结论：两组总体接近等双轴，H 的大幅漂移不能简单归因于非等双轴路径；后续优先检查 ROI 有效面积、局部化、应变测量和约化本构假设。

## [2026-09-25] audit | S16/S18 面积覆盖随加载变化

- 结果：S16 每帧面积比均为 `0.892248`，S18 每帧均为 `0.891147`；首帧、末帧、最小值和最大值一致。
- 结论：面积门槛失败主要是固定的 DIC 有效场与理论 ROI 面积口径差异，不是后段局部化造成的新增丢点；仍不能解除 `0.95` 门槛。
- 下一步：核对 DIC 有效区域和 ROI 几何口径，取得证据后再决定是否定义新的有效积分域并重算。

## [2026-09-25] audit | S16/S18 DIC 有效点外接框与 Job ROI

- 结果：S16 有效点外接框约 `25.639×26.424 mm`、面积 `677.51 mm²`，Job ROI `759.32 mm²`；S18 约 `24.927×25.190 mm`、面积 `627.91 mm²`，Job ROI `704.61 mm²`。
- 结论：积分面积比恒定偏低主要来自 DIC 有效点区域小于 Job ROI，而非逐帧三角剖分随机丢失；在没有 DIC 有效域/ROI 几何证据前，不重定义积分域。

## [2026-09-25] audit | S16 DIC subset 参数与有效域内缩假设

- 来源：S16 `Job.m2inp` 的 Polygon、`Subset$size=15` 和 `Step$size=3` 设置。
- 结论：subset 中心只能落在可完成相关的内缩区域，能够解释有效点外接框小于 Job ROI；但 Job 文件未证明该内缩框就是物理 VFM 边界。
- 状态：保留为解释性工作假设，不据此解除面积门槛或重写 ROI。

## [2026-09-25] audit | S16 subset 网格数量与有效域跨度闭合

- 结果：`.mti` ROI 为 `312×320 px`，subset=`15 px`、step=`3 px`；有效点数 `10098=99×102`，对应有效跨度约 `294×303 px`，与 DIC 有效坐标外接框一致。
- 结论：面积比恒定偏低的直接数据处理原因基本闭合为 subset 中心网格内缩，而不是随机三角形缺失；但“相关域边界=物理 VFM 边界”仍未被证明。

## [2026-09-25] decision-gate | PA12 VFM 物理积分域口径

- 记录：区分 Job ROI 完整 Polygon 与 DIC subset 中心内缩域，不自动把二者合并。
- 当前选择：主结果继续采用 Job ROI，面积比低于 `0.95` 时保持 `REVIEW_REQUIRED`。
- 待人工确认：实际试样中心区域/厚度边界、DIC ROI 定义或项目明确的 VFM 有效积分域规则；确认前不得用内缩域重算并发布参数。

## [2026-09-25] handoff | PA12 阶段 C 物理积分域人工复核清单

- 更新：`Agents/PA12实验数据处理/VFM自建/汇总/PA12自建VFM阶段C人工复核清单.md`、`index.md`。
- 内容：将待确认事项收敛为物理 ROI、DIC 内缩有效域定义、外功边界对应关系三项；列出三种确认后的处理分支。

## [2026-09-26] experiment | PA12 自建 VFM DIC 有效域敏感性分析

- 来源：用户确认“继续使用完整 Job ROI；采用 DIC subset 内缩有效域做独立敏感性分析”；既有 S15–S18 DIC—力合并 CSV、Job/mti 参数和主 VFM runner。
- 更新：`tools/run_pa12_self_vfm_effective_domain.py`、`tools/run_pa12_self_vfm.py`、`tests/test_pa12_self_vfm.py`、`Agents/PA12实验数据处理/VFM自建/敏感性分析/`、阶段 C 文档、`index.md`。
- 结果：S15 E/Y/H=`3396.59/35.42/162.86 MPa`；S16=`3215.68/44.97/139.37 MPa`；S17 E=`4747.28 MPa`、阶段 2 点数不足；S18=`4349.01/53.43/331.91 MPa`。所有结果标记 `SELF_VFM_SENSITIVITY_ONLY`。
- 结论：完整 Job ROI 主结果和 DIC 有效域敏感性结果已隔离；积分域口径确实改变参数，敏感性结果不替代主结果，也不直接作为最终材料参数。
- 验证：敏感性批处理生成四组独立结果目录；待完成全量测试与输出字段审计。

## [2026-09-25] test | PA12 固定窗口稳定性审计回归

- 更新：`tests/test_pa12_self_vfm_stability.py`。
- 验证：固定窗口线性硬化斜率符号测试通过；自建 VFM 相关测试 `21/21 passed`。
- 结论：稳定性审计脚本已纳入回归测试，不能因后续公式改动静默反转 H 的符号。

## [2026-09-25] analysis | PA12 自建 VFM 阶段输出

- 来源：已完成同步的 DIC 全场—Press 合并数据、`configs/pa12_self_vfm.json`、旋转方向标定和中心/外围厚度证据。
- 更新：`Agents/PA12实验数据处理/VFM自建/`、`tools/pa12_self_vfm.py`、`tools/run_pa12_self_vfm.py`。
- 结论：S16_XY_0.2 与 S18_XY_2 达到当前自建阶段候选门槛；S15_XY_0.2 需复核；S17_XY_20 帧数不足以完成阶段 2；S19–S24 因单轴几何/外功边界未确认或记录不完整而跳过。输出包含逐帧内外虚功、应力空间、E/Y/H、参数稳定性和 Linear/Ludwik/Swift/通用 Voce I/II 对比。
- 限制：这些是自建 VFM 候选结果，不替代 MatchID 正式工程或最终材料结论；单轴组和 S23/S24 不得静默补值。
## [2026-09-21] config | 真实 Obsidian vault 同步

- 来源：用户截图与 Obsidian 本地配置
- 更新：`.obsidian/`, `raw/`, `wiki/`, `schema/`, `index.md`, `log.md`
- 结论：已将框架配置到 Obsidian 当前打开的 `second brain` vault，并保留 Obsidian 自动生成的工作区状态。
- 待验证：Obsidian 重新加载后能在文件浏览器、书签和模板中看到对应入口。

## [2026-09-21] policy | 论文写作框架

- 来源：用户指令
- 更新：`AGENTS/论文写作框架.md`, `AGENTS.md`, `index.md`, `log.md`
- 结论：已将论文润色、Discussion 写作和论文结构化总结要求写入长期协议。
- 待验证：后续论文写作任务中按该框架先澄清需求，再输出方案或正文。

## [2026-09-21] policy | Introduction 与 Discussion 结构

- 来源：用户指令
- 更新：`AGENTS/论文写作框架.md`, `log.md`
- 结论：已补充 Introduction 倒三角结构和 Discussion 正三角结构，用于组织论文宏观论证。
- 待验证：后续论文引言与讨论写作中按该结构检查段落功能。

## [2026-09-22] config | MinerU 与 Semantic Scholar

- 来源：用户提供的 API 配置
- 更新：`AGENTS/科研工具环境.md`, `AGENTS.md`, `index.md`, `log.md`
- 结论：MinerU `4.0.5` 远程解析和 Semantic Scholar API 已配置并通过只读接口验证；密钥仅保存在用户级环境变量和本机工具配置中。
- 待验证：重启 Codex 后确认新进程自动读取用户级环境变量。

## [2026-09-22] schema | Skill 分类与调用协议

- 来源：用户要求统一分类 skill 并规定调用顺序
- 更新：`AGENTS/技能分类与调用协议.md`, `AGENTS.md`, `index.md`
- 结论：已按流程控制、资料解析、文献检索、论文写作、数据分析、视觉材料和环境维护分类，并为常见科研任务指定主 skill 与辅助 skill。
- 待验证：后续任务按路由协议调用，并在交付前执行对应验证。

## [2026-09-22] config | 科研工具环境补齐

- 来源：环境检测结果与用户要求
- 更新：用户级 MinerU 后端变量、本机 Python 依赖、`AGENTS/科研工具环境.md`
- 结论：CUDA Torch、MinerU Torch/llama-cpp、本地 managed standard 服务和远程 MinerU 均已通过验证；已有实验图片已成功完成本地 standard 解析。
- 待验证：重启 Codex 后确认当前新进程继承后端变量；Semantic Scholar 等待服务端限流解除后复测。

## [2026-09-22] experiment | MinerU 新文件可用性验证

- 来源：`AGENTS/PA12实验数据处理/VFM专用力值/X方向/X-0.1-258.csv`
- 更新：MinerU 本地文档库解析缓存
- 结论：此前未解析过的 CSV 文件首次解析完成，`cache_hit=false`、`status=done`、`tier=flash`，返回非空 Markdown 表格内容。
- 待验证：后续如需继续读取，使用 `doc:8152268/tier:flash/page:1/block:1` 及其 continuation locator。

## [2026-09-22] ingest | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

- 来源：`raw/papers/lewis2020-rag-knowledge-intensive-nlp-v4.pdf`、`raw/papers/lewis2020-rag-knowledge-intensive-nlp-v4.md`
- 更新：`wiki/literature/rag-2020-knowledge-intensive-nlp.md`、`wiki/README.md`、`index.md`
- 核心问题：检索器与生成器能否通过端到端训练组合参数化记忆和可更新的非参数化记忆，并在多类知识密集型任务上获得收益？
- 关键结论：RAG 在文中报告的开放域问答、生成和事实核验任务上取得竞争力；消融、人工评价和索引热替换实验共同支持检索增强、事实性和知识更新的论证。
- 证据：本地 MinerU 4.0.5 `standard` 解析完成，文档标识为 `doc:23e3249`，覆盖 19 页；关键证据位于第 2、6–8、17、19 页及对应 block locator。
- 冲突：Semantic Scholar 本次元数据请求返回 HTTP 429；因此元数据以 arXiv 官方页面核对，未将限流误判为解析故障。
- 待验证：本页尚未独立复现实验数值；后续若要验证模型效果，应固定数据切分、检索数量、索引版本、解码策略和评估指标。

## [2026-09-22] review | research-agent-skills 外部科研流水线评估

- 来源：https://github.com/Sun-tech2020/research-agent-skills
- 更新：`AGENTS/技能分类与调用协议.md`
- 结论：该仓库是面向经济学、计量经济学和量化金融的 11 个 `*.skill` JSON 模块集合，不包含 Codex 所需的 `SKILL.md`，因此未直接安装或注册。
- 可复用：文献捕获、原文客观解构、分阶段人工确认、文献综述与结果合成的流程思想。
- 不可直接复用：经济学变量、市场/政策语义、计量模型预设和宏观数据字典。
- 力学适配边界：后续必须改写为载荷、位移、应力、应变、材料参数、边界条件、单位、误差、收敛与独立验证；在改写完成前继续使用本库现有 `mineru`、`NovaForge` 和数据分析路由。

## [2026-09-22] ingest | PA12 外部数据源与双轴试样几何登记

- 来源：`D:\C盘迁移\Desktop\yuan\data`
- 更新：`raw/datasets/PA12数据源登记.md`、`AGENTS/PA12双轴试样仿真与实验全流程.md`、`wiki/methods/PA12双轴中心区均匀性筛选.md`、`AGENTS/PA12双轴试样仿真/`
- 结论：已核对 XY/XZ 实验数据、MatchID/VFM 文件和五个中心厚度 STEP；中心厚度为 3.0/2.5/2.0/1.5/1.0 mm，总厚度均为 3.0 mm。
- 待验证：材料参数、力值单位、实际加载比、XZ 数据的 Z 向标定含义，以及备用形状和长宽尺寸来源。

## [2026-09-22] experiment | Abaqus 与数据接入可执行性检查

- 来源：Abaqus 2025、MinerU 4.0.5、本地数据目录和 `verification.json`
- 更新：`AGENTS/PA12双轴试样仿真/pa12_biaxial_scan.py`、`postprocess_uniformity.py`、`run_scan.ps1`
- 结论：Abaqus 2025 可执行；MinerU 本地 `standard` 服务健康；五个 STEP 均登记为单一实体且包围盒为 150.4 × 150.4 × 3.0 mm。已建立导入、网格、四臂耦合、位移加载和中心区 ODB 指标提取入口。
- 待验证：本次先验证输入文件生成链路；脚本中的 PA12 材料卡明确为流程临时值，不能作为正式科学结论，正式提交需替换为实验标定参数。

## [2026-09-22] experiment | PA12 Abaqus 前处理、求解与 ODB 后处理验证

- 来源：五个真实 STEP、`pa12_biaxial_scan.py`、`postprocess_uniformity.py`、Abaqus 2025。
- 更新：`AGENTS/PA12双轴试样仿真/runs/`、`AGENTS/PA12双轴试样仿真/验证/2026-09-22_流程验证报告.md`、`index.md`、`AGENTS/PA12双轴试样仿真与实验全流程.md`。
- 结论：五个 STEP 均生成 `.inp/.cae`；`a=3.0 mm` 粗网格临时材料值作业成功完成，ODB 中心区后处理输出 `primary_score=0.0353768`。
- 限制：材料卡为流程临时值，不能用于论文或正式设计排序；正式任务仍需材料标定、网格收敛、五模型求解和实验留出验证。
## [2026-09-25] experiment | PA12 自建 VFM 阶段 A 逐点积分复核

- 来源：`Agents/PA12实验数据处理/MatchID_VFM准备/S15_XY_0.2/merged/`、`configs/pa12_rotated_batch.json`、`configs/pa12_self_vfm.json`
- 更新：`tools/pa12_self_vfm.py`、`tools/run_pa12_self_vfm.py`、`tests/test_pa12_self_vfm.py`、`Agents/PA12实验数据处理/VFM自建/README.md`、`Agents/PA12实验数据处理/VFM自建/汇总/PA12自建VFM阶段A记录.md`、`index.md`
- 结论：自建 VFM 已加入 ROI 逐点数值积分；规则网格使用二维梯形求积，非结构化帧使用三角形回退，矩形均值法保留为基线。S15 完整处理 284 帧，面积比约 `0.895–0.923`，低于 `0.95` 门槛，状态为 `SELF_VFM_REVIEW_REQUIRED`。`E=3536.35 MPa`、`Y=34.06 MPa`、`H=154.56 MPa` 仅为候选值。
- 验证：自建 VFM 目标测试 `14 passed`；核心模块编译通过；S15 逐帧 CSV、JSON、参数收敛和图表已写出。
- 待验证：S15 ROI 与实体 1 mm 区域的空间叠合；S16/S17/S18 分组重算；单轴几何/外功门槛；参数稳定性和留出验证。

## [2026-09-25] audit | PA12 自建 VFM 阶段 A 四组批处理复核

- 来源：`configs/pa12_self_vfm.json`、S15/S16/S17/S18 自建 VFM 结果 JSON/CSV。
- 更新：`Agents/PA12实验数据处理/VFM自建/汇总/PA12自建VFM阶段A记录.md`。
- 结论：四组等双轴批处理分别写出 284/257/12/126 帧；正式逐点积分实际均为 `pointwise_triangle`，面积比约为 0.891–0.923，均低于 0.95，因此全部保持 `SELF_VFM_REVIEW_REQUIRED`。E、Y、H 仍是候选值，不是最终材料参数。
- 验证：自建 VFM 目标测试 `15 passed`；全量测试 `91 passed`；工具编译通过；真实 S15 单帧 100489 点积分约 0.014 s。
- 待验证：先完成 ROI 与实体中心 1 mm 区域的空间叠合解释，再建立单轴几何、厚度、ROI 和外功证据；在这些门槛通过前不进行单轴正式参数识别。

## [2026-09-25] refactor | PA12 VFM 主流程切换与交接状态同步

- 来源：用户明确选择“历史 MatchID 资料保留为审计证据，主流程改为自建 VFM”；自建 VFM 阶段 A 四组结果及 S16 GUI 审计记录。
- 更新：`Agents/PA12实验数据处理/处理记录/PA12实验总体方法与防跑偏协议.md`、`Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md`、`Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json`、`Agents/PA12实验数据处理/MatchID_VFM准备/PA12_VFM边界载荷说明.md`、`index.md`。
- 结论：自建 VFM 成为当前计算主路径；MatchID `.vfm`、Boundary/Forces 和 GUI 试算保留为历史格式/方向/载荷审计。四组等双轴阶段 A 结果均为 `SELF_VFM_REVIEW_REQUIRED`，候选 E/Y/H 不升格为最终材料参数。
- 保留的历史问题：S16 `3try` X/Y 力 MAE=`26.1206/23.4119 N`、末帧差=`1452.79/1478.85 N`；`4try_step3` 的 Forces 数量为 `0`；第 16 轮 `Y=63.93 MPa`、`H=41.55 MPa` 仅为 GUI 中间候选。
- 验证：自建 VFM 目标测试 `15 passed`；全量测试 `94 passed`；工具编译通过；四组结果一致性审计通过。
- 下一步：复核四组自建 VFM 的 ROI/面积比、内外虚功、残差和参数稳定性，再补齐单轴几何、厚度、积分域和外功证据。

## [2026-09-25] refactor | PA12 自建 VFM 正式积分规则收敛

- 来源：`tools/pa12_self_vfm.py` 的规则网格积分实现、`tests/test_pa12_self_vfm.py` 新增规则网格方法测试、四组阶段 A 重算结果。
- 更新：正式积分统一为 `pointwise_triangle`；删除规则网格二维梯形求积作为正式路径的歧义；更新配置、阶段 A 记录、GPT 交接文档和 README。
- 结论：S15/S16/S17/S18 的最低积分面积比均低于 `0.95`，全部保持 `SELF_VFM_REVIEW_REQUIRED`；候选 E/Y/H 不能升格为最终材料参数。
- 下一步：取得实际 DIC 有效场边界与中心 1 mm 厚度的几何证据，再决定是否修改 ROI 配置并重算；单轴实验继续等待独立几何和外功证据。

## [2026-09-25] plan | PA12 执行目标修订

- 来源：当前 VFM 结果审计、ROI 面积覆盖门槛、S23/S24 数据限制和单轴几何证据缺口。
- 更新：修订总目标路线图、总体方法协议和 GPT 机器状态。
- 结论：主线固定为“数据闭环 → 等双轴自建 VFM 阶段 A → ROI/虚功/稳定性复核 → 跨实验验证 → 单轴证据补齐 → 最终材料参数”；MatchID 只作历史审计。
- 当前执行：复核四组等双轴 ROI 有效场覆盖、内外虚功残差和参数稳定性；面积门槛未通过前不发布正式材料参数。

## [2026-09-25] audit | PA12 阶段 A 虚功残差与参数稳定性

- 来源：四组 `*_内外虚功.csv`、`*_参数收敛.csv` 和对应结果 JSON。
- 结果：S15 阶段 1 累计 E 范围为 `-8529.02–6993.93 MPa`，S16 为 `3405.14–9794.54 MPa`，S17 为 `4991.17–5109.21 MPa`，S18 为 `4004.73–4624.11 MPa`；S15/S16 明显不稳定，S17 帧数不足，S18 相对稳定但面积门槛未通过。
- 结论：四组均保持 `REVIEW_REQUIRED`；不得通过平滑、删帧或人工替换把候选值升格为材料参数。
- 下一步：先解释 ROI 有效点场与 1 mm 中心区域的空间关系，再针对通过几何门槛的实验重新选择弹性拟合区间并复核虚功残差。

## [2026-09-26] audit | PA12 自建 VFM 阶段 D 双口径残差与稳定性比较

- 来源：四组完整 Job ROI 结果、四组 DIC subset 内缩有效域结果、tools/audit_pa12_self_vfm_stability.py、tools/audit_pa12_self_vfm_strict_holdout.py。
- 更新：Agents/PA12实验数据处理/VFM自建/汇总/PA12自建VFM阶段D双口径残差与稳定性比较.md、index.md、Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json。
- 结论：DIC 内缩域使 S16/S18 阶段 2 描述性残差下降，但没有一致改善阶段 1 虚功残差；E/Y/H 发生明显口径漂移，尤其 S18 的 H 从 632.27 变为 331.91 MPa。严格留出 RMSE 仍为 16.66/19.26 MPa，固定窗口 H 仍大幅漂移并出现负值。
- 门槛判断：完整 Job ROI 继续作为正式主结果，DIC subset 内缩域只作隔离敏感性证据；四组仍不发布最终材料参数，S17 阶段 2仍因点数不足未计算。
- 下一步：转入单轴独立几何、有效积分域和外部虚功证据门槛，优先审查 S19；双轴两种口径不得混合。

## [2026-09-26] audit | PA12 自建 VFM 阶段 E S19 单轴准入复核

- 来源：S19 Job.m2inp、X_0.2.vfm、S19 帧—力索引、000002/000127 合并 DIC 全场和 S19 自建 VFM 结果。
- 更新：Agents/PA12实验数据处理/VFM自建/汇总/PA12自建VFM阶段E S19单轴准入复核.md、index.md、Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json。
- 证据：Job Polygon 面积 674.346638 mm²；正式索引 126 帧；首帧 000002.jpg 为零力；末帧 000127.jpg 的 X 力为 178.6 N；末帧 DIC 点数 9144；VFM 设置文件未发现 Boundary、Forces、Thickness。
- 结论：S19 仍是单轴数据质量首选，但实际厚度、有效宽度、标距、Polygon 物理含义和外部虚功边界未通过独立证据门槛；现有 E/Y/H 仍是诊断候选，不启动新的正式识别。
- 下一步：补齐单轴专属几何与外功证据；确认后再决定是否进行 S19 的 DIC 内缩域敏感性分析和阶段 1/2 识别。

## [2026-09-26] audit | PA12 阶段 F 与单轴方向映射

- 来源：阶段 F E–ν 剖面、S15–S18 主/敏感性逐实验 JSON、S19–S22 单轴结果 JSON、方向标定图及 S22 `000016.jpg` 对应的 DIC—力结果。
- 更新：阶段 B、阶段 E、GPT 交接文档与状态、`index.md`；阶段 D 双口径结果表核对为逐实验 JSON 和只读稳定性/留出审计结果。
- 结论：完整 Job ROI 保持双轴主结果，DIC subset 内缩有效域只作隔离敏感性分析；阶段 F 未识别出稳定 ν。单轴计算暂用的机器 X=`Eyy`、机器 Y=`Exx` 映射仅由双轴旋转约定支持，未由 S19–S22 单轴装夹独立确认；S22 在该条件映射下得到非正 E，阶段 2 未运行。所有单轴 E/Y/H 仍为方向条件诊断候选。
- 下一步：补齐真实 ROI/厚度边界及 ν 独立约束；单轴正式识别前逐实验确认机器力方向与 DIC 轴映射，再处理几何和外功门槛。
## [2026-09-26] experiment | PA12 自建 VFM 目标验收和 E–ν 可辨识性

- 来源：用户修订后的任务目标、旋转后 DIC 全场—Press 合并数据、阶段 A–F 结果。
- 更新：`wiki/PA12单轴到双轴弹塑性VFM总目标与阶段路线图.md`、PA12 GPT 交接文档与状态 JSON；明确完整中文应力—应变曲线、X/Y 同图、显示平滑不回写数据，以及 MatchID 不可用时继续自建 VFM。
- 结论：旋转后的机器 X/Y 应变数组映射修正已纳入主积分并有回归测试；全量测试 `100/100`、编译、输出契约和应力—应变结构审计通过。formal VFM/材料参数状态仍未通过门槛。
- 流程改进：环境检查不再把 MatchID 缺失当作整条任务失败；依赖和输入齐备时标记 `READY_FOR_SELF_VFM`，单独报告 MatchID 导出能力。
- 待验证：真实 ROI/中心 1 mm 厚度边界、独立 ν 约束、单轴几何/外功定义、跨实验参数稳定性；S23 视觉断裂时缺少同步力，S24 是预载释放记录。
- 下一步：补实物几何和 ν 证据后重算 E/J2，并做独立跨实验留出；不把当前固定 ν 候选发布为正式参数。

## [2026-09-26] audit | PA12 自建 VFM 阶段 G S22 单轴横向应变诊断

- 来源：S22 完整 Job ROI 的 `内外虚功.csv`、结果 JSON、照片—力同步表及实验配置；仅分析已有数据，未修改原始 JPG/DAT/XLS 或计算配置。
- 更新：`Agents/PA12实验数据处理/VFM自建/汇总/PA12自建VFM阶段G S22单轴横向应变诊断.md`、`index.md`、GPT 交接文档与状态。
- 结论：222 条有效加载记录中，前 2/5/10/20/40/60 个观测的过原点斜率为 `0.39945/0.42791/0.43284/0.41785/0.43399/0.44776`；窗口相关性和弹性区间均未获独立确认，不能据此识别正式 ν。S22 的 Y→`Eyy` 是待确认映射，不触发代码轴交换。
- 下一步：确认 S22 传感器 Y 与导出 DIC `Eyy` 的坐标对应及图像旋转，再界定可验证的弹性窗口；单轴正式识别仍等待方向、几何和外功门槛。

## [2026-09-26] audit | PA12 自建 VFM 阶段 H 双轴 ROI 与厚度几何门槛

- 来源：五个中心厚度 STEP 与源拓扑 JSON、S16 Job ROI/标定、S16 自建 VFM 结果及候选 FE/DIC 映射预检。
- 更新：归档 STEP 与拓扑 JSON 到 `raw/assets/PA12_几何STEP/`；新增阶段 H 报告并更新 `index.md`、VFM README 和 GPT 交接状态。
- 结论：`tc1000.step` 中心平坦面为 `28.01×28.01 mm`；S16 Job ROI `27.209×27.907 mm` 仅在严格居中时可容纳，纵向余量每侧 `0.05156 mm≈0.59 px`。现有积分面积占该平坦面 `86.3548%`，未达 `0.95` 覆盖门槛。试样—STEP 对应与亚像素配准未确认，保持 `REVIEW_REQUIRED`。
- 下一步：获取 S16 试样标识/实测几何或 CAD 对应，并通过图像—CAD 特征配准确定 ROI 偏移；同时继续处理 S22 单轴方向/弹性窗口及独立 ν、外功和跨实验验证门槛。

## [2026-09-26] audit | PA12 单轴图像方向与自建 VFM 映射

- 来源：S19–S22 `000016.jpg`、单轴配置、S22 完整 Job ROI 尺寸与逐帧结果、`run_pa12_self_vfm.py` 及 `rotated_machine_axes` 实现。
- 更新：阶段 B、阶段 G、GPT 交接文档与状态、`index.md`。
- 结论：S19–S22 长条试样图像长轴均竖直；S22 配置为 Y 单轴且 ROI 长边沿 DIC `y`，而 runner 固定将机器 Y 映射到 `Exx` 并用 `Ly` 计算 Y 边界应力。S22 现有负 E 是映射条件下结果，不能作材料解释；实际有效宽度和传感器—DIC 轴注册仍待确认。
- 下一步：确认 S22 机器 Y 与 Job/DIC `y` 轴的对应；实现显式逐实验轴映射及关联虚功长度、边界截面、阶段 2 应力的同步映射前，保留现有计算输出不覆盖。

## [2026-09-26] experiment | PA12 阶段 I 单轴映射驱动重算

- 来源：S19–S22 原始参考照片与 Job ROI、已有逐点 DIC—Press 合并数据及单轴轴映射候选审计。
- 更新：`tools/pa12_self_vfm.py`、`tools/run_pa12_self_vfm.py`、`configs/pa12_self_vfm.json`、单轴 VFM 结果及阶段 B/G/I 报告、GPT 交接状态和 `index.md`。
- 方法：双轴保留机器 X→DIC y、机器 Y→DIC x；单轴逐实验配置机器轴到 DIC 轴映射，并用该映射一致计算应变、虚场加载长度和正交受力边长度。
- 结论：S22 候选 Y→DIC y 后得到条件 `E=10535.04 MPa`、`Y=103.58 MPa`、`H=238.04 MPa`；旧映射 E 为非正值，说明轴/边长选取会改变反演。S19–S21 数值不变。所有单轴仍为 `SELF_VFM_REVIEW_REQUIRED`，最低面积比 0.826930–0.870952，候选映射未完成坐标标定。
- 验证：当前全量测试 `104/104` 通过（包含阶段 2 合成单轴应变/虚功映射端到端测试），`compileall` 通过，输出契约审计通过；应力—应变审计仍含 `REVIEW_REQUIRED`，formal VFM 为 false。原始 JPG/DAT/XLS 未修改。
- 下一步：确认 S19–S22 传感器/夹具—Job/DIC 坐标关系及物理有效宽度、厚度、标距、积分域和外功；并推进 S16 实物—STEP 配准、独立 ν 和跨实验验证。

## [2026-09-26] ingest | PA12 Stage 2 S16 坐标与厚度预检记录

- 来源：`D:\C盘迁移\Desktop\yuan\second brain\wiki\methods\阶段2_G4_S16_FE-DIC坐标映射预检.md`、`阶段2_G2_G4_S16厚度匹配锚点模型.md`。
- 更新：原文按字节原样归档至 `raw/PA12_Stage2_Evidence/`；更新阶段 H/I 报告、VFM README、`index.md`。
- 结论：S16 FE–DIC 预检支持已登记的双轴机器/图像方向关系，且外部工作流以 tc1000 建立 1 mm 诊断锚点；原文将空间映射标为候选、模型标为预检，不能证明实物—STEP 身份或实际厚度。
- 待验证：S16 实物编号与 CAD 对应、Job ROI 实际亚像素位置、真实厚度；单轴坐标映射不可从 S16 双轴记录外推。

## [2026-09-26] ingest | PA12 Stage 2 单轴 ROI 与材料门槛记录

- 来源：`D:\C盘迁移\Desktop\yuan\second brain\wiki\methods\阶段2_G1_DIC标定图像ROI尺寸候选.md`、`阶段2_G1材料弹性标定候选与门禁.md`。
- 更新：原文按字节归档至 `raw/PA12_Stage2_Evidence/`；阶段 I 报告与 `index.md`。
- 结论：ROI 尺寸不能替代单轴试样的实测宽度、厚度、标距和有效截面；加载轴、图像轴、设备通道与材料坐标的对应仍需逐样确认，正式弹性/材料卡尚未放行。
- 待验证：逐试样取得标距/截面测量及坐标映射记录，并完成重复试验与独立留出验证。

## [2026-09-26] experiment | PA12 S22 阶段 2轴映射与 Job ROI 重算

- 来源：S22 完整 Job ROI 的 223 帧 DIC—力合并数据、`configs/pa12_self_vfm.json`、自建 VFM runner。
- 更新：阶段 2等效塑性应变与内部虚功沿同一逐实验机器轴—DIC映射计算；刷新 S22 正式逐帧结果、总汇总、README、阶段 I 记录与 `index.md`。
- 方法：S22 候选映射机器 X→DIC x、机器 Y→DIC y；完整 Job ROI 作为主结果。DIC subset 内缩有效域仍与主口径隔离，仅用于敏感性分析。
- 结果：固定 `ν=0.375` 时条件 `E=10535.04 MPa`；阶段 2条件 `Y=113.09 MPa`、`H=202.77 MPa`。阶段 1/2各自拟合误差阈值通过，但阶段 2机器 Y 内部虚功残差 RMSE=`163.81 N`、最大绝对值=`772.57 N`；积分面积比=`0.826930–0.847520`，单轴几何与设备坐标门槛未通过，结果维持 `SELF_VFM_REVIEW_REQUIRED`。
- 待验证：确认 S22 传感器—夹具—Job/DIC 坐标注册、单轴厚度及有效截面/外功边界；再开展独立 ν 与参数稳定性/留出验证。

## [2026-09-26] audit | PA12 等双轴阶段 A 逐点虚功复核

- 来源：S15–S18 当前逐点内外虚功 CSV、逐实验结果 JSON、阶段 C/D 固定窗口与严格留出审计脚本。
- 更新：阶段 C/D 的舍入数值、`index.md`、GPT 交接机器状态新增阶段 A 逐帧审计字段。
- 结论：679 个逐帧记录的照片唯一性、时间单调性、阶段 1 `E×虚场系数`/残差、阶段 2 内部虚功/残差及面积比 CSV—JSON 一致性均通过。更正 S18 阶段 1 相对 RMSE 为 `0.0136`、S15 为 `0.1120`；S15 仍超过 `0.10` 门槛。四组面积比均低于 `0.95`，S17 阶段 2 点数不足；S16/S18 窗口 H 漂移和严格留出误差仍阻断参数发布。
- 下一步：保持全部双轴参数为条件候选；取得物理积分域/中心厚度注册和独立 ν 证据后，再按冻结口径进行严格留出及跨实验验证。
## [2026-09-26] refactor | PA12 执行目标修订与阶段 I 结果同步

- 来源：用户提供的 PA12 项目目标截图、当前自建 VFM 阶段 I 结果 JSON、阶段 I 报告及 GPT 交接材料。
- 更新：`Agents/PA12实验数据处理/处理记录/PA12总目标与阶段计划.md`、GPT 交接文档、`index.md`。
- 结论：将 MatchID 由主流程必需项调整为可选审计/对照；正式参数发布门槛与可先行交付的诊断候选分层。修正 S22 条件候选 E/Y/H 为 `10535.04/113.09/202.77 MPa`；单轴仍为复核状态。
- 验证：全量 pytest `104 passed`；本次运行用于发现软件回归失败，不代替生产数据审计和物理参数验证。
- 下一步：继续核对单轴/双轴完整曲线图与数据关系，复核批次诊断产物和跨实验参数稳定性；正式参数仍需补齐 ROI/几何/边界、ν、坐标和留出证据。

## [2026-09-26] audit | PA12 应力—应变复核报告补充失败原因

- 来源：9 组现有应力—应变 CSV/PNG、批次配置及只读曲线审计。
- 更新：`tools/audit_pa12_stress_strain.py`、`tests/test_pa12_stress_strain.py`、`Agents/PA12实验数据处理/处理记录/PA12应力应变曲线审计.md`、对应 JSON、GPT 交接状态和 `index.md`。
- 方法：审计 Markdown 对各活动方向列出非有限/缺失、应变非单调、首行零力、峰后掉载等触发项；无显著掉载时记录峰后最低应力/峰值与 `≤0.20` 门槛。审计不改 CSV/PNG。
- 结论：9 组曲线文件均存在，6 PASS、S15/S22/S23 三组 REVIEW_REQUIRED、S24 为预载释放。S15/S22/S23 均未满足自动峰后掉载判据；报告据此要求人工核对，不补造断裂力或重写曲线。
- 验证：新增测试先复现报告缺少掉载解释，再经实现通过；全量 pytest `105 passed`，`compileall` 通过，交接/曲线审计 JSON UTF-8 解析通过，`git diff --check` 通过。审计结果 6 PASS、3 REVIEW_REQUIRED、1 PRELOAD_RELEASE_ONLY，formal_curve_audit_ready=false。
- 下一步：核对三组数据终点与视觉/有效 DIC 帧的对应，完成仍可计算的 VFM诊断和留出分析；正式材料参数仍按物理证据与稳定性门槛发布。
