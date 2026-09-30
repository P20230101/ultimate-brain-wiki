# 工作日志

本文件只追加，不改写旧记录。每条记录使用一致标题，便于搜索和脚本处理。

## [2026-09-26] goal | PA12 自建 VFM 诊断交付与正式发布分线

- 来源：用户要求纠正停滞并继续执行 PA12 实验/VFM总目标；S16 部分场支持结果复核。
- 更新：`Agents/PA12实验数据处理/处理记录/PA12总目标与阶段计划.md`、`index.md`、`tools/run_pa12_finite_vfm_diagnostic.py`。
- 结论：把任务验收拆为持续推进的诊断交付线和需要独立物理证据的正式参数/J2发布线；S16 Job ROI 尺度分支明确标为仅部分 DIC 积分候选，不能称完整 ROI 结果。
- 待验证：MatchID 派生 Job 能否外扩相关域并覆盖完整积分 ROI；扩展场须先通过点覆盖和相关质量审计。

## [2026-09-26] audit | PA12 曲线事件与有限变形候选口径复核

- 来源：`configs/pa12_rotated_batch.json`、同步/DIC派生产物、S16 原始 Job 与 DAT 审计。
- 更新：`tools/run_pa12_finite_vfm_diagnostic.py`、`Agents/PA12实验数据处理/VFM自建/有限变形诊断/S16_XY_0.2/`、`Agents/PA12实验数据处理/处理记录/PA12应力应变曲线审计.md`、总目标与 GPT 交接文档/状态、`index.md`。
- 结论：S16 Job ROI 虚场尺度分支准确标为部分 DIC 积分候选；曲线审计为 PASS 6 组、REVIEW_REQUIRED 3 组、预载释放 1 组。S15 断裂帧 DAT 不完整，S22 自动掉载门槛未通过，S23 视觉断裂帧无力数据。
- 验证：`python -m pytest -q`（132 passed）、S16 有限变形诊断重跑、曲线审计重跑、`python -m compileall -q tools tests`、JSON解析、`git diff --check`。
- 待验证：安全建立 MatchID 派生 Job 的 GUI 流程；扩展 DIC 通过覆盖和相关质量审计后才可用于完整 ROI 积分。

## [2026-09-26] report | PA12 逐组诊断交付总览

- 来源：批次清单、应力—应变曲线审计 JSON、自建 VFM 阶段 A 结果与逐帧一致性审计。
- 更新：`tools/build_pa12_diagnostic_dashboard.py`、`tests/test_pa12_diagnostic_dashboard.py`、`Agents/PA12实验数据处理/VFM自建/汇总/PA12逐组诊断交付总览.{md,csv,json}`、`index.md`、GPT交接文档。
- 结论：建立 10 组统一导航表，分列曲线审计、帧数、覆盖门槛、阶段 1/2 质量和诊断条件参数；明确内部一致性审计不等于物理闭合或正式参数资格。
- 验证：总览契约测试、10 组 Markdown/CSV/JSON 对照和全量 VFM 阶段 A 一致性审计通过。
- 待验证：审查所有实验虚功模型独立性、ROI 覆盖、条件参数稳定性并完成未结曲线事件记录。

## [2026-09-26] audit | S16 有限变形候选标签与二维模型范围

- 来源：`tools/run_pa12_finite_vfm_diagnostic.py`、S16 Job/DIC 覆盖统计及合成运动学/功共轭测试。
- 更新：有限变形 runner、S16 诊断摘要/逐帧表、Stage 2 独立性审计、总目标与 GPT 交接、`index.md`、有限变形诊断测试。
- 结论：Job ROI 尺度结果标为仅部分 DIC 积分候选（覆盖 89.2248%）；明确该原型只定义二维面内 `P₂=J₂σ₂F₂⁻ᵀ` 功共轭，未识别三维厚度伸长 `λz`，不称完整三维平面应力本构识别。257 帧 `det(F)` 为 0.6638–2.1817 且无非正 Jacobian 三角形；末帧平均面内 Euler–Almansi 应变约 8.5%，绝对应变分量 P99 约 0.181，显示后段不属小应变区。保留现有数值为诊断结果。
- 验证：有限变形标签、运动学摘要、总览字段契约及全量回归通过；8 组/1127 帧阶段 A 一致性审计通过；曲线审计与总览重建。
- 待验证：扩展 DIC 的可执行派生 Job、完整 ROI 积分、独立外功边界验证及有限应变弹塑性本构更新。

## [2026-09-26] plot | 曲线峰值与有效照片断裂终点标记

- 来源：PA12 应力—应变曲线和照片—力终点判定规则。
- 更新：`tools/pa12_sync.py`、`tools/run_pa12_batch.py`、`tests/test_pa12_sync.py`、批次派生应力—应变图/处理报告/清单、诊断总览、GPT 交接和索引。
- 结论：曲线标注各活动方向峰值；只有视觉断裂帧是最后有效 DIC 帧或掉载力时刻与最后照片在半帧周期内对应时，才标断裂/掉载终点。S15 DAT 异常帧和 S23 视觉断裂处缺力均不误标。
- 验证：终点匹配及绘图测试通过；10 组批次重建后抽查 S16/S23 图像，终点图例/符号与断裂照片证据一致；曲线状态仍为 6 PASS、3 REVIEW_REQUIRED、1 PRELOAD_RELEASE_ONLY。
- 待验证：手工检查其余各组峰值与事件照片，并继续完成独立应力更新/虚功 Stage 2。

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

## [2026-09-26] audit | PA12 等双轴跨实验留出诊断

- 来源：S15–S18 完整 Job ROI 逐帧虚功 CSV、对应结果 JSON 和冻结的自建 VFM 配置。
- 更新：新增 `tools/audit_pa12_self_vfm_cross_experiment.py`、合成数据回归测试、跨实验 CSV/报告；更新总目标、GPT 交接文档、机器状态和 `index.md`。
- 方法：按现行阈值执行留一实验 E 迁移与峰值前 Linear Y/H 候选迁移；只纳入等双轴完整 Job ROI，不混用 subset 敏感性口径。阶段 2训练点数不足或质量不合格时不拟合。
- 结论：审计限定为 S15–S18 等双轴完整 Job ROI，共 12 个有向配对。阶段 2资格、质量分母修正为生产 runner 口径；S17 为 4 个候选点，未拟合。S15/S16 间 E 迁移相对 RMSE 为 8.84–19.10%，与 S18 的配对为 23.32–35.85%；加载速度与组别混杂，不能解释为速率因果或材料重复性。S18 到低速组的阶段 2迁移 RMSE 为 41.63–52.82 MPa。所有输出保持 `DIAGNOSTIC_ONLY`，正式门槛不变。
- 验证：合成已知 E/Y/H 的留出测试和生产口径回归测试通过；重算 CSV 确认为 12 个等双轴配对；全量 pytest `110 passed`、`compileall`、审计状态核对和 `git diff --check` 通过。
- 下一步：继续处理 S15/S22/S23 曲线审计项和仍可计算的诊断；取得同速率重复试验及几何、ν、坐标、外功证据后再评估正式参数。

## [2026-09-26] experiment | PA12 自建 VFM 双轴 ROI 双口径复现

- 来源：`configs/pa12_rotated_batch.json`、`configs/pa12_self_vfm.json`、S15–S18 DIC 全场—同步力输入、阶段 D 双口径审计。
- 更新：重跑 `tools/run_pa12_self_vfm_effective_domain.py`；刷新四组 subset 敏感性逐实验 JSON；同步自建 VFM 方法协议、GPT 交接文档/状态、历史 MatchID 边界说明和 `index.md`。
- 方法：完整 Job ROI 保持主结果；DIC subset 内缩有效域作为独立敏感性域，输出不覆盖主结果。所有实验仍按显式机器轴—DIC映射计算。
- 结果：S15/S16/S17/S18 分别重现 284/257/12/126 帧；条件 E 为 3396.71/3221.41/4754.54/4348.34 MPa，S17 阶段 2点数不足，其他三组条件 Y/H 为 35.42/162.86、44.97/139.37、53.43/331.91 MPa。数值与阶段 D 敏感性表一致；参数随域变化，仍只作敏感性候选。
- 限制：DIC 内缩域的面积闭合不证明其是实物 VFM 边界。完整 Job ROI 面积覆盖、ROI/厚度注册、独立 ν、参数稳定性及正式留出门槛仍未通过。原始 JPG/DAT/XLS 未修改。
- 下一步：完成 S15/S22/S23 曲线末端与照片、同步力和有效 DIC 场之间的事件复核，并继续复现可计算的残差/留出诊断；不发布正式材料参数。

## [2026-09-26] audit | PA12 曲线事件与单轴 VFM 稳定性复核

- 来源：S15/S22/S23 应力—应变 CSV、照片—力对应表、DIC DAT/照片及自建 VFM 逐帧结果；S19–S22 完整 Job Polygon 自建 VFM CSV。
- 更新：总体方法协议、GPT 交接文档/机器状态、VFM 边界说明和 `index.md`。
- 方法：逐帧核对照片、力、曲线和可用 DIC/VFM；只读执行四窗口审计；对候选轴映射与脚本一致的 S19–S21 执行 75/25 时间留出。未修改曲线、VFM 结果、原始 JPG/DAT/XLS、配置或计算脚本。
- 结论：S15 视觉断裂帧缺完整 DAT，曲线止于 `000284.jpg`；S22 末端降载照片仍见连续试样，且阶段 2窗口在曲线峰值前截止；S23 断裂帧 `001547.jpg` 晚于最后有力照片 `001528.jpg`，断裂力缺失。S19–S22 窗口 H 均显著漂移并变号；S19–S21 留出 RMSE 为 `145.80/71.79/114.61 MPa`。S22 未套用轴映射不匹配的留出脚本。所有单轴候选保持 `REVIEW_REQUIRED`。
- 验证：四窗口及留出脚本只向终端输出；本次没有运行测试套件或生产 writer。交接文档注明 S22 阶段 2 CSV 的 125 个有效预测区间，以区分窗口外空白与产物生成问题。
- 下一步：取得单轴实测截面/标距与传感器—DIC 坐标证据；代码范围允许后，为 S22 增加映射感知的严格留出。正式参数发布门槛不变。

## [2026-09-26] audit | PA12 S22 映射感知留出状态同步

- 来源：阶段 I 单轴机器轴与 DIC 轴映射复核报告、`PA12_GPT交接状态.json` 的 `stage_i_gate.strict_holdout`、映射感知留出实现及其定向测试。
- 更新：GPT 交接文档、总体方法协议、机器状态、边界载荷历史审计说明和 `index.md`。
- 方法：按时间顺序 75/25 留出，使用逐实验机器轴—DIC 映射；固定切分，不为增加测试点事后移动边界。未重写原始数据或 VFM 计算输出。
- 结论：S22 训练/留出为 167/56 帧，训练段含 3 个弹性观察点和 125 个峰前塑性拟合点；留出段仅 1 个有效峰前塑性点。条件 E/Y/H 为 `10535.04/113.09/202.77 MPa`，单点留出 RMSE=`26.114771 MPa`，状态 `INSUFFICIENT_TEST_POINTS`，不构成独立验证通过；单轴仍为 `REVIEW_REQUIRED`。
- 验证：`python -m pytest -q tests/test_pa12_self_vfm_strict_holdout.py`，`3 passed`。该测试只验证映射与点数状态逻辑，不证明材料参数有效。
- 下一步：补齐 S19–S22 传感器—夹具—Job/DIC 坐标和单轴实测几何；补 S16 试样—STEP/ROI 配准及独立 ν 证据。门槛满足前不发布正式参数。

## [2026-09-26] refactor | PA12 总目标拆分为诊断交付与正式发布

- 来源：当前 PA12 数据、同步/DIC/VFM 派生结果、曲线与跨实验审计，以及用户指定的完整有效区间曲线和自建 VFM 目标。
- 更新：`Agents/PA12实验数据处理/处理记录/PA12总目标与阶段计划.md`、GPT 交接文档/状态、总体方法协议、`index.md`；跨实验报告和曲线审计重新生成。
- 决策：把目标拆为持续进行的诊断交付线与受物理证据门槛约束的正式材料参数/J2发布线。曲线保留完整有效加载范围，X/Y 同图，PNG 显示平滑不改数值 CSV；MatchID 不再是任务阻塞条件。
- 结果：应力—应变曲线审计为 6 PASS、3 REVIEW_REQUIRED、1 PRELOAD_RELEASE_ONLY；9 组曲线的行数和首末帧均与有效清单一致。跨实验报告重算 12 个有向配对；S22 严格留出仅 1 个有效塑性点，不能作为验证。
- 验证：全量 pytest `116 passed`；`compileall`、三份关键 JSON 解析及 `git diff --check` 通过。原始 JPG/DAT/XLS 未修改。正式材料参数/J2 仍未通过几何、坐标、独立 ν、虚功闭合与稳定性等门槛。
- 下一步：补齐 S16 实物—STEP/ROI 配准、单轴实际几何和机器—DIC 坐标、独立 ν 与边界外功证据；然后重算诊断并重新评估发布门槛。

## [2026-09-26] lint | PA12 索引中的 VFM 主线措辞

- 发现：`index.md` 将自建 VFM 描述为“MatchID VFM 不可用时”的替代路线，与当前“VFM 全部由自建代码执行、MatchID 仅作历史审计”的固定决策不一致。
- 修改：将总目标入口改为当前固定主线；将旧版 S15 MatchID 核验提议和 `.vfm` 准备包标为历史资料，保留其几何、DIC/力同步和方向审计证据。
- 下一步：继续以物理 ROI/厚度配准、单轴实测几何与坐标、独立 ν 为参数发布门槛；不从缺失资料推断或补造数据。

## [2026-09-26] fix | PA12 同步输入审计状态语义

- 来源：重跑 PA12 自建 VFM 主流程及照片/X/Y 输出契约审计。
- 更新：`tools/audit_pa12_outputs.py`、测试、同步审计 JSON/报告、边界审计 writer/报告、GPT 交接状态/文档、`index.md`。
- 结论：分实验旧字段 `formal_vfm_ready=true` 只证明照片—力—X/Y 同步输入契约通过，容易被误读为正式 VFM/材料参数通过。现改用 `sync_triplet_ready`、`all_sync_triplets_ready`；报告明确不判定材料参数或 VFM 识别发布。边界说明恢复用户确认的机器力直接作为自建 VFM 与 MatchID 对照的 ROI 边界合力口径，同时说明该输入约定不证明虚功闭合。
- 验证：自建 VFM 主流程完成 10 组；8 组同步三件套契约成立，S23/S24 不进入完整输入审计；输出契约审计无失败，正式识别状态仍未放行。回归测试 `117 passed`，`compileall`、状态 JSON 断言和 `git diff --check` 通过。
- 下一步：补齐 ROI/厚度/截面、机器—DIC 坐标、独立 ν 和外功/虚功闭合证据，继续阶段 A–I 诊断及正式门槛审查。

## [2026-09-26] lint | PA12 旧批处理报告与当前 VFM 主线

- 发现：历史《PA12批量处理报告.md》仍保留“MatchID 下一步”旧流程指引，虽其中 `VFM_READY/正式 VFM` 仅代表同步输入契约，仍可能被误作当前执行清单。
- 修改：在总体方法协议、GPT 交接文档和 `index.md` 明确该段已被自建 VFM 主线取代；原报告保留为历史审计资料，不改写其内容。
- 当前口径：双轴完整 Job ROI 保持主结果，DIC subset 内缩有效域仅作隔离敏感性分析，两套结果不混合。
- 下一步：继续补齐 ROI/厚度实物配准、坐标、独立 ν 与内外虚功闭合证据；旧 MatchID 操作清单不作为推进条件。

## [2026-09-26] audit | PA12 自建 VFM 阶段 A 产物一致性

- 来源：S15–S22 的 Stage A 逐帧 CSV/JSON 与各组 DIC—力同步索引。
- 关联产物：`tools/audit_pa12_self_vfm_results.py`、`tests/test_pa12_self_vfm_results_audit.py`、阶段 A 一致性审计 Markdown/JSON；索引、GPT 交接文档和机器状态已登记入口与结果。
- 结果：8 组共 1127 帧通过，审计失败项为 0；定向单元测试 `3/3` 通过，覆盖缺失 Stage A 结果、Stage A 与同步索引力值不一致及旧 CP936 编码读取。
- 结论边界：该审计复核派生产物与已合并同步索引的内部一致性，不验证原始机器力—照片的物理同步、Job ROI 是否为真实物理边界、虚功模型是否适用或参数是否可识别。
- 下一步：继续补齐双轴 ROI/厚度实物配准、单轴传感器—DIC 坐标与几何、独立 ν 和物理外功闭合证据；保持 Job ROI 主结果与 subset 内缩域敏感性分析分离。

## [2026-09-26] refactor | PA12 自建 VFM 执行目标改为诊断优先、物理门槛并行

- 来源：用户要求修正停滞的任务目标，并继续执行 PA12 VFM 工作。
- 更新：`Agents/PA12实验数据处理/处理记录/PA12总目标与阶段计划.md`、`PA12实验总体方法与防跑偏协议.md`、GPT 交接文档/状态、`index.md`。
- 目标：Stage A–I 诊断继续基于现有资料推进；下一项是核查虚场/内外虚功定义、单位、广义外功条件、均匀应力近似和完整图表。ROI/厚度、机器—DIC 坐标、独立 ν、本构/应变测度及独立验证只控制正式参数/J2发布，不阻塞可计算诊断。
- 方程审阅结论：代码实现单位伸长虚场，阶段 1 平面应力弹性系数单位 N/MPa，内虚功 `E·B` 单位 N。外部虚功直接使用 Press 合力，仅在边界单位虚位移差为 1 且其余边界外功为零时成立；该物理条件未逐组证明。阶段 2 将力/名义截面形成的应力视为 ROI 内均匀，属于简化假设。二者均保留为诊断级，不作为已验证真实场。
- 验证：全量 `pytest` 120/120 通过；`compileall` 通过；阶段 A 产物一致性审计 8 组、1127 帧、0 项内部失败。原始 JPG/DAT/XLS 未修改。
- 下一步：核对每阶段图表与逐帧值及其生成代码；若发现代码可验证的问题，先添加失败测试再修复和重算。正式参数门槛仍需独立物理证据，不能由软件审计替代。

## [2026-09-26] audit | PA12 Stage 2 虚功与 Press 力独立性

- 来源：`tools/run_pa12_self_vfm.py` 的 Stage 2 生产路径、8 组 Stage 2 逐帧 CSV、旋转/单轴 MatchID Job 应变约定。
- 更新：新增 `Agents/PA12实验数据处理/VFM自建/汇总/PA12Stage2现行实现与虚功独立性审计.md`；更新总目标、总体方法、GPT 交接状态/文档及 `index.md`。
- 结论：现行 Stage 2 从 Press 反算名义应力，拟合 `σeq(εp)` 后再按拟合/实测等效应力比例缩放原应力。矩形 ROI 中 X 向内部虚功化为 `Fx·σeq,fit/σeq,force`。逐帧结果 S15/S16/S18/S22 与此式的最大绝对差不超过 `1.6×10⁻⁶ N`；该残差不是独立全场 VFM 闭合。旧 Y/H 和 Stage 2 虚功降级为力耦合名义曲线诊断。
- 运动学证据：8 组 Job 的应变约定均为 1（Job 注释为 `LOGEulerAlmansi`）；DIC 合并场含 `x/y/u/v`。这提供重建有限变形运动学的输入基础，但不证明真实 ROI/边界/材料模型通过。
- 验证边界：只读计算及文档整理；未改算法或原始数据。阶段 A 审计和全量测试以前述独立命令结果为据，本轮未重跑。
- 下一步：以 DIC 位移历史恢复功共轭应力场，设计并验证有限变形 Stage 2；在真正的独立虚功残差闭合前，不发布新的 `Y/H` 材料参数。

## [2026-09-26] audit | PA12 双轴完整 Job ROI 与名义平坦区尺寸筛查

- 来源：S15–S18 `Job.m2inp` 的 Shape 与 Conversion；`tc1000.step` 名义中心平坦区尺寸记录。
- 更新：总体方法协议、GPT 交接文档/状态、历史 MatchID 边界说明和 `index.md`。
- 方法：以 Job Shape 像素跨度乘标定，分别与名义 `28.01×28.01 mm` 平坦区比较；此步骤只判尺寸关系，不推断 ROI 位置或实物身份。
- 结果：S15/S16/S17/S18 完整 ROI 尺寸依次为 `28.775656×28.775656`、`27.209208×27.906880`、`27.638624×28.075944`、`26.326664×26.763984 mm`。尺寸条件下 S15/S17 至少一向超出，S16/S18 可容纳。
- 结论：没有试样—STEP 身份和 ROI 对实际 1 mm 平坦区的二维/亚像素配准证据，故不把尺寸筛查解释为实际 containment 通过或失败。完整 Job ROI 仍为主结果；DIC subset 内缩域仅作独立敏感性分析，不裁切或替换主 ROI。正式几何门槛维持 `REVIEW_REQUIRED`。
- 下一步：取得各试样与厚度 STEP 的身份对应及平坦区/Job ROI 配准证据；在此之前继续区分诊断候选与正式材料参数，不修改原始 JPG/DAT/XLS、计算代码、配置或生成检查报告。

## [2026-09-26] refactor | PA12 执行目标重写为独立有限变形 VFM

- 来源：用户要求直接修改任务，并强调最终需要可审计的整段应力—应变、真实 VFM 虚功/参数结果及后续 GPT/MatchID 衔接。
- 更新：`Agents/PA12实验数据处理/处理记录/PA12总目标与阶段计划.md`、GPT 机器状态和 `index.md`。
- 新目标：诊断交付与正式参数发布分轨；旧 Stage 2 明确降级为力耦合曲线诊断；优先通过合成真值测试实现 DIC 位移/应变驱动的有限变形 Stage 2，以独立内外虚功残差评估；完整输出曲线线性段、屈服候选、峰值和可确认断裂。J2 在独立虚功链后评估。
- 完成判据：逐组同步数据、完整曲线、逐帧内外虚功/残差、积分覆盖、稳定性/灵敏度/留出、诊断结论、中文复现/交接通过审计；真实几何/边界/独立验证缺失只阻止正式参数发布，不阻塞诊断实施。
- 本次验证：目标 JSON 可解析；Stage 2 审计记录路径存在；机器状态含合成真值测试下一步；`git diff --check` 无错误。此为目标/文档更新，不代表新算法已实现或物理结果已验证。
- 下一步：为有限变形 Stage 2 先写合成真值测试，再实现计算器并验证；之后批量重算、人工复核，审阅 Git 变更并推送，不上传原始实验数据。

## [2026-09-26] experiment | PA12 有限变形运动学内核

- 来源：修订后的自建 VFM 目标；DIC 合并场包含 `x/y/u/v`，MatchID Job 应变约定为 `LOGEulerAlmansi`。
- 更新：新增 `tools/pa12_finite_kinematics.py` 与 `tests/test_pa12_finite_kinematics.py`；总目标、Stage 2 审计页、GPT 机器状态和 `index.md` 记录当前边界。
- 方法：先测试后实现二维 Euler–Almansi 应变 `e=0.5(I-(F Fᵀ)⁻¹)`。
- 结果：纯刚体旋转应变为零；λ=1.25 的均匀 X 向伸长与解析解一致。定向测试 2/2 通过；全量测试 122/122 通过，`compileall` 通过。
- 限制：仅运动学张量函数；尚无从逐点 DIC 位移恢复 F、局部应力更新、内外虚功或材料参数识别；不能称为有限变形 Stage 2 完成。
- 下一步：对 `x/y/u/v` 建立仿射位移场 F 重建测试，再以 work-conjugate 第一 Piola 应力和参考构形虚位移建立独立虚功合成测试。

## [2026-09-26] experiment | PA12 有限变形 VFM 合成内核

- 来源：PA12 自建有限变形 Stage 2 执行计划；既有 DIC `x/y/u/v` 字段映射和 MatchID `LOGEulerAlmansi` 设置仅作为待核输入证据。
- 更新：扩展 `tools/pa12_finite_kinematics.py` 与 `tests/test_pa12_finite_kinematics.py`；同步更新总目标、Stage 2 独立性审计、GPT 交接文档/状态和 `index.md`。
- 方法：三节点位移恢复常值 F；由 Euler–Almansi 应变计算线性平面应力诊断 Cauchy 应力并转为第一 Piola；在参考三角网格积分 `P:Grad_X(v*)`。合成边界合力独立用均匀第一 Piola 应力与参考边界面积计算，合成 E/ν 只用于验证拟合闭环。
- 结果：旋转客观性、伸长解析值、仿射伸长/剪切 F、单位缩放、平面应力小应变极限、Cauchy/Piola 功率恒等式、内虚功—解析边界合力和合成参数反演通过；定向 pytest 7/7，全量 pytest 128/128。
- 限制：没有逐帧实验接入、真实 ROI 网格/子集敏感性重算、塑性应力更新、实验内外虚功残差或 Y/H 参数识别。完整 Job ROI 主结果与 subset 内缩域敏感性规则不变；实验阶段 1 仍固定 `ν=0.375`，合成 E/ν 拟合不能作为实验识别。
- 下一步：核实 DIC `x/y` 参考构形语义及 `u/v` 同单位映射，接入同帧 DIC/同步力，分开生成完整 Job ROI 主网格与 subset 内缩域网格，计算实验内外虚功和残差后再进入弹塑性本构更新。

## [2026-09-26] audit | PA12 S16 有限变形弹性虚功首轮窗口

- 来源：`Agents/PA12实验数据处理/MatchID_VFM准备/S16_XY_0.2/merged/` 的 9 个早期 DIC—力帧和 S16 Job ROI。
- 方法：以 `000001.jpg` 为位移基准，使用参考 x/y 唯一键而非 CSV 行号对齐 u/v；Delaunay 三角剖分计算参考域内虚功。机器 X/Y 按旋转后映射至 DIC y/x。固定 `ν=0.375`，以线性 Euler–Almansi 平面应力诊断律和 `P=JσF⁻ᵀ` 计算 E 条件候选；另算自由 ν 剖面仅检查可辨识性。
- 结果：9 帧、10,098 点、19,796 三角形，积分面积 `677.505105 mm²`，与 Job ROI 一致。固定 ν 候选 E=`3313.213 MPa`；虚功残差 RMS=`33.406 N`，活动力 RMS=`345.411 N` 的 `9.67%`。自由 ν 的 1% 残差带约 `0.299–0.499`，E 条件范围约 `2649–3722 MPa`，不具独立识别能力。
- 判读：只属 9 帧诊断；残差显著，尚未全帧/窗口稳定性、缺口/积分敏感性或真实边界外功验证。非材料参数发布。
- 环境：当前 Python 3.12 安装 SciPy 1.18.1；新增 `requirements-pa12-vfm.txt`，环境检查器现要求 SciPy 和 xlrd。全量 `pytest` 128/128、`compileall`、输入路径和七项依赖检查通过，状态 `READY_FOR_SELF_VFM`。
- 下一步：将 x/y/u/v 对齐、ROI 网格、固定 ν E 反演、自由 ν 剖面、逐帧残差/覆盖率和图表封装为可复现运行器，再扩展至各适用试验。

## [2026-09-26] experiment | PA12 S16 有限变形逐帧诊断与 ROI 覆盖复核

- 来源：S16 旋转后照片/DAT、257 帧 DIC—Press 合并数据、原始 `Job.m2inp` Shape 与 conversion。
- 更新：新增 `tools/run_pa12_finite_vfm_diagnostic.py`、`configs/pa12_finite_vfm_s16.json`、坐标键对齐函数及测试；生成 `Agents/PA12实验数据处理/VFM自建/有限变形诊断/S16_XY_0.2/` 诊断表、图、剖面和摘要；同步修订 Stage 2 审计、总目标、GPT 状态与索引。
- 方法：以 `000001.jpg` 为参考，逐帧对齐 DIC `u/v`，由参考点三角网恢复变形梯度，固定 `ν=0.375` 计算 Euler–Almansi 平面应力诊断内功；外功将同步 Press 合力作为单位伸长虚场的广义力候选。
- 结果：有效索引 257 帧；DIC 网格面积 `677.505105 mm²`，Job ROI 面积 `759.324103 mm²`，覆盖率 `89.2248%`。此前“面积与 Job ROI 相符”的陈述不正确，已更正。九帧固定 ν 条件 E=`3313.376 MPa`，残差 RMS=`33.400 N`，力 RMS=`345.411 N` 的 `9.67%`；自由 ν 的 1% 残差带约为 `0.299–0.499`。
- 判读：当前只是 DIC 内缩域诊断，完整 Job ROI 因约 10.8% 场缺失不可计算；外功边界等价、坐标单位、实物 ROI/厚度和本构均未全部独立验证，不能发布材料参数或声称 VFM 闭合。
- 下一步：定位/恢复 DIC 子域外位移场；若原始资料不能恢复，则明确记录完整 ROI 不可计算。再将诊断runner扩展到其他实验，继续审计有效区间曲线、稳定性、塑性更新与独立验证。

## [2026-09-26] refactor | PA12 S16 Job ROI 与 DIC 内缩域分支分离

- 更新：同一三角网现按 Job ROI 与 DIC 内缩域两种虚场长度分别计算；输出 CSV 标记积分域/覆盖率，摘要分别报告条件 E 和残差，图表按域分面。Job ROI 尺度分支因 DIC 覆盖率 `89.2248%` 保持 `REVIEW_REQUIRED`，不能解释为完整 ROI 积分。
- 数值：Job ROI 尺度候选 E=`3507.812 MPa`、拟合帧残差 RMS=`33.315 N`；DIC 内缩域 E=`3313.376 MPa`、残差 RMS=`33.400 N`。两者均为诊断候选；全 257 帧残差 RMS 约 `4969.4 N`，线弹性模型不能代表全历程。
- 验证：分域真值测试核对 Job/DIC 虚场尺度分离及 E 独立拟合；全量 pytest `132/132`、compileall 通过。更新状态/索引后需再做最终产物数量、NaN 和 JSON 检查。
- 下一步：确认缺失边缘位移场能否恢复；之后将可用分域流程扩展至其他实验。塑性更新、跨窗参数稳定性和正式发布仍未完成。

## [2026-09-26] audit | S16 DAT 边缘场可恢复性

- 来源：S16 `PA12_DIC_DAT质量审计.csv`、原始 `000001.jpg.dat` / `000257.jpg.dat`、同帧合并导出和原始 `Job.m2inp`。
- 结果：257 个有效 DAT 全部为 10,098 点；抽查首末帧时，原始 DAT 有效坐标集合与对应 CSV 完全一致。坐标点域小于 Job ROI；没有额外边缘位移点可供现有数据重建完整 ROI。
- 结论：不从已有场插值或外推补足。若要计算完整 ROI，应使用原始 JPG 建立独立的扩展相关区域 Job，在物理积分 ROI 外提供 subset 支撑，再将积分严格裁回原 Job ROI；不覆盖当前 Job/DAT。

## [2026-09-26] audit | S16 完整 Job ROI 主结果与内缩域敏感性产物复核

- 来源：S16 257 帧 DIC—力索引、原始 Job ROI 几何及有限变形诊断 runner 产物。
- 更新：摘要/机器状态/交接/索引明确区分完整 Job ROI 主分支与 DIC subset 内缩域独立敏感性；两分支文件分别存放。
- 结果：两分支各 257 行逐帧 CSV、50 点 ν 剖面和诊断图，数值均有限；主分支覆盖率 `89.2248%`、条件 E `3507.812 MPa`、状态 `REVIEW_REQUIRED`；内缩敏感性条件 E `3313.376 MPa`。自由 ν 的 1% 残差带分别为 `0.328–0.499` 和 `0.299–0.499`。
- 判读：主结果使用完整 Job ROI 虚场尺度，但实际内虚功只积分现有 DIC 网格，故不是完整 ROI 内部积分或闭合；内缩分支不能替代主域。未新增或改写原始 JPG/DAT/Job。
- 下一步：只读核对 subset/相关区设置语义，评估独立派生 DIC Job 的外扩场支持；同时继续其他可分析实验诊断。

## [2026-09-26] audit | MatchID S16 DIC 边缘重建设置证据

- 来源：S16 原始 `Job.m2inp` 的 `<Shape>`、subset/step 设置；MatchID 公开软件页与 Wiki。
- 结果：Job 注释将 Boolean `False` 定义为 Selection、`True` 定义为 Cutting；全局 subset/step 为 `15/3 px`。MatchID 公开软件页提到 2D DIC 边缘数据重建，但未说明它对 Selection ROI 的 subset 支撑规则；详细交互手册标为用户专属。
- 结论：公开资料不足以推导可复现的扩展 ROI 参数；MatchID 当前未运行。本轮未生成扩展 Job、未改写原始 Job/DAT，也未启动重算。
- 下一步：在可访问的本机手册或界面确认边缘/Selection 规则后，再评估独立派生 Job；其他实验诊断继续进行。
## [2026-09-26] experiment | PA12 自建 J2 平面应力材料点核

- 来源：项目阶段计划、现有有限变形 DIC 诊断及 Stage 2 虚功独立性审计。
- 更新：新增 `tools/pa12_j2_plane_stress.py`、`tests/test_pa12_j2_plane_stress.py` 和[材料点核说明](Agents/PA12实验数据处理/VFM自建/汇总/PA12自建J2平面应力材料点核.md)；修订总目标的直接执行子目标和 `index.md`。
- 方法：实现小应变增量 J2 关联流动、线性各向同性硬化及局部平面应力求解；以 `H>0` 定义硬化，并使用合成弹性解、屈服面/卸载和增量步长细化测试。
- 结论：4 项材料点合成测试通过；该核尚未接入实验 VFM。当前 DIC 为 `LOGEulerAlmansi` 且存在大变形，不能直接送入小应变核；真实实验 `Y/H`、虚功闭合及正式参数均未由此产生。
- 待验证：核实 DIC 位移/应变测度、剪切约定与旋转映射；实现有限变形平面应力弹塑性和匹配功共轭虚功后，再用合成非均匀场验证解析外功/已知参数回收，再进入逐帧实验诊断。

## [2026-09-26] audit | S16 DIC 输出应变与位移运动学交叉复核

- 来源：S16 `Job.m2inp` 的应变约定/单位设置、两帧 DAT 原始字段与同帧 DIC—力合并 CSV。
- 更新：新增 `tools/audit_pa12_dic_kinematics.py` 和局部仿射位移应变函数；生成两帧 CSV/JSON/Markdown 交叉审计结果；修正首审计帧的坐标重合数显示。
- 结果：所选 `000003.jpg`、`000257.jpg` 的导出 Exy 与位移导出张量剪切相比，误差均小于与工程剪切 `2e_xy` 的比较；DAT `gamma` 与导出应变主方向角最大差分别约 `0.944°`、`0.078°`。该结果支持工作假设，不是官方字段定义或 MatchID 滤波复现；局部拟合半径 15 px（1.308135 mm）是审计参数。
- 待验证：查明 Exy/gamma 官方语义和应变滤波定义；将位移/应变运动学接入经过合成变形、功共轭与参数回收验证的有限变形弹塑性 VFM。现有二维线性 Euler–Almansi 结果仍为诊断代理，不能发布实验材料参数。

## [2026-09-26] experiment | TC1000 源 STEP 加载比预筛

- 来源：`D:\PA12_Stage2\source_geometry_inspection\inputs\tc1000.step`。
- 更新：[加载比预筛报告](Agents/PA12双轴试样仿真/验证/2026-09-26_TC1000_载荷比预筛.md)、中心区指标 CSV、网格截图和指标图；Abaqus 原件保存在 `D:\PA12_Stage2\g0_tc1000_ratio_source_step_scan_20260926\`。
- 方法：固定 STEP、临时正交各向异性线弹性卡、C3D10/4 mm 网格与 `ΔX=0.05 mm`，仅改变 `ΔY` 为 0.025、0.05、0.10 mm；三档求解状态文件均报告成功结束。
- 结果：`r=1.0` 的中心区 `K=0.0011`、未加权积分点主评分 `0.06413`，在三档中最低；该工况作为后续几何筛选参考比值，不是全局最优结论。
- 限制：网格尚未收敛，材料卡为临时弹性参数；未评价塑性、边界柔度、DIC/VFM 可识别性或实验校准。
- 下一步：在 `r=1.0` 参考工况下完成槽端局部峰值网格收敛和边界敏感性，再接入实验标定材料与 FE–DIC 对照。

## [2026-09-26] experiment | 有限变形 J2 更新核与实验规模估算

- 更新：归档[有限变形 J2 材料点更新核](Agents/PA12实验数据处理/VFM自建/汇总/PA12有限变形J2材料点更新核.md)，记录 Hencky 弹性、乘法分解 J2、平面应力厚度求解、`P=τF⁻ᵀ`、测试和适用边界。
- 验证：有限变形材料点核 4 项合成测试通过；全量 `pytest` `145/145` 通过，`compileall` 及 GPT 状态/运动学审计 JSON 解析通过。双轴曲线图已人工检查：X/Y 共图、中文标签、线性段/屈服候选/峰值/已确认掉载终点齐全。
- 计算规模：200 次弹性材料点厚度求解约 `0.174 s`；按 S16 19,796 三角形、257 帧线性外推约 `1.23 CPU 小时/遍`，未含塑性分支和参数搜索。参数反演前需要批量求解并验证数值等价。
- 待验证：非比例加载/增量细化/耗散，非均匀合成场独立边界力与已知参数回收，批量厚度求解；之后接入实验逐帧 VFM。材料点测试通过不等于实验参数识别通过。

## [2026-09-26] refactor | 有限变形 J2 批量虚功与 Y0/H 合成反演

- 更新：`tools/pa12_finite_j2.py` 新增批量平面应力材料点更新、批量历史状态接口，并将有限 J2 逐帧内虚功积分改为批量单元更新；新增 `fit_finite_j2_yield_hardening` 直接拟合 Y0/H。
- 验证：批量与标量更新的混合弹性/塑性状态一致；空间非均匀弹性场回收 E；多轴加载—卸载合成历程回收已知 Y0/H。材料点专测 9/9、全库 `pytest` 151/151；compileall 与状态/审计 JSON 解析通过。
- 计算规模：19,796 单元批量材料点一帧约 0.335 s（弹性）和 0.596 s（全塑性测试态），厚度 τzz 残差最大约 `3.1×10⁻¹³/1.3×10⁻⁸ MPa`；S16 257 帧线性外推约 86–153 s/遍，不含参数优化多遍。
- 限制：Y0/H 回收使用同一核合成载荷，是拟合器/历程管理自洽检查，不是独立本构验证；实验 ROI 覆盖、单位伸长虚场外功边界条件和独立 ν 仍未满足。下一步做独立非均匀弹塑性外功测试，再运行 S16 诊断候选。

## [2026-09-26] experiment | TC1000 源 STEP 全局网格收敛

- 来源：`D:\PA12_Stage2\source_geometry_inspection\inputs\tc1000.step`；三档 Abaqus ODB。
- 更新：新增[全局网格收敛报告](Agents/PA12双轴试样仿真/验证/2026-09-26_TC1000_网格收敛.md)、逐网格 CSV 和趋势图；中心区后处理改为固定质心 ROI 与 `IVOL` 体积加权，并新增对应回归测试。
- 方法：C3D10、临时正交各向异性线弹性材料、`ΔX=ΔY=0.05 mm`，比较 `h=4/3/2 mm`；固定 `28×28 mm` XY ROI，按单元质心选点并对积分点体积加权。
- 结果：三档 ROI 体积约 `784.86–785.23 mm³`；主评分为 `0.133574/0.136226/0.133861`，相邻变化 `+1.986%/−1.736%`，满足当前 `<5%` 全局主指标门槛。
- 限制：应变为 ODB `LE`，均值约 `0.0433%`，本轮小位移不是目标实验应变；材料仍为流程临时弹性卡，未验证局部峰值、塑性、断裂、边界柔度、DIC 或 VFM 参数恢复。
- 下一步：定位狭缝端部和减薄过渡并检查局部峰值网格敏感性；进行边界敏感性分析，再依据 X/Y/Z 向实验标定材料并接入 FE–DIC/VFM。

## [2026-09-26] experiment | TC1000 源 STEP 端面耦合敏感性

- 来源：同一源 STEP 的 `h=3 mm` 刚性端面基线与分布式均匀耦合 ODB。
- 更新：新增[边界敏感性报告](Agents/PA12双轴试样仿真/验证/2026-09-26_TC1000_边界敏感性.md)、CSV 和对照图；参数化扫描脚本新增 `--coupling-mode`，默认保持 `kinematic`，并可指定 `distributing`。
- 方法：固定 ROI、网格、载荷和临时材料，只改变耦合类型；分布式模式按 `UNIFORM` 权重，四端面 `.inp` 关键词和成功求解状态均已核实。
- 结果：分布式相对刚性耦合主评分变化 `−3.570%`；四项 CV 变化约 `−3.53%` 至 `−3.64%`；中心平均应力/应变变化约 `−0.57%`。
- 限制：边界敏感性不是物理边界确认；尚未纳入真实夹具接触、滑移/转动、材料非线性、局部峰值或实验场验证。
- 下一步：确认实物夹具边界证据，之后执行狭缝端部/减薄过渡峰值网格检查，并在标定材料下复核。

## [2026-09-26] experiment | TC1000 中心过渡带峰值筛查

- 来源：`D:\PA12_Stage2\g0_tc1000_global_mesh_convergence_20260926\` 中 `h=4/3/2/1.5 mm` 刚性耦合 ODB 与 `h=3 mm` 分布式耦合 ODB。
- 更新：新增[中心过渡峰值网格检查报告](Agents/PA12双轴试样仿真/验证/2026-09-26_TC1000_中心过渡峰值网格检查.md)、峰值坐标/指标 CSV 和三联趋势图；后处理输出单元质心近似位置、中心/过渡带峰值和 `G_transition_Mises`。
- 方法：固定 `28×28 mm` ROI，另取 `14 < max(|x|,|y|) ≤ 16 mm` 中心过渡筛选带；按积分点提取 Mises 峰值，用相应区域峰值之比计算集中系数。现有 ODB 重用同一后处理脚本，无重复求解。
- 结果：四档峰值为 `2.4214/2.1463/2.1798/2.1865 MPa`，集中系数为 `1.9686/1.7220/1.7341/1.6740`；`h=3/2/1.5 mm` 两项指标相邻变化最大分别为 `1.56%/3.47%`，`h=4→3 mm` 仍变化 `−11.36%/−12.53%`。全模型峰值均处于中心过渡筛选带。
- 验证：6 项中心区/峰值/过渡带指标测试通过；5 份 ODB 均成功完成同版后处理；峰值图已目视核对。
- 限制：网格为全局均匀种子，未完成 STEP 特征级局部加密/梯度核查；中心应变仍约 `0.0433%`，临时弹性材料、真实夹具边界、塑性/断裂、DIC/VFM 仍未验证。
- 下一步：按 STEP 实体定位狭缝端部与减薄边界并开展局部加密；同步推进实际夹具映射和 X/Y/Z 向材料标定，再进入实验加载区间下的 FE–DIC/VFM 验证。

## [2026-09-26] refactor | 有限应变 J2 弹性 E 闭式拟合

- 更新：`fit_finite_j2_youngs_modulus` 改为 `E=1 MPa` 单次内虚功积分，再以非负标量最小二乘缩放；移除失效的 E 初值参数。更新[有限变形 J2 材料点核记录](Agents/PA12实验数据处理/VFM自建/汇总/PA12有限变形J2材料点更新核.md)及首页索引。
- 验证：有限应变 J2 专测 `10/10` 通过；非均匀弹性场恢复已知 E，且拟合只调用一次积分器。该简化仅用于固定 ν、未屈服弹性分支。
- 状态：S16 主 Job ROI 与 DIC subset 内缩域的 50%/75%/100% 参数窗口及逐帧虚功作业仍在运行，尚无 CSV/图可审；实验参数未确认或放行。
- 下一步：作业完成后核验两域各 257 帧、内外虚功残差、覆盖率与窗口漂移；随后补独立非均匀弹塑性合成外功验证。

## [2026-09-26] experiment | 阶段2文献参数与 L18 几何 DOE 审计

- 来源：本地论文 MinerU 定位 `doc:b39265e/tier:standard/page:17-37`；D 盘 `D:\PA12_Stage2\generated\DOE-L18-01` 至 `DOE-L18-18` 的模型清单、指标 JSON、求解状态和预览图。
- 更新：新增[阶段2文献与 L18 审计页](Agents/PA12双轴试样仿真/验证/2026-09-26_阶段2文献与L18几何DOE审计.md)、L18 汇总 CSV 和三张顶视图。
- 结果：18/18 L18 `.sta` 成功；`primary_score` 与四项应力/应变 CV 之和完全一致。论文参考设计为中心厚度 1 mm、每臂 7 槽、槽长 40 mm、圆角 3 mm、槽端距 0.2 mm；SLS 方向口径为 XY 打印平面、Z 构建方向。
- 限制：L18 为直接草图、中心厚度 2 mm、等双轴、临时弹性模型，未与源 STEP 回归；中心样本数 864–4924 且分数强分组，不能据此定最优。论文式 (2.19) 负号与正硬化模量冲突，文献参数不进入正式材料卡。
- 下一步：以真实 tc1000 STEP 建几何回归锚点，逐项测出关键平面参数并固定 ROI/网格采样，再启动与文献设计一致的候选比较及加载比验证。

## [2026-09-26] ingest | PA12 双轴十字试样论文全文研读

- 来源：本地本科毕业设计 PDF，MinerU `doc:b39265e/tier:standard/page:1-45`；原件保持在外部数据目录，只读解析。
- 更新：新增[全文研读卡](wiki/literature/PA12双轴十字试样优化与DIC验证_全文研读.md)；补充[中心区均匀性筛选方法页](wiki/methods/PA12双轴中心区均匀性筛选.md)、阶段2 DOE 审计页和首页索引。
- 结论：论文报告的几何参考组合为中心厚度 1 mm、每臂 7 槽、槽长 40 mm、R3、槽端距 0.2 mm；实验以等双轴为主，XZ 屈服点偏离各向同性 Von Mises 面。DIC 证明的是其试样的中心应变/断裂位置趋势，不是本项目 VFM 参数回收。
- 待验证：论文式 (2.19) 的负硬化斜率与正 `H=180 MPa` 冲突；将文献尺寸逐项映射到源 STEP、确认 XY/Z 与实物材料轴关系，并继续做非等双轴实验加载比和方向相关材料验证。

## [2026-09-26] refactor | PA12 总目标拆分诊断交付与正式参数发布

- 更新：修订 PA12 总目标为双轨验收：诊断交付不再被正式物理证据门槛阻塞；正式 E/ν/Y/H/J2 参数须独立满足 ROI/厚度/边界、本构/测度、虚功闭合、稳定性与留出要求。更新 GPT 交接文档与机器状态，明确 S16 当前接续点和唯一执行顺序。
- 诊断流程：为 S16 有限变形 J2 runner 增加按域/拟合窗口单独运行、每窗口落盘逐帧诊断与 JSON 检查点、开始/完成进度信息，避免整批结束才写结果。
- 验证：runner 与 J2 定向测试 `12 passed`；runner 编译通过；`git diff --check` 无空白错误（仅有仓库既存 CRLF 转换提示）。
- 当前执行：完整 Job ROI 的 50% 窗口正在运行，PID `30152`；不能将尚未写出的拟合结果作为完成。另一个较早的同类运行进程不由本轮启动，不做干预。
- 限制与下一步：S16 DIC 面积覆盖率仍为 `89.2248%`，Press 广义外功边界条件仍待证，Y0/H 仅可标诊断候选；单窗完成后审计结果，再按检查点继续其余域/窗口，并行推进其他实验诊断和独立非均匀弹塑性外功测试。

## [2026-09-26] audit | S16 长时窗口运行状态更正

- 状态：本轮启动的单窗进程在 20 分钟无窗口结果后已停止，检查点未标记完成；不能将其记作拟合结果。
- 现场：另一个较早启动的同配置全量 runner 仍活跃，所有后续运行须先查询进程和目标目录，避免同目录并发写入；不对不属本轮启动的进程作干预。
- 更新：交接状态已改为不硬编码 PID，启动前检查活动 runner/检查点。外层 Y0/H 拟合停止阈值改为 `1e-8`，内部厚度平面应力求解精度未改；阈值契约与已知合成 Y0/H 回收测试 `2 passed`。
- 下一步：执行全部有限变形 J2 专测；旧进程退出后，以单域/单窗方式重启并审计，任何候选仍不得作为正式参数。

## [2026-09-26] refactor | PA12 目标队列调整与长时 J2 拟合评估

- 目标：诊断交付与正式材料参数发布分轨；单项真实 J2 优化不得阻塞现有 10 组曲线、同步、DIC 质量/覆盖及已生成虚功/残差的复核交付。
- 实现：J2 runner 新增单域/单窗 CLI、逐窗口输出、检查点续接与稳定性 CSV 累计；外层 Y0/H 优化阈值设为 `1e-8`，局部厚度平面应力精度保持不变。
- 运行评估：旧版全量 runner 和隔离新版单窗均未在 20 分钟内完成首个窗口；新版试跑已停止，checkpoint 显示零完成窗口。更早的同配置进程仍活跃，启动新运行前必须核查活动进程/输出，不能并发写入。
- 验证：全仓 `163 passed`；`compileall`、3 份 touched JSON 解析、`git diff --check` 通过；原始 `raw/` Git 状态为空。Git 只提示若干既存 LF→CRLF 转换警告。
- 下一步：继续现有诊断产物的交付审计；独立完成非均匀弹塑性外功闭合/参数回收测试并量化单次 objective evaluation，先验证可复现的提速方案，再恢复真实 S16 参数窗口。无正式 PA12 参数发布。

## [2026-09-26] audit | PA12 既有同步、曲线与 Stage A 输出复核

- 检查范围：对照批次配置、实验清单、照片—力表、X/Y 单列力 CSV、10 组应力—应变 CSV/PNG/报告及 8 组 Stage A 内外虚功派生结果。
- 结果：目录/概览/索引审计 `audit_passed=true`；8 组同步三件套数量逐组相等；Stage A `8/8` 实验、`1127` 帧内部一致性通过。10 组应力—应变状态为 `PASS=6`、`REVIEW_REQUIRED=3`、`PRELOAD_RELEASE_ONLY=1`。
- 限制：同步三件套全部就绪标志为否，原因是 S23 为断裂力缺失的数据受限组、S24 为预载释放；并非 8 组可用数据的行数不等。S15 无有效峰后段、S22 峰后掉载比 `0.207442` 未达 `0.20` 自动门槛、S23 断裂照片 `001547.jpg` 晚于最后有力照片 `001528.jpg`；均维持人工复核，不补造或自动放行。
- 更新：刷新同步输出契约、曲线审计和 Stage A 一致性审计报告/JSON；原始目录仍无 Git 变更。
- 下一步：完成非均匀弹塑性独立闭合测试和 J2 性能优化，物理证据缺口仍只限制正式参数发布。

## [2026-09-26] experiment | TC1000 五厚度源 STEP 表面描述回归

- 来源：`D:\PA12_Stage2\source_geometry_inspection\BASE-TC-*_source_topology.json` 与 `D:\PA12_Stage2\g0_rounded_baselines\G0-BASE-TC-*\topology.json`。
- 更新：新增[五厚度几何回归报告](Agents/PA12双轴试样仿真/验证/2026-09-26_TC1000_五厚度源STEP表面描述回归.md)和 CSV；D 盘及 Vault 各保存一份逐模型结果；更新仿真流程、阶段2 DOE 审计和 `index.md`。
- 方法：源 STEP 的 Z 坐标平移 `+1.5 mm` 与参数模型对齐；比较实体拓扑计数、外包围盒及逐面面积/空间包围盒多重集，精度 `1e-6`。
- 结论：中心厚度 1.0/1.5/2.0/2.5/3.0 mm 五档均为单实体，计数与包围盒一致，逐面描述差异数为 0，判定为表面描述级通过。
- 限制：生成侧未导出逐边几何记录，因此不宣称精确 B-rep 等价；该结果不覆盖 L18 直接草图候选。模型材料仍为临时值，本次未求解新工况。
- 下一步：逐样本闭合打印材料轴—加载机通道—DIC 图像坐标映射，并以合格 X/Y/Z 数据建立独立材料标定；映射和标定通过前，不按临时材料分数发布设计排名。

## [2026-09-26] refactor | 有限变形 J2 参考网格逆矩阵复用

- 更新：虚功积分器将参考三角形边矩阵的逆移至时间帧循环外，每个网格仅计算一次并复用于各帧；不改变变形梯度公式、本构、ROI、载荷或参数定义。
- 验证：新增三帧回归测试，确认旧实现调用 3 次参考矩阵求逆、更新后只调用 1 次；有限变形 J2 专测 `13/13` 通过。
- 状态：这只消除了逐帧重复的固定几何运算；Y0/H 优化仍需逐候选重放历史，S16 完整双域/多窗口实验结果尚未审阅，不能发布为正式材料参数。

## [2026-09-26] audit | G1 材料—试验机—DIC 坐标变换矩阵

- 读取范围：`AGENTS/PA12双轴试样仿真与实验全流程.md`、`index.md`、PA12 总体方法协议、S15–S24 批次配置、单轴映射复核、阶段 2 坐标预检、D 盘打印方向图；只读检查外部数据目录中的构建/方向记录文件名。
- 更新：[G1 坐标变换矩阵](Agents/PA12双轴试样仿真/验证/2026-09-26_G1材料-机器-DIC坐标变换矩阵.md)、`index.md`。
- 结论：双轴 S15–S18 的机器 X→DIC y、Y→DIC x 轴置换可用于现有诊断；S19–S21 与 S22 仍是不同的单轴候选映射。已确认打印层面 XY/构建 Z 和 STEP 厚度轴，但没有逐样本打印材料轴到机架的变换。外部目录未找到打印平台/构建任务记录；DIC `orientation_report` 只评估图像参考轴角度。
- 待验证：试样编号到打印布局/构建任务的映射；各组机器通道、夹具方向、DIC 旋转/镜像/正负号和材料 X/Y/Z 的有向闭合。闭合前材料主轴归属、正式 E_X/E_Y/E_Z 与正式设计排名均不放行。
- 下一步：取得打印批次布局或有轴标记的装夹记录，补齐逐试样变换登记；同时保持候选映射诊断与正式参数发布隔离。

## [2026-09-26] audit | 单轴机台应变与 DIC 全场方向响应核验

- 来源：S19–S22 的 DIC—力索引、逐帧合并全场和应力—应变派生表；原始 JPG/DAT/XLS 只读。
- 更新：[G1 坐标变换矩阵](Agents/PA12双轴试样仿真/验证/2026-09-26_G1材料-机器-DIC坐标变换矩阵.md)、[VFM 阶段 I 单轴映射复核](Agents/PA12实验数据处理/VFM自建/汇总/PA12自建VFM阶段I单轴机器轴与DIC轴映射复核.md)、[逐组核验 CSV](Agents/PA12双轴试样仿真/验证/2026-09-26_G1_机器位移-DIC轴向响应核验.csv)；CSV 同步保存于 `D:\PA12_Stage2\g1_coordinate_mapping_20260926\`；更新 `index.md`。
- 方法：索引帧状态全为 READY；按机台轴力 `>5 N`、正机台名义应变、峰前力区间筛选；相关分析要求机台应变至少为峰前最大值的 `15%` 且 `≥0.002`。用逐帧有效 DIC 点的 Exx/Eyy 均值计算 Pearson r 和线性斜率。
- 结果：S19/S20/S21/S22 的 `r(Eyy,机台应变)=0.99997/0.99492/0.95116/0.99927`，`r(Exx,机台应变)=-0.99110/-0.99131/-0.93642/-0.99900`；支持单轴加载方向对应 DIC y、横向对应 DIC x 的轴序候选。
- 限制：复用现有照片时间—机台位置同步与 `30 mm` 工作标距；时间序列相关性不是独立样本统计或硬件标定，不能识别坐标正负号、镜像或打印材料轴方向。S19–S22 仍为 `REVIEW_REQUIRED`，不发布正式参数。
- 下一步：将该轴序用于候选级诊断；继续补齐构建布局/有向设备坐标证据，并在正式材料标定前解决 S22 单轴几何、外功边界和留出点不足。

## [2026-09-26] audit | S16 现有自建 VFM 内外虚功曲线复核

- 输入：完整 Job ROI 尺度诊断与 DIC subset 内缩域敏感性各自的 `逐帧虚功诊断.csv/.png`；原始 DIC—力合并数据保持只读。
- 核验：两域各 257 帧，照片唯一、时间单调、数值列无缺失；照片和时间对齐，X/Y 外虚功序列一致；两张图与 CSV 趋势一致。Job ROI 的 DIC 覆盖率为 89.2248%，subset 内缩域为 100%。
- 结果：完整历程 X/Y 残差 RMS 分别为 4946.23/4992.54 N；内缩域为 4931.64/5007.02 N。图中内虚功与外虚功在后段明显分离，末帧外力掉载。
- 判读：这些是有限运动学线性平面应力诊断曲线，不是弹塑性 J2 结果；不能宣称虚功闭合或参数识别通过。两域结果保留为现有诊断证据，不重复生成或合并。
- 下一步：继续审计独立 J2 拟合窗口；只有 J2 计算完成并通过覆盖率、残差和窗口稳定性审查后，才发布对应 J2 内外虚功曲线及参数候选。
## [2026-09-26] experiment | PA12 目标修订与非均匀弹塑性虚功分解

- 更新：[总目标与阶段计划](Agents/PA12实验数据处理/处理记录/PA12总目标与阶段计划.md)修订为依赖驱动并行执行；诊断交付不再等待正式物理参数门槛，S16 J2 需先通过单域单窗口资源预算基准。更新 GPT 交接及 `index.md`。
- 验证：新增非均匀塑性应力场的边界/界面弱形式虚功分解函数与合成测试；RED 阶段确认 API 缺失，GREEN 后专项 `tests/test_pa12_finite_j2.py` 为 `14 passed`。
- 结论：`∫P:Grad(v)` 等于外边界虚功加单元界面牵引跳跃项；非平衡局部场下边界项单独不闭合。该测试验证离散积分分解，不构成独立本构参数回收。
- 运行状态：S16 全量 runner PID 45360 仍活动，超过一小时检查点为 0 窗口完成；未在相同输出目录另起任务，后续转隔离目录限时单窗基准。
- 下一步：补解析平衡场/已知边界牵引测试；并行审计现有 10 组诊断产物；按基准决定 J2 提速或分块策略。

## [2026-09-26] verify | PA12 弱形式解析边界牵引与全仓回归

- 测试：常量第一 Piola 应力场在矩形三角网中，单元界面牵引贡献抵消；解析边界牵引按 `t=P·N` 积分得到的外虚功与 `∫P:Grad(v*)dA` 内虚功一致。将所有单元节点方向翻转后结果不变。
- 限制：此合成场确认单位伸长虚场下广义力的数学条件，不验证实际夹具其他边界功为零，也不验证 PA12 本构参数恢复。
- 验证：`python -m pytest -q`，`166 passed`；代码编译、交接 JSON 解析、`git diff --check` 通过；`raw/` 未修改。
- 下一步：构造独立已知参数非均匀弹塑性回收测试；旧 S16 全量 runner 仍为活动状态且未完成窗口，不在其目录并发运行。

## [2026-09-26] verify | PA12 独立解析载荷生成的 J2 参数恢复

- 方法：由一维单调 J2 的解析关系 `τ=Y0+H·εp`、`εe=τ/E`、塑性横向 Hencky 应变 `−εp/2` 构造 41 帧均匀变形；按参考构形第一 Piola 合力作为独立观测，不调用生产材料点更新器生成载荷。
- 结果：生产有限变形 J2/VFM 对 `Y0=18 MPa`、`H=120 MPa` 的回收测试通过，设定相对误差容限 1.5%；全仓测试 `167 passed`。
- 限制：这是均匀单轴解析合成路径，不验证空间非均匀/双轴可辨识性、噪声稳定性或真实 PA12 参数。
- 下一步：扩展空间非均匀/双轴合成识别及噪声/窗口稳定性；隔离目录内测 S16 单域单窗计算预算。

## [2026-09-26] audit | S16 有限变形 J2 单窗运行预算

- 输入：隔离目录配置 `configs/pa12_finite_j2_s16_window_validation.json`，仅 `full_job_roi`、50% 峰前加载窗；不与旧全量任务共享输出目录。
- 结果：限时 10 分钟后仍未完成该窗口，检查点 `completed_windows=[]`；隔离任务已停止，原始输入未写入，旧全量 runner PID 45360 保持活动。
- 判定：当前全分辨率历史依赖拟合不适合直接扩展到双域/多窗口批处理。后续先验证低成本空间预拟合/分层积分的精度，再重跑隔离窗口基准。

## [2026-09-26] audit | PA12 曲线与 Stage A VFM 帧数交叉核对

- 范围：只读比较 `PA12应力应变曲线审计.json`、`PA12自建VFM阶段A一致性审计.json` 和 `PA12自建VFM结果.csv`。
- 结果：曲线审计 9 组，Stage A 与 VFM 汇总各 8 组。共同 8 组的应力—应变行数、Stage A 虚功帧数、VFM 汇总帧数完全一致，无帧数差异。
- 例外：曲线侧仅多出 S23；其断裂视觉帧无同步力支持，按既定资格规则未纳入 Stage A。S24 为预载释放，仅属排除记录。
- 判读：索引数量契约通过不等于虚功闭合或参数识别通过；8 组 VFM 仍按各自 `SELF_VFM_REVIEW_REQUIRED` 条件状态解释。

## [2026-09-26] audit | Stage F S18 ν 剖面残差带端点复核

- 输入：S15–S18 Job ROI `E_nu_profile.csv`，用 `RMSE(ν) ≤ 1.01 × min(RMSE)` 重算 1% 残差带。
- 结果：S15、S16、S17 报告端点与逐点 CSV 相符；S18 原报告下限 `0.475` 超过 1% 阈值，首个符合阈值的网格点为 `ν=0.476`。
- 更新：将[阶段 F 可辨识性报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12自建VFM阶段F泊松比可辨识性.md)下限更正为 `0.476`；不改变“ν 未独立识别”的结论或任何参数。

## [2026-09-26] audit | S19 单轴几何模型来源核验

- 来源：S19 原始 DIC 目录、`moxing/README_厚度模型顺序.txt`、`moxing/verification.json` 和 [PA12 数据源登记](raw/datasets/PA12数据源登记.md)；原始资料只读。
- 结果：S19 目录有 DIC Job/MTI/VFM 与 JPG/DAT，没有 S19 专属 STEP、DXF 或尺寸图。共享 `moxing` 中 5 个厚度 STEP 的 README 明确其为 PA12 双轴十字试样中心减薄系列，平面设计为 30 mm 臂宽和狭缝；附加 `finally.step` 也未登记为 S19 模型。
- 结论：双轴模型中的中心 1 mm 厚度、30 mm 臂宽及十字试样积分域不能作为 S19 单轴几何事实。S19 的厚度、有效宽度、标距、Polygon 积分域及单轴外功定义仍未确认，参数识别门槛保持关闭。
- 下一步：取得与 S19 样品编号对应的图纸、实测试样尺寸或夹具/标距记录；证据到位前只保留 S19 为曲线/数据候选，不套用双轴模型。

## [2026-09-26] experiment | PA12 有限变形 J2 均匀等双轴合成恢复与噪声敏感性

- 方法：使用独立等双轴 Hencky-J2 解析路径生成 `8×8 mm`、18 三角形、31 帧均匀平面应力全场及参考构形边界合力；固定 `E=2100 MPa, ν=0.35`，拟合已知 `Y0=18 MPa, H=120 MPa`。对首帧之后的 X/Y 力分别加入峰值力 0.1%、1%、5% 的独立高斯扰动，各用 5 个种子。
- 结果：无噪声恢复 `Y0=18.00000000000015 MPa`、`H=119.9999999999998 MPa`，虚功残差 RMS `1.11×10⁻¹² N`；缩放灵敏度矩阵秩 2、条件数 17.5143。5% 力噪声下 H 相对误差范围 `−7.863%…+17.440%`，中位绝对误差 `7.863%`。
- 输出：[审计说明](Agents/PA12实验数据处理/VFM自建/汇总/PA12有限变形J2等双轴合成稳定性审计.md)、[逐种子 CSV](Agents/PA12实验数据处理/VFM自建/汇总/PA12有限变形J2等双轴合成噪声敏感性.csv)。
- 限制：同质、均匀、比例等双轴合成场；固定 E/ν；不包含空间应变梯度、局部化、相关噪声、实际边界/同步不确定性。不是 PA12 实验参数或非均匀场验证。
- 下一步：完成空间非均匀弹塑性全场的独立已知参数及边界外功闭合验证，再决定是否启动隔离目录的 S16 单域单窗口预算测试。

## [2026-09-26] optimize | 有限变形 J2 平面应力求根

- 范围：`tools/pa12_finite_j2.py` 的批量平面应力更新；不改变材料模型、求根变量、收敛阈值或 VFM 残差定义。
- 修改：厚度伸长求根的中间迭代只计算 `τzz`；塑性梯度恢复、张量指数映射、Cauchy/Piola 应力只在最终收敛伸长处计算。
- 验证：回归测试先失败，测得两点塑性批次完整指数映射调用 `14` 次；改后断言并验证为 `2` 次。`tests/test_pa12_finite_j2.py` 为 `18 passed`，J2 材料点、平面应力与 runner 三个测试文件合计 `23 passed`。
- 微基准：同一 2,048 点合成场从 `0.063 s` 降至 `0.028 s`；批量特征值分解调用 `24` 次降至 `10` 次，塑性点数与面外应力残差一致。该局部微基准不代表全历程拟合加速比。
- 运行状态：PID `45360` 已核实为 S16 全量 J2 runner，使用 `configs/pa12_finite_j2_s16.json`，在本次代码修改前启动；截至检查时进程仍运行、检查点完成窗口数为 0。按同目录运行约定未中断或另起并发任务。
- 待验证与下一步：旧运行完成后审查窗口及参数；若仍无法按预算产出，在独立输出目录执行优化版单域/单窗对照，测量整段拟合墙钟时间并核对结果容差。任何阶段均不据此发布正式 PA12 参数。

## [2026-09-26] optimize | J2 单次材料点状态逆矩阵复用

- 范围：`tools/pa12_finite_j2.py` 的批量平面应力材料点更新；材料状态仅在本次局部厚度求根过程中复用，不跨实验帧复用或近似。
- 修改：将不随厚度伸长试算变化的逆塑性梯度提升到本次批量更新入口计算一次，供所有残差试算共用。
- 验证：新增测试先失败并记录两点塑性批次调用 8 次矩阵逆，修改后通过断言降为 2 次（一次逆塑性梯度、一次最终变形梯度）。J2 材料点测试 `19 passed`，J2/VFM 三个相关测试文件 `24 passed`，全仓 `169 passed`。
- 微基准：2,048 点单帧更新由原始版本 `0.063 s` 降至两项优化后的 `0.025 s`；批量特征值分解 `24→10` 次，矩阵逆 `8→2` 次；塑性点计数为 457，最大 `|τzz|=2.08×10⁻⁷ MPa`。不得外推为整段拟合加速比。
- 运行状态：旧 S16 全量 runner PID `45360` 仍在运行，使用 `configs/pa12_finite_j2_s16.json`，检查点无已完成窗口；该实例在优化前启动，未中断且未并发写入其输出目录。
- 下一步：等待旧运行状态变化并审核其首个窗口；其后在独立目录执行优化版单域/单窗全历程对照，验证真实墙钟、参数恢复和窗口残差稳定性。

## [2026-09-26] plan | PA12 总目标改为依赖驱动的双轨验收

- 调整：诊断交付线继续完成所有现有数据支持的曲线、逐帧内外虚功、覆盖/残差、可辨识性与复现文档；正式材料参数/J2 发布单独受几何、边界、测度、本构、闭合、稳定性和独立验证门槛约束。MatchID 不作为项目完成条件。
- 预算：旧 S16 全量拟合超过一小时仍无完成窗口，不再作为总体任务前置条件；保持其运行现场，不与其输出目录并发写入。
- 验收：只运行分层三角积分的两个专项合成测试，检查均匀场总面积/空间覆盖及等双轴已知参数回收，结果 `2 passed`。尚未验证非均匀场近似误差或 S16 单窗拟合耗时，故不据此宣称实验 J2 通过。
- 接续：先评估非均匀合成场的预拟合与全网格精修参数差异，再在隔离目录测 S16 单域单窗口时间；并行收束 10 组曲线、8 组 Stage A/VFM 诊断交付。原始 JPG/DAT/XLS 只读。

## [2026-09-26] verify | 有限 J2 runner 回归与 S16 分层窗口基准

- 回归：`tests/test_pa12_finite_j2.py`、`tests/test_pa12_finite_j2_runner.py`、`tests/test_pa12_finite_kinematics.py`，`35 passed`。
- 基准观察：隔离配置 `configs/pa12_finite_j2_s16_stratified_window.json` 的 PID `25712` 正在执行 `full_job_roi / 50%`；观察已超过 10 分钟，进程仍响应且 CPU 时间增长，检查点 `completed_windows=[]`、尚无窗口输出。该状态是运行预算风险，不是材料参数结果。
- 运行处置：保留 PID `25712` 和旧 PID `45360`；未触碰其进程或输出。另一个重复基准由当前会话启动后发现，已仅停止当前会话的重复进程，避免争抢同一计算资源；其独立空检查点未作为结果使用。
- 接续：继续观察 PID `25712` 的同一检查点；进程完成后审阅分层预拟合值、全网格精修值、nfev、耗时、全程内外虚功和残差。若仍无窗口产物，不重启同一重计算，转向可并行的诊断交付和性能根因分析。原始 JPG/DAT/XLS 只读。

## [2026-09-26] experiment | PA12 有限变形 J2 分层预拟合与全网精修

- 更新：有限变形 J2 积分器增加面积加权三角求积；runner 按域/窗口执行分层预拟合，并将其 `Y0/H` 仅用作全三角网无权重精修初值；主/隔离配置、材料核说明、阶段计划、交接与 `index.md` 已同步。
- 合成基准：12×12 mm 网格、288 个三角形、41 帧平滑空间非均匀等双轴位移；目标 32 个代表单元实际选中 30 个。预拟合 `Y0/H` 相对误差 `0.0167%/0.0119%`、耗时 `0.643 s`；全网精修 7 次评估、`2.892 s`，恢复输入参数。
- 验证：加权参数恢复、满网预算退化、两阶段 runner 数据流及现有 J2/runner 回归共 `25 passed`；全仓 `174 passed`。本合成载荷由同一 J2 核生成，仅为数值积分/初值精度证据。
- 口径：完整 Job ROI 保持主分析域，但 S16 仅有 `89.2248%` DIC 支持，不补缺失场；内缩域单独作敏感性，沿用整 ROI 机器合力，不能解释为自身边界闭合或独立材料识别。
- 运行状态：旧 S16 PID `45360` 仍活动且 `completed_windows=[]`，未与其目录并发写；上述合成基准不等于 S16 实验窗口验证，当前无正式参数。
- 下一步：在全新隔离输出目录运行 `full_job_roi + 50%` 单窗口，核对实际墙钟、全网精修参数/残差及覆盖状态；再单独复核 subset 敏感性。原始 JPG/DAT/XLS 保持只读。

## [2026-09-26] audit | S16 分层 J2 峰前 50% 全网格窗口

- 输入/配置：`configs/pa12_finite_j2_s16_stratified_window.json`；`full_job_roi`，峰前 50%，拟合帧 `000001.jpg–000128.jpg`，该窗上限配置为 `000256.jpg`；同次全历程诊断输出 257 帧。
- 计算：分层预拟合 506/19,796 个三角形，`Y0=97.9357 MPa`、`H≈8.08×10⁻¹¹ MPa`、残差 RMS `40.481 N`、耗时 `20.328 s`；全网格精修 `Y0=95.9710 MPa`、`H≈1.01×10⁻¹⁹ MPa`、残差 RMS `38.873 N`、5 次评估、耗时 `711.111 s`。`H` 落在非负约束下界附近，按近零硬化候选解释，不声称真实 PA12 硬化为零。
- 全历程/覆盖：257 行逐帧文件连续覆盖 `000001–000257.jpg`，时间严格递增、数值有限、首帧 X/Y 外功为 0；全程残差 RMS `156.703 N`，最大绝对残差 X/Y `1489.137/1516.683 N`；DIC 网格只覆盖 Job ROI 面积 `89.2248%`，结果状态 `REVIEW_REQUIRED`，不补缺失场。
- 物理解读：峰后末帧力快速掉载，但无损伤 J2 内虚功未相应下降，留下约 1.5 kN 残差；该末帧是断裂/模型适用性诊断，不参与训练。固定 `E=3507.812 MPa, ν=0.375`，外功边界等价仍需独立证据，所有 Y0/H 仅为条件诊断候选。
- 报告修正：窗口 Markdown/JSON 原将配置峰前上限 `000256.jpg` 写成 50% 窗实际终帧；新增 `window_fit_end_photo=000128.jpg` 并保留配置上限字段。新增 runner 回归测试先复现旧错误后通过；J2 材料点、runner、运动学相关测试 `35 passed`。
- 下一步：对照同配置的第二次隔离复算完成与否；随后用独立输出比较 75%/100% 窗口的参数稳定性及适用区间，不把本单窗口结果升级为材料参数。S23 断裂力缺失不补造、S24 不作拉伸；原始数据只读。

## [2026-09-26] verify | S16 50% 窗口重复性与拟合终帧报告

- 独立复算：`configs/pa12_finite_j2_s16_stratified_window_validation.json` 在单独输出目录重复 `full_job_roi / 50%`。最终 `Y0=95.9709747451 MPa`、`H=1.0131788453×10⁻¹⁹ MPa`、拟合残差 RMS `38.8733756 N` 与首跑一致；预拟合/精修耗时分别 `22.697/695.504 s`，首跑为 `20.328/711.111 s`。两次均 506/19,796 个三角形预拟合、5 次全网格目标函数评估。重复性只证明该数值流程在同一输入下可复现。
- 根因修复：`_fit_windows` 返回窗口终帧 `000128.jpg`；总摘要原误将配置峰前上限 `000256.jpg` 写作实际终帧。保留既有 `fit_end_photo` 上限语义，新增 `window_fit_end_photo`；Markdown 分列实际区间与上限。先新增回归断言观察到旧值失败，再修改实现，专项 runner 回归 `1 passed`，J2/runner/运动学测试 `35 passed`。两个 50% 窗口派生摘要均更正。
- 并行作业：PID `30172` 执行 `full_job_roi / 75%`，PID `24060` 执行 `dic_subset_inset_sensitivity / 50%`；输出目录相互隔离且未完成。旧全量 PID `45360` 仍保留。当前没有正式参数发布。

## [2026-09-26] plan | PA12交付目标纠偏与窗口敏感性更新

- 目标：明确完整有效区间曲线是诊断交付；双轴 X/Y 叠加同图，单轴只画加载方向。显示可以平滑但源 CSV/原始值不改；事件标记需能从数据核验。检查图只显示力曲线、起点/峰值/掉载/有效区间和照片采样点。J2 长窗口不得阻塞其他诊断交付。
- 证据更新：S16 75% 主域窗口完成，`Y0=88.621847 MPa`、`H≈0`、拟合 RMS `75.3948 N`、全历程 RMS `114.5413 N`、精修约 `1051.605 s`；相对 50% 主域 `Y0=95.970975 MPa` 漂移约 −7.7%。50% 内缩域 `Y0=90.651958 MPa`，沿用完整 Job ROI 合力，只作敏感性。各候选 `H` 均在非负下界附近，参数稳定性未通过。
- 更新：[总目标与阶段计划](Agents/PA12实验数据处理/处理记录/PA12总目标与阶段计划.md)、[有限变形 J2 窗口审计](Agents/PA12实验数据处理/VFM自建/汇总/PA12有限变形J2分层预拟合与全网精修审计.md)、GPT 交接与状态、材料核说明、`index.md`。
- 运行：PID `46440` 仍运行一个隔离 100% 窗口；另一个隔离目录检查点未完成且没有活动进程，不能视为结果。旧 PID `45360` 仍活动但不作为诊断交付前置条件。
- 验证：全仓 `pytest` 为 `175 passed`；`compileall`、交接状态 JSON 解析及 `git diff --check` 通过。应力—应变审计为 6 组 PASS、3 组 REVIEW_REQUIRED、1 组预载释放；所有已生成 CSV 行数与照片清单一致、PNG 有效。Stage A 帧级审计 8 组/1127 帧通过；批处理 10 组总索引齐全，8 组三件套长度一致；VFM Boundary 4 边/4 力序列/258 帧映射通过；Python 依赖、输入路径及 MatchID 均可用。MatchID 正式资格仍为 8 ready、1 force review、1 preload release。
- 下一步：先完成全组完整有效区间应力—应变和逐帧虚功/残差交付；观察 PID `46440` 后更新窗口趋势。S23 缺失的断裂力不补造，S24 预载释放不作为拉伸；正式参数发布门槛保持不变。

## [2026-09-26] audit | S16 有限变形 J2 100% 峰前窗口完成

- 输入：`configs/pa12_finite_j2_s16_stratified_window_100.json`；完整 Job ROI，峰前拟合 `000001–000256.jpg`（256 帧），峰后 `000257.jpg` 仅进入全历程诊断。分层预拟合实际选 506/19,796 个三角形。
- 拟合：预拟合 `Y0=90.0718 MPa,H=6.1610 MPa`、14 次目标评估、67.313 s；全网格精修 `Y0=88.7702 MPa,H=13.3847 MPa`、6 次目标评估、1610.495 s。拟合 RMS `73.8386 N`，全历程 RMS `114.1612 N`，全历程最大绝对残差 `1411.128 N`。
- 审核：检查点记录 `full_job_roi / 1.0` 完成；逐帧 CSV 257 行、照片唯一、首末帧为 `000001/000257.jpg`、时间严格递增、所有数值有限；摘要状态 `REVIEW_REQUIRED`、DIC 覆盖率 `89.2248%`，PNG 已生成。100% 窗口 `H` 为正，但 50%/75% 的 `H` 贴近约束下界；75%/100% 的 `Y0` 接近，不能据此单独认定 `H` 稳定可辨识。
- 输出：`Agents/PA12实验数据处理/VFM自建/有限变形J2诊断/S16_XY_0.2_分层初值对照_100pct/`；窗口图和全量指标已并入[审计页](Agents/PA12实验数据处理/VFM自建/汇总/PA12有限变形J2分层预拟合与全网精修审计.md)、`index.md`、阶段计划与 GPT 交接。
- 下一步：对 100% 候选审计缩放灵敏度/Jacobian 秩与条件数；继续完整应力—应变、DIC 覆盖及帧级虚功/残差交付。另一全峰前输出目录只有空检查点且无 runner，不计为重复结果；旧 PID `45360` 保留但不作交付前置条件。原始 JPG/DAT/XLS 只读，所有参数仍为条件诊断候选。

## [2026-09-26] audit | S16 100% 候选局部灵敏度与内缩域计算状态

- 审计：完整 Job ROI 100% 峰前拟合的缩放 Jacobian 为 `512×2`、秩 `2`，奇异值 `33998.325/248.540`，条件数 `136.792`，参数列余弦相似度 `0.885513`。仅说明固定 `E/ν`、网格、ROI 与残差权重下局部数值满秩；不提供噪声稳健性、置信区间或物理识别证明。
- 运行：PID `33844` 的 `dic_subset_inset_sensitivity / 100%` 仍活动，检查点 `completed_windows=[]`。该分支沿用完整 Job ROI 机器合力，只能作积分域敏感性；PID `45360` 旧全量作业保留，未触碰其进程和目录。
- 更新：阶段计划、GPT 交接说明/状态、`index.md` 与 Stage 2/窗口审计页同步记录；原始 JPG/DAT/XLS 未修改。
- 待验证：取得 PID `33844` 的有效输出后比较域变化；继续补齐独立边界位移/外功、DIC 覆盖及材料模型证据。正式 `Y0/H` 发布保持关闭。

## [2026-09-26] audit | S16 J2 100% DIC subset 内缩域敏感性完成

- 输入：`configs/pa12_finite_j2_s16_stratified_inset_100.json`；DIC subset 内缩域，拟合 `000001–000256.jpg` 共 256 帧，完整诊断覆盖 257 帧；厚度 `1 mm`、固定 `E=3313.376 MPa`、`ν=0.375`。
- 拟合：分层预拟合选取 `506/19,796` 个三角形，`Y0=85.0867 MPa`、`H=5.7596 MPa`，耗时 `74.832 s`；全网格精修 `Y0=83.851239 MPa`、`H=12.626794 MPa`，7 次目标函数评估、耗时 `1669.069 s`。拟合 RMS `74.1644 N`，全历程 RMS `114.3708 N`，最大绝对残差 `1414.791 N`。
- 审核：`dic_subset_inset_sensitivity` 检查点完成，状态 `DIAGNOSTIC_ONLY`、有效域覆盖率 100%；CSV 257 行，照片 `000001–000257.jpg` 连续、时间严格递增、所有数值有限、首帧 X/Y 外虚功为零。与主域 100% 输出相比，257 帧 X/Y 外虚功序列逐帧完全相同。
- 敏感性：同一 100% 窗口下主域 `Y0/H=88.770153/13.384673 MPa`，内缩域 `83.851239/12.626794 MPa`，相对主域分别约 `−5.54%/−5.66%`；拟合 RMS 差 `0.326 N`、全历程 RMS 差 `0.210 N`。内缩域仍使用完整 Job ROI 机器合力，因此仅表示积分域/虚场口径敏感性，不是内缩域自身边界闭合或独立材料参数识别。主域支持率为 `89.2248%`、状态 `REVIEW_REQUIRED`；窗口参数仍属条件诊断，不发布为 PA12 正式参数。
- 输出：[内缩域 100% 诊断摘要](Agents/PA12实验数据处理/VFM自建/有限变形J2诊断/S16_XY_0.2_分层初值对照_内缩100pct/dic_subset_inset_sensitivity/诊断摘要.md)、[逐帧虚功 CSV](Agents/PA12实验数据处理/VFM自建/有限变形J2诊断/S16_XY_0.2_分层初值对照_内缩100pct/dic_subset_inset_sensitivity/逐帧有限变形J2虚功.csv)；机器状态与 GPT 交接已同步。
- 下一步：按总目标继续完成其他可支持实验的全有效区间曲线、逐帧虚功/残差与质量汇总，并补独立边界位移/外功、ROI、厚度、本构定义和实验验证证据。S23 缺失断裂力不补造，S24 不作为拉伸；原始 JPG/DAT/XLS 保持只读。

## [2026-09-26] audit | S16 J2 状态对齐与八组 VFM 文件核对

- 核对对象：S16 完整 Job ROI 主域与 DIC subset 内缩域 100% 窗口；S15–S22 八组阶段 A 逐帧内外虚功 CSV。
- 结果：S16 主域 50%/75%/100% 与内缩域 50%/100% 均已完成；当前无活动 J2 runner。历史 PID 45360 已退出，另一隔离目录的空 completed_windows 检查点不计为结果。
- 文件核对：八组 CSV 均存在，行数与阶段 A 审计一致，总计 1127 帧；逐字段扫描未发现 NaN/Inf。该核对不替代物理积分域、边界外功或材料参数验证。
- 轴序证据：G1 机台—DIC 交叉核验中，S19–S22 加载应变与 DIC Eyy 场均值的相关系数为 0.9512–0.99997，与 Exx 场均值为 −0.9990 至 −0.9364，支持加载轴沿 DIC y。该统计依赖 30 mm 工作标距和现有时间索引，只支持轴序候选，不是有向设备标定，也不闭合打印材料轴。
- 参数解释：100% 主/内缩域 Y0/H 分别为 88.770153/13.384673 MPa 与 83.851239/12.626794 MPa，相差约 −5.54%/−5.66%；两分支 257 帧 X/Y 外虚功一致，但内缩域仍使用完整 Job ROI 合力，只能作为积分/虚场敏感性结果。完整 ROI DIC 支持率 89.2248%，候选不作为正式材料参数。
- 更新：窗口审计、总目标与阶段计划、GPT 交接文档/状态、index.md。原始 JPG/DAT/XLS、check/config 文件及分析代码未修改。
- 下一步：基于现有 G1 机台—DIC 运动学证据继续核实单轴逐试样有向坐标；补实测厚度、有效截面和独立外功边界证据，并处理 S15/S22/S23 曲线事件复核；不重复运行已完成的 S16 窗口。

## [2026-09-26] audit | TC1000 源 STEP 载荷比 IVOL 加权复核

- 输入：`tc1000.step` 源几何，XY 平面、Z 构建/厚度方向，总厚 `3 mm`、中心厚 `1 mm`；比较 `r=ΔY/ΔX=0.5/1/2`，`ΔX=0.05 mm`，`4 mm` 网格、C3D10、同一临时弹性材料卡。
- 方法：在 D 盘隔离目录重求解三份输入副本并输出 `IVOL`；按元素质心筛选固定中心 `28×28 mm` 区域，再以 IVOL 加权应力/应变 CV。每工况均有 `1660` 个积分点，累计 ROI 体积 `784.78–785.01 mm³`。
- 结果：`r=0.5/1/2` 的加权综合 CV 为 `0.175913/0.133574/0.176910`，`K` 为 `0.539220/0.000153/0.539282`，过渡带/中心最大 Mises 比为 `2.191034/1.968638/1.997078`。三档中 `r=1` 的中心应变最平衡且综合 CV 最低；过渡带峰值仍约为中心峰值的两倍，未证明中心先屈服或断裂可控。
- 限制：此为固定几何的临时线弹性载荷比筛查，不是几何最优、材料标定或实验工况发布。等权旧分数与本次固定 ROI/IVOL 加权结果不直接比较。
- 更新：[IVOL 加权复核页](Agents/PA12双轴试样仿真/验证/2026-09-26_TC1000_载荷比IVOL加权复核.md)、`index.md`；合并 CSV 和逐工况 `.inp/.odb/.json` 保存在 `D:\PA12_Stage2\g0_tc1000_ratio_source_step_scan_20260926_ivol_reaudit\`。原始 STEP 与先前模型输出未覆盖。
- 下一步：转入同口径的源 STEP 几何参数化比较，并针对过渡带做局部网格/材料/真实边界复核；维持正式设计排名未放行。

## [2026-09-26] audit | S19 单轴 75/25 严格留出

- 输入：S19 全有效区间自建 VFM 内外虚功 CSV；按时间顺序 75/25 划分，原始 JPG/DAT/XLS 未修改。
- 结果：训练/留出 94/32 行，24 个弹性观察点，训练/留出塑性点 81/31；脚本点数状态 `PASS`。条件 `E=5389.402871 MPa`、`Y=-17.592800 MPa`、`H=40772.497524 MPa`，留出 RMSE=`40.975690 MPa`。
- 判定：该脚本的 `PASS` 仅代表留出塑性点数达到配置门槛。负 Y、与全数据阶段 2 候选相比明显的 H 漂移及留出误差说明当前材料模型/参数未通过验证；S19 仍为 `REVIEW_REQUIRED`。单轴几何、面积覆盖、坐标标定和外功边界未解除。
- 更新：[阶段 I 单轴映射复核](Agents/PA12实验数据处理/VFM自建/汇总/PA12自建VFM阶段I单轴机器轴与DIC轴映射复核.md)、GPT 交接文档/状态、`index.md`。完整 Job Polygon 继续作为主域；DIC subset 内缩域仅作独立敏感性分支。
- 下一步：先修正有限变形 J2 runner 对真实 Polygon 支持域的处理，并建立来源可追溯的参考位移基线；在此之前不对 S19 启动会误用外接框面积的有限 J2 拟合。

## [2026-09-26] experiment | TC1000 真实 STEP 五厚度 IVOL 线弹性筛查

- 输入：五个只读源 STEP，中心厚度 `1.0/1.5/2.0/2.5/3.0 mm`、总厚 `3 mm`；打印平面 `XY`、构建方向 `Z`。
- 方法：统一 `ΔX=ΔY=0.05 mm`、`r=1`、KINEMATIC 四臂耦合、自由 C3D10、名义种子 `4 mm`、临时正交弹性材料；按固定中心 `28×28 mm` 质心 ROI 和 `IVOL` 权重计算应力/LE 变异系数、`K_ratio` 与 `G_transition`。
- 结果：1.0–2.5 mm 各有 `36,344–36,954` 个 C3D10 单元；3.0 mm 为 `171,412`。CV 总分为 `0.133574/0.115210/0.107743/0.115030/0.053493`，对应 `G_transition=1.969/2.514/5.382/3.076/2.629`。2.0 mm 的 CV 总分最低但过渡带集中最高；3.0 mm 网格约为减薄组均值的 4.68 倍，未进入最终排序。
- 复核：3.0 mm 源 STEP 与先前直接参数化基线单元数差约 0.10%，高密度并非直接草图独有；具体网格生成原因仍未定位。所有结论限于临时线弹性小位移筛查，不证明塑性、断裂位置、实验 DIC/VFM 或最终最优厚度。
- 输出：[筛查报告](Agents/PA12双轴试样仿真/验证/2026-09-26_TC1000真实STEP五厚度IVOL线弹性筛查.md)、`index.md`、阶段计划及 GPT 交接状态已更新。逐档 `.inp/.cae/.odb/.sta` 和 IVOL JSON/CSV 保存在 `D:\PA12_Stage2\g0_tc1000_source_step_3000_mesh_diagnostic_20260926\` 与 `D:\PA12_Stage2\g0_tc1000_source_step_5thickness_ivol_screen_20260926\`。原始 STEP 保持只读。
- 运行状态：系统扫描时旧 PID `45360` 仍存在且响应；未终止该进程或触碰其输出目录。历史记录中“已退出”与本次进程扫描不一致，以后续新扫描为准；该进程不作为本轮 G0 或近期诊断交付前置条件。
- 下一步：对 `1.0/1.5/2.0/2.5 mm` 做逐档网格收敛，单独复核 `3.0 mm` 网格；收敛后再使用已标定材料卡进行多目标比较。VFM 诊断线继续处理单轴坐标/截面/外功证据和 S15/S22/S23 事件复核。

## [2026-09-26] audit | S19 有限变形 VFM 网格支持

- 输入：S19 126 个有效 DIC—力帧、参考 DIC 场 9,144 点、Job Polygon；完整 Job ROI 为主域，DIC subset 内缩域独立输出。原始 JPG/DAT/XLS 保持只读。
- 固定支持：`000068/000083/000125.jpg` 均缺参考坐标 `(49.152680, 50.762854) mm`；使用 9,143 个全程共同点建固定网格，凸包面积与 9,144 点网格差约 `1.1×10⁻¹³ mm²`。
- 未过滤基线：Delaunay 最长边最大 `52.887 mm`，Job ROI 面积覆盖 `87.0952%`；固定 `ν=0.375` 时联合 E 触及 `0 MPa`，X-only 无约束 E=`−20.240 MPa`。126 帧累计 1,371 个非正 Jacobian，最小 `det(F)=−6.509`，不能进入 J2 拟合。
- 只读边长敏感性：`0.5/1/2 mm` cap 下全程无非正 Jacobian，主域 X-only E=`5058.318/5058.980/5060.363 MPa`，X 拟合 RMS=`12.082/12.010/11.791 N`；ROI 覆盖率=`84.867/84.972/85.164%`。subset E 比主域低约 `2.32%`；Y 虚功 RMS 仍为 `147.65–156.54 N`。边长规则未进入 runner，E 仅为待审条件候选。
- 交付：[审计页](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S19有限变形VFM网格支持审计.md)；[未过滤双域输出](Agents/PA12实验数据处理/VFM自建/有限变形诊断/S19_X_0.2/)。新增全程共同点选择器并接入线性诊断/J2 历史加载；专项运动学与 J2 runner 测试 `17 passed`，排除此单模块后的测试为 `179 passed`。全量 pytest 收集仍被 `tests/test_pa12_biaxial_coupling_mode.py` 的 `material_orientation` 导入失败阻断，该模块未改。完整 Job ROI 仍 `REVIEW_REQUIRED`，不发布 E/Y/H。
- 下一步：先确认是否把 `2 mm` edge cap 作为主网格候选、`1/0.5 mm` 作为敏感性。随后再复跑双域线性诊断与 J2 候选；不得把网格敏感性通过当成独立材料验证。同步核验单轴轴向、有效截面、ν 与有向外功边界。

## [2026-09-26] experiment | TC1000 平放/竖直材料轴与加载比 IVOL 筛查

- 输入：只读 `tc1000.step` 源几何；中心厚度 `1.0 mm`、总厚 `3.0 mm`。平放取向为 `M-Z→FE-Z`；竖直取向将构建轴 `M-Z` 映射到面内 `-FE-Y`，保持 CAD 几何与加载边界不变。
- 方法：竖直取向新增 `r=ΔY/ΔX=0.5/1/2` 三个 C3D10 求解，`ΔX=0.05 mm`、全局种子 `4 mm`、KINEMATIC 耦合；与既有平放 IVOL 结果同口径对照。后处理依据 ODB `localCoordSystem` 把张量回转到全局 FE 轴；剪切应变按工程剪切约定转换后参与张量旋转。每工况 ROI 均为 1660 个积分点。
- 结果：竖直 `r=0.5/1/2` 加权 CV 总和为 `0.176705/0.129796/0.154179`，`K_ratio` 为 `0.547439/0.026442/0.486089`，`G_transition` 为 `2.279897/2.140243/2.068272`。`r=1` 最平衡；`r=2` 虽 CV 总和较低但双轴失衡明显。六个取向/比值工况均未证明中心先失效、断裂可控或 VFM 参数可识别。
- 限制：材料卡为未标定的临时正交弹性参数，位移仅 `0.05 mm` 基准，网格 `4 mm`，无塑性/损伤、实物打印布局及真实夹具验证；结果仅作材料方向—加载比敏感性筛查。
- 更新：[结果报告](Agents/PA12双轴试样仿真/验证/2026-09-26_TC1000_平放竖直取向载荷比筛查.md)、[对照 CSV](Agents/PA12双轴试样仿真/验证/2026-09-26_TC1000_平放竖直载荷比对照.csv)、[对照图](Agents/PA12双轴试样仿真/验证/2026-09-26_TC1000_平放竖直载荷比对照.png)、阶段计划和 `index.md`。Abaqus `.cae/.inp/.odb/.sta`、逐工况 JSON/CSV 与副本脚本均保存在 `D:\PA12_Stage2\g1_vertical_ratio_screen_20260926\`；源 STEP 未改写。
- 下一步：对 `1.5/2.0/2.5/3.0 mm` 完成同口径网格收敛并复核减薄过渡/槽端局部特征；取得实际构建布局、材料标定和夹具边界证据后，再复算取向与加载比组合。

## [2026-09-26] audit | PA12 单轴有限变形 VFM 跨组网格支持

- 输入：S19/S20/S21/S22 共 448 帧有效 DIC—力记录及各组 Job Polygon；原始 JPG/DAT/XLS 未修改。S19 使用有效 Results Viewer 参考场，S20–S22 使用有效 DAT 点。
- 结果：6 位坐标键处理跨 DAT/CSV 的浮点序列化差异（最大 `1.42×10⁻¹⁴ mm`）；共同支持恢复至 `9143/7920/7765/5425` 点。未截断 Delaunay 的 ROI 支持率为 `87.10/84.69/86.75/82.64%`，非正 Jacobian 总数为 `1371/350/81/522`。
- 边长敏感性：`0.5–2 mm` 上限消除 S19–S21 的非正 Jacobian，但 S22 仍残留 `20–22` 个；S22 支持率降至 `72.75–80.93%`，不将截断规则推广为生产方法。
- 修改：更新有限运动学坐标键匹配及两项回归测试；新增[跨组网格支持审计](Agents/PA12实验数据处理/VFM自建/汇总/PA12单轴有限变形VFM跨组网格支持审计.md)，更新 S19 审计、GPT 交接状态和 `index.md`。完整 Job ROI 仍为主域，DIC subset 内缩域保持独立；无实验参数拟合。
- 验证：有限变形运动学、VFM 诊断、J2 材料点核与 runner 定向模块共 `45 passed`；四组共同点和网格统计已通过生产匹配函数复核。
- 下一步：评估能处理 S22 全程支持变化及局部非正 Jacobian、同时满足 ROI 积分证据的网格支持方法；边长截断未接入生产 runner。

## [2026-09-26] experiment | TC2000 中心厚度 2.0 mm 网格敏感性复核

- 输入：只读源 STEP `03_a2p0.5mm.step`，中心厚度 `2.0 mm`、总厚 `3.0 mm`；载荷比 `r=1`、`ΔX=ΔY=0.05 mm`、C3D10、KINEMATIC 四臂耦合、临时正交弹性材料卡。
- 计算：全局名义种子 `h=4/3/2/1.75/1.6 mm` 均成功建网格并求解；全局单元数为 `36953/42933/72406/75960/83973`。`h=1.5 mm` 默认 `TET/FREE` 未生成网格，诊断为 0 节点、0 单元、1 个未网格化几何单元，未提交分析。
- 结果：细网格 `h=1.6–2.0 mm` 平均 `LE11/LE22` 变化小于 `0.08%`，综合 IVOL 加权 CV 相邻变化 `1.7%–4.0%`，过渡带峰值比相邻变化 `1.5%–4.2%`；粗网格 `h=4/3 mm` 的过渡带峰值比明显偏高。由于未预先设定容差且细化指标并非全部单调，判为初步数值稳定，不声称正式网格收敛。
- 限制：材料卡无实验标定且无塑性/损伤/断裂；载荷位移仅 `0.05 mm`，不能对照实验约 `8%` 或目标示例 `20%+`。质心 ROI 纳入完整单元 IVOL，ROI 体积随网格为 `1577.85–1601.09 mm³`；该工况不证明最终厚度、中心先断裂或 VFM 可识别性。
- 输出：[网格敏感性报告](Agents/PA12双轴试样仿真/验证/2026-09-26_TC2000中心厚度2mm网格敏感性复核.md)、[结果 CSV](Agents/PA12双轴试样仿真/验证/2026-09-26_TC2000中心厚度2mm网格敏感性复核.csv)、[H1.6 网格截图](Agents/PA12双轴试样仿真/验证/2026-09-26_TC2000_H1P6_C3D10网格截图.png)；完整 `.cae/.inp/.odb/.sta`、运行清单及分辨率截图位于 `D:\PA12_Stage2\g0_tc2000_mesh_convergence_20260926\`。源 STEP 未修改，`index.md`、阶段计划和 GPT 交接状态已同步。
- 下一步：对中心厚度 `1.5/2.5/1.0 mm` 继续同口径细网格敏感性，并对 `2.0 mm` 过渡带做局部加密；取得实测材料与打印方向证据后再进入正式多目标设计比较。

## [2026-09-26] audit | S22 局部 Jacobian 与 DIC 时序

- 输入：S22_Y_0.2 的 223 个有效 DIC—力帧、5,425 个全程共同点、帧—力索引及异常帧原始 JPG/DAT；原始数据只读。
- 结果：只读 1 mm 边长敏感性仍有 20 个非正 Jacobian，分布于 8 帧，最小 `det(F)=-1.7072`。其中 7 帧的 Fy 为峰值的 88.2%–97.9%，异常网格顶点均属于全程共同点。多个异常区的单帧位移步长高于全场 P99；点 4747 在三帧重复出现约 0.57–0.63 mm 跳变。末帧 001784 为自动掉载，位移步长未高于全场 P99。
- 判定：缺点不能单独解释异常；证据支持局部运动学突变/局部化，但不能区分物理变形与 DIC 相关异常。原图首批异常帧未见清晰裂纹，末帧可见颈缩/损伤外观但未确认完全断裂；`r/sigma` 未用于质量筛选。
- 输出：[S22 局部 Jacobian 与 DIC 时序诊断](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S22有限变形局部Jacobian与DIC时序诊断.md)、`index.md`、GPT 交接文档/状态。完整 Job ROI 继续为主域；subset 内缩域独立；边长截断没有进入生产流程，无材料参数拟合。
- 下一步：核实 DIC 像素到原图的有向映射，配准异常单元与原图；再评估保留完整 Job ROI、且不对缺失场外推的积分支持方法。门槛未通过前保持 `REVIEW_REQUIRED`。

## [2026-09-26] audit | 完整 Job ROI 多边形交叠积分与 S22 支持率

- 输入：S22 原始 `000000.jpg.dat`、223 个有效 DIC—力帧、Job 五边形及现有 DIC—力索引；原始 JPG/DAT/Job 未修改。
- 实现：新增简单凹多边形耳切与三角形交叠面积计算；弹性虚功和有限变形 J2 共用交叠面积权重。完整 Job ROI 保持主域，DIC subset 内缩有效域保持独立敏感性；不外推未覆盖 ROI 面积。
- 结果：S22 参考有效点 6,166、共同点 5,425、三角形 10,558；Job ROI `441.652717 mm²`，实测交叠 `364.997080 mm²`，覆盖率 `82.6435%`，`76.655637 mm²` 未覆盖，仍 `REVIEW_REQUIRED`，没有参数拟合。
- 更新：[ROI 交叠积分与支持率核算](Agents/PA12实验数据处理/VFM自建/汇总/PA12完整JobROI多边形交叠积分与S22实测支持率核算.md)、[S22 时序诊断](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S22有限变形局部Jacobian与DIC时序诊断.md)、GPT 交接文档/状态及 `index.md`。
- 验证：VFM/J2 相关测试 `47 passed`；全仓排除 `tests/test_pa12_biaxial_coupling_mode.py` 后 `185 passed`；`python -m compileall -q tools tests` 通过。完整 pytest 收集仍受该并行双轴扫描测试的同目录导入路径问题阻断，该测试与文件未修改。
- 下一步：确认扩展 DIC 相关支撑不会跨越厚度/材料边界；满足时用输出隔离的派生 Job 扩展点场支持，但仍以原 Job 多边形积分，否则继续保持面积复核，不拟合参数。

## [2026-09-26] experiment | TC1500/TC2500 竖直取向网格与位移比筛查

- 输入：几何回归表与运行清单核对 TC1500=`04_a1p0.75mm.step`（中心 1.5 mm）、TC2500=`02_a2p0.25mm.step`（中心 2.5 mm），总厚均为 3.0 mm；打印平面 XY、构建轴 Z，竖直材料映射 `M-Z→FE-Y`。
- 计算：两种几何均完成 `h=4/3/2/1.75/1.6/1.5 mm`、`r=ΔY/ΔX=1` C3D10 静力求解；在 `h=1.6 mm` 完成 `r=0.5/1/2` 位移比筛查。所有工况使用相同 provisional engineering-constants 弹性卡、KINEMATIC 四臂耦合、`ΔX=0.05 mm`，按中心 `28×28 mm` 质心 ROI 与 IVOL 统计。
- 结果：TC1500 网格序列 `primary_score=0.097496–0.106758`、`G_transition=1.861–3.360`；TC2500 为 `0.073733–0.113619`、`2.235–3.165`。细网格指标并非单调，ROI IVOL 分别变化 `1,170.220–1,222.883 mm³` 和 `1,953.895–2,016.500 mm³`。两种厚度的位移比筛查均以 `r=1` 获得较低的综合 CV 和 `K_ratio`，但其结果仍是临时弹性小位移诊断。
- 身份纠正：目录 `D:\PA12_Stage2\g0_tc1500_mesh_sensitivity_20260926\` 的旧作业名与 STEP 来源不符，实际使用 TC2500 的 `02_a2p0.25mm.step`、平放 `flat_xy` 方向；已在合并报告与交接状态中标注，未改写原运行数据。
- 输出：[合并报告](Agents/PA12双轴试样仿真/验证/2026-09-26_TC1500_TC2500竖直网格与位移比筛查.md)、[网格 IVOL CSV](Agents/PA12双轴试样仿真/验证/2026-09-26_TC1500_TC2500竖直网格IVOL结果.csv)、[位移比 IVOL CSV](Agents/PA12双轴试样仿真/验证/2026-09-26_TC1500_TC2500竖直H1P6位移比IVOL结果.csv)、两张 H1.6 网格截图、`index.md`、阶段计划和 GPT 交接状态。全部 `.cae/.inp/.odb/.sta`、运行清单与逐工况 JSON/CSV 保存在 `D:\PA12_Stage2\g0_tc1500_vertical_r1_mesh_sensitivity_20260926\` 与 `D:\PA12_Stage2\g0_tc2500_vertical_r1_mesh_sensitivity_20260926\`。
- 限制与下一步：没有预设收敛容差，材料卡无实测标定且没有塑性/损伤/断裂模型；当前中心平均 LE 不到 0.1%，不能验证实验约 8% 或 VFM 识别。下一步做 TC1000 竖直 `r=1` 网格敏感性，再专项诊断 TC3000 网格与过渡区局部加密，接入真实材料和实验位移范围后进行 FE–DIC/VFM 对照。

## [2026-09-26] audit | Job 网格相邻三角化与 S22 ROI 支持率复核

- 输入：S15–S22 原始参考 DAT、Job `Step size`/标定元数据；S22 的 223 帧有效 DIC—力索引与共同全场。原始 JPG/DAT/Job 未改写。
- 更新：有限运动学网格构造、弹性诊断与 J2 历史加载；Job 几何元数据；网格/报告回归测试；S22 Jacobian 与 ROI 核算、GPT 交接状态、`index.md`。
- 结论：八组参考点坐标均与 Job 步长网格吻合。S22 相邻网格为 10,062 个三角形，Job ROI 交叠支持面积 `314.434985 mm²`、覆盖率 `71.1951%`；旧 Delaunay 值 `82.6435%` 跨过缺失格点，不再作为实测支持。生产网格有 15 个非正 Jacobian 事件、分布于 7 帧，最小 `det(F)=-1.3484`。完整 Job ROI 仍为主域，DIC subset 内缩域保持独立敏感性；S22 维持 `REVIEW_REQUIRED`，未拟合材料参数。
- 验证：运动学、弹性诊断、J2 核/runner 与 Job 几何相关测试 `80 passed`；排除 `tests/test_pa12_biaxial_coupling_mode.py` 后全仓 `188 passed`；`python -m compileall -q tools tests` 通过。
- 待验证：按新生产网格重跑完整 Job ROI 主诊断及独立 subset 内缩敏感性；解决 S22 面积支持与 Jacobian 门槛后，再评估参数识别。旧 `1 mm` Delaunay 边长敏感性仍仅作历史对照。

## [2026-09-26] experiment | TC1000 竖直 r=1 网格敏感性

- 输入：只读真实源 STEP `tc1000.step`，中心厚度 1.0 mm、总厚度 3.0 mm；打印 XY 层面、Z 构建方向，竖直材料映射 `M-Z→-FE-Y`。
- 计算：复用竖直 `h=4 mm` 基准，并新增 `h=3/2/1.75/1.6/1.5 mm` 五档；六档均使用 `ΔX=ΔY=0.05 mm`、C3D10、KINEMATIC 四臂耦合、同一临时正交弹性卡与固定中心 ROI；全部求解和 IVOL 后处理成功。
- 结果：`primary_score=0.128546–0.131575`，平均 `LE11/LE22` 分别约 `4.585–4.588×10⁻⁴/4.351–4.353×10⁻⁴`，六档变化低于 0.1%；`G_transition=1.874–2.140`，过渡带峰值仍高于中心峰值。未预先设定正式收敛容差，不能据此声称正式收敛或断裂可控。
- 更新：[TC1000 竖直网格报告](Agents/PA12双轴试样仿真/验证/2026-09-26_TC1000竖直r1网格敏感性.md)、逐档 CSV、H1.6/H1.5 网格截图、`index.md`、阶段计划及 GPT 交接文档/状态。
- Abaqus 全量工程文件：`D:\PA12_Stage2\g0_tc1000_vertical_r1_mesh_sensitivity_20260926\`；H4 基准沿用 `D:\PA12_Stage2\g1_vertical_ratio_screen_20260926\R1P0\`。原始 STEP 未修改。
- 限制与下一步：材料仍为未标定线弹性且无塑性/损伤/断裂；继续检查 TC3000 高密度几何与中心过渡/槽端局部加密，再冻结 ROI、材料与夹具边界后开展 FE–DIC/VFM 对照。

## [2026-09-26] experiment | S19–S21 单轴有限变形 VFM 生产网格诊断

- 输入：S19_X_0.2、S20_X_2、S21_X_20 的有效 DIC—力索引、Job 文件及 `000000.jpg.dat` 参考场；原始 JPG/DAT/力数据只读。三组分别 126、63、36 个有效帧，阶段1窗口分别为 24、27、17 帧，X 力非零、Y 力为零。
- 计算：按 Job `Step size × Conversion` 构建相邻格点三角网，不跨缺失格点；三角片与完整 Job ROI 多边形交叠面积作为主域积分权重，不对未覆盖面积外推。DIC subset 内缩有效域另行输出，仍使用完整 Job ROI 机器合力，仅作独立积分域敏感性。
- 结果：完整 Job ROI 支持率 S19/S20/S21=`84.8667/83.5938/84.1189%`，均低于 `0.95` 门槛；非正 Jacobian 数均为 0。固定 `ν=0.375` 的条件 E 主域为 `2577.886/7540.211/9498.399 MPa`，内缩域为 `2267.323/6213.593/9134.000 MPa`，分别变化 `−12.05/−17.59/−3.84%`。全历程 X/Y 残差 RMS（N）分别为 S19=`403.740/57.171`、S20=`368.701/274.418`、S21=`287.028/186.456`。
- 虚功核对：逐帧 X 外虚功与索引 X 力最大差 `0 N`；Y 外虚功为零；主域/内缩域外虚功序列一致。该项验证同帧力输入和单位虚位移计算口径，不验证真实边界运动学或闭合。Y 内虚功明显非零，所有单轴全历程残差仍需复核。
- 输出：[S19–S21 汇总报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12单轴有限变形VFM诊断_S19-S21.md)、三组生产配置及逐帧主域/内缩 CSV、虚功图和摘要。各 CSV 主/内缩行数与有效帧数一致，虚功/残差列有限；主域图完成视觉检查。
- 结论与待验证：三组全部 `REVIEW_REQUIRED`；E 是固定泊松比、二维 Euler–Almansi 线性平面应力代理下的条件诊断，不是材料弹性模量；未识别 Y/H。单轴实测厚度/有效截面/标距、机器—DIC 有向坐标及边界虚位移定义未独立确认。下一步按同口径对照已有 S22 单轴 Y 诊断，并继续检查虚功残差来源。

## [2026-09-26] audit | S19–S22 单轴跨轴虚功诊断

- 输入：四组单轴生产网格诊断 CSV/JSON、照片—力索引、S22 局部 Jacobian 时序审计；原始 JPG/DAT/力数据保持只读。
- 更新：[S19–S22 跨轴诊断报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12单轴有限变形VFM跨轴虚功诊断_S19-S22.md)、GPT 交接文档/状态、`index.md`。
- 结果：逐帧活动方向外虚功与索引力最大差为 `0 N`，输出时间与索引相同；此为数据列/计算口径一致，不证明独立物理同步或边界虚位移闭合。四组完整 Job ROI 支持率 `71.1951%–84.8667%`；主域与 subset 条件 E 差 `−3.836%` 至 `−17.594%`；S22 有 15 个非正 Jacobian 事件。JSON 全历程 RMS 汇总 X/Y 两个残差分量，报告另列活动轴逐轴 RMS。
- 判定：四组仍为 `REVIEW_REQUIRED`；条件 E 不作为材料 E，未识别 Y/H。subset 内缩域仍是独立敏感性，外功继续使用完整 Job ROI 机器合力。
- 下一步：核实各单轴试样实测截面/厚度/标距、机器—DIC 有向变换和边界虚位移；审查 S22 异常相关质量，并在同材料/厚度范围内评估提高 ROI DIC 支持。门槛通过后再逐加载速度执行固定 `ν=0.375` 的 E 与 Y/H 分阶段识别。

## [2026-09-26] experiment | S16 峰值位移真实 STEP 回放诊断

- 输入：只读 `tc1000.step`、S16 位置表和同步力索引；峰值帧 `000256.jpg`（`25.7335 s`），机器 X/Y 力 `1632.32/1613.26 N`，候选相对位移 `5.1328/5.1333 mm`。
- 结果：竖直候选映射下真实 STEP 的 C3D10 静力步完成；中心 ROI IVOL 加权平均 `LE11/LE22=4.5909%/4.2873%`，但材料卡仅为临时正交弹性。求解日志有 2 条参考点 DOF 2/3 数值奇异警告，`1,373/36,463` 个单元标记畸变；DIC 与 FE ROI 尚未空间配准。
- 更新：[回放诊断页](Agents/PA12双轴试样仿真/验证/2026-09-26_S16峰值位移真实STEP回放诊断.md)、指标 CSV/JSON、网格截图、`index.md`、阶段计划及 GPT 交接文档/状态。全量 Abaqus 工程保存在 `D:\PA12_Stage2\g4_tc1000_s16_source_step_peak_replay_20260926_r2\`，源几何和实验文件未改写。
- 判定：仅为受限几何/场响应诊断；不作真实应力、断裂控制、材料参数或设计排名结论。
- 下一步：从 ODB 提取四臂控制点位移/反力并核验机器载荷平衡；定位奇异告警及畸变单元对中心 ROI 的影响，再进行同物理 ROI 的 FE–DIC 配准。

## [2026-09-26] audit | S19–S22 完整 Job ROI DIC 支持空间复核

- 输入：四组单轴生产诊断摘要、Job Shape、000000 参考 DAT 与原始参考 JPG；JPG/DAT/Job 和既有生产输出只读。
- 计算：按全程共同点和 Job Step size×Conversion 构建相邻三角网，分别叠加原 Job ROI 与参考照片；未重跑 VFM，不对缺失面积插值或外推。
- 结果：S19/S20/S21/S22 支持率为 84.8667%/83.5938%/84.1189%/71.1951%，未覆盖面积为 102.051/95.347/98.096/127.218 mm²。S19–S21 缺口主要沿周缘并夹少量离散孔；S22 另有多个内部不连续缺口。
- 更新：[空间支持核算与图](Agents/PA12实验数据处理/VFM自建/汇总/PA12完整JobROI多边形交叠积分与S22实测支持率核算.md)、[坐标覆盖图](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S19-S22完整JobROI_DIC支持空间分布.png)、[参考图叠加](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S19-S22_完整JobROI_DIC支持_参考图叠加.png)、`index.md`、GPT 交接文档/状态。
- 结论：完整 Job ROI 保持主结果，DIC subset 内缩域保持独立敏感性；照片不能确认同厚度或 S22 缺口成因。四组仍为 `REVIEW_REQUIRED`，不拟合、不扩 ROI、不补场。
- 下一步：核实各单轴试样实体边界、有效截面/厚度与 ROI 包含关系；优先检查 S22 内部缺口对应的参考纹理和逐帧有效点变化。只有确认同材料/厚度且图像可观测后，才建立输出隔离的派生 DIC 相关任务。

## [2026-09-26] experiment | TC3000 竖直网格与局部加密诊断

- 输入：运行清单指向只读 `01_a3p0mm.step`；临时正交弹性卡、C3D10、竖直材料轴候选、`ΔX=ΔY=0.05 mm`、中心 `28×28 mm` ROI。
- 完成性：H4/H6/H8 全局网格及 H8 局部 0.5/0.25 mm 共 5 个作业均有成功日志、成功 `.sta`、ODB 和 0 个求解错误。
- 网格质量：全局畸变单元分别为 `1,357/171,411`、`282/54,612`、`170/18,762`；局部组为 `3,599/33,083`、`13,108/61,654`。所有组均有参考点奇异警告；两个局部组另有 1 个负特征值警告。
- 判读：中心平均 LE 在各网格接近，但局部 H8 组的 `G_transition=2.5780/2.4813` 高于 H8 全局 `2.3269`，且畸变比例高，排除出局部设计优劣排名。全局序列未设先验收敛容差，亦有奇异警告，只记为筛查，不宣称网格收敛。
- 更新：[TC3000 诊断报告](Agents/PA12双轴试样仿真/验证/2026-09-26_TC3000竖直网格局部加密比较.md)、`index.md`、阶段计划及 GPT 交接文档/状态；原始 STEP 未改写，全量 Abaqus 工程在 `D:\PA12_Stage2\g0_tc3000_vertical_mesh_diagnostic_20260926\`。
- 下一步：将 `WarnElemDistorted` 单元映射到中心过渡带/边种子区，并检查控制点 U/RF；调整局部尺寸增长后再决定是否重跑。

## [2026-09-26] audit | 单轴 ROI 包络与实体几何门槛对照

- 来源：[G1 DIC ROI 尺寸候选卡](raw/PA12_Stage2_Evidence/阶段2_G1_DIC标定图像ROI尺寸候选.md)、[单轴几何证据缺口](Agents/PA12实验数据处理/处理记录/PA12单轴几何证据缺口.md)、S19–S22 生产 DIC 支持摘要与原图叠加。
- 发现：S19 的轴对齐外接框为 11.525×65.848 mm，而最小面积旋转包络候选为 10.510×66.000 mm；两者都是 Job ROI 几何，不是实体尺寸。S19–S22 完整 ROI 支持率为 84.8667%/83.5938%/84.1189%/71.1951%。
- 判定：ROI 面积与支持分布可追溯，但仍无样品编号绑定的单轴厚度/有效宽度/标距证据；照片不能证明缺口区域同厚度。完整 Job ROI 主口径和独立 subset 敏感性不变，未补场、未进行正式参数拟合。
- 更新：[几何门禁页](Agents/PA12实验数据处理/处理记录/PA12单轴几何证据缺口.md)、`index.md`；原始数据只读。
- 下一步：取得或定位 S19–S22 对应的实测截面/厚度/标距及打印/装夹记录；再判定周缘缺口是否可在相同材料/厚度区域内通过独立 DIC 支持扩展恢复。S22 内部孔洞先单独核查。

## [2026-09-26] audit | S16 ODB 参考点 U/RF 与机器力对照

- 输入：S16 峰值回放 ODB `G4_S16_TC1000_PEAK_VERTICAL_H4.odb`、峰值帧同步机器力、输入卡的四个加载/约束参考点定义；ODB 以只读方式打开，原始实验文件未修改。
- 提取：[参考点 U/RF CSV](Agents/PA12双轴试样仿真/验证/2026-09-26_S16峰值位移真实STEP回放参考点审计.csv)、[参考点 U/RF JSON](Agents/PA12双轴试样仿真/验证/2026-09-26_S16峰值位移真实STEP回放参考点审计.json)，脚本 [extract_s16_odb_reference_points.py](Agents/PA12双轴试样仿真/验证/extract_s16_odb_reference_points.py)；原始 ODB 和同名结果副本位于 `D:\PA12_Stage2\g4_tc1000_s16_source_step_peak_replay_20260926_r2\`。
- 结果：四参考点合反力 `(0.000244, -0.000076, 0.0000029) N`，整体平衡误差约 `2.6×10⁻⁴ N`。按机器 X→FE-Y、机器 Y→FE-X 的已记录映射，FE-X/XMAX 对机器-Y 力比 `2.4202`，FE-Y/YMAX 对机器-X 力比 `2.0846`；控制点存在非加载方向位移。本结果确认有限元内部反力平衡，不确认实验力—位移复现。
- 更新：[S16 回放诊断](Agents/PA12双轴试样仿真/验证/2026-09-26_S16峰值位移真实STEP回放诊断.md)、`index.md`、阶段计划及 GPT 交接状态。
- 待验证：临时材料卡、机架相对位移与试样端面位移的关系、边界自由度和坐标注册对幅值差异的贡献尚不能区分。下一步对同一物理 ROI 做 FE–DIC 空间配准，并把畸变单元位置映射到 ROI/过渡带/狭缝端；之后再决定校准或模型修改。

## [2026-09-26] audit | S16 WarnElemDistorted 中心 ROI 空间定位

- 输入：S16 回放 `.dat/.inp/.odb`，中心 ROI `28×28 mm`；原始 STEP、实验照片和力数据未修改。
- 方法：将 `.dat` 的 1,373 个 `WarnElemDistorted` 标签映射到 ODB/输入网格；ODB 全 10 节点算术均值与 `.inp` 四角节点位置均值的 ROI/过渡带/外区分区计数一致。另以全部 10 个节点坐标包围盒核查中心 ROI 平面相交。
- 结果：总网格 `36,463` 个单元；畸变单元位置分类为中心 ROI/14–16 mm 过渡带/臂部外区 `21/752/600`，中心 ROI 位置半径 `8.25–13.12 mm`，中央 `14×14 mm` 子区无告警单元。四角节点位置代理的 21 个中心标签均在 `|z|≤0.5 mm`；26 个单元包围盒与 ROI 平面相交，另有 5 个边界相交标签。该结果不等于真实体积交叠率或场误差。
- 更新：[S16 回放诊断](Agents/PA12双轴试样仿真/验证/2026-09-26_S16峰值位移真实STEP回放诊断.md)、`index.md`、GPT 交接文档/状态；未重跑 Abaqus。
- 下一步：核对机架相对位移与试样端面位移、完成同一物理 ROI 的 FE–DIC 配准；计算畸变单元与 ROI 的真实交叠/体积分数及场指标敏感性。正式材料校准和设计排名继续挂起。

## [2026-09-26] experiment | S16 峰值帧 FE–DIC 位移候选对照

- 输入：S16 峰值帧 ODB、`z=+0.5 mm` FE 上表面节点 U、现有 DIC—力合并表 `000256_DIC全场—力.csv`；原始 DIC 文件只读。坐标/位移轴置换沿用已有候选预检变换，不视为正式标定。
- 方法：对 225 个 FE 上表面节点建立 2D 线性 Delaunay 插值，只在 FE 节点凸包内计算；不对覆盖外测点外推。输出逐点比较 CSV、汇总 JSON 和残差图。
- 结果：DIC 点 `10,098` 个，公共覆盖 `8,554` 个（`84.7098%`），未覆盖 `1,544` 个，低于 `0.95` 门槛。原始 U1/U2 RMSE=`2.5456/2.6363 mm`，均值偏置=`2.5121/2.6072 mm`；减去拟合常量偏置后的 RMSE=`0.4112/0.3909 mm`，相关系数=`0.9438/0.9532`。偏置校正和高相关仅描述候选空间趋势，不构成 FE–DIC 验证；FE/DIC ROI、机器—试样端面位移及方向符号尚未闭合。
- 更新：[S16 回放诊断](Agents/PA12双轴试样仿真/验证/2026-09-26_S16峰值位移真实STEP回放诊断.md)、[逐点 CSV](Agents/PA12双轴试样仿真/验证/2026-09-26_S16_FE-DIC峰值位移候选.csv)、[JSON](Agents/PA12双轴试样仿真/验证/2026-09-26_S16_FE-DIC峰值位移候选.json)、[候选图](Agents/PA12双轴试样仿真/验证/2026-09-26_S16_FE-DIC峰值位移候选图.png)、FE 节点 CSV、`index.md`、阶段计划及 GPT 交接状态/文档。完整 Abaqus 文件及计算结果保存在 `D:\PA12_Stage2\g4_tc1000_s16_source_step_peak_replay_20260926_r2\`。
- 下一步：以物理图像标记/夹具轴核实 DIC 原点、方向符号、镜像和机器相对位移到试样端面的关系；调整峰值 FE 表面网格/共同 ROI，使不外推覆盖通过门槛，再做同一物理 ROI 位移对照。之后核算畸变单元与 ROI 的真实体积交叠和场指标敏感性。

## [2026-09-26] audit | S16 FE-DIC 候选映射尺度敏感性

- 输入：峰值帧 `000256.jpg` DIC 合并点、FE 上表面节点位移及既有候选原点/轴向；原始 DIC 和 ODB 未改写。
- 方法：保持候选原点、轴交换/反射、FE 节点和二维插值不变，仅将 FE-X/FE-Y 变换缩放从 `1.0033368/1.0290634` 改为 `1/1`；DIC 坐标与位移分量均保留原标定尺度。
- 结果：预检缩放覆盖 `8,554/10,098=84.71%`，保留原尺度覆盖 `8,742/10,098=86.57%`，两者均低于 `95%`。原始 RMSE 分别为 `2.546/2.636 mm` 与 `2.545/2.634 mm`；去偏置 RMSE 分别为 `0.411/0.391 mm` 与 `0.410/0.388 mm`。去掉缩放使覆盖增加 `1.86` 个百分点，但没有解除候选原点、方向和样品—STEP 对应不确定性。
- 更新：[尺度敏感性 CSV](Agents/PA12双轴试样仿真/验证/2026-09-26_S16_FE-DIC候选尺度敏感性.csv)、[S16 回放诊断](Agents/PA12双轴试样仿真/验证/2026-09-26_S16峰值位移真实STEP回放诊断.md)、`index.md`、GPT 交接状态。
- 结论与下一步：两套残差都只作候选诊断，不作为 FE–DIC 通过。正式对照固定原 `0.087209 mm/pixel`，确认物理原点后仅在共同 ROI 比较；先核实机器相对位移与试样端面位移，再解决低于门槛的 FE 表面覆盖。

## [2026-09-26] audit | PA12 逐组诊断交付总览刷新

- 来源：`Agents/PA12实验数据处理/处理记录/PA12应力应变曲线审计.json`、`PA12批量处理清单.json`、`Agents/PA12实验数据处理/VFM自建/汇总/PA12自建VFM阶段A一致性审计.json` 与 8 组阶段 A 结果 JSON。
- 更新：刷新 [逐组诊断交付总览](Agents/PA12实验数据处理/VFM自建/汇总/PA12逐组诊断交付总览.md) 及同名 CSV/JSON，并确认索引入口。
- 结论：10 组曲线状态为 PASS 6、REVIEW_REQUIRED 3、PRELOAD_RELEASE_ONLY 1；阶段 A 8 组、1127 帧的派生文件一致性审计通过。该审计不证明物理虚功闭合，也不放行正式材料参数。
- 待验证：S15/S22/S23 曲线事件、完整 Job ROI 的 DIC 面积支持与外功边界、S16 FE–DIC 物理配准及正式本构/参数门槛仍未闭合。

## [2026-09-26] audit | S22 曲线终点照片复核

- 来源：S22 应力—应变 CSV、照片—力对应表、原始 `001776.jpg` 与 `001784.jpg`；照片只读。
- 方法：按曲线实际列头复算峰值、峰后最低应力比与末两帧力降，并对照两张原始全幅照片。
- 结果：峰值在 `001024.jpg`，`50.3433 MPa`；`001784.jpg` 为 `10.4433 MPa`，占峰值 `20.7442%`，略高于自动门槛 `20%`。末一步力从 `1332.21 N` 降到 `313.30 N`，下降 `76.48%`。所查两帧未提供独立、清晰的断裂视觉证据。
- 结论与下一步：保持 `REVIEW_REQUIRED`，不改自动阈值、不补断裂力、不改应力—应变曲线。完整逐组结论见[曲线审计](Agents/PA12实验数据处理/处理记录/PA12应力应变曲线审计.md)。

## [2026-09-27] experiment | S16 实际外表面 FE–DIC 与对称夹爪诊断归档

- 输入：2026-09-26 生成的 S16 `Pos` 通道审计、单侧/对称边界 Abaqus ODB、C3D10 外表面片插值结果和 IVOL 均匀性指标；原始工作簿、DIC 文件、STEP 与既有 Abaqus 工程保持只读。
- 方法：将 D 盘候选 CSV/JSON/PNG 归档到 Vault；将 4 个复现脚本复制到对称候选工程目录；以实际 C3D10 外表面邻接和二次三角形形函数复核覆盖，不外推。
- 结果：128 个实际表面三角面、289 个节点覆盖 `10,098/10,098` DIC 点（100%）。旧 225 节点线性凸包的 `84.71%` 是边界节点过滤导致的低报。Pos 两轴相对开口与 FE 目标差约 `0.24%/0.27%`，但 Pos 通道不提供夹爪全局运动符号。对称边界候选 FE–DIC RMSE 为 `0.4284/0.4167 mm`、相关系数 `0.99836/0.99870`；加载反力仍是实验力的 `2.02/2.40` 倍。均匀性分数下降，但过渡带峰值比从 `1.9374` 增至 `2.1357`，体现指标权衡。
- 更新：[S16 回放诊断](Agents/PA12双轴试样仿真/验证/2026-09-26_S16峰值位移真实STEP回放诊断.md)、`index.md`、[PA12 总目标与阶段计划](Agents/PA12实验数据处理/处理记录/PA12总目标与阶段计划.md)、GPT 交接文档/状态；新增 Pos、真实表面节点、单侧/对称 FE–DIC、对称反力及均匀性数据与图。候选全量工程保存在 `D:\PA12_Stage2\g4_tc1000_s16_symmetric_grips_candidate_20260926\`。
- 限制与下一步：对称边界仍为诊断候选，存在 2 条参考点数值奇异警告、`1,373/36,463` 个畸变单元，材料卡仅为临时正交弹性；DIC 原点/方向/镜像、样品—STEP 对应和机架—试样端面位移关系尚未标定。先闭合这些运动学与配准证据，再定位数值告警影响并以实测标定材料复核反力；不进行正式 FE–DIC 验证、断裂判断或设计排名。

## [2026-09-27] audit | S16 畸变单元 IVOL 与场指标敏感性

- 输入：S16 峰值回放 ODB 与 WarnElemDistorted 位置精核 JSON；ODB 只读，未重跑 Abaqus，原始实验数据未修改。
- 方法：在完整 Job ROI 的现行元素质心选择下，按 IVOL 对 S11/S22/LE11/LE22 统计；另剔除 ROI 内 21 个警告单元作敏感性对照。
- 结果：完整 ROI 选入 415 个单元/1660 个积分点，IVOL 合计 822.2938 mm³；相对名义 28×28×1 mm³ 的 784 mm³ 高 4.8844%。21 个警告单元占当前选入 IVOL 的 2.7263%；剔除后四场均值变化小于 0.046%，标准差/CV 变化 0.97%–2.36%。另有 26 个包围盒相交警告单元，其中 5 个质心在 ROI 外。
- 判定：场指标剔除敏感性已完成，但全单元质心积分不是精确几何裁切；包围盒候选数不等于真实体积交叠。保持完整 Job ROI 主口径、DIC subset 内缩域独立敏感性；仍不发布正式参数或设计排名。
- 更新：[S16 畸变单元敏感性报告](Agents/PA12双轴试样仿真/验证/2026-09-27_S16畸变单元IVOL与场指标敏感性.md)、阶段计划、GPT 交接文档/状态及 index.md。
- 下一步：核算精确三维几何交叠，继续闭合 S16 FE–DIC 物理配准及机架位移—试样端面位移关系。

## [2026-09-27] audit | S16 参考点奇异警告与输入约束映射核查

- 输入：S16 单侧基线及对称夹爪候选 `.inp/.msg`；均只读检查，未重新求解或修改 Abaqus 输入卡。
- 发现：两作业均在 `CRUCIFORM-1.1` 的 DOF 2/3 报告相同数值奇异比值 `1.E+09/1.E+12`。基线输入卡中 `_PickedSet8`（XMIN 耦合参考点）与 `_PickedSet15`（XMIN 边界点）均为节点 1；后者明确约束 U1–U3。对称候选保持同一约束，仅改变四个加载端位移。
- 结论：已排除 XMIN DOF 2/3 漏设平动约束这一简单解释；但现有 `.msg` 没有给出方程/约束链诊断，不能据此判为过约束或稳定，根因仍未定位。未为消除警告而删改边界。
- 来源与下一步：[S16 回放诊断](Agents/PA12双轴试样仿真/验证/2026-09-26_S16峰值位移真实STEP回放诊断.md)、[Abaqus 2025 过约束检查说明](https://docs.software.vt.edu/abaqusv2025/English/SIMACAECSTRefMap/simacst-c-overconstraintchecks.htm)。后续在隔离副本中用适用的 Abaqus 方程级诊断追查，并同时完成图像坐标/夹爪运动方向和机架—试样端面位移配准。
## [2026-09-27] audit | S16 DIC subset 中心域全帧坐标核对

- 输入：S16 原始 `Job.m2inp` 与 `000001/000128/000257.jpg.dat`；源文件只读。
- 方法：按已核实的 `<18>/<53>` DAT 字段逐个解析同步的 257 帧有效点坐标，并与原 Job Shape、subset `15 px`、step `3 px` 对照。
- 结果：257 帧各有 10,098 个有效点，且坐标外接框全程恒定：X=`411–705 px`、Y=`419–722 px`；原 Job ROI 为 X=`402–714 px`、Y=`410–730 px`，有效点中心相对四边内缩 `9/9/9/8 px`。候选扩展测量选区为 X=`393–723 px`、Y=`401–739 px`，尚未运行。
- 判定与后续：[Stage 2 独立性审计](Agents/PA12实验数据处理/VFM自建/汇总/PA12Stage2现行实现与虚功独立性审计.md)已记录坐标和实现约束。扩展仅用于获取 DIC 边缘测量支撑；VFM 仍须使用原始完整 Job Polygon，subset 内缩域单独作敏感性。因边缘 subset 可能跨越邻近厚度过渡，必须检查相关质量与覆盖；不插值、不外推。原始 Job/DAT 未修改。

## [2026-09-27] experiment | S16 夹爪图像位移与 Pos 时间同步核验

- 输入：S16 原始四夹爪图像、`Job.m2inp` 像素换算、DIC 合并帧时间及只读 `Pos` 工作簿；原始图像、工程文件和工作簿未修改。
- 方法：在启动帧固定四个夹爪纹理 ROI，以整数像素 NCC 追踪 8 帧；按 DIC CSV 时间与 Pos `T` 列做线性插值，未把时间换算为行号。Pos 截止 `25.733 s` 有 `25,673` 条记录，其中 `1 ms` 间隔 `25,611` 次、`2 ms` 间隔 `61` 次；按 `t×1000` 作行号会错开 `61 ms`。
- 结果：峰值 `000256.jpg` (`25.7335 s`) 的四端外张位移为 `30–31 px`，按 `0.087209 mm/px` 换算为 `2.6163–2.7035 mm`，NCC=`0.9782–0.9904`；四路 Pos 均值为 `2.572875 mm`、极差 `0.0029 mm`，与图像位移差约 `1.7%–5.1%`。四路编码器在 8 个采样时刻的相关系数 `0.9999987–0.9999993`，不能辨识轴通道与图像端点配对。
- 更新：[S16 运动学核验报告](Agents/PA12双轴试样仿真/验证/2026-09-27_S16夹爪图像位移与Pos时间同步核验.md)、[追踪图](Agents/PA12双轴试样仿真/验证/2026-09-27_S16夹爪影像位移_Pos同步核验.png)、逐帧 CSV/JSON、`index.md`、[PA12 总目标与阶段计划](Agents/PA12实验数据处理/处理记录/PA12总目标与阶段计划.md)；派生数据同时保存在 `D:\PA12_Stage2\g1_s16_grip_image_motion_20260927\`。
- 判定与下一步：支持四端在图像坐标下向外运动，不构成硬件全局符号、机器—DIC 仿射变换或端面位移标定。由于等双轴 Pos 通道高度共线，下一步须在同一机位分别对 X/Y 夹爪对做已知低载荷微动并加方向标记，再结合逐件打印布局闭合材料轴映射。

## [2026-09-27] experiment | PA12 自建 VFM 模型应力—应变比较图

- 输入：完整 Job ROI 与 DIC subset 内缩域敏感性下已有的 12 份模型对比 CSV；未重跑 VFM，原始 JPG/DAT/XLS 保持只读。
- 方法：在 `tools/run_pa12_self_vfm.py` 增加独立模型比较图输出；实测/边界等效应力按 CSV 行绘制散点，非空模型预测按等效塑性应变排序连线；当前无模型预测时清除同名过期图。Voce I/II 标记为通用模型。
- 结果：完整 Job ROI 6 组、subset 内缩敏感性 3 组有模型预测，共生成 9 张 PNG；S17 两分支及 S21 主分支预测行数为零，不生成占位图。自动绘图行为回归测试通过。
- 更新：[Stage 2 实现与虚功独立性审计](Agents/PA12实验数据处理/VFM自建/汇总/PA12Stage2现行实现与虚功独立性审计.md)、`index.md`、绘图函数及测试。
- 限制与下一步：这些图仍表达现行力耦合名义曲线诊断，不能证明独立全场虚功闭合、参数可辨识或正式材料参数。继续完成基于 DIC 局部应力恢复的独立 VFM 与模型验证。

## [2026-09-27] experiment | PA12 竖直取向四厚度位移比矩阵

- 输入：TC1000/1500/2000/2500 真实 STEP；TC1000、TC2000 新增 5 个缺失组合，合并已有 TC1500/TC2500 同口径竖直 `r=0.5/1/2` 结果。所有 Abaqus 全量工件保留在 D 盘 `D:\PA12_Stage2`，未修改源 STEP 和已有 ODB。
- 方法：Abaqus/Standard、C3D10、`h=1.6 mm`、`vertical_z_in_plane`、临时线弹性材料卡；`ΔX=0.05 mm`、`ΔY=0.025/0.05/0.10 mm`。按中心 ROI 质心选取和积分点 `IVOL` 加权汇总 `LE`/应力场指标。
- 结果：12 个工况均正常结束；错误和负特征值警告为 0，但每组仍有 1–2 条数值奇异警告。畸变单元比例为 `1.0131%–1.8198%`。四个厚度下 `r=1` 的综合 CV 分数与应变失衡指标均最低；过渡带峰值比仍高于中心区，且不满足最终设计/物理验证门槛。
- 更新：[矩阵筛查报告](Agents/PA12双轴试样仿真/验证/2026-09-27_竖直位移比四厚度矩阵筛查.md)、CSV/JSON、预筛图、TC1000/TC2000 网格截图、`index.md`、[阶段计划](Agents/PA12实验数据处理/处理记录/PA12总目标与阶段计划.md)、[GPT 交接文档](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)及机器状态。
- 限制与下一步：本轮是小位移线弹性诊断，不预测塑性、断裂、DIC 可测性或 VFM 可识别性，不据此选出最优几何。先在隔离副本追查数值奇异与畸变单元影响，再做有物理依据的局部网格复算；并行闭合夹具—DIC 运动学、打印方向和标定材料证据。

## [2026-09-27] experiment | PA12 竖直矩阵面外刚体模态约束探针

- 输入：四个厚度、三个位移比的 12 份原始 `.inp/.odb` 与中心 ROI 预筛指标；原模型与源 STEP 只读。
- 方法：在 D 盘新建隔离模型副本，仅对 YMIN 与 XMAX 参考点增加 `U3=0`，重算 Abaqus/Standard 12 工况；使用相同 `postprocess_uniformity.py`、固定中心 ROI 和 IVOL 权重提取结果。
- 结果：12/12 正常完成；数值奇异警告、负特征值警告和错误数均为 0。相对基线的综合分最大变化 `0.000073%`、K 最大绝对变化 `9.7×10⁻⁹`、过渡带峰值比最大变化 `7.9×10⁻⁵`。TC1000/1500/2000/2500 各自最低综合分仍为 `r=1`。畸变单元比例 `1.0131%–1.8198%` 未消失。
- 更新：[矩阵及约束探针报告](Agents/PA12双轴试样仿真/验证/2026-09-27_竖直位移比四厚度矩阵筛查.md)、面外约束版 CSV/JSON/PNG、`index.md`、[阶段计划](Agents/PA12实验数据处理/处理记录/PA12总目标与阶段计划.md)、[GPT 交接文档](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)及机器状态；12 组全量探针作业保存在 `D:\PA12_Stage2\g1_out_of_plane_restraint_probe_matrix_20260927\`。
- 判定与下一步：结果支持面外刚体转动欠约束是原警告来源，且该数值处理对当前线弹性场指标影响可忽略；但 `U3=0` 是否符合真实夹具仍待夹具结构/装夹证据确认。下一步定位畸变单元并评估局部网格影响，随后结合物理边界和标定材料继续设计筛查。

## [2026-09-27] experiment | S19 单轴有限变形 J2 双域 50% 窗口诊断

- 输入：S19_X_0.2 的 126 帧 DIC—力历程；峰前拟合上限为 000126.jpg，50% 实际窗口为 000002–000063.jpg，共 62 帧。完整 Job ROI 为主域，DIC subset 内缩域单独作为敏感性分支。
- 方法：固定 ν=0.375，分别固定既有阶段 1 的 E 候选；采用有限变形 J2 正线性各向同性硬化候选，厚度 1.0 mm 作为未实测工作假设。
- 结果：主域条件 E/Y0/H=2577.886/335.526/208.215 MPa，覆盖 84.8667%，拟合窗合并残差 RMS=157.819 N；内缩分支为 2267.323/295.081/1368.008 MPa，覆盖 100%，拟合窗合并残差 RMS=168.590 N。内缩分支 H 比主域高约 557%，两域内外虚功未闭合。
- 更新：双域诊断报告、总阶段计划、GPT 交接文档/状态和 index.md。完整 Job ROI 主口径与内缩域敏感性分支保持分离。
- 下一步：先核实 S19 实测单轴几何/ROI、机器—DIC 有向轴、外功虚位移条件与论文 H 符号；75%/100% 窗口未完成。本结果不发布材料参数，不作为训练标签。

## [2026-09-27] experiment | TC2500 过渡带局部网格敏感性

- 输入：TC2500 真实 STEP、`r=1` 全局 `h=1.6 mm` 面外约束探针，以及全局 1.6 mm + 局部边播种 1.2/0.8 mm 的两份独立模型；源 STEP、基线输入和 ODB 均只读。
- 方法：两档局部播种均选择 152 条 `14–16 mm` 环带 B-rep 边；保持 `vertical_z_in_plane`、`ΔX=ΔY=0.05 mm`、临时正交线弹性材料与 YMIN/XMAX 参考点 `U3=0`。使用同一 IVOL 后处理和畸变单元位置审计。
- 结果：三组单元数为 `84,403/102,521/134,424`，畸变占比 `1.8198%/1.2807%/0.9634%`；中心平均 LE11/LE22 差异均不超过约 `0.06%`。`PrimaryScore` 为 `0.073733/0.068936/0.060870`，`K` 为 `0.033758/0.033427/0.033630`，`G_transition` 为 `2.234678/2.907334/2.749953`。局部 0.8 mm 的过渡峰值仍较全局基线高 `23.1%`；脚本提取的最小质量指标从 `1.76398e-8` 降至 `8.11864e-10`。三组求解均无数值问题、负特征值或错误。
- 判定：局部播种使畸变单元占比下降，但最差质量指标没有改善，且过渡峰值对网格仍敏感；中心平均场稳定不能替代峰值收敛、断裂控制或 VFM 可识别性验证。本轮不作设计排序。
- 更新：[局部网格敏感性报告](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2500局部网格加密敏感性.md)、两张局部网格截图、`index.md`、阶段计划、GPT 交接文档/状态及矩阵筛查报告；完整 CAE/INP/ODB/CSV/JSON/求解日志保存在 D 盘 `PA12_Stage2` 局部网格目录。
- 下一步：将变量聚焦到 `14–16 mm` 过渡带圆角和厚度坡度，建立少量可解释的几何对照；正式排序前确认真实夹具面外约束并标定材料，之后把 DIC/VFM 可观测性和参数可识别性纳入指标。

## [2026-09-27] audit | TC2500 STEP 微边与畸变位置关联

- 输入：TC2500 源 STEP、局部 0.8 mm 模型的畸变单元坐标清单；源 STEP 与 ODB 只读。
- 方法：用 Abaqus/CAE 从 STEP 导入几何，统计边的长度和 `pointOn` 坐标；将局部网格畸变单元四角节点质心与近似的 `(±15,±15,±1.5) mm` 角点距离作空间对照。
- 结果：STEP 为 `1` 个 cell、`148` 个 face、`424` 条 edge、`280` 个 vertex。过渡环带 152 条边中，8 条长度为 `0.00125 mm`，位于四个过渡角点的上下表面；另有 8 条约 `0.475 mm` 边。局部 0.8 mm 网格的 1,295 个畸变单元中，100/196/454 个角节点质心分别距上述角点不超过 1/2/5 mm。
- 判定：小边与畸变集中区存在空间关联，但距离统计不证明因果，也不能判断微边是否对应真实打印几何。作为下一项隔离实验，在 CAE 副本仅忽略 8 条 `0.00125 mm` 边，通过相同网格/载荷/ROI 比较质量和场指标；原 STEP 不变。Abaqus `Part.ignoreEntity()` 用于创建虚拟拓扑并在网格生成中忽略选定边/顶点，见[官方 Part API](https://docs.software.vt.edu/abaqusv2025/English/SIMACAEKERRefMap/simaker-c-partmgnpyc.htm)。
- 更新：[TC2500 局部网格敏感性与拓扑关联报告](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2500局部网格加密敏感性.md)、`index.md`、阶段计划、GPT 交接文档/状态；正确标识的 STEP 边清单与摘要保存在 D 盘 `g1_tc2500_step_edge_inventory_20260927\feature_inventory\`。

## [2026-09-27] experiment | TC2500 微边虚拟拓扑对照

- 输入：TC2500 源 STEP、全局 `1.6 mm` 原拓扑基线及 8 条 `0.00125 mm` 过渡角点微边清单；源 STEP、原始 CAE/INP 与基线 ODB 保持只读。
- 方法：在独立 CAE 副本用 `Part.ignoreEntity()` 忽略过渡带内 `<=0.01 mm` 的 8 条边，重建全局 C3D10 网格；只在求解输入副本中加入 YMIN/XMAX `U3=0`，保持 `vertical_z_in_plane`、`r=1`、临时正交弹性材料、位移与 IVOL ROI 指标口径一致。
- 结果：作业完成，84,099 个单元、1,568 个畸变（1.8645%），四角节点质心中心/过渡/外区 `0/1566/2`。相对原拓扑基线 `84,403/1,536（1.8198%）`，最小四面体质量指标从 `1.76398e-8` 提高到 `4.78227e-7`，但仍远低于 Abaqus 建议 `0.02`；最小/最大角为 `0.0487°/178.318°`。`PrimaryScore=0.076167`、`K=0.033879`、`G_transition=2.240335`，均未优于基线 `0.073733/0.033758/2.234678`。分析数值警告、负特征值警告及错误为 0；`.dat` 报告 1,568 个畸变单元。
- 判定：仅忽略微边不是有效网格改进方案；最小质量改善与畸变率/场指标方向不一致，不据此证明微边与畸变存在因果关系，也不宣称收敛或设计优胜。
- 更新：[虚拟拓扑试验报告](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2500虚拟拓扑微边试验.md)、[局部网格报告](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2500局部网格加密敏感性.md)、网格截图、`index.md`、阶段计划、GPT 交接文档/状态；全量 CAE/INP/ODB/CSV/JSON/求解输出保存在 `D:\PA12_Stage2\g1_tc2500_virtual_topology_microedge_probe_20260927\`。
- 下一步：从真实 STEP 提取中心减薄过渡面的几何尺寸，在可复现参数化副本中对圆角或厚度坡度做单变量几何对照；不再把微边忽略作为默认策略。正式排序前仍需确认面外夹具、打印方向及实测材料参数，再纳入 DIC/VFM 指标。

## [2026-09-27] experiment | TC2500 参数化中心减薄几何与加载比筛查

- 输入：只读 TC2500 源 STEP（`02_a2p0.25mm.step`）、源 STEP 的 `r=1` 竖直线弹性基准；本次所有 CAE 和求解文件均写入 `D:\PA12_Stage2` 独立目录。
- 方法：按源顶面轮廓重建十字和 28 条槽，在独立副本形成总厚 `3.0 mm`、中心厚 `2.5 mm`、中心半宽 `14.75125 mm`、单侧线性减薄过渡宽 `0.24875 mm` 的候选。采用 `vertical_z_in_plane`、临时正交弹性材料、全局 C3D10 `h=1.6 mm`，求解 `r=ΔY/ΔX=0.5/1/2`，以固定中心 ROI 和 IVOL 权重评估场量。
- 结果：三工况均完成；每个候选有 `137580` 节点、`82070` 单元，`.dat` 报告 86 个畸变单元（`0.1048%`，84 个在过渡带、2 个在外区、ROI 内 0 个）。原型 `r=1` 的 `PrimaryScore/K/G_transition` 为 `0.0856866/0.0334814/2.13013`，源 STEP 基准为 `0.0737332/0.0337579/2.23468`；中心应变均值基本相同。`r=0.5/2` 的 `K` 分别为 `0.616175/0.536350`。分析数值问题、负特征值警告和错误数均为 0。
- 判定：本原型尚未改善中心均匀性，且线性坡面近似源曲面、临时材料与端部边界未获实物确认；畸变率下降不能与几何改变分离归因。该结果仅为参数化/加载比先导筛查，不验证塑性、断裂、DIC/VFM 或最终设计。
- 更新：[参数化原型报告](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2500参数化中心减薄几何原型与加载比筛查.md)、[筛查 CSV](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2500参数化中心减薄几何原型与加载比筛查.csv)、几何/网格及应变云图、`index.md`、阶段计划和 GPT 交接文档/状态。原型分析和汇总表位于 `D:\PA12_Stage2\g2_tc2500_center_transition_w0p24875_r*_20260927\` 与 `D:\PA12_Stage2\stage2_tc2500_w025_ratio_screen_20260927.csv`。
- 下一步：对过渡宽度/坡度建立有足够局部网格分辨率的单变量配对，先排除离散误差，再评价均匀性与过渡峰值；实测材料、夹具边界闭合后才进入塑性及 DIC/VFM 可识别性分析。

## [2026-09-27] experiment | TC2500 参数化过渡宽度与网格敏感性

- 输入：只读 TC2500 源 STEP `02_a2p0.25mm.step`、既有源 STEP `r=1` 基准及参数化坡面原型；所有新模型、输入卡、ODB、日志和指标文件保存在 `D:\PA12_Stage2`。
- 方法：固定总厚 `3.0 mm`、中心厚 `2.5 mm`、中心半宽 `14.75125 mm`、单侧减薄 `0.25 mm`、竖直材料轴、`ΔX=ΔY=0.05 mm` 和临时正交线弹性材料。以 `h=1.6 mm` 比较 `4.8/9.6/14.4 mm` 三个坡面宽度；随后对 `9.6 mm` 几何比较 `h=1.6/1.2/1.0/0.8 mm`。中心 ROI 固定 `±14 mm`，积分点按单元质心选择并以 IVOL 加权。
- 结果：粗网格宽度筛查中 `9.6 mm` 得到最低 PrimaryScore `0.0723866`（比真实 STEP 参照低 `1.83%`），但中心打印轴 `LE22` 均值低约 `0.76%`，`G_transition=2.25061` 略高于基准。网格系列 PrimaryScore 相邻变化 `−8.72%/−4.41%/+0.61%`，`G_transition` 变化 `+5.69%/−1.50%/+1.50%`；最细三个连续尺度的相邻变化小于 `5%`，但 `1.6→1.2 mm` 超限。宽度工况畸变单元 `2/10/5`，网格工况 `10/3/1/0`；所有作业成功结束，数值问题警告、负特征值警告和错误均为 0。
- 判定：过渡坡面进入开槽臂段，宽度效果与槽区耦合；中心厚度和半宽不变，中心打印轴应变没有提高，过渡峰值比仍约 `2.2–2.4`。只将细网格段记为初步稳定，不宣称正式收敛，不选定最终设计；材料、夹具、塑性、断裂、DIC/VFM 可识别性均未验证。
- 更新：[过渡宽度与网格报告](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2500过渡宽度单变量筛查.md)、两份 CSV、几何/网格/LE33 截图、`index.md`、阶段计划、GPT 交接文档与状态 JSON。
- 下一步：把几何变量转到直接改变中心刚度的中心厚度/有效区设计；维持竖直材料轴和加载比口径，并在候选比较中保留至少三个网格尺度以及中心应变、均匀性、过渡峰值和 DIC/VFM 观测门槛。

## [2026-09-27] experiment | TC2500 中心厚度与细网格敏感性

- 输入：只读源 STEP `02_a2p0.25mm.step` 和既有 `2.5 mm`、9.6 mm 过渡基准；所有新 CAE、INP、ODB 和求解输出写入 `D:\PA12_Stage2` 独立目录。
- 方法：保持总厚 `3.0 mm`、中心半宽 `14.75125 mm`、过渡宽 `9.6 mm`、`vertical_z_in_plane`、`ΔX=ΔY=0.05 mm`、临时正交线弹性材料、C3D10 和固定 ±14 mm IVOL 加权 ROI。粗筛中心厚度 `2.5/2.0/1.5 mm`；对 `2.0 mm` 复算 `h=1.6/1.2/1.0/0.8 mm`。
- 结果：粗筛 `2.0/1.5 mm` 中心平均 `LE22` 相对 `2.5 mm` 提高 `19.22%/48.41%`，PrimaryScore 变化 `+2.15%/+10.84%`，畸变单元数 `179/147`。`2.0 mm` 网格序列单元数 `92,422/157,127/202,266/339,707`、畸变单元 `179/1/3/2`；细三档 PrimaryScore 相邻变化 `+1.74%/+1.28%`，`G_transition` 变化 `−3.41%/+2.77%`，中心 `LE22` 均值近似不变。全部 5 个本轮分析作业均正常完成。
- 判定：只记录细网格段初步稳定；`1.6→1.2 mm` PrimaryScore 变化 `−17.07%`，不称整个序列正式收敛。中心厚度变化同时改变坡面角；当前 `LE22≈0.025%`，属于小位移线弹性筛查，未验证约 `8%` 实验应变、塑性、断裂、DIC/VFM 或最终设计。
- 更新：[中心厚度筛查报告](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2500中心厚度与细网格敏感性.md)、[厚度 CSV](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2500中心厚度粗筛.csv)、[网格 CSV](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2000细网格敏感性.csv)、几何/网格/LE33 截图、`index.md`、总目标与阶段计划、GPT 交接文档及机器状态 JSON。D 盘工件目录：`g4_tc2500_center_thickness_*_20260927`、`g5_tc2000_mesh_h*_20260927`。
- 下一步：为 `1.5 mm` 档完成 `h=1.2/1.0/0.8 mm` 同口径复算和同尺度对照，再检查中心 ROI 厚度区交叠、坡面/槽端峰值，并逐步接入实测材料、夹具边界与 DIC/VFM 可观测性约束。

## [2026-09-27] experiment | TC1500 中心厚度网格敏感性续算

- 输入：只读 TC2500 源 STEP、中心厚度 `1.5 mm` 参数化候选及既有 `h=1.6 mm` ODB；新增工件保存在 D 盘独立 `g6_tc1500_mesh_h*` 目录。
- 方法：保持总厚 `3.0 mm`、中心半宽 `14.75125 mm`、过渡宽 `9.6 mm`、竖直材料轴、`r=1`、临时正交线弹性卡及固定中心 ROI/IVOL 后处理；新增全局 C3D10 `h=1.2/1.0/0.8 mm` 三档。
- 结果：三作业均正常完成。四档中心平均 `LE22` 为 `0.0003146975/0.0003145820/0.0003145037/0.0003145513`，相邻变化绝对值均小于 `0.04%`、全序列最大—最小差约 `0.062%`；细档 PrimaryScore 相邻变化 `+12.26%/−6.79%`，`G_transition` 变化 `+3.49%/+2.58%`。细档畸变单元为 `2/0/9`。
- 同尺度比较：`1.5 mm` 相对 `2.0 mm` 在 `h=1.2/1.0/0.8 mm` 的中心 `LE22` 均高约 `24.4%`，但 PrimaryScore 在不同网格下排序翻转。故中心平均应变增幅较稳健，均匀性排名仍网格敏感；不作最终厚度选择。
- 更新：[中心厚度报告](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2500中心厚度与细网格敏感性.md)、[TC1500 网格 CSV](Agents/PA12双轴试样仿真/验证/2026-09-27_TC1500细网格敏感性.csv)、TC1500 几何截图、`index.md`、阶段计划、GPT 交接文档/状态及本日志。三档 Abaqus 全量 CAE/INP/ODB/日志/指标位于 `D:\PA12_Stage2\g6_tc1500_mesh_h*_20260927\`。
- 下一步：追查均匀性排名翻转的离散/过渡因素，核验 ROI 厚度区与槽端场；再固定中心厚度比较有效区尺寸或过渡曲率，并接入材料、夹具、DIC 与 VFM 可辨识性约束。

## [2026-09-27] experiment | S19 有限变形 J2 双域窗口稳定性

- 输入：S19_X_0.2 的 126 帧全历程；完整 Job ROI 为主分析域，DIC subset 内缩域为独立敏感性域；原始 JPG/DAT/XLS 未修改。
- 方法：固定 `ν=0.375` 和各域阶段1候选 E，分别以峰前 50/75/100%窗口拟合 `Y0/H`；从六份拟合 JSON 和逐帧 CSV 整理参数、残差及虚功证据。
- 结果：六组参数均随窗口明显变化；完整 Job ROI 覆盖率 `84.8667%`，内缩域使用完整 Job ROI 机器力而非自身边界力。Y 外虚功为零，Y 内虚功 RMS `61.9965–78.2607 N`，全历程内外虚功未闭合；正式参数及训练标签均不放行。内缩域100%精修用时 `8884.300 s`、146 次函数评估。
- 更新：[双域窗口报告](Agents/PA12实验数据处理/VFM自建/有限变形J2诊断/S19_X_0.2/S19有限变形J2双域窗口稳定性.md)、六窗口 CSV/运行检查点、总目标与阶段计划、GPT交接文档/状态、`index.md`。
- 下一步：先核实 S19 实测几何、厚度和 ROI 包含关系，机器—DIC有向坐标、外功边界虚位移及论文 H 符号；不因拟合残差变化盲目扩窗。

## [2026-09-27] refactor | PA12 VFM 当前执行指针同步

- 依据：已完成的 S19 有限变形 J2 双域 50/75/100%六窗口报告、CSV、运行检查点，以及单轴几何证据缺口页。
- 更新：将总阶段计划中 2026-09-26 的 S16 执行段明确标为历史快照；把 GPT 交接文档唯一执行队列改为 S19 当前状态、正式识别物理缺口和有限 J2 合成验证待办。S16 与旧数据段保留，不覆盖。
- 下一步：在不重跑 S19 窗口的前提下，沿有限变形 J2 的非比例路径、应变步长细化和塑性耗散/能量核验继续；材料硬化律扩展需单独明确范围。

## [2026-09-27] experiment | TC2500 中心 ROI 与网格口径敏感性

- 输入：TC1500/TC2000 六份既有 `h=1.2/1.0/0.8 mm` ODB；原始 STEP、CAE 与 ODB 保持只读。固定竖直材料轴 `M-Z -> -FE-Y`、`r=1`、临时正交线弹性工况。
- 方法：对 ROI 半宽 `12/13/14 mm` 分别使用质心筛选与全节点内含筛选，按完整入选单元的积分点 `IVOL` 加权计算 `PrimaryScore`、`K_ratio` 与 `G_transition`；共 36 组。全节点方式不是精确 ROI 体积裁切。
- 结果：36 组唯一组合、缺失指标 0；原 ±14 mm 质心口径在六份 ODB 上与既有 `PrimaryScore`、`G_transition` 最大绝对差均为 0。±12 mm 下 TC2000 分数较低 6/6；±13 与 ±14 mm 均为 3/6，排序会随网格/选取方式翻转。
- 判定：ROI 边界定义与网格离散共同影响排名，现有线弹性筛查不支持最终厚度选择，也不替代应变、DIC/VFM 可辨识性及断裂控制评价。
- 更新：[敏感性报告](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2500中心ROI网格敏感性.md)、CSV、JSON、`index.md`、阶段计划与 GPT 交接文档/状态；完整结果在 `D:\PA12_Stage2\g7final_center_roi_mesh_sensitivity_20260927\`。
- 下一步：依据实物 DIC ROI 与中心平坦区冻结评价域及边界单元权重，再固定 ROI 比较中心有效区/过渡几何；材料和夹具边界闭合后再加塑性、DIC 与 VFM 可辨识性评价。

## [2026-09-27] audit | S16 DIC ROI 物理定位门槛复核

- 来源：阶段 H 双轴 ROI/中心厚度几何门槛、S16 Stage 2 虚功独立性审计；仅读取现有 Wiki 证据，未改写 `raw/` 原始资料。
- 核对：S16 Job ROI `27.209208×27.906880 mm`；TC1500/TC2000/TC2500 归档候选中心平坦区分别为 `28.5075/29.005/29.5025 mm`。若假设同心，较长边方向单侧余量分别 `0.300310/0.549060/0.797810 mm`。
- 判定：尺寸上可容纳仅是条件性包络比较。S16 Job ROI 的 DIC 支持率为 `89.2248%`，且样件—STEP 身份和亚像素图像—几何注册未确认；不能把 S16 定位结果当作当前 TC1500/TC2000 模型的物理 DIC 验证。
- 更新：[中心 ROI 敏感性报告](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2500中心ROI网格敏感性.md)、阶段计划、GPT 交接文档及交接状态 JSON。
- 下一步：确认待设计样件的 STEP/打印身份和实际标定图像标记，建立图像到中心平坦区的坐标变换；按真实支持网格定义 DIC ROI 和积分边界，再进入下一组几何 DOE。

## [2026-09-27] audit | S16 FE 几何锚点版本追溯

- 来源：只读核对 G4 FE–DIC 预检、后续中心场诊断和 G2/G4 厚度匹配锚点原文。
- 发现：G4 早期预检使用 `G0-BASE-TC-2000-RATIO-R1P0`；后续中心场诊断使用 `G0-BASE-TC-1000-LOCAL-SEED-H2P0`；厚度匹配锚点为 `G0-BASE-TC-1000-RATIO-R1P0`。它们是不同版本/用途，不应当作同一 S16 FE 模型。
- 判定：S16 后续诊断可暂以 TC1000 锚点作为工作厚度假设，TC2000 保留为早期分支对照；均未证明实物厚度或当前新设计候选的样件身份。FE ROI `28×28 mm` 与 DIC ROI `27.209×27.907 mm` 的差异及 `89.2248%` 支持率仍未闭合。
- 更新：[中心 ROI 敏感性报告](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2500中心ROI网格敏感性.md)、阶段计划、GPT 交接文档和机器状态 JSON；`raw/` 证据保持只读。
- 下一步：沿 TC1000 S16 锚点复核 ROI 定义与图像—几何配准，保持 257 个有效 DIC/力帧一致；通过后再将验证方法迁移到 TC1500/TC2000 候选。

## [2026-09-27] experiment | 有限变形 J2 非比例路径与耗散/能量核查

- 输入：`tools/pa12_finite_j2.py` 线性各向同性硬化材料点核；解析 Hencky 单轴弹塑性历史及等双轴端点的两种非比例轴序。参数仅用于合成验证：`E=2100 MPa`、`ν=0.35`、`Y0=21 MPa`、`H=180 MPa`。
- 方法：新增 X→Y/Y→X 轴交换对称测试；用参考构形共轭 `P:dF` 梯形积分，比较每个弹性/塑性段 8 与 64 个增量，并核对 `D=Y0 ε̄p + 0.5 H ε̄p²` 解析塑性耗散。
- 结果：有限变形 J2 材料点专项 `24 passed`。等双轴端点的非比例历史响应不同，交换 X/Y 后应力与塑性梯度相符。解析外功为 `0.736071428571 MPa`；8 子步外功误差 `1.99154×10⁻⁵ MPa`，64 子步为 `3.11179×10⁻⁷ MPa`，约缩小 64 倍。累计塑性耗散为 `0.58125 MPa`，与解析积分差低于 `1.46×10⁻¹⁴ MPa`；逐步塑性增量非负。
- 判定：通过的是材料点层级的路径对称、步长收敛和能量一致性；未验证空间非均匀弹塑性全场闭合，也不代表真实 PA12 参数或实验 VFM 已通过。本轮只新增测试，没有改生产材料核。
- 更新：[有限变形 J2 材料点更新核说明](Agents/PA12实验数据处理/VFM自建/汇总/PA12有限变形J2材料点更新核.md)、`index.md`、阶段计划、GPT 交接文档及机器状态。
- 下一步：核对通用曲线拟合中各硬化方程与参数语义，先将 Voce I 接入有限变形 J2 材料点更新，再逐个扩展其他模型；每个模型单独验证状态更新、非比例路径、耗散/能量和独立合成 VFM 回收。

## [2026-09-27] audit | PA12 自建 VFM 内外虚功产物完整性

- 范围：S15–S22 八组可分析实验的 `实验结果/<实验编号>/` 逐帧内外虚功 CSV 与虚功检查 PNG；S23/S24 不纳入完整拉伸 VFM 数量门槛，分别有断裂力缺失/预载释放限制。
- 核对：八份 CSV 行数分别为 `284/257/12/126/126/63/36/223`，合计 1127 帧；每份均有 6 个内/外虚功字段，合计 6762 个非空有限数值。八张 PNG 均为可解码的 `2080×1440` 图像；抽查 S15 图可见 X/Y 方向阶段 1 内部功、外部功及阶段 2 模型内部功轨迹和单位。
- 判定：逐组虚功数据和图件齐备，但图上内外曲线并不自动闭合；阶段 2 曲线/残差仍受力耦合构造限制，不能据此声称独立 VFM 验证通过。未重跑 VFM 或覆盖已有结果。
- 更新：刷新 `index.md` 中自建 VFM 交付状态，并保留各组原 CSV/PNG。
- 下一步：继续完成有限变形材料点模型扩展及独立合成 VFM 回收；实验正式参数仍待物理边界、覆盖和独立验证门槛通过。

## [2026-09-27] experiment | S16 四臂槽阵列图像几何定位

- 输入：外部 S16 参考照片 `000000.jpg`（只读）、既有 DIC ROI 中心/像素尺度候选，以及源 STEP 登记的 `3.75 mm` 槽距假设。
- 方法：新增 `tools/fit_pa12_cross_image_registration.py` 和定向测试；对上/下/左/右臂分别检出七槽并作线性阵列拟合，最大绝对残差门槛 `2 px`。四个阵列均通过，最大残差为 `1.25/1.964/1.857/1.357 px`。
- 结果：相对臂平均槽阵列中心 `(561.143,568.500) px`，比既有 DIC ROI 中心 `(558,570) px` 偏移 `(+3.143,−1.500) px`。若条件性采用 `3.75 mm` 槽距，平均尺度为 `0.088927 mm/px`，比既有 DIC 配置高 `1.969%`。上下臂中心差 `2.000 px`，左右臂节距差 `0.607 px`。
- 判定：仅支持图像局部几何候选；样件—STEP 身份、透视/尺度、厚度、镜像/符号和完整 FE–DIC 变换未验证。不据此重映射场或更新正式 ROI。
- 更新：[四臂图像几何报告](Agents/PA12双轴试样仿真/验证/2026-09-27_S16四臂槽阵列图像几何定位.md)、CSV/JSON/叠加图、G1 阶段计划和 `index.md`；D 盘输出位于 `D:\PA12_Stage2\g1_s16_image_registration_20260927\`。
- 下一步：确认照片对应 STEP/打印批次，再用独立多点标记闭合尺度、旋转、镜像和原点；G1 物理坐标确认前，S16 FE–DIC 维持诊断候选状态。

## [2026-09-27] experiment | 有限变形 J2 Voce I 材料点更新

- 输入：现有 Hencky 弹性、乘法分解 J2 材料点核；Voce I 方程 `Y=Y0+Q(1−exp(−b ε̄p))`，合成参数 `E=2100 MPa`、`ν=0.35`、`Y0=21 MPa`、`Q=120 MPa`、`b=12`。
- 方法：在塑性一致性方程中隐式求解 Voce 塑性乘子，并使标量/批量平面应力更新共用同一屈服曲线。验证当前屈服面、混合状态与历史延续、X→Y/Y→X 轴交换对称及非比例路径依赖；单轴解析 Voce 路径比较 8 与 64 子步的 `P:dF` 外功和解析塑性耗散。
- 结果：`tests/test_pa12_finite_j2.py` 全模块 `28 passed`；Voce 标量/批量面内响应和内变量对齐，`τzz` 均在 `1×10⁻⁷ MPa` 门槛内；耗散、外功误差随细化下降，逐步塑性增量非负。
- 判定：完成的是合成材料点 Voce I 更新，不是 `Y0/Q/b` 虚功拟合、空间非均匀合成 VFM 参数回收或 PA12 实验验证；不产生正式材料参数或训练标签。完整 Job ROI 维持主域，DIC subset 内缩维持独立敏感性域，现有实验产物未重算。
- 更新：[有限变形 J2 材料点更新核](Agents/PA12实验数据处理/VFM自建/汇总/PA12有限变形J2材料点更新核.md)、[总目标与阶段计划](Agents/PA12实验数据处理/处理记录/PA12总目标与阶段计划.md)、GPT 交接文档/状态、`index.md`。
- 下一步：以独立解析响应/边界力驱动 Voce I 有限变形虚功回收，评估 `Y0/Q/b` 灵敏度与秩；通过后再进入逐试验参数拟合及下一硬化律。

## [2026-09-27] experiment | Voce I 独立解析 VFM 参数回收

- 输入：均匀仿射单轴解析路径；固定 `E=2100 MPa`、`ν=0.35`，已知 `Y0=21 MPa`、`Q=120 MPa`、`b=12`。DIC 位移由解析 Hencky 轴向/横向应变生成，边界力由解析 Voce 屈服应力及 `Pxx=τxx/Fxx` 计算，不调用材料点更新器生成载荷。
- 方法：新增 `fit_finite_j2_voce_i`，固定 `E/ν`，通过有限变形逐帧虚功积分反演非负 `Y0/Q/b`；报告拟合残差以及按初值尺度化的数值 Jacobian 秩/条件数。
- 结果：独立合成回收测试达到 `Y0/Q/b` 各自相对误差 `2×10⁻⁴` 内、虚功拟合 RMS `<1×10⁻⁵ N`，灵敏度 Jacobian 数值秩为 3；有限变形 J2 专项 `29 passed`，全仓 `216 passed`。真值参数直接积分与解析力的 RMS 约 `1.78×10⁻⁷ N`、最大差约 `1.25×10⁻⁶ N`，确认应力功共轭/载荷映射一致。
- 判定：证明的是固定 `E/ν`、均匀仿射单轴路径上的算法回收与局部满秩；不证明空间非均匀场、噪声/窗口稳健性、真实 PA12 参数或实验边界闭合。未重算实验数据，不生成正式参数或训练标签。
- 更新：`fit_finite_j2_voce_i`、独立解析合成测试、[材料点/VFM 说明](Agents/PA12实验数据处理/VFM自建/汇总/PA12有限变形J2材料点更新核.md)、总目标与阶段计划、GPT 交接文档/状态及 `index.md`。
- 下一步：先以空间非均匀解析场复核 Voce 回收，并扫描数据噪声/加载窗口下的参数秩、条件性与稳定性，再决定实验拟合准入。

## [2026-09-27] audit | S16 图像—Job—STEP 身份链

- 范围：只读 S16 `Job.m2inp`、照片目录 README、实验清单 S16 行、五档 STEP README/核验 JSON 和现有尺寸叠加图；未改写原始资料。
- 证据：Job 显式记录 `0.087209 mm/px` 与 ROI `(402,410)–(714,730)`；`experiment_manifest.csv` 的 S16 行虽可确认序列标签，但方向、载荷模式、力文件和同步状态为 `UNKNOWN`，没有 STEP/打印批次字段。照片 README 所引仿射 `manifest.csv/refinement.csv` 在数据树中未找到；“30.09 mm”叠加注释无量测方法。五档中心厚度 STEP 仅登记论文参数序列。
- 判定：S16 软件 ROI/尺度配置已核实，物理标尺、图像变换和样件厚度/STEP 身份仍未闭合；不能选定对应厚度模型或重映射 FE 场。
- 更新：[四臂图像几何与身份链报告](Agents/PA12双轴试样仿真/验证/2026-09-27_S16四臂槽阵列图像几何定位.md)、G1 阶段计划与 `index.md`。
- 下一步：不让身份缺口阻断独立 VFM 算法验证，继续 Voce I 空间非均匀合成回收及噪声/窗口稳健性审计。

## [2026-09-27] experiment | Voce I 合成力噪声与窗口敏感性

- 输入：独立解析 Voce I 均匀单轴路径，固定 `E=2100 MPa`、`ν=0.35`、`Y0=21 MPa`、`Q=120 MPa`、`b=12`；完整域合成矩形 `12×9 mm`，内缩域 `8.4×6.3 mm`。
- 方法：两个域分别按自身尺寸计算 `Pxx=τxx/Fxx` 边界力；扫描 50/75/100% 加载窗和 0/0.1/1/5% 峰值力独立高斯噪声，非零噪声各用种子 0–4，共 96 次固定 `E/ν` 的 `Y0/Q/b` 拟合。
- 结果：全部拟合 Jacobian 数值秩为 3，参数未触及零下界。完整域主结果中，5%噪声下 50%窗的 `Y0/Q/b` 最大绝对相对误差为 `50.50%/38.46%/102.76%`；100%窗为 `44.57%/6.44%/26.14%`。无噪声最大缩放条件数从 50%窗 `32.64` 降至全窗 `20.01`。两域逐种子参数结果近似相同（最大差 `Y0=2.324×10⁻⁴ MPa`、`Q=3.619×10⁻³ MPa`、`b=2.394×10⁻⁴`），条件数最大差 `0.2928`。
- 判定：满秩不等于噪声下稳定；`b` 对短窗口和高噪声尤其敏感。内缩域独立使用自己的解析边界力，尺度对照不代表真实 DIC 子域边界载荷已知。数据均为均匀仿射解析合成场，不验证空间非均匀平衡、DIC 噪声或 PA12 实验，不放行正式参数。
- 更新：新增 `tools/audit_pa12_voce_i_synthetic_stability.py`、96 组逐种子 [CSV](Agents/PA12实验数据处理/VFM自建/汇总/PA12有限变形J2VoceI合成噪声窗口敏感性.csv) 和[敏感性报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12有限变形J2VoceI合成噪声窗口敏感性.md)，并更新材料核、总路线、GPT 交接文档/状态、`index.md`。
- 下一步：用独立前向有限元生成空间非均匀平衡 Voce I 场，以完整 Job ROI 做主回收；subset 内缩以切割边界虚功独立做敏感性。实验拟合继续等待既有物理门槛。

## [2026-09-27] experiment | 非均匀等双轴 Voce-I 有限元闭环与敏感性

- 输入：合成参数 `E=2100 MPa`、`ν=0.35`、`Y0=21 MPa`、`Q=120 MPa`、`b=12`；自建 P1 三角形有限元前向解算，矩形分析域 `12×9 mm`、厚度 `1 mm`，24 个非零等双轴位移增量，边界应变沿正交坐标非均匀变化。
- 方法：新增 `tools/pa12_voce_i_nonuniform_fe.py` 和 `tools/audit_pa12_voce_i_nonuniform_fe.py`。完整域主分支从全域支反力取虚功；中心内缩域独立裁单元，并从对应子网格等效节点力取切边界虚功。反演固定 `E/ν`，拟合 `Y0/Q/b`；两个域均独立拟合。
- 闭环结果：完整域 `49` 节点/`72` 三角形，内缩域 `25` 节点/`32` 三角形。无噪声两域均回收 `Y0/Q/b` 真值至 `1e-8%` 量级、Jacobian 秩 `3`；自由节点最大平衡残差 `1.535e-9 N`，两域最大前向内外虚功差分别 `7.615e-10/4.190e-10 N`。完整域终帧等效塑性应变范围 `0.02020–0.06706`。
- 稳定性结果：96 组窗口/噪声扫描中 `77` 组收敛、`19` 组达到 300 次评估上限；77 个收敛组均满秩，但最大参数相对误差约 `1.103e4%`。完整域 50%窗/0.1%噪声最大误差 `115.4%`，全窗/0.1%为 `2.278%`，全窗/5%达到 `830%`；短窗和高噪声稳定性不通过。
- 判定与限制：只证明同一材料点更新核下，独立全局平衡求解、两域边界虚功与 VFM 反演路径的一致性；矩形是完整 Job ROI 分析口径的合成映射，非实际 Job 多边形。前向与反演复用本构核，不构成独立本构交叉验证；没有重算实验数据，不产生 PA12 正式参数或训练标签。
- 更新：[合成闭环报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12有限变形J2VoceI非均匀等双轴合成闭环.md)、[参数 CSV](Agents/PA12实验数据处理/VFM自建/汇总/PA12有限变形J2VoceI非均匀等双轴合成参数回收.csv)、[逐帧虚功 CSV](Agents/PA12实验数据处理/VFM自建/汇总/PA12有限变形J2VoceI非均匀等双轴合成逐帧虚功.csv)、[噪声窗口报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12有限变形J2VoceI非均匀等双轴合成噪声窗口敏感性.md)及 [96 组 CSV](Agents/PA12实验数据处理/VFM自建/汇总/PA12有限变形J2VoceI非均匀等双轴合成噪声窗口敏感性.csv)；同步更新总路线、GPT 交接文档/状态及 `index.md`。
- 验证：`python -m pytest -q tests/test_pa12_finite_j2.py` 为 `36 passed`；`python -m pytest -q` 为 `228 passed`。扫描对 19 组优化器未收敛保留了独立状态行；其他材料更新运行时错误继续抛出。
- 下一步：先降低参数扫描中的重复材料历史积分成本，审查短窗口下 `Y0/Q/b` 灵敏度耦合；保持未收敛种子显式记录。数值稳定性有依据后，再与独立本构求解器交叉验证并推进实验准入。

## [2026-09-27] experiment | Abaqus 合成 Voce 十字试样与 VFM 恢复

- 输入：合成平面应力圆角十字试样，Abaqus Mises-Voce 真值 `E=2100 MPa`、`ν=0.35`、`Y0=21 MPa`、`Q=120 MPa`、`b=12`；完整模型与 ODB 保存在 `D:\PA12_Stage2\h8_voce_nonuniform_cross_20260927_verified\`。
- 方法：51 帧 ODB 导出网格、位移、四端反力虚功和 PEEQ；真值内部虚功与边界外虚功对照后，使用固定 `E/ν` 的有限应变 J2-VFM 恢复 `Y0/Q/b`。
- 结果：最大虚功闭合差 `0.01439 N`（相对 `1.275×10⁻⁵`）；参数最大相对误差 `0.006981%`，拟合 RMS `0.001593 N`，Jacobian 秩 3、条件数 `73.73`。中心 ROI 的 PEEQ 均值/最大值 `0.02758/0.04682`，低于全域最大值 `0.09838`，塑性集中在内凹过渡区。
- 更新：[验证报告](Agents/PA12双轴试样仿真/验证/2026-09-27_Abaqus合成Voce十字试样VFM恢复.md)、截图附件 `raw/assets/PA12_合成Voce十字试样验证/peeq_peak.png`、ODB 导出与参数恢复脚本及其 D 盘数据；更新阶段计划和 `index.md`。
- 限制：仅为无噪声合成材料、固定弹性参数的 2D 流程验证；非 PA12 标定、非实验 FE-DIC 验证，未评价中心减薄/狭缝设计优劣。
- 下一步：真实 STEP 参数化候选与打印方向材料/夹具证据闭合后，开展网格和边界收敛，并把 DIC 支持、VFM 参数条件性纳入多目标筛选。

## [2026-09-27] audit | 非均匀等双轴 Voce-I 短窗参数耦合与计算热点

- 输入：非均匀等双轴有限元合成 Voce-I 场；完整域主分支及 subset 内缩切域，均使用各自独立外虚功。固定 `E=2100 MPa`、`ν=0.35`，合成真值 `Y0/Q/b=21/120/12`。
- 方法：按原扫描初值尺度 `[24,100,8]` 计算无噪声最优点缩放 Jacobian；分别使用 50/75/100% 窗，排除零载帧。另对一个 6×6 网格、5 帧拟合进行只读性能剖析。
- 结果：两域六种组合 Jacobian 均为秩 3。完整域条件数随窗口从 `568.441` 降至 `191.194/104.677`，`cos(Q,b)` 从 `0.999879` 降至 `0.999569/0.999025`；subset 分支对应为 `523.734→185.830→103.764`、`0.999879→0.999587→0.999078`。最弱方向由 `Q` 正向、`b` 负向分量主导，支持短窗下 Q/b 难分离的判断。性能剖析中 SciPy 报告 `nfev=6`，剖析器观察到 24 次残差历史积分与 1 次最终全历程积分，合计 25 次，耗时约 `0.283 s`；主要成本为平面应力厚度割线求解，不是几何重建。
- 判定：短窗主要局部耦合位于 `Q–b`，与 Voce 曲线小塑性应变近似 `Qb ε̄p` 相符；满秩不足以证明稳定识别。完整 Job ROI 口径继续为主，subset 内缩只作独立敏感性。所有结论来自合成矩形，不是实验 DIC 或 PA12 参数。
- 更新：[短窗参数耦合审计](Agents/PA12实验数据处理/VFM自建/汇总/PA12有限变形J2VoceI短窗参数耦合审计.md)、总目标阶段计划、GPT 交接文档/状态与 `index.md`；未改本构代码、实验文件或既有扫描产物。
- 下一步：评估将同一材料点上一帧厚度伸长用作下一帧割线初值；本构方程与停止容差保持不变，分别在完整域主分支和内缩敏感性域验证应力、内变量、虚功、拟合参数及耗时后，再决定是否用于批量扫描。

## [2026-09-27] audit | Abaqus 合成 Voce 十字试样自建 VFM 独立重放

- 输入：归档 Abaqus CPS3 十字试样 ODB 导出文件 `finite_j2_vfm_input.npz`；材料输入卡与运行清单确认合成 Voce I 真值 `E=2100 MPa、ν=0.35、Y0=21 MPa、Q=120 MPa、b=12`，Abaqus 作业状态为成功完成。
- 方法：不运行 Abaqus、不覆盖输出；从 NPZ 读取网格、51 帧位移和边界虚功，调用本地 `integrate_finite_j2_virtual_work` 按真值复核内外虚功，再调用 `fit_finite_j2_voce_i` 固定 E/ν 重跑 50 帧参数识别；对照 ODB 导出 CSV 与 VFM 工作 CSV。
- 结果：1053 节点、1928 个 CPS3 单元、51 帧；外虚功 CSV 与 NPZ 最大差 `4.32×10⁻¹² N`，拟合工作 CSV 与 NPZ 外功一致。真值虚功闭合最大差 `0.014387931 N`，相对最大外功 `1.274763×10⁻⁵`。重拟合恢复 `Y0/Q/b=20.998533991/120.000924039/12.000060380`，与归档参数、残差 RMS `0.001592571/0.001576880 N`、Jacobian 秩/条件数 `3/73.728468` 一致。
- 判定：独立 Abaqus 前向场与自建 VFM 逆向在此无噪声合成基准上可复现；不证明 PA12 参数、实验 FE-DIC 闭合或实际 DIC subset 切边界外功。未运行 MatchID，未重算实验数据，不发布材料参数。
- 更新：[Abaqus 合成 Voce 十字试样 VFM 报告](Agents/PA12双轴试样仿真/验证/2026-09-27_Abaqus合成Voce十字试样VFM恢复.md)、总目标阶段计划、GPT 交接文档/状态与 `index.md`。
- 下一步：继续处理有限变形历史积分的计算成本；完整 Job ROI 保持主分析域，subset 内缩域保持独立敏感性，不将本合成基准替代真实实验物理门槛。

## [2026-09-27] experiment | 非均匀 Voce I 历史积分厚度伸长暖启动

- 输入：`build_nonuniform_voce_i_fe_case(cells_x=6, cells_y=6, load_steps=24)` 生成的 25 帧合成等双轴历史，材料真值 `E/ν/Y0/Q/b=2100/0.35/21/120/12`；完整域 `72` 个三角形，内缩域 `32` 个三角形。
- 方法：冷启动每帧用默认 `0` 与 `1e-4` 割线点；暖启动使用上一帧收敛 `log(F33)` 和 `+1e-4` 邻点。保持本构、残差、归一化阈值 `1e-10`、迭代上限 40 不变；对比逐帧应力、塑性梯度/应变、厚度伸长、虚功、拟合参数和运行时间。
- 结果：完整域材料点评估数 `191→174`（下降 `8.90%`）、中位历史积分时间 `0.03812→0.03646 s`；内缩域 `188→169`（下降 `10.11%`）、`0.02719→0.02605 s`。端到端拟合分别缩短 `6.11%/5.25%`。最大 Kirchhoff 应力差 `5.43×10⁻¹² MPa`，最大塑性状态差约 `4×10⁻¹⁵`，虚功最大差 `2.50×10⁻¹²/2.05×10⁻¹² N`；拟合参数相对差低于 `2.82×10⁻¹³`。
- 判定：暖启动可留在通用历史积分路径，当前证据支持数值等价并有约 `4%` 的小网格积分加速；不外推为真实 PA12 全场加速或材料验证。详见[审计报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12有限变形J2厚度伸长暖启动审计.md)。
- 更新：`tools/pa12_finite_j2.py`、`tests/test_pa12_finite_j2.py`、[材料点核说明](Agents/PA12实验数据处理/VFM自建/汇总/PA12有限变形J2材料点更新核.md)、阶段计划、`index.md`；D 盘保留 `audit_warmstart.py`、汇总 JSON 和逐帧 CSV。
- 验证：有限变形 J2 模块 `38 passed`；完整域/内缩域拟合均秩 3，冷/暖拟合的参数、残差及条件数一致至数值精度。
- 下一步：回到 G1 物理映射门槛，核对 S16 照片、试样编号、STEP 与打印批次身份，并查找独立标尺/多点标记以闭合 FE—DIC 尺度、旋转、镜像与原点；未闭合前保持诊断状态。

## [2026-09-27] audit | Voce I 暖启动拟合计时复核

- 范围：对既有 `6×6`、25 帧非均匀 Voce I 合成场的完整域主分支和 DIC subset 内缩敏感性分支，按冷/热启动交替各重复 5 次拟合；冷启动仅在内存中取消跨帧厚度种子，未写入仿真或实验输出。
- 结果：每次拟合均为 6 次优化函数评估。完整域冷/热中位耗时 `0.96850/0.92103 s`，热启动快 `4.90%`；内缩域 `0.69364/0.64615 s`，快 `6.85%`。参数回收与原审计一致，差异在浮点精度内。
- 判定：五次复核确认两域均有小型合成拟合加速；不外推到真实全场或 PA12 物理结论，完整 Job ROI 仍为主分支，内缩域仍为独立敏感性。
- 更新：[暖启动审计](Agents/PA12实验数据处理/VFM自建/汇总/PA12有限变形J2厚度伸长暖启动审计.md)、`index.md`、GPT 交接文档和机器状态；未重跑会覆盖 D 盘归档的审计脚本。
- 下一步：回到 G1，核实 S16 图像/试样/STEP 身份及 FE—DIC 尺度和坐标变换；缺少物理注册证据前不把合成结果升级为实验参数。

## [2026-09-27] audit | S16 30.09 mm 尺寸标注来源核对

- 范围：只读 S16 原始参考照片、`DAT_photo_dimension_overlay.png`、MatchID `Job.m2inp`、当前实验清单及图像目录仿射记录路径；未改写原始文件。
- 发现：叠加图的蓝色尺寸箭头笔画宽度为 `426 px`；按叠加图宽 `1393 px` 等比例还原到 `1120 px` 源图约 `342.51 px`。使用 Job 的 `0.087209 mm/px` 换算约 `29.87 mm`，与图注 `30.09 mm` 相差约 `0.22 mm`（`0.73%`）。此测量含箭头端点且原始量测定义/脚本未找到；`reports/manifest.csv`、`reports/refinement.csv` 在数据目录缺失，文件名盘点也未找到标尺/校准标记记录。
- 判定：近似数值一致不足以证明图注与 Job 尺度独立；30.09 mm 仍是待溯源候选，不作 FE–DIC 标尺。S16 specimen ID 已存在，但 STEP/打印批次、厚度、旋转/镜像和物理原点未闭合。
- 更新：[S16 四臂槽阵列图像几何定位报告](Agents/PA12双轴试样仿真/验证/2026-09-27_S16四臂槽阵列图像几何定位.md)、阶段计划及 `index.md`。
- 下一步：继续在外部数据清单中寻找 S16 与打印任务/STEP 的关联记录；若没有，保持条件性图像—几何变换，不把 30.09 mm 或槽距假设升级为独立标定。

## [2026-09-27] audit | 双轴 VFM 轴映射证据状态更正

- 范围：复核 `run_pa12_self_vfm.py` 的双轴映射状态生成逻辑及 S15–S18 主结果、敏感性结果 JSON；轴置换计算保持不变。
- 发现：运行器曾将由处理配置推导的 `X↔DIC y、Y↔DIC x` 自动标为 `CALIBRATED_CRUCIFORM`，但 S16 图像—STEP 身份、物理尺度与坐标变换尚无独立确认。
- 更新：运行器改为 `CANDIDATE_UNVERIFIED` 并写明证据边界；更正 S15–S18 八份派生 JSON 的同一元数据。补充[状态复核说明](Agents/PA12双轴试样仿真/验证/2026-09-27_S16四臂槽阵列图像几何定位.md#vfm-轴映射状态标记复核)、阶段计划和 `index.md`。未更改原始实验数据、输入配置、轴序或数值结果。
- 验证：定向测试 `1 passed`；`tests/test_pa12_self_vfm.py` 为 `29 passed`；全仓回归 `232 passed`。JSON 回读确认八份目标文件均为未验证候选且轴序未变，VFM 结果目录与运行器不再含旧“已校准”标签。
- 判定与待验证：这是软件证据状态更正，不代表 G1 通过，也不发布正式材料参数。S16 的试样—STEP/打印批次身份、物理尺度、旋转/镜像、原点及机器—DIC 有向坐标仍待独立证据闭合。

## [2026-09-27] audit | S16 结构化项目清单映射复核


- 范围：只读项目副本的 `experiment_manifest.csv`、`known_information.md` 和厚度模型 README，并与 S16 图像几何审计中已核对的原始目录记录交叉检查。
- 证据：项目副本的 S16 清单行将 `orientation`、`loading_mode`、`force_file`、同步方法等字段记为 `UNKNOWN`，备注明确目录名未解释为物理条件；五档厚度模型 README 标明其来源是论文参数组；已知信息将整体厚度 `3 mm` 作为待实测假设。
- 判定：本次检查的结构化清单和几何说明未提供 S16—STEP/打印批次的逐件映射，也不支持选定某一厚度模型；这表示现存记录不足，不表示映射记录从未存在。G1 保持未闭合。
- 更新：扩充[S16 图像几何与身份链审计](Agents/PA12双轴试样仿真/验证/2026-09-27_S16四臂槽阵列图像几何定位.md)与阶段计划、`index.md`；未修改外部项目文件。
- 下一步：继续查找试样标签/打印任务号与 CAD 文件之间的直接记录；在获取前不把图像槽距、Job 尺度或论文厚度序列当作物理身份依据。

## [2026-09-27] audit | S16 图像—Pos 候选时间映射可识别性

- 范围：复核 S16 处理配置/报告、无 EXIF 原始帧、逐帧 NCC/Pos 派生表和生成图；原始照片及控制器工作簿只读。
- 证据：处理报告明确记录无可靠 EXIF，并按帧号把照片时间映射到所选力文件有效区间；配置文件将 `xy-2-0.1_state_20250529104919_20250529104947.xls` 作为候选关联，依据是目录速度口径及 `Pos` 斜率，而实验清单仍将 `force_file` 标为 `UNKNOWN`。
- 判定：四端在原始图像中的向外运动是直接证据；峰值图像位移与 `Pos` 的 `1.7%–5.1%` 差异仅是候选文件/相对时间映射下的条件一致性，不独立验证试验文件配对、时间同步或坐标标定。
- 更新：改写[S16 候选映射对照页](Agents/PA12双轴试样仿真/验证/2026-09-27_S16夹爪图像位移与Pos时间同步核验.md)，另存带明确限制的[候选映射图](Agents/PA12双轴试样仿真/验证/2026-09-27_S16夹爪影像位移_Pos候选时间映射.png)，调整逐帧 CSV 时间列名和 JSON 来源状态，更新阶段计划与 `index.md`。旧同步标题图保留但不再作为当前入口。
- 下一步：查找独立的相机触发/采集时间戳及试样—控制器文件对应记录；若不可得，保留候选关联并先做已标记的单轴夹爪微动标定。

## [2026-09-27] audit | S16 DAT 完整性与 STEP 资产映射追加核对

- 范围：只读复核外部 `dic_inventory.csv`、`file_inventory.csv`；不改动照片、DAT、STEP 或项目副本。
- 结果：S16 清单缺少 `000258.jpg.dat`；目录登记非图像文件为 Job、VFM 和两个 MTI；六个归档 STEP 资产均无 S16/打印任务关联字段。
- 判定：本轮归档表复核没有找到样件身份连接键，G1 仍未闭合。完整 Job ROI 保持主分析域，DIC subset 内缩域只作独立敏感性分析。
- 下一步：由逐件实验/打印记录建立 S16—STEP 对应，并提供同平面独立标尺或多点几何标记；同步继续诊断线工作。

## [2026-09-27] audit | S16 MatchID 比例字段与图像根目录核对

- 范围：只读 S16 的 `Job.m2inp` 和两份 `.mti`，抽取比例字段、嵌入图像根目录及帧名序列；不改写原始工程或图像。
- 发现：Job 的 `Conversion` 与 `xy_2try_step1.mti` 字段 `<11>` 均为 `0.087209`；`xy_0.2_289.mti` 字段 `<11>` 为 `0.086705`，指向当前不存在的旧图像根目录。两份 MTI 的唯一帧名序列相同，均为 `000000.jpg`–`000257.jpg`，但因旧根目录缺失，无法证明两工程对应相同图像字节。
- 判定：保存配置字段相差约 `0.578%`，不构成独立物理标定证据。复现既有分析继续使用当前 Job 设置，不对 MTI 字段平均；G1 尺度及试样—STEP 身份仍未闭合。
- 更新：[S16 图像几何与身份链审计](Agents/PA12双轴试样仿真/验证/2026-09-27_S16四臂槽阵列图像几何定位.md)、`index.md`。
- 下一步：追溯旧图像根目录的归档来源并取得独立标尺/多点几何标记；在此之前保持 S16 尺度与坐标关系为候选。

## [2026-09-27] report | PA12 有限变形 J2 窗口/域敏感性总览

- 输入：`PA12_GPT交接状态.json` 中已登记的 S16 与 S19 有限变形 J2 窗口/域摘要；不扫描旧运行目录、不重算实验曲线。
- 更新：扩展 `tools/build_pa12_diagnostic_dashboard.py` 与对应测试；刷新逐组诊断总览 JSON/CSV/Markdown，生成独立 `PA12有限变形J2窗口域敏感性.csv`，更新 `index.md`。
- 结果：新增 11 条窗口记录（S16 主域 3、内缩敏感性 2；S19 主域 3、内缩敏感性 3）。完整 Job ROI 明确为主域，DIC subset 内缩域单独作敏感性；S16 未登记的 75% 内缩窗口未补造。S16 主域 DIC 支持率为 89.2248%；S19 主域支持率为 84.8669%，内缩域为 subset 内 100%。S19 虚功未闭合，本构 H 符号/描述冲突和厚度待实测状态保留；正式参数与代理模型训练标签均未放行。
- 验证：总览定向测试通过；全量单元测试 132 项通过；生成产物核对确认 JSON/CSV 11 条、阶段 A 仍为 10 组、S19 虚功状态未被升级。原始 JPG/DAT/XLS/Job 未修改。
- 下一步：继续诊断线与物理证据门槛并行推进；在 S19 实测几何/厚度、轴映射、本构定义及内外虚功闭合复核前，不发布正式材料参数。

## [2026-09-27] report | PA12 八组 VFM 虚功与参数门槛联合诊断

- 输入：S15–S22 现有 Stage A 结果 JSON/逐帧 CSV、Stage C/D/I、有限变形 J2 窗口与 S19–S22 跨轴审计；不重算实验曲线或 VFM。
- 更新：新增[八组联合诊断报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12八组VFM虚功与参数门槛联合诊断.md)，修正 Stage C 中“ S16 与 S18 最佳模型不一致”的表述，更新阶段计划、GPT 交接文档/机器状态及 `index.md`。
- 结果：Stage A 8 组、1127 帧内部一致性审计通过，但 8 组完整 Job ROI 最小面积比均低于 0.95；全历程逐帧残差、样本内模型误差、有限变形跨轴残差及留出分别按口径记录。Stage 2 不是独立 VFM 验证；S19 留出 RMSE 在两条状态记录中为 40.975690 与 145.800336 MPa，保留待核。
- 判定：完整 Job ROI 继续作为主结果，DIC subset 内缩域为独立敏感性；物理 ROI/坐标/边界、独立 ν、虚功闭合和参数稳定性门槛未通过，正式参数及代理模型训练标签不放行。
- 下一步：先追溯 S19 RMSE 冲突的来源关系，再继续实物—Job/DIC 配准及广义外功边界虚位移证据。

## [2026-09-27] audit | S19 75/25 留出 RMSE 样本口径核对

- 范围：只读复核 S19 现有 `内外虚功.csv`、结果 JSON、留出配置与 `audit_pa12_self_vfm_strict_holdout.py`；未修改原始数据或重生成 VFM CSV。
- 结果：严格留出筛选出 31 个峰前塑性点，RMSE 为 `40.975690 MPa`；以相同训练 `E/Y/H` 对完整 32 行时间测试段计算，RMSE 为 `145.800336 MPa`。两值均从当前 CSV 复现，样本口径不同。
- 更新：在联合诊断报告和机器状态中标注两种 RMSE 的评价集；旧 `single_axis_stability_diagnostic` 的 S19 项增加“完整 32 行、未使用 Stage I 点筛选”的口径说明。
- 判定：原记录不是同口径数值冲突。S19 留出仍只作诊断，不证明模型通过；负 `Y`、极大 `H`、全历程覆盖不足及几何/边界门槛仍阻止正式参数发布。
- 下一步：继续实物—Job/DIC 配准、单轴几何与边界虚位移证据，不改完整 Job ROI 主域和内缩敏感性分支。

## [2026-09-27] audit | 八组 VFM 联合诊断待办复核

- 范围：对照联合诊断报告、S19 留出复算日志、总目标阶段计划和机器状态中的下一步。
- 发现：S19 的 `40.975690 MPa` 与 `145.800336 MPa` 已确认对应不同评价集，但联合诊断报告仍把口径核对列为待办。
- 更新：修正联合诊断报告和机器状态的下一步；完整 Job ROI 仍为主域，DIC subset 内缩仍为独立敏感性；未重算实验 VFM。
- 下一步：推进已确认范围内的自建 VFM 本构能力设计；正式实验参数仍受实物几何、边界、独立 ν、虚功闭合与稳定性门槛约束。

## [2026-09-27] experiment | TC2500 平面圆角半径与网格敏感性

- 输入：只读源 STEP `D:\PA12_Stage2\g0_tc1000_source_step_5thickness_ivol_screen_20260926\input\02_a2p0.25mm.step`；中心厚 `2.5 mm`、总厚 `3 mm`、半宽 `14.75125 mm`、过渡宽 `9.6 mm` 的参数化重建几何。
- 方法：改变两个 cutter 平面轮廓共同使用的圆角 `R=0/1/2/4 mm`，`h=1.6 mm` 扫掠半径；`R=0/4 mm` 另比较 `h=1.2/0.8 mm`。共用竖直材料轴候选、`r=1`、`ΔX=ΔY=0.05 mm`、C3D10 与同一数值边界；用 `±10 mm` IVOL 加权共同核心 ROI 对照，并单独计算 `14–16 mm` 过渡带峰值比。
- 结果：8 个作业全部成功；数值警告、负特征值警告和错误数为 0。`R=4` 的畸变提示数配对减少，但同网格 PrimaryScore 分别变差 `4.57%/3.72%/2.55%`；`G_transition` 在细网格反而升高 `3.01%/1.12%`，中心 `LE22` 提升仅 `0.013%–0.020%`。ROI 体积随网格/几何约变化 `1.6%`，保留点数与体积用于解释离散差异。
- 判定：没有半径被放行为最优；当前为临时线弹性筛选，不是材料校准、正式收敛、断裂定位、实验 FE–DIC 或 VFM 可辨识性结果。源 STEP 未改。
- 更新：[圆角半径报告](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2500平面圆角半径与网格敏感性.md)、配套几何/网格/指标图、`index.md` 与阶段计划；D 盘完整输出位于 `D:\PA12_Stage2\g8_tc2500_corner_radius_20260927\`，汇总 CSV/JSON 在其中。
- 下一步：补 `R=1/2 mm` 的细网格配对，并继续闭合物理几何/坐标、材料和夹具证据，再纳入 DIC 支持及 VFM 灵敏度/稳定性指标。

## [2026-09-27] experiment | TC2500 R1/R2 细网格圆角配对扩展

- 输入：既有 `R=0/1/2/4 mm, h=1.6 mm` 及 `R=0/4 mm, h=1.2/0.8 mm` 结果；只读 TC2500 源 STEP；参数化重建几何与临时正交线弹性材料。
- 方法：补算 `R=1/2 mm` 的 `h=1.2/0.8 mm` 四组 C3D10 工况，竖直材料轴、`r=1`、`ΔX=ΔY=0.05 mm` 和原数值边界保持不变；使用 `±10 mm` 共同核心 ROI 与 IVOL 加权后处理。四个新工况逐一通过几何、材料方向、求解状态、警告计数和结果文件验收。
- 结果：12 个作业成功结束，数值问题警告、负特征值警告和错误数均为 0。R1 的 PrimaryScore 相对同网格 R0 在 `h=1.6/1.2/0.8 mm` 为 `+0.095%/+1.269%/+0.197%`，R2 为 `−0.075%/+0.673%/−0.035%`；过渡峰值比优势在 `h=0.8 mm` 反转；中心 `LE22` 改变量均低于 `0.006%`。R1/R2 的 `h=0.8 mm` 网格各有 1 个畸变提示单元。
- 判定：不放行某一平面圆角半径；暂留 R0 作后续几何对照，而非最优设计。结果仅是重建几何的临时线弹性网格敏感性诊断，不等于收敛证明、材料标定、DIC/VFM 识别或断裂验证。
- 更新：[圆角半径报告](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2500平面圆角半径与网格敏感性.md)、[索引](index.md)、阶段计划、扩展汇总生成脚本；新增独立 12 算例 CSV/JSON/PNG 和 R1/R2 Abaqus 几何/网格截图。D 盘工件目录：`D:\PA12_Stage2\g8_tc2500_corner_radius_20260927\`。
- 下一步：以 R0 为对照单独改变中心平坦有效区尺寸或过渡轮廓，同时推进试样—STEP/打印批次身份、实际厚度、DIC 尺度/ROI 与夹具边界核验，再逐步加入塑性材料、DIC 支持和 VFM 可辨识性评价。

## [2026-09-27] audit | G1 方向照片与构建记录范围复核

- 范围：查看 Second Brain 原始方向/旋转照片；只读扫描 `D:\C盘迁移\Desktop\yuan\data` 与 `D:\C盘迁移\Desktop\yuan\PA12_biaxial_project` 中非图像元数据文件名，并读取 `XY-0.1-02` 方向质量 CSV 和 S16 实验清单行。未修改外部数据。
- 证据：照片只显示四臂夹具和红色标注，没有可读 S16 ID、构建平台轴标或独立标尺。搜索命中的 `orientation_report*.csv` 属于 `XY-0.1-02` 图像帧，记录 DIC/纸面轴角度和 PASS 状态，不是打印方向记录。S16 的 orientation/loading_mode/force_file/synchronization_method 仍为 `UNKNOWN`，且清单未连接 STEP/构建任务。
- 判定：不将夹具照片或其它实验组的 DIC 方向质量结果解释成 S16 的材料—机器坐标标定；S16 的 `Q_i/R_i` 及尺度仍未闭合，历史 VFM 结果维持候选状态。
- 更新：[S16 身份链审计](Agents/PA12双轴试样仿真/验证/2026-09-27_S16四臂槽阵列图像几何定位.md)、[G1 坐标矩阵与采集规程](Agents/PA12双轴试样仿真/验证/2026-09-26_G1材料-机器-DIC坐标变换矩阵.md)、[逐样件 CSV 模板](Agents/PA12双轴试样仿真/验证/2026-09-27_G1逐样件标定采集模板.csv)、`index.md` 和阶段计划。
- 下一步：从新试样开始同步记录构建任务、STEP/CAD 轴标和样件 ID；完成机台 X/Y 正向低载位移与同平面独立 DIC 标定后，再核验有向变换及留出残差。未取得这些实物记录前，不填造 S16 标定参数。

## [2026-09-27] artifact | G1 逐样件采集表 D 盘副本

- 新增可填写的空白模板副本：`D:\PA12_Stage2\g1_coordinate_mapping_20260927\G1逐样件标定采集模板.csv`。
- 模板只有字段标题，不含伪造样本数据；字段说明与采集规程以 Second Brain 的 [G1 坐标矩阵](Agents/PA12双轴试样仿真/验证/2026-09-26_G1材料-机器-DIC坐标变换矩阵.md) 为准。

## [2026-09-27] experiment | S20_X_2 有限变形 J2 双域 50% 窗口

- 输入：S20_X_2 的63条对齐 DIC—力记录，峰值拟合终点 `000064.jpg`；原始 JPG/DAT/XLS 未修改。
- 方法：使用本地自建有限变形 J2 VFM。完整 Job ROI 为主域，DIC subset 内缩域单独作敏感性；固定 `ν=0.375` 及各域阶段1条件 E，拟合正线性硬化 `Y0/H`。拟合只用30帧、截至 `000034.jpg`；63行逐帧输出保留至 `000067.jpg`，包括3个峰后审计帧。
- 结果：主域/内缩域 `Y0/H` 分别为 `438.0329/0.1235` 与 `361.8843/0.0075 MPa`；合并全历程残差 RMS 为 `282.1351/317.7257 N`，最大绝对残差为 `570.1250/663.9654 N`。主域 DIC 支持率 `83.5938%`，低于95%门槛；内缩域虽100%受支持，外虚功仍取完整 Job ROI 合力。
- 判定：两域结果均为条件诊断候选，不是正式材料参数或代理模型标签；单轴实测厚度/有效截面、轴映射和广义外功边界运动仍待确认。
- 更新：[S20 双域诊断报告](Agents/PA12实验数据处理/VFM自建/有限变形J2诊断/S20_X_2/S20有限变形J2双域窗口稳定性.md)、`index.md`、GPT交接文档与机器状态。75%/100%窗口扫描已启动，完成窗口以扫描 checkpoint 为准。
- 下一步：审计已完成的扩展窗口及内外虚功曲线，再判断参数窗口稳定性；保持完整 Job ROI 主分析域、subset 内缩域独立敏感性，不发布正式参数。

## [2026-09-27] experiment | TC2500 中心平坦半宽单网格诊断筛查

- 输入：只读源 STEP `D:\PA12_Stage2\g0_tc1000_source_step_5thickness_ivol_screen_20260926\input\02_a2p0.25mm.step`；中心厚 `2.5 mm`、总厚 `3.0 mm`、过渡宽 `9.6 mm` 的平面重建原型。
- 方法：比较中心平坦半宽 `12/14.75125/16 mm`；统一临时正交线弹性材料、竖直打印轴映射 `M-Z→-FE-Y`、`r=1`、`ΔX=ΔY=0.05 mm`、C3D10 全局种子 `1.6 mm`。固定 `±14 mm` 中心 ROI IVOL 加权，另统计固定 `14–16 mm` 带峰值比。
- 结果：三档均成功完成求解，数值问题警告、负特征值警告和错误数均为 0；畸变单元提示为 `0/10/12`。16 mm 档原始 PrimaryScore 最低，但 ROI 积分点数为对照的约 14.4 倍，且峰值比升至 `2.3872`；不能将 CV 差值归因于几何，不作排名。中心 `LE22` 均值约 `0.021%`，仅是小位移线弹性诊断。
- 判定：本轮不选型、不宣称网格收敛、塑性提升、断裂控制或 VFM 识别改善；重建坡面不等于源 STEP 精确 B-rep，S16 实物身份与坐标/ROI 注册仍未闭合。
- 更新：[筛查报告](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2500中心平坦半宽筛查.md)、[结果 CSV](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2500中心半宽筛查数据.csv)、六张 Obsidian 可预览截图、`index.md` 与阶段计划。D 盘完整 Abaqus 工件位于 `D:\PA12_Stage2\g9_tc2500_center_halfwidth_scan_20260927\`。
- 下一步：优先建立可控新试样的打印任务—STEP—样件身份和 DIC 物理 ROI 注册；再调整过渡几何，解决槽根耦合并做网格可比性复核，随后接入已标定弹塑性材料与 VFM recovery 门槛。

## [2026-09-27] experiment | S20_X_2 有限变形 J2 扩展窗口

- 输入：S20_X_2 的现有63条对齐 DIC—力记录，拟合上限 `000064.jpg`；原始 JPG/DAT/XLS 保持只读。
- 方法：固定 `ν=0.375` 和各域阶段1条件 E，完整 Job ROI 为主域，DIC subset 内缩域独立作敏感性；扩展拟合的函数评估上限设为 `max_nfev=400`。
- 状态：当前仅计算完整 Job ROI 主域75%峰前窗口；参数与逐帧结果尚未生成。50%双域结果仍为诊断候选。
- 下一步：完成该窗口后核对参数 JSON、63行逐帧 CSV 和检查点，再逐项计算内缩域75%及两域100%窗口；不发布正式参数或训练标签。

## [2026-09-27] audit | S20_X_2 75%窗口收敛与 Y/H 可辨识性

- 范围：检查 S20_X_2 的75%峰前45帧、464个分层抽样三角形与完整 Job ROI 15,288个三角形；固定阶段1候选 `E`、`ν=0.375` 和工作假设厚度1.0 mm。原始 JPG/DAT/XLS 未修改。
- 结果：完整 ROI 的 Y/H 拟合在 `max_nfev=400` 内未收敛，未生成75%参数结果。粗网格从50%全域解及配置默认值起算，分别收敛至 `Y0/H=262.4323/0.076661` 与 `263.7384/134.9221 MPa`，拟合残差 RMS 为 `296.2619/296.5858 N`；两参数对在完整 ROI 的固定值残差 RMS 为 `258.8291/257.3070 N`。参数差异巨大而残差近似，局部对数灵敏度条件数最高约 `3.57×10^4`。
- 判定：当前数据与固定材料/边界假设下，线性 J2 的 `Y0/H` 联合识别未证明稳定唯一；不把失败迭代或粗网格候选作为材料结果、Abaqus 材料卡或代理模型标签。内缩域75%及两域100%暂缓，不重复进行同设定长时优化。
- 更新：[S20诊断报告](Agents/PA12实验数据处理/VFM自建/有限变形J2诊断/S20_X_2/S20有限变形J2双域窗口稳定性.md)、`index.md`；检查点保留未完成状态。
- 下一步：优先核实实测厚度/有效截面、机器—DIC坐标及边界虚位移；再用独立材料数据或更具信息量的加载路径、合成场回收测试和候选本构对照评估 Y/H 可辨识性，满足门槛后再续算窗口。

## [2026-09-27] experiment | 有限变形 J2 非均匀塑性合成参数回收

- 输入：测试内构造的已知有限变形 J2 材料参数和空间非均匀塑性历史；不读取或修改 S20 原始实验数据。
- 方法：运行 `tests/test_pa12_finite_j2.py::test_nonuniform_plastic_history_recovers_known_yield_and_hardening`，检查从合成 DIC 位移和对应虚功回收 `Y0/H` 的精度。
- 结果：`Y0=18 MPa`、`H=120 MPa` 均在 `1e-5` 相对容差内回收；测试结果 `1 passed in 2.34s`。
- 判定：核心拟合器在受控、模型一致的非均匀塑性历史下可恢复已知参数；这不构成 S20 的实验验证，也不消除其 75% 窗口的多解/病态证据。
- 更新：[S20 Y/H 敏感性 JSON](Agents/PA12实验数据处理/VFM自建/有限变形J2诊断/S20_X_2/S20_X_2_75pct_YH_sensitivity.json)、[S20诊断报告](Agents/PA12实验数据处理/VFM自建/有限变形J2诊断/S20_X_2/S20有限变形J2双域窗口稳定性.md)、`index.md`。
- 下一步：把 Y/H 回收误差、Jacobian 条件数与 DIC 覆盖率加入试样设计评价；优先为多轴应变路径和独立边界力学证据设计下一轮参数化仿真/实验。

## [2026-09-27] refactor | PA12 双轴试样筛选纳入 VFM 参数可辨识性

- 范围：更新双轴中心区均匀性筛选方法页；对照 S20 单轴窗口结果、线性 J2 等双轴合成噪声审计及非均匀等双轴 Voce-I 合成闭环。
- 结论：中心区 CV/局部应变只能用于几何初筛；最终设计评价必须包含已知参数恢复误差、灵敏度秩/条件数、多初值和窗口稳定性、DIC 覆盖、局部失效风险与设备载荷/位移约束。理想双轴合成可恢复参数，不代表实验 PA12 验证；S20 当前单轴窗口不能稳定确定 Y/H。
- 更新：[PA12 双轴中心区均匀性筛选方法](wiki/methods/PA12双轴中心区均匀性筛选.md)、`index.md`。
- 下一步：将 VFM recovery 指标接入参数化 Abaqus 设计矩阵，先用受控已知材料卡/合成观测筛查加载路径和几何，再以校准材料、真实 DIC 覆盖及独立边界证据决定制样候选；未通过回收门槛的算例不进入代理模型训练集。

## [2026-09-27] audit | S16 双轴线性 J2 参数窗口稳定性

- 范围：只读核对 S16_XY_0.2 完整 ROI 的50/75/100%窗口拟合 JSON、100%局部灵敏度和诊断摘要；未重算或修改原始实验数据。
- 结果：Y0 分别为 `95.971/88.622/88.770 MPa`；H 在50%/75%窗口约为零，100%窗口为 `13.3847 MPa`。100%局部 Jacobian 秩2、条件数136.79，但 DIC 面积支持率89.2248%，状态为 `REVIEW_REQUIRED`；E/ν/厚度及广义外功边界仍是条件假设。
- 判定：局部满秩不等于稳定识别或正式参数放行；多轴加载本身不足以证明硬化参数可辨识，需联合考察窗口稳定性、DIC 覆盖、噪声和边界独立性。
- 更新：[PA12双轴筛选方法](wiki/methods/PA12双轴中心区均匀性筛选.md)、`index.md`。
- 下一步：把窗口间参数漂移、多初值差异和 Jacobian 条件数纳入几何—加载路径筛选；暂不使用 S16/S20 条件候选训练代理模型。

## [2026-09-27] experiment | 合成十字加载比与 Voce I-VFM 参数恢复

- 输入：既有 `r=1` Abaqus 平面应力合成 Voce I 十字基准；新增 `r=0.5/2` 两个独立目录。未读取、修改或拷贝原始 PA12 实验数据。
- 方法：固定十字几何、CPS3 网格、各向同性 Voce I 真值、E/ν、X 向端位移及分析步；由真实 ODB 导出 51 帧位移/反力，使用 50 个非零帧进行有限应变 J2-VFM 参数回收，并以真值材料独立复算虚功闭合。
- 结果：各组 1053 节点/1928 单元、Jacobian 秩均为 3；条件数 `r=0.5/1/2` 为 `55.704/73.728/21.418`，最大参数相对误差为 `0.01324%/0.006981%/0.005291%`。真值内外虚功最大相对差为 `1.578×10⁻⁵/1.275×10⁻⁵/1.542×10⁻⁵`。中心 `16×16 mm` PEEQ 均值为 `0.021684/0.027582/0.043153`。
- 判定：本无噪声二维各向同性合成基准中，`r=2` 的局部灵敏度最高且中心塑性利用更大；不表示竖直打印方向、PA12、实际设备载荷限制或最终试样优选。结果不发布正式参数或代理模型标签。
- 更新：[加载比与 VFM 报告](Agents/PA12双轴试样仿真/验证/2026-09-27_Abaqus合成十字试样加载比与VFM参数恢复.md)、两张 PEEQ 附件、加载比 CLI 与测试、阶段计划、GPT 交接文档/状态及 `index.md`。Abaqus CAE/INP/ODB、NPZ、逐帧 CSV、参数 CSV/JSON 和模型/云图截图保存在 `D:\PA12_Stage2\h10_voce_loading_ratio_20260927\`。
- 下一步：依据真实 DIC 位移波动确定噪声幅值，再做窗口/多随机种子恢复稳定性；并行补齐 G1 样件—STEP—打印批次身份和独立尺度/坐标变换证据。

## [2026-09-27] audit | 合成加载比工况材料表范围核验

- 范围：只读检查新增 `r=0.5/2` 的 Abaqus `.dat/.msg` 与 ODB 导出 PEEQ 汇总。
- 结果：两组 `.dat` 无错误/畸变标记，`.msg` 数值问题警告计数均为 0。`r=2` 全场积分点 PEEQ 最大值 `0.198881999`，未超过分析用 Voce 表上限 `0.2`，但距离末端较近；节点平均云图色标极值与表中积分点/单元统计不是同一量。
- 更新：加载比报告、总目标阶段计划、GPT 交接和 `index.md` 明确表格末端限制及截图/统计口径。
- 下一步：在加载比噪声和窗口稳健性排序前，先把合成 Voce 表范围外扩并复核 `r=2`；实物材料结论仍待真实 PA12 证据。

## [2026-09-27] experiment | S20_X_2 完整 Job ROI 75%有限变形 J2 窗口

- 输入：S20_X_2 的63条对齐 DIC—力记录；拟合使用峰前45帧 `000005–000049.jpg`，全历程审计覆盖 `000005–000067.jpg`。原始 JPG/DAT/XLS 未修改。
- 方法：完整 Job ROI 为主域，固定 `E=7540.2112 MPa`、`ν=0.375` 与工作假设厚度 `1.0 mm`；配置 `fit_ftol=1e-6`、`max_nfev=400`，2048目标的分层预拟合实际使用1988个三角形，再做完整 ROI 精修。
- 结果：`Y0/H=467.7074/16.1247 MPa`，拟合窗残差 RMS `230.2839 N`；全历程合并残差 RMS `280.8652 N`，最大绝对残差 `563.0639 N`。全历程 CSV 63行、帧号连续；逐帧独立复算与 JSON 摘要一致。DIC 支持率83.5938%，状态 `REVIEW_REQUIRED`。
- 判定：75%主域相对50%主域的 H 约变化130.6倍；结果仍是条件诊断候选，不是正式材料参数或代理模型标签。完整 ROI 合力的外功边界运动条件、S20实测厚度/有效截面及有向坐标仍未闭合。
- 更新：[S20双域诊断报告](Agents/PA12实验数据处理/VFM自建/有限变形J2诊断/S20_X_2/S20有限变形J2双域窗口稳定性.md)、`index.md`、GPT交接文档与状态；扫描 checkpoint 已记录完整 Job ROI 75%窗口。
- 下一步：依次计算完整 Job ROI 主域100%、DIC subset 内缩敏感性75%和100%，逐窗审查参数与虚功稳定性；不发布正式参数。

## [2026-09-27] experiment | S20_X_2 完整 Job ROI 100%有限变形 J2 窗口

- 输入：同一组63条 S20_X_2 对齐 DIC—力记录；拟合使用峰前60帧 `000005–000064.jpg`，全历程审计覆盖 `000005–000067.jpg`。原始 JPG/DAT/XLS 未修改。
- 方法：完整 Job ROI 主域，固定 `E=7540.2112 MPa`、`ν=0.375` 和工作假设厚度 `1.0 mm`；沿用75%窗口配置 `fit_ftol=1e-6`、`max_nfev=400`、1988三角形分层预拟合，再在完整 ROI 精修。
- 结果：`Y0/H=484.1296/651.0777 MPa`，拟合 RMS `279.0019 N`；全历程合并残差 RMS `280.7887 N`，最大绝对残差 `556.5794 N`。CSV 63行、照片连续；独立复算与窗口 JSON一致。支持率83.5938%，状态 `REVIEW_REQUIRED`。
- 判定：H 从75%到100%窗口变化约40.4倍；结合50%窗口，当前数据和条件假设没有提供稳定 Y/H 参数证据，结果仅为诊断候选，不作为正式材料参数或代理模型标签。
- 数据留存：75%参数 JSON仍在；用同一积分器按已保存参数重建75%全历程 CSV/PNG，未重复优化，残差摘要复现至数值精度。75%/100%逐帧曲线和摘要均按窗口比例独立保存。
- 更新：[S20双域诊断报告](Agents/PA12实验数据处理/VFM自建/有限变形J2诊断/S20_X_2/S20有限变形J2双域窗口稳定性.md)、`index.md`、GPT交接文档与状态。
- 下一步：依次计算 DIC subset 内缩敏感性75%和100%窗口，再联合判断域/窗口稳定性；不发布正式参数。

## [2026-09-27] experiment | 合成 Voce 表范围敏感性复核

- 输入：既有 `r=2` 二维各向同性合成 Voce 十字模型；新增表上限 `ε̄p=0.3` 的 Abaqus 工件。未读取或修改 PA12 原始实验数据。
- 方法：保持 `0.001` 塑性应变间隔，将表格区间数从 200 增至 300；重新求解、ODB 导出，并用同一有限变形 J2-VFM 脚本恢复材料参数。与上限 `0.2` 工件逐项比较网格、坐标、位移及虚功数组。
- 结果：作业正常结束，51 帧、1053 节点、1928 单元；`.msg` 分析警告和错误计数为 0。两 ODB 最大位移差 `0 mm`、导出虚功最大差 `0 N`；VFM 恢复 `Y0/Q/b=20.9988888/119.9961248/12.0005542`，Jacobian 秩 3、条件数 `21.4185`；全场最大 PEEQ `0.198881999`。
- 判定：本模型本载荷路径下，`0.2→0.3` 表外扩不改变前向场和恢复解，表格截断不是本次 `r=2` 数值结果的成因。峰值仍接近 `0.2`，不据此宣称高应变外推、断裂或 PA12 验证。
- 更新：[加载比与 VFM 报告](Agents/PA12双轴试样仿真/验证/2026-09-27_Abaqus合成十字试样加载比与VFM参数恢复.md)、[阶段计划](Agents/PA12实验数据处理/处理记录/PA12总目标与阶段计划.md)、[交接文档](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、交接状态 JSON、`index.md` 与 PEEQ 截图附件。Abaqus/ODB/NPZ/CSV/JSON 保存在 `D:\PA12_Stage2\h11_voce_table_range_sensitivity_20260927\r2p0_pmax0p3\`。
- 下一步：从原始 DIC 重复帧/零载波动估计位移噪声；并行核验 S16 原始序列与归档序列的跨帧图像变换和 DAT 记录对应关系。继续保留 G1 打印任务—STEP 身份、FE—DIC 独立尺度/坐标标定为未闭合项。

## [2026-09-27] audit | S16 原始与选取图像序列同源核验

- 范围：只读读取 S16 原始照片/DAT、选取照片/DAT；外部文件均未更改。逐一比较 259 组同序号 JPG，并用仓库 DAT gzip 元数据检查器抽查帧 `0/129/257/258`。
- 方法：SIFT 最多 4500 特征点，Lowe 比率 `0.72`，每帧以 RANSAC 单应矩阵拟合原始 `768×768` 到选取 `1120×1120` 照片的像素变换。
- 结果：259/259 帧配准成功，内点率最小/中位/最大 `96.22/97.45/98.96%`；每帧变换相对首帧的最大角点差最大 `0.538 px`，最坏重投影误差 P95 为 `0.548 px`。图像同源/帧序映射得到强支持。原始与选取 DAT 尺度分别为 `0.097519/0.087209 mm/px` 且 ROI 不同；抽查原始 DAT 均无 `<53>` 应变记录，帧258仅有 7599 条 `<18>` 位移记录，选取帧258 DAT 缺失。
- 判定：不得用原始 DAT 替换选取 DAT 或合并两 Job 的位移/应变；本结果闭合照片源序列关系，不闭合独立尺度、打印批次/STEP、材料方向或力—图像同步，暂不据此估计 DIC 噪声。
- 更新：[同源核验报告](Agents/PA12双轴试样仿真/验证/2026-09-27_S16原始与选取图像序列同源核验.md)、[逐帧 CSV](Agents/PA12双轴试样仿真/验证/2026-09-27_S16原始与选取图像序列逐帧配准.csv)、[元数据 JSON](Agents/PA12双轴试样仿真/验证/2026-09-27_S16原始与选取图像序列核验.json)、阶段计划、`index.md`、GPT交接文档与交接状态。只读复算输出副本保存在 `D:\PA12_Stage2\g12_s16_image_sequence_match_20260927\`。
- 下一步：审查原始序列候选力/位移工作簿的采样时基与物理关联；在独立同步证据出现前保持 `UNKNOWN/CANDIDATE`，不把该工作簿并入正式 S16 VFM。

## [2026-09-27] audit | S16 候选力/位移工作簿时基

- 范围：按只读方式读取 `XY-0.1-02_配置.json` 与其登记的 `.xls` 文件；不更改工作簿或原始数据。
- 结果：配置把原始照片目录 `33061_1_16` 指向该 Pos/Press 工作簿。Pos 27981 行、时间 `0–28.050 s`；Press 27980 行、时间 `0–28.049 s`；时间单调，步长中位数 `1 ms`，观测 `1/2 ms`。相机配置登记 10 fps，259 帧名义跨度为 `25.8 s`，与工作簿全时长相差 `2.25 s`。
- 判定：图像全序列同源只把该文件纳入 S16 的候选来源链；文件名/配置和时长近似不构成独立试验配对或同步证据。未找到相机绝对时间戳/触发，帧时间原点未知；不得用首帧假定静止或据此估计 DIC 噪声。
- 更新：[S16 图像/DAT 与时基核验](Agents/PA12双轴试样仿真/验证/2026-09-27_S16原始与选取图像序列同源核验.md)、交接状态 JSON、交接文档、阶段计划、`index.md`。
- 下一步：寻找相机触发/绝对时间戳、试样编号—控制器文件直接对应记录，或带 X/Y 通道编号的低载微动试验；同步未核实前不更新 S16 正式数据或 VFM 输入。

## [2026-09-27] audit | S16 JPG 拍摄时间元数据

- 范围：只读检查原始和选取图像目录的全部 `259+259` 张 JPEG 的 EXIF/JPEG 元数据。
- 结果：两序列均为 `0/259` 张含 EXIF 时间字段；原始照片均含相同的一条 JPEG comment，但无日期格式，选取照片没有 comment。仅见 JFIF、密度等格式字段。
- 判定：图像文件不能提供相机绝对时间或触发沿；不以文件系统时间代替拍摄时间。S16—候选 Pos/Press 同步仍标为 `UNKNOWN/CANDIDATE`，不从该证据估计 DIC 噪声。
- 更新：[S16 图像/DAT 与时基核验](Agents/PA12双轴试样仿真/验证/2026-09-27_S16原始与选取图像序列同源核验.md)、核验 JSON、阶段计划、GPT交接文档/状态与 `index.md`。
- 下一步：查找控制器采集记录、相机触发日志或新试样同步标定记录；在同步和物理坐标/尺度证据出现前，不更新正式 S16 VFM。

## [2026-09-27] audit | S16 末帧 DAT 替代项搜索

- 范围：只读递归搜索 `vertical_all_45°` 处理树中的 `000258.jpg.dat` 文件名；不复制或更改命中文件。
- 结果：唯一命中属于 `PAPER/biaxal/S15_XY_0.2/`，未找到 S16 序列的另一份末帧 DAT。
- 判定：S15 不属于 S16 同一试样/Job，不可用于补帧；S16 选取序列缺少 `000258.jpg.dat` 仍是未解决的数据缺口。
- 更新：S16 图像/DAT 同源核验报告、GPT 交接状态 JSON 与本日志。
- 下一步：若将来找到 S16 同一 Job 的原始完整导出，再做尺度/ROI/帧一致性核验；否则保留缺测，不插补、不跨 Job 合并。

## [2026-09-27] audit | S16 XY 原始分卷归档索引

- 范围：只读列出 `XY.zip` 目录项，并筛查已提取 XY 数据树与结构化项目中的可读元数据文件名；未解压、覆盖或修改归档及原始数据。
- 结果：可见 Pos/Press 工作簿和按试样组织的 DIC 派生 CSV；未发现独立命名的相机触发/时间戳、控制器采集日志或打印构建/平台排版记录。现有 XY 照片/DAT/工作簿关系仍只是候选，文件名检查不排除数据藏在工作簿字段或其它未登记来源。
- 判定：S16 同步、试样—STEP/打印批次和材料方向仍为 `UNKNOWN/CANDIDATE`，不跨试样继承映射。
- 更新：[S16 图像序列同源核验](Agents/PA12双轴试样仿真/验证/2026-09-27_S16原始与选取图像序列同源核验.md)、[阶段计划](Agents/PA12实验数据处理/处理记录/PA12总目标与阶段计划.md)及 `index.md`。
- 下一步：历史记录保持候选状态；在下一可控试样上使用逐样件模板同步记录试样 ID、构建方向、STEP、独立标尺、机器 X/Y 有向微动及相机/控制器时间基。

## [2026-09-27] experiment | TC2500 中心半宽共同 ROI 与网格敏感性

- 输入：TC2500 中心半宽 `12/14.75125/16 mm` 的三份既有竖直 `r=1` ODB；没有重新生成网格或提交求解。中心厚度 `2.5 mm`、重建过渡宽度 `9.6 mm`、临时正交线弹性卡、全局 C3D10 种子 `1.6 mm`。
- 方法：后处理器以含单元的试样实例计算；按 `IVOL` 加权复算 ROI 半宽 `12/13/14 mm`，每个 ROI 外侧取 `2 mm` 环带。默认 `±14 mm` 新结果与原基线指标一致；自定义 ROI 结果使用独立后缀。
- 结果：共 9 组 CSV/JSON 均通过 ROI 标签和正体积检查。`PrimaryScore` 最低档在 `±12 mm` 为 W12，在 `±13/14 mm` 为 W16；W16 与 W14.75125 的 `±13 mm` 分差仅 `2.708×10⁻⁶`。W16 的积分点数约为 W14.75125 的 `14.4–14.6` 倍，而同口径 ROI 体积相近；局部离散使当前 CV 差异不能作几何排名。
- 判定：不选择半宽，不宣称网格收敛或几何优化；实际 DIC ROI 未注册，材料仍为线弹性候选，未评估塑性、断裂、DIC 支持率或 VFM recovery。
- 更新：[复算报告](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2500中心半宽ROI网格敏感性.md)、[汇总 CSV](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2500中心半宽ROI敏感性.csv)、[对比图](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2500中心半宽ROI敏感性.png)、来源清单，阶段计划、全流程说明、`index.md`；D 盘汇总目录为 `D:\PA12_Stage2\g13_tc2500_halfwidth_roi_sensitivity_20260927\`。
- 下一步：统一注册后的物理 ROI，控制各几何的局部网格尺度并做多档敏感性；并行保留 G1 逐样件 ID/方向/同步标定为前置证据缺口。

## [2026-09-27] experiment | S20_X_2 内缩域有限变形 J2 75%/100%窗口

- 输入：S20_X_2 的63条对齐 DIC—力记录；DIC subset 内缩域作为独立敏感性积分域，外虚功继续取完整 Job ROI 机器合力。拟合分别使用峰前45帧至 `000049.jpg`、60帧至 `000064.jpg`；原始 JPG/DAT/XLS 未修改。
- 方法：固定 `E=6213.5927 MPa`、`ν=0.375` 和工作假设厚度 `1.0 mm`；使用既有有限变形 J2 runner。75%/100%拟合后，将 CSV、PNG、摘要 JSON按窗口比例另存；对两窗口逐帧残差重新计算拟合 RMS、全历程 RMS和最大绝对值。
- 结果：75% `Y0/H=384.1143/209.6180 MPa`，拟合/全历程 RMS `259.3284/316.7055 N`，最大残差 `657.4512 N`；100% `413.9207/143.3081 MPa`，拟合/全历程 RMS `316.5673/316.4018 N`，最大残差 `652.4631 N`。两者状态均为 `DIAGNOSTIC_ONLY`；四个扩展窗口CSV均63行、照片连续，重新计算结果与对应 JSON 一致。内缩域 X 残差 RMS约 `422.4/420.3 N`，Y 残差 RMS约 `148.9/153.5 N`，Y 外虚功为0，当前虚功未闭合。
- 判定：内缩域结果只代表积分域敏感性，因外功仍由完整 ROI 合力提供，不能称为子域独立闭合或正式材料识别。主域与内缩域均未建立稳定 `Y0/H` 证据；厚度、单轴有效截面/标距、机器—DIC 有向轴和外功边界条件仍待核实，不发布参数或训练标签。
- 更新：[S20双域诊断报告](Agents/PA12实验数据处理/VFM自建/有限变形J2诊断/S20_X_2/S20有限变形J2双域窗口稳定性.md)、`index.md`、GPT交接文档/状态及比例专属曲线、CSV、摘要 JSON。
- 下一步：先核对 S20 单轴机器—DIC 轴向关系及加载/自由边界的单位虚位移条件，再据此决定是否继续材料参数识别。

## [2026-09-27] audit | S20_X_2 非加载 Y 力通道与虚功轴向映射

- 范围：只读核对 S20 同步配置、单轴机器轴映射实现、处理报告及配置登记的 Press 工作簿；原始工作簿、JPG、DAT 和力索引均未修改。
- 方法：确认有限变形 runner 先按 `X→DIC y/v`、`Y→DIC x/u` 重排参考坐标和位移；按现有 `Press` 通道平均、前50点基线和符号 `−1`，在加载起点 `0.105 s` 至掉载 `1.341 s` 重算原始 Y 合力。
- 结果：`.xls` 文件内部为 XLSX 格式。有效区间校正 Y 合力范围 `−0.22…+0.28 N`、RMS `0.223933 N`；X 校正峰值 `1184.15 N`，Y峰值约占其 `0.0236%`。正式 VFM 索引的 Y 力为全零，来源是单轴配置的非加载轴归零规则。实现中的机器轴重排与配置一致，但有向物理映射仍未独立标定。
- 判定：被归零的横向反力过小，不足以解释约 `149–153 N` 的 Y 内虚功残差；当前虚功未闭合更需检查单位虚位移边界条件、物理轴标定及其他模型假设。没有理由据此改力序列或重拟合。
- 更新：S20 双域窗口诊断报告、`index.md`、GPT交接文档/状态。
- 下一步：核对 S20 加载边界的实际虚位移差和自由边界外功条件，并补齐单轴物理坐标/有效截面与实测厚度证据。

## [2026-09-27] audit | S20_X_2 边界单位虚位移与名义几何复核

- 范围：只读核对 S20 Job、Job 标定与 Extensometer 定义、同步配置、有限变形 J2 虚场实现及名义应力—应变计算/审计口径；未改动原始 JPG、DAT、Job 或工作簿。
- 方法：按 X→DIC y/v 将五点 ROI Polygon 投影到机器轴；用 Job 的 0.084034 mm/pixel 标定计算完整 Job ROI 虚场长度和顶/底切面单位虚位移差。检查曲线代码中的宽度、厚度和标距使用位置，并与 S20 Job 包络及标记间距对照。
- 结果：完整 ROI 机器 X/Y 虚场长度约 59.580106/10.168114 mm；顶/底切面 X 向虚位移差范围 0.994358–0.998590，端边中值估计 0.996474，顶边虚场沿边变化 0.4231%。对向轴向合力假设下归一化误差小于约 0.6%，不足以解释当前数百牛残差；精确边界外功仍依赖恒定端面虚位移或力加权证据，并假定机器力可通过准静态平衡传递至 ROI 切面。
- 几何冲突：S20 当前名义曲线配置为宽 30 mm、厚 1 mm、标距 30 mm，且未找到 S20 专属几何来源；同配置标定下 Job ROI 包络约 10.168×59.580 mm，Job Extensometer 像素标记距离约 44.036 mm。两种 Job 尺寸都不能代替实物尺寸，但名义曲线使用的几何定义未闭合；曲线审计 PASS 不覆盖几何。没有把 ROI 宽度或标记距离擅自写成试样宽度/标距，也没有改配置或重算曲线。
- 更新：S20 双域报告、单轴几何证据缺口页、GPT 交接文档/状态与 index.md；完整 Job ROI 仍为主域，DIC subset 内缩仍独立作敏感性。所有参数维持诊断候选，不作为正式参数或训练标签。
- 下一步：取得 S20 样件编号可追溯的图纸、切片或实测宽度/厚度/标距，并核实尺度与机器—DIC 有向轴；随后再审查名义曲线与边界外功，不用 ROI 包络/像素标记替代实物几何。

## [2026-09-27] audit | S20_X_2 样件几何来源检索

- 范围：只读检索原始资料归档中的 `S20_X_2` 文件名及几何文件清单；未读取或修改原始 JPG、DAT、Job、力工作簿及 STEP。
- 结果：S20 精确名称命中为历史 `.mti/.vfm` 文件；清单中有六个通用 STEP 设计件名称，未发现 S20 与某一 STEP、图纸或打印任务的直接对应记录，也未找到样件级宽度、厚度或标距实测值。
- 判定：样件几何仍未闭合。文件名检索不能证明其他未登记来源中不存在实测数据；不将通用 STEP 指派给 S20，不用历史 MatchID VFM 计算，不改配置或重拟合。
- 更新：[GPT/VFM 交接文档](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、[机器状态](Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json)、[索引](index.md)。完整 Job ROI 保持主域，DIC subset 内缩域保持独立敏感性分析。
- 下一步：取得能直接关联 S20 样件编号的图纸/CAD/切片/构建记录或实测宽度、厚度、标距；在此之前几何依赖的正式曲线与材料参数保持未放行。

## [2026-09-27] audit | PA12 自建 VFM 四类终稿图要求

- 来源：用户提供的总目标、材料模型界面、历史应力—应变图及四类识别结果图截图；原图归档于 `raw/assets/PA12_VFM目标原图/`。
- 解析：四类要求为应力—应变模型对比、参数估计迭代收敛、实验应力状态与屈服面/拟合包络、内部/外部驱动响应。当前模型曲线图只是 Stage 2 力耦合样本内诊断；参数图是累计拟合点稳定性而非优化器迭代；应力空间图没有屈服面；虚功图显示内外虚功随实验时间变化，单位 N，不等于 MatchID 未核实的“驱动—算法步长”。
- 判定：四类要求仍作为终稿验收项。自建 VFM 第四类采用可追溯的内外虚功—时间/帧图，不复刻或猜测 MatchID 私有字段。完整 Job ROI 是主结果，DIC subset 内缩有效域单独输出为敏感性分支；不把现有诊断图升级成识别通过。
- 更新：[PA12 总目标与阶段路线图](wiki/PA12单轴到双轴弹塑性VFM总目标与阶段路线图.md#当前图件实现与终稿验收口径)、`index.md` 及四张原始截图归档；原有 VFM 图件和计算数据未改写。
- 下一步：本构定义确认后，逐步接入模型识别和优化器迭代记录，再生成参数轨迹与屈服面图；对每个适用 ROI 分支保留数值源 CSV。

## [2026-09-27] test | 有限变形 J2 材料点拟合与 runner

- 目的：在增加迭代记录功能前，确认现有有限变形 J2 合成拟合与双域 runner 的基线测试状态。
- 结果：`pytest -q tests/test_pa12_finite_j2.py tests/test_pa12_finite_j2_runner.py` 控制台入口在测试收集时无法导入根目录 namespace package `tools`；从仓库根目录运行 `python -m pytest -q tests/test_pa12_finite_j2.py tests/test_pa12_finite_j2_runner.py` 后 `47 passed in 10.71s`。`python` 进程可直接导入 `tools`，因此是测试入口路径差异，不是本构/runner 用例失败；未改包结构或测试代码。
- 边界：该组测试覆盖合成参数回收和 runner 输出契约，不证明真实实验参数可辨识、内外虚功闭合或正式发布条件通过。
- 更新：`index.md` 补录测试范围与标准调用方式；有限变形 J2 源码和实验结果未改动。
- 下一步：等待用户选择迭代图设计；获批后先对现有全网格拟合输出真实 solver iteration history，并保持完整 Job ROI 主结果与 DIC subset 内缩敏感性分支分开。

## [2026-09-27] experiment | TC2500 中心半宽几何拓扑与网格收敛对照

- 输入：只读 TC2500 STEP 重建几何；W12/W14.75125/W16 三种中心半宽基线，以及 W16 全局种子 `3.8 mm` 的独立网格副本。原始 STEP 未修改。
- 方法：直接导出候选件 B-rep 边长/位置；对 W12、W14.75125 以 C3D10、竖直材料轴候选、`r=1` 和临时正交线弹性卡完成 `h=1.2/1.6/2.0 mm` 三档求解；统一后处理 `ROI±12/13/14 mm`，IVOL 加权统计应力/应变 CV、`K_ratio` 与过渡峰值比。
- 结果：W16 方形平坦区切过臂根轮廓 `15.869–15.956 mm`，生成 120 条 `0.175–0.334 mm` 短边，B-rep 变为 `202` 面/`768` 边；W12/W14.75125 为 `146` 面/`600` 边且无亚毫米边。W16 将全局种子由 `1.6` 调至 `3.8 mm` 未改变中心局部网格（中位边长约 `0.74→0.73 mm`）。W12/W14.75125 平均场量稳定，但 PrimaryScore 跨网格/ROI 的跨度最高分别为 `6.07%/34.97%`。
- 判定：W16 的指标受重建几何短边和局部细化混杂，不参与设计排名；两个较小半宽的平均响应较稳定，但均匀性综合分数未证明正式网格收敛。材料、夹具、实物身份/方向与 DIC ROI 尚未闭合，不得据此发布最优设计、塑性或 VFM 结论。
- 更新：[拓扑与网格对照报告](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2500中心半宽几何拓扑与网格收敛对照.md)、18 组指标/拓扑 CSV、两张诊断图与网格截图；更新 `index.md` 和阶段计划。D 盘完整网格收敛作业在 `D:\PA12_Stage2\g15_tc2500_mesh_convergence_w12_w1475125_20260927\`，W16 拓扑探针在 `D:\PA12_Stage2\g14_tc2500_equal_core_mesh_probe_20260927\`。
- 下一步：以 W14.75125 为参照构造不穿越臂根特征的过渡轮廓；并行推进 G1 逐样件 STEP/打印方向/实测 ROI 注册，闭合前所有仿真指标均保持诊断状态。

## [2026-09-27] audit | TC2500 三档网格畸变单元复核

- 范围：只读检查 W12/W14.75125 在 `h=1.2/1.6/2.0 mm` 六个作业的 `.dat/.msg/.sta`，未修改 ODB 或求解输入。
- 结果：六个 `.sta` 均成功结束；`.msg` 数值问题与负特征值消息均为 0。全件畸变计数依次为 W12 `2/141,650`、`0/99,461`、`222/74,512`；W14.75125 `3/159,651`、`10/92,164`、`160/67,836`。粗网格畸变比例约 `0.24–0.30%`；警告未提供本次报告所需的 ROI 归属，未据此断言局部 CV 的变化由畸变单元导致。
- 判定：`h=2.0 mm` 仅作为网格敏感性点，不作为可靠收敛端点。前述报告/CSV已补充质量统计；无材料或边界模型升级。
- 更新：[六作业质量 CSV](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2500网格求解质量.csv)、中心半宽对照报告和收敛图、`index.md` 与阶段计划。D 盘汇总目录：`D:\PA12_Stage2\g15_tc2500_mesh_convergence_w12_w1475125_20260927\`。
- 下一步：如需正式讨论网格收敛，先建立畸变单元与 ROI 的位置对应并提高粗网格质量；现有结果继续作为线弹性筛查，不参与最终设计选型。

## [2026-09-27] query | PA12 厚度输入前提与逐件核验边界

- 来源：用户确认其余所涉实验文件按 `1 mm` 厚度输入、结构完整，并要求逐步实现。
- 结论：将 `1 mm` 作为用户给定计算前提记录；具体文件—样件映射、独立测厚、结构完整性复核和 Job ROI 实物包含关系仍未逐项验证，不把输入前提升级为实测证据。
- 更新：[总体方法与防跑偏协议](Agents/PA12实验数据处理/处理记录/PA12实验总体方法与防跑偏协议.md)、[GPT 交接文档](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、[机器状态](Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json)及 `index.md`。
- 下一步：按样件逐步核对几何身份与 ROI 物理包含关系；完整 Job ROI 保持主域，DIC subset 内缩有效域保持隔离敏感性分支。

## [2026-09-27] refactor | S19 厚度输入前提与执行队列对齐

- 依据：用户确认其余所涉实验文件按 `1 mm` 厚度输入并认为结构完整；机器状态已记录该信息不是独立测厚或逐件 ROI 几何验证。
- 更新：在 GPT 交接文档唯一执行队列中明确区分用户输入前提与实测/结构核验门槛，并同步 `index.md`；不改参数、配置、原始数据或 VFM 计算产物。
- 结论：S19 当前可按用户给定 `1 mm` 继续计算诊断，但有效截面、标距、Job ROI 实物包含关系、机器—DIC 坐标及边界虚位移仍未闭合，不能据此发布正式参数。
- 下一步：保持完整 Job ROI 主分析、DIC subset 内缩独立敏感性；优化器迭代轨迹图按待确认的输出口径实施。

## [2026-09-27] experiment | TC2500 W15.0 中心半宽拓扑与竖直加载比

- 输入：只读 TC2500 源 STEP；中心半宽 `15.0/15.125/15.3125/15.5 mm` 拓扑探针；W15.0 三个 `r=ΔY/ΔX=0.5/1/2` Abaqus ODB。几何厚度/坡面、材料卡、边界和加载设置见专项报告。
- 方法：由同一 STEP 重建线性方形减薄轮廓，导出 B-rep 边数和长度；用相同 `h=1.6 mm`、C3D10 网格、竖直候选材料映射和 `ΔX=0.05 mm` 求解三加载比；中心 `ROI±12 mm` 的应力/应变指标按 IVOL 加权。
- 结果：拓扑由 `146/600` 面/边变为 `202/768` 的区间位于 `15.125–15.3125 mm`；W15.0 最短边 `1.242851 mm`。三档均成功，网格相同；`.msg` 数值/负特征值/错误数均为 0，`.dat` 每档 15 个畸变单元。r=1 的 `PrimaryScore/K_ratio/G_transition` 为 `0.016299/0.032233/1.125881`；其余加载比见指标 CSV。
- 判定：W15.0 只作为拓扑较稳定的可运行候选；本轮为临时线弹性单网格探针，没有真实材料、实体 ROI、夹具、塑性、断裂或 VFM 识别证据，不排序、不发布设计结论。
- 更新：[专项报告](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2500_W15p0中心半宽拓扑与加载比探针.md)、拓扑与加载比 CSV、两张截图、`index.md`、阶段计划和三份 D 盘求解清单。Abaqus 全量工件：`D:\PA12_Stage2\g16_tc2500_center_edge_sweep_20260927\`。
- 下一步：W15.0 做多档网格和畸变位置—ROI 映射；同时闭合 G1 样件、STEP、打印方向、DIC 坐标及物理夹具边界。

## [2026-09-27] experiment | TC2500 W15.0 竖直 r=1 网格敏感性

- 输入：W15.0 重建几何，竖直候选材料映射、临时正交线弹性卡、`r=1`、`ΔX=ΔY=0.05 mm`；全局 C3D10 网格 `h=1.6/1.2/0.8 mm`。STEP 保持只读。
- 方法：每档独立建模并由 Abaqus/Standard 求解；按固定 `ROI±12 mm`、元素质心筛选和 `IVOL` 权重提取最终帧应力/应变 CV、`K_ratio` 与过渡峰值比。
- 结果：单元数 `92,598/161,892/331,291`；平均场量跨档变化小于约 `0.05%`，PrimaryScore 跨度 `4.04%`、`G_transition` 变化 `7.09%`。三个 `.sta` 成功，`.msg` 数值/负特征值/错误数均为 0；`.dat` 畸变单元数 `15/1/5`，ROI 归属尚未映射。
- 判定：没有预设收敛容差，不能宣称空间均匀性综合指标收敛；平均值稳定不等于 CV 与峰值指标稳定。结果仍受临时材料/边界及未注册物理 ROI 限制。
- 更新：专项报告、网格敏感性 CSV、D 盘 h=1.2/0.8 mm CAE/INP/ODB/日志/截图及分析清单；索引、阶段计划已补充。
- 下一步：空间定位畸变单元并映射 ROI，之后按物理注册域继续 FE–DIC 和 VFM 适用性核验。

## [2026-09-27] refactor | 有限变形 J2 优化器迭代轨迹

- 更新：线性有限变形 J2 fitter 记录全网格精修初值及 SciPy 接受迭代；分层预拟合只提供初值。runner 为每个分析域和拟合窗口分别输出优化轨迹 CSV/PNG，并以 JSON 保存终止状态、停止原因、最优性、最终代价及收敛设置。
- 口径：完整 Job ROI 保持主结果域；DIC subset 内缩有效域独立作为敏感性分支。内缩域仍使用完整 Job ROI 机器合力，不代表子域边界闭合。`function_evaluations` 与接受迭代编号分开记录。
- 验证：有限 J2 fitter/runner 定向测试 `48/48` 通过；真实 SciPy 合成回调从 `(20,80)` 收敛到指定 `(30,120)`；测试生成图布局可读。未重跑 S16 或其他实验，未生成实验轨迹，也未改变任何材料参数状态。
- 更新入口：[四类终稿图验收状态](wiki/PA12单轴到双轴弹塑性VFM总目标与阶段路线图.md#当前图件实现与终稿验收口径)、[J2 预拟合与精修审计](Agents/PA12实验数据处理/VFM自建/汇总/PA12有限变形J2分层预拟合与全网精修审计.md)及 `index.md`。
- 下一步：继续补齐四图中的材料模型应力—应变对比与屈服面/应力空间输出；正式图须使用通过参数识别门槛的实验结果，完整 Job ROI 与内缩敏感性分开呈现。

## [2026-09-27] audit | TC2500 W15.0 网格畸变单元位置

- 范围：W15.0 竖直 `r=1`、`h=1.6/1.2/0.8 mm` 三份 ODB 与 `.dat`；原始 STEP 未修改。
- 方法：按 `.dat` 的 `WarnElemDistorted` 标签读取 ODB 中 C3D10 节点坐标，以四角节点质心划分中心 `ROI±12 mm`、过渡带 `12–14 mm` 和外区，并检查十节点 XY 包围盒与中心 ROI 方框的相交。
- 结果：畸变数 `15/1/5`；中心区质心均为 0，包围盒候选均为 0；过渡带为 `3/0/0`，外区为 `12/1/5`。无警告单元直接落入本轮计算中心 ROI；分类仍非精确裁切积分，也不说明过渡峰值比的网格变化原因。
- 更新：新增 Abaqus 定位脚本、21 行逐单元坐标/质量 CSV，并补充专项报告、阶段计划和索引。
- 下一步：针对过渡区 `G_transition` 开展局部网格敏感性，并保持 G1 物理注册、材料和夹具证据门槛。

## [2026-09-27] experiment | 自建 VFM Stage A 完整 Job ROI 网格拓扑复算

- 输入：S15–S22 共 8 组、1127 帧的既有 DIC—力合并表与 Job 元数据；原始 JPG/DAT/XLS、同步表及历史 Stage A 输出未修改。
- 方法：按 Job `Step size × Conversion` 生成实际相邻参考网格三角形；逐帧按坐标交集映射节点，缺失点三角形不补、不跨接；用 ROI 多边形交叠区线性形函数面积权重积分虚功系数。完整 Job ROI 是主域；DIC subset 内缩域保持独立敏感性分支。
- 结果：8 组新 CSV 行数与记录帧数一致，面积比均处于 `[0,1]`，范围 `0.728012–0.922534`，全部低于 `0.95` 门槛。新旧逐帧面积比的最大差在 S22 达 `0.111158`；新结果仍全部为 `SELF_VFM_SENSITIVITY_ONLY`，不发布 E/Y/H。
- 验证：`python -m pytest tests/test_pa12_self_vfm.py -q` 为 `31 passed`；`python -m pytest tests/test_pa12_finite_kinematics.py -q` 为 `16 passed`；缺列、ROI 裁切线性场和 runner 输出回归均通过。
- 更新：[阶段 A 网格拓扑复算报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12自建VFM阶段A完整JobROI网格拓扑复算.md)；新逐组结果位于 `Agents/PA12实验数据处理/VFM自建/实验结果_JobROI网格拓扑复算_20260927/`。旧 Stage A 记录和一致性审计已标注为历史，未覆盖。
- 下一步：将完整 Job ROI 新主结果与既有 DIC subset 内缩敏感性逐组对照；继续处理面积支持、物理 ROI 注册、单轴边界和 E–ν 参数门槛后，再进入正式弹塑性参数识别。

## [2026-09-27] audit | G1 S16 样件级证据登记与下一件执行单

- 范围：根据现有 G1 坐标矩阵、S16 图像序列同源核验、四臂槽阵列定位和夹爪—Pos 对照报告，整理 S16 直接证据、条件候选与未知字段；原始 JPG、DAT、Job、工作簿及 STEP 均只读。
- 结果：S16 仍为 `CANDIDATE_UNVERIFIED`。已知 259 帧图像配对、图像间单应矩阵、Job ROI 和配置 Conversion；选取 DAT 为 258/259，Job 尺度和槽距反推尺度相差约 1.97%。实物编号—STEP/构建平台、力文件/共同时间基、独立物理尺度以及 `Q_i/R_i` 尚未闭合。
- 更新：[S16 逐样件证据登记](Agents/PA12双轴试样仿真/验证/2026-09-27_G1_S16逐样件现有证据登记.csv)、[下一件实体标定执行单](Agents/PA12双轴试样仿真/验证/2026-09-27_G1下一件实体试样坐标标定执行单.md)、G1 坐标矩阵页、阶段计划和 `index.md`。未改历史计算值，未生成或发布新 Abaqus 设计排名。
- 下一步：对一件具唯一编号且可追溯构建记录的实物执行 X/Y 分轴可逆微动、同平面可追溯标尺、共同时间事件和独立 holdout；放行前不把历史候选用于正式 FE–DIC、材料主轴、VFM 参数或代理模型标签。

## [2026-09-27] experiment | Stage A 完整 Job ROI 与 DIC subset 内缩域拓扑修正对照

- 输入：S15–S18 双轴、S20/S22 单轴，共 965 帧已合并 DIC—力记录及对应 Job 几何；原始照片、DAT、力表与完整 Job ROI 输出保持不变。
- 方法：完整 Job ROI 保持主域；对 DIC 点云外接框经几何包含审查后建立独立内缩敏感性域。两域使用 `reference_grid_roi_shape_functions`、同一帧/时间/机器力、`ν=0.375`、中心厚度 `1 mm` 和相同两阶段拟合规则。S19/S21 外接框不完全落入 Job Polygon，未生成内缩域参数。
- 结果：六组双域 CSV 的照片、时间、X/Y 力逐帧一致，输入差异为 0。完整 ROI 最低面积比 `0.728012–0.905004`，均低于 `0.95`；内缩域 S22 为 `0.854568`。候选 E 在内缩域变化 `−2.68% 至 −5.59%`；可计算的 Y/H 分别变化 `+4.00% 至 +73.78%`、`−47.50% 至 +33.69%`。参数对积分域敏感，均不作为最终材料参数。
- 更新：[阶段 A 双口径复算对照](Agents/PA12实验数据处理/VFM自建/汇总/PA12自建VFM阶段A完整JobROI与DICsubset内缩域网格拓扑复算对照.md)、参数变化图和 `index.md`；内缩域逐组输出位于 `Agents/PA12实验数据处理/VFM自建/实验结果_DICsubset内缩域网格拓扑复算_20260927/`。
- 下一步：继续核对物理 ROI、厚度、方向和支持门槛；S19/S21 几何包含关系未闭合前不生成矩形内缩域结果。

## [2026-09-27] audit | Stage A 完整 Job ROI 支持缺口与时变失点拆分

- 范围：S15/S16/S17/S18/S20/S22 六组完整 Job ROI 主域，对照 DIC subset 内缩独立敏感性；原始 JPG/DAT/XLS、Job 和同步输入只读。
- 方法：读取 Job `subset/step/Conversion`；比较 DIC 首帧点云与 Job 外接框边距；从 Stage A 逐帧 CSV 提取首帧和最低覆盖帧，并以合并 DIC 坐标交集统计最低帧参考点缺失。
- 结果：首帧外接框各边内缩约 `6–11 px`，对应 Job subset/step 设置为 S15 `13/1 px`、其余五组 `15/3 px`，与 subset 中心有效点域内缩相符。S16/S17/S18 最低覆盖仍在首帧且无时变失点；S15 从 `0.922534` 降至 `0.896666`（最低帧缺 2310 点），S20 降 `0.174974` 个百分点（缺 7 点），S22 从 `0.843275` 降至 `0.728012`（缺 601 点，其中 542 点位于 DIC-y 三等分的低 y 区）。
- 判定：固定支持缺口与 DIC subset 中心点域内缩相符，但不证明内缩域是物理边界；S15/S22 存在额外时变缺点。完整 Job ROI 保持主域，subset 继续仅作独立敏感性；`0.95` 门槛不变，不插值/外推，不发布正式参数。
- 更新：[GPT/VFM 交接记录](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、机器状态、总体方法协议、边界载荷说明、`index.md`。
- 下一步：逐件配准 Job 多边形、DIC 可测域与中心 1 mm 平坦区；确定不补造缺失场、且外功边界仍对应完整 ROI 的可验证积分/虚场口径。

## [2026-09-27] verification | Stage A S15–S18 DIC 子域独立复算

- 输入：既有拓扑修正后的 DIC 子域结果；S15–S18 共 679 帧。原始 DIC、照片、力表和完整 Job ROI 结果只读。
- 方法：使用现有有效域 runner 和临时配置，将输出改到 D:\PA12_Stage2\vfm_subset_grid_reprocess_20260927\；不改分析参数和积分算法。
- 结果：四组逐帧内外虚功 CSV 的全部字段逐行一致；E/Y/H、拟合质量、面积支撑率等关键 JSON 值一致。S17 的阶段 2 仍未计算。
- 判定：独立复算确认实现可复现，不增加物理边界或正式材料参数证据；现有拓扑修正双域报告仍是汇总基准。
- 更新：双域报告追加复算一致性记录与配对指标 CSV；D 盘保留独立复算产物。
- 下一步：继续按阶段计划推进 G1 实物身份/坐标注册，同时不把子域敏感性结果升级为正式参数。

## [2026-09-27] analysis | L18 与 TC2000 源 STEP 性能基线对照

- 输入：TC2000 源 STEP smoke solve 与 DOE-L18-01 至 DOE-L18-18 已完成结果；不重跑 Abaqus，不改源 STEP、CAE、INP 或 ODB。
- 方法：核对 18/18 个 manifest 的厚度、坐标方向、位移比、位移量、网格、ROI 和材料字段；源 STEP 与 DOE-L18-16 输入卡的材料方向、运动耦合和位移边界一致。
- 结果：源 STEP PrimaryScore 为 0.0252721、模型 LE22 均值为 2.56969×10⁻⁴；18 案中 2 案 PrimaryScore 更低、6 案 LE22 均值更高。DOE-L18-16 的分数变化为 −55.60%，LE22 均值变化为 +6.89%。ROI 采样数 864–4924，源 STEP 为 1104；各 L18 的 B-rep 计数都与源 STEP 不同。
- 判定：这是同工况性能基线，不是几何回归。DOE-L18-16 仅为预筛候选；材料仍为临时正交线弹性，正式排名、实验参数和代理模型标签均不放行。
- 更新：[性能对照报告](Agents/PA12双轴试样仿真/验证/2026-09-27_L18与TC2000源STEP基线性能对照.md)、配对 CSV、index.md 和阶段计划；Vault 与 D 盘均保存机器可读表。
- 下一步：将候选槽几何映射到源 STEP 的参数化副本并统一局部网格/采样，再做可比敏感性；G1 身份/材料/夹具证据仍需实验闭合。

## [2026-09-27] audit | 自建 VFM 逐组内外虚功输出验收

- 范围：完整 Job ROI 主域 S15–S22 八组，以及已建立的六组 DIC subset 内缩域独立敏感性结果；计算产物只读。
- 方法：逐组检查内外虚功 CSV、虚功图和结果 JSON；核对有效帧行数、照片键唯一性、阶段 1 X/Y 内虚功/外虚功/残差六列数值可解析性、图文件非空及 JSON 状态。
- 结果：主域 8 组共 1127 帧，subset 敏感性 6 组共 965 帧；14 组所需产物齐全，CSV 行数匹配，照片键无重复，虚功图非空，全部标为 `SELF_VFM_SENSITIVITY_ONLY`。S19/S21 未生成矩形 subset 结果，因为 DIC 点云外接矩形不完全位于 Job Polygon 内。
- 判定：逐组数据与曲线可直接使用作诊断；完整 Job ROI 支持率仍低于 `0.95`，候选 E/Y/H 不发布为正式材料参数或代理模型标签。完整 ROI 与内缩敏感性保持分开。
- 更新：[逐组 CSV/曲线/JSON 链接表](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、机器状态 JSON、`index.md`。未重算、覆盖或修改任何实验输出。
- 下一步：以完整 Job ROI 为主，继续逐件闭合 DIC 测量域支持、实物 ROI/厚度配准及机器—DIC 方向/边界外功定义，再推进内外虚功残差与参数稳定性审核。

## [2026-09-27] audit | 单轴表观泊松比跨实验筛查

- 范围：S19_X_0.2、S20_X_2、S21_X_20、S22_Y_0.2 的完整 Job ROI 逐帧 CSV；不改动原始 JPG/DAT/XLS 或计算产物。
- 方法：沿用 `configs/pa12_self_vfm.json` 阶段 1 条件（活动力 `>5 N`、`max(|Exx|,|Eyy|)≤0.005`），并要求轴向 `Eyy>0`；按阶段 I 候选轴映射取活动通道。计算 `−Exx` 对 `Eyy` 的过原点和含截距 OLS 斜率。
- 结果：S19 `N=24，0.17422/0.26666`；S20 `N=27，0.41034/0.42869`；S21 `N=17，0.35348/0.34097`；S22 `N=3，0.44265/0.50421`（过原点/OLS）。Job ROI 最低面积比为 `0.826930–0.870952`。
- 判定：组间与回归口径差异、S22 样本数和 DIC 支持不足，不构成独立泊松比测量；当前拓扑修正主 CSV 的最低面积比为 `0.728012–0.848619`。`ν=0.375` 继续作为条件识别工作假设，不发布正式参数。
- 更新：[GPT/VFM 交接文档](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、交接状态 JSON、`index.md`。未重拟合 E/Y/H。
- 下一步：独立测量横向应变，或先闭合逐件坐标/物理 ROI 并确认有效弹性段，再评估 ν；同时继续现有条件 VFM 诊断与残差核查。

## [2026-09-27] analysis | TC2000 源 STEP 几何特征审计

- 范围：只读 `D:\PA12_Stage2\source_geometry_inspection\inputs\tc2000.step`；Abaqus 几何导入清单、源 STEP 基线 manifest 与现有顶视预览。
- 方法：核对 B-rep 计数、平面面高度/范围和顶面边界；按 edge index 配对槽端边、端点及 `pointOn`，由槽端弦长/边长和内凹角弧长/端点推导半径。
- 结果：B-rep 为 1 cell、148 面、424 边、280 顶点；外包络 150.4 mm、臂宽 30 mm、中心平坦区 29.005 mm×29.005 mm（厚 2 mm）；四臂各 7 槽，槽宽 1.25 mm、槽距 3.75 mm、直线段 38.75 mm、含圆弧槽总长 40 mm。槽端半径 0.625 mm、内凹角半径 3 mm 为几何推导值。
- 判定：形成 TC2000 源 STEP 参数化副本的几何基线；未生成新候选模型、未重跑性能求解，也不证明该 STEP 对应特定实物或打印批次。
- 更新：[几何审计报告](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2000源STEP几何特征审计.md)、参数 CSV、顶视图副本、`index.md` 和阶段计划；D 盘完整清单位于 `D:\PA12_Stage2\tc2000_source_geometry_audit_20260927\`。
- 下一步：建立源 STEP 对齐的 TC2000 参数化副本并做几何/B-rep 回归，再进入统一 ROI/网格的竖直加载比对照；G1 实物身份、打印材料方向与夹具边界仍待实验确认。

## [2026-09-27] audit | S19–S21 单轴原始目录几何文件清单

- 范围：只读检索 `D:\C盘迁移\Desktop\yuan\data\XY\picture-20250529\vertical_all_45°\PAPER\unixal` 下 S19_X_0.2、S20_X_2、S21_X_20 目录；原始 JPG/DAT/Job/MTI/VFM 未修改。
- 方法：按 CAD、图纸、表格、文本和 MatchID 工程扩展名枚举目录文件，不从 Job ROI 或双轴 STEP 推断实物尺寸。
- 结果：每组仅见各自 `Job.m2inp`、`.mti`、`.vfm` 设置文件；未见样件专属 STEP/STP、DXF、PDF 尺寸图或表格测量记录。结论限于该目录树，目录外档案未覆盖。
- 判定：S19–S21 实物厚度、有效宽度和标距仍未确认，单轴正式参数识别几何门槛未解除。
- 更新：[GPT/VFM 交接文档](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、机器状态、`index.md`。原始资料只读。
- 下一步：取得与样品编号关联的图纸、CAD、打印记录或实测尺寸；在此之前不把 Job 包络或双轴试样几何当作单轴实测值。

## [2026-09-27] audit | 自建有限变形 J2 Voce-I 实验 runner 接入状态

- 范围：只读核对有限变形 J2 核心拟合接口、PA12 实验 runner 与 S19 配置；不修改代码、实验配置或既有拟合结果。
- 结果：核心已有通用 Voce-I `Y0/Q/b` 拟合器及合成场回收；实验 runner 目前只连接线性 `Y0/H`，S19 配置没有 Voce-I 的 `Q/b` 初值，尚无真实 PA12 Voce-I 拟合。runner 将结果写到配置指定目录，多模型接入前须隔离输出目录。
- 判定：Voce-I 的合成闭环不等于真实实验 runner 已支持；单轴实物几何、DIC 覆盖与外功边界门槛仍未解除，实验候选不作为正式材料参数。
- 更新：[GPT/VFM 交接文档](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、机器状态和 `index.md`。
- 下一步：在确认模型接入方案后，为 Voce-I 增加独立实验输出路径与优化轨迹；保持完整 Job ROI 主分析域、subset 内缩域独立敏感性，并先用合成稳定性门槛验收后再运行实验候选。

## [2026-09-27] audit | TC2000 源 STEP 原生曲面与微壁复核

- 范围：只读 `D:\PA12_Stage2\source_geometry_inspection\inputs\tc2000.step`、Abaqus 全面/边清单。
- 结果：STEP 原生 `CYLINDRICAL_SURFACE` 共 68 个，半径分组为中心过渡 `8×0.4975 mm`、槽端 `56×0.625 mm`、十字根部 `4×3 mm`；Abaqus 面清单另有 8 个 `0.0025 mm` 高、各 `0.075 mm²` 的中心过渡微壁。圆柱轴向及位置与对应过渡/槽端/根部几何一致。
- 判定：中心过渡曲率已从边长推导提升为 STEP 原生 B-rep 证据；原参数页中半径证据状态已更正。微壁小于现有全局网格尺度，源对齐副本需保留后单独评估网格影响。
- 更新：[几何审计报告](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2000源STEP几何特征审计.md)、参数 CSV、[曲面特征 CSV](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2000源STEP曲面特征审计.csv)、`index.md` 和阶段计划；D 盘完整清单仍位于 `D:\PA12_Stage2\tc2000_source_geometry_audit_20260927\`。
- 下一步：参数化几何回归不得忽略 `0.0025 mm` 微壁；先完成源 STEP 对齐基准，再做竖直加载比和网格/ROI 可比计算。

## [2026-09-27] audit | S19–S21 力学工作簿几何元数据

- 范围：只读核对 `configs/pa12_rotated_batch.json` 关联的 S19–S21 三份原始力学工作簿；未修改原始 JPG/DAT/工作簿、VFM 检查器或配置。
- 方法：依据批处理配置建立实验—文件映射，读取各工作表字段、行数、选定文档属性和命名区域。
- 结果：三份 `.xls` 文件实际为 OOXML/XLSX 容器，均含 `Pos`、`Speed`、`Press` 表；S19/S20/S21 各表含表头总行数为 `14737/14736/14736`、`2790/2790/2790`、`404/403/403`。字段为时间与夹头位置、速度、力；未找到厚度、有效宽度、标距、截面尺寸或样件图号，选定文档属性为空且无命名区域。
- 判定：这些工作簿不能独立确认 S19–S21 实物几何；该结果仅覆盖配置映射的三份力学文件，正式参数识别的几何门槛保持未通过。
- 更新：[GPT/VFM 交接文档](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、机器状态、`index.md`。原始数据只读。
- 下一步：继续使用完整 Job ROI 作为主域、DIC subset 内缩域作为独立敏感性分析；单轴正式参数识别前，补齐与样件编号绑定的厚度、有效截面和标距证据。

## [2026-09-27] experiment | TC2000 源 STEP 锁定 B-rep 基准 CAE

- 输入：只读 `D:\PA12_Stage2\source_geometry_inspection\inputs\tc2000.step`；旧 smoke-solve STEP 副本与该文件逐字节相同。
- 方法：Abaqus 直接导入，不重画或修改 B-rep；建立中心平坦面、外表面、加载端面命名集合和竖直打印坐标框架，导出几何回归、面清单与视图。
- 结果：`1/148/424/280` 个 Cell/Face/Edge/Vertex；包络 `150.4×150.4×3.0 mm`；上下中心平坦面各一面、面积各 `841.290025 mm²`；全部回归项通过。原生曲面审计确认中心圆柱过渡和 8 个微壁保留。
- 判定：形成源 STEP 锁定几何基准；CAE 未赋材料、划网格、施加载荷或求解。旧 smoke-solve manifest 的平面过渡文字与 STEP 圆柱 B-rep 不一致，记录为元数据冲突，不改写历史结果。
- 更新：[锁定基准报告](Agents/PA12双轴试样仿真/验证/2026-09-27_TC2000源STEP锁定基准CAE.md)、回归 CSV、面清单、manifest、顶视/等轴测图、阶段计划和 `index.md`；D 盘完整 CAE 工件在 `D:\PA12_Stage2\g0_tc2000_source_brep_locked_baseline_20260927\`。
- 下一步：在锁定 B-rep 上实现首个中心几何参数化副本并回归曲面/微壁，再统一 ROI/局部网格比较竖直 `r=0.5/1/2`；实物身份、打印方向、材料和夹具边界未闭合前不做正式设计排序或代理模型训练。

## [2026-09-28] audit | S19–S21 几何来源扩展核查

- 范围：只读检查 `vertical_all_45°/moxing` 下三份 PDF；MinerU 使用本地 `standard` 解析，未上传、导出或修改原文件。
- 结果：`简易版.pdf` 为双轴十字试样简版尺寸页；`moxing.pdf` 为 REV B 双轴十字几何重建，明确区分照片/DAT 尺寸、论文参数和推定厚度/夹持尺寸；厚度总览 PDF 描述双轴模型 `3.0/2.5/2.0/1.5/1.0 mm` 中心厚度序列。三份全文均未出现 S19/S20/S21 单轴样件映射。MinerU 定位为 `doc:953d05c/tier:standard/page:1`、`doc:7535ee9/tier:standard/page:1`、`doc:7535ee9/tier:standard/page:4`、`doc:863dcf3/tier:standard/page:1`。
- 判定：这批文件可支持双轴十字几何/厚度模型追溯，不能作为 S19–S21 单轴实际厚度、有效截面或标距依据；正式单轴参数几何门槛保持未通过。
- 更新：GPT/VFM 交接文档、机器状态、`index.md` 和本日志；历史 MatchID 资料、自建 VFM 全 ROI 主口径及 DIC subset 内缩敏感性设置不变。
- 下一步：继续使用完整 Job ROI 主结果与 DIC subset 内缩独立敏感性；若要放行 S19–S21 正式参数，需取得样件编号关联的单轴图纸、打印/试样记录或实测尺寸。

## [2026-09-28] decision | 自建 VFM 双域分析口径

- 决定：完整 Job ROI 保持主分析域；DIC subset 内缩有效域只作为独立敏感性分支。
- 判定：主域仅积分实测 DIC 网格支持区域，不插值/外推；支持率低于 `0.95` 时仍为 `REVIEW_REQUIRED`。内缩分支使用完整 Job ROI 机器合力，不代表子域边界闭合；两域结果不混合。
- 更新：[阶段 C 等双轴虚功与稳定性门槛](Agents/PA12实验数据处理/VFM自建/汇总/PA12自建VFM阶段C等双轴虚功与稳定性门槛.md)。该报告已在 `index.md` 收录。
- 下一步：继续按该双域口径推进自建有限变形虚功与参数诊断；正式参数仍需满足几何、方向、面积支持、稳定性和独立验证门槛。

## [2026-09-28] audit | 阶段 C 人工复核清单口径更新

- 范围：更新现行 Stage C 人工复核清单与索引说明；历史审计及计算结果不变。
- 结果：清单不再把 Job ROI 与 DIC 内缩域列为待二选一；明确完整 Job ROI 为主分析域、内缩域为独立敏感性，并保留物理配准、`0.95` 支持率和外功定义为未通过门槛。
- 更新：[阶段 C 人工复核清单](Agents/PA12实验数据处理/VFM自建/汇总/PA12自建VFM阶段C人工复核清单.md)及 `index.md`。
- 下一步：按已确认的双域输出口径继续自建 VFM 诊断，不以口径选择替代物理闭合或参数放行。

## [2026-09-28] verify | 有限变形 J2 与 Voce-I 合成闭环

- 范围：运行有限变形 J2 材料点、窗口 runner 和 Voce-I 非均匀合成基准三个测试模块。
- 结果：`python -m pytest tests/test_pa12_finite_j2.py tests/test_pa12_finite_j2_runner.py tests/test_pa12_voce_nonuniform_benchmark.py -q`，`64 passed`。
- 判定：当前材料点更新、线性 J2 窗口 runner 和既有 Voce-I 合成基准的测试通过；这不等于实验参数验证，也未证明实验 Voce-I runner 已接入。
- 更新：本日志；合成闭环与噪声/窗口敏感性报告已由 `index.md` 收录。
- 下一步：Voce-I 实验 runner 接入后，先用既有非均匀合成及噪声/窗口基准验收，再生成隔离的实验诊断分支。

## [2026-09-28] experiment | S19 Voce-I 主域首个 100% 窗口

- 输入：只读 S19_X_0.2 已同步 DIC—力索引、全场导出和 Job ROI；使用新建 [Voce-I 配置](configs/pa12_finite_j2_s19_voce_i.json)，原始照片/DAT/力学文件未修改。
- 方法：固定诊断候选 `E=2577.8864 MPa`、`ν=0.375`、工作假设厚度 `1 mm`；对完整 Job ROI 的实测 DIC 交叠网格做 100% 峰前 Voce-I `Y0/Q/b` 拟合；内缩域作为独立敏感性分支串行运行。
- 结果：主域 `Y0=395.5698 MPa`、`Q=14.2983 MPa`、`b=0.239940/应变`；拟合窗/全历程 RMS 为 `285.7882/285.4081 N`，最大绝对残差 `637.8412 N`。优化器 `ftol` 终止，18 次函数评估、10 次接受迭代；RMS 仅从 `285.9235` 降至 `285.7882 N`。DIC 面积支持率 `84.8667%`，状态 `REVIEW_REQUIRED`。同域同窗 Linear RMS 为 `285.7894 N`，未显示 Voce-I 拟合误差优势。
- 判定：本构模型的数值终止不等于参数充分/可辨识；内外虚功未闭合、支持率未过 `0.95`，参数不正式发布、不作训练标签。本次运行未保存局部 Jacobian 秩/条件数，记为未知。
- 更新：[S19 Voce-I 双域诊断记录](Agents/PA12实验数据处理/VFM自建/有限变形J2VoceI诊断/S19_X_0.2/S19有限变形J2VoceI双域100pct诊断.md)、完整 Job ROI 的诊断摘要、`index.md`；Voce-I 实验 runner 现在记录缩放 Jacobian 秩、参数数目和条件数，秩亏条件数使用 JSON `null`。
- 下一步：等待 DIC subset 内缩敏感性分支完成；单列报告其覆盖率、参数、残差、虚功与优化状态，不与主域混合。之后评估窗口稳定性及几何/边界物理门槛。

## [2026-09-28] experiment | PA12 五档源 STEP 竖直坐标几何族

- 输入：只读 `D:\PA12_Stage2\source_geometry_inspection\inputs\tc1000.step` 至 `tc3000.step` 五个源 B-rep；未修改源 STEP。
- 方法：Abaqus 直接导入五个独立模型，建立竖直 Datum 坐标定义；回归实体拓扑、外包络、中心上下平坦面和过渡微壁，并保存顶视/等轴测图。
- 结果：五个模型均为 1 个实体、包络均为 `150.4×150.4×3.0 mm`；TC1000–TC2500 为 `148/424/280` 个 Face/Edge/Vertex，TC3000 为 `130/384/256`。77 项检查全部通过；中心平坦面和微壁实测值见[验证报告](Agents/PA12双轴试样仿真/验证/2026-09-28_PA12源厚度STEP族竖直坐标几何库.md)及回归 CSV/manifest。
- 判定：形成五档源 STEP 几何库和截图。CAE 未赋材料、未划网格、无载荷且未求解；Datum 坐标不证明实体打印方向、机台/DIC 方向已物理标定，不产生几何排名。
- 更新：[验证报告](Agents/PA12双轴试样仿真/验证/2026-09-28_PA12源厚度STEP族竖直坐标几何库.md)、`index.md`、阶段计划；Abaqus 文件在 `D:\PA12_Stage2\g18_source_thickness_family_vertical_20260928\`。
- 下一步：在独立副本上做有几何依据的单变量改型并回归 B-rep/微壁，再统一 ROI、局部网格和竖直 `r=0.5/1/2` 评价；材料、打印方向、夹具与 DIC/VFM 物理证据门槛仍未解除。

## [2026-09-28] experiment | S16 载荷匹配 FE-DIC 位移候选诊断

- 输入：只读 S16 `000256_DIC全场—力.csv` 峰值帧；以已有直接草图粗网格输入为父模型，在 `D:\PA12_Stage2\g4_s16_peak_field_candidate_20260928\` 建立独立副本，仅增加全模型节点 `U` 场输出。
- 方法：Abaqus 2025 完成 `Load` 步 21 帧；提取上表面 `z=+0.5 mm`、中心 `±14 mm` 内 841 个节点。依据两轴峰值力和 FE 参考点历史，选 `t=0.40`（FE-X `1609.839 N` 对机器 Y `1613.26 N`；FE-Y `1623.4872 N` 对机器 X `1632.32 N`），按候选坐标映射做不外推凸包插值。
- 结果：覆盖 `9700/10098` 点（`96.06%`）；载荷匹配帧 U1/U2 原始偏置 `0.9930/1.1071 mm`、原始 RMSE `1.1809/1.2584 mm`、相关 `0.9308/0.9467`。终点帧原始 RMSE 为 `2.5549/2.6465 mm`。同一数据的去偏 RMSE 仅作诊断，不能视为物理配准。
- 判定：已有真实 STEP 表面单元插值覆盖为 100%，本次线性凸包的 96.06% 不构成覆盖改进。候选几何、材料、坐标原点/方向和实际夹具边界均未正式校准；不发布 FE-DIC 验证、材料参数、几何排名或代理模型标签。
- 更新：[诊断报告](Agents/PA12双轴试样仿真/验证/2026-09-28_S16_FE-DIC载荷匹配位移候选诊断.md)、图、`index.md`、阶段计划；全量 Abaqus 与对照 CSV/JSON/PNG 保存在上述 D 盘目录，提取和比较脚本支持指定实例/帧并动态标注覆盖率。
- 下一步：优先按 G1 执行单绑定样件坐标与实体身份标定，并取得实际夹持端位移；随后用源 STEP、实测材料和物理校准边界重做 FE-DIC/VFM 对照，再推进参数化设计和可辨识性评价。

## [2026-09-28] refine | S16 C3D10 实际表面 FE-DIC 插值与数值风险

- 输入：同一载荷匹配 ODB/第 0.40 帧；从 INP 装配实例读取 Z 平移 `-1.5 mm`，统一局部节点坐标与 ODB 全局坐标后，按 C3D10 外表面连通关系进行二次三角插值。
- 结果：筛得 `450` 个外表面面片和 `961` 个表面节点，`10,098/10,098` 个 DIC 点均位于实际面片内，无外推。载荷匹配帧 U1/U2 原始 RMSE 为 `1.1879/1.2638 mm`，偏置 `0.9934/1.1067 mm`；与节点凸包插值的共同区域统计接近。
- 数值审计：`884/110,952` 个畸变单元（约 `0.797%`），其中中心 ROI 质心代理 `16` 个、过渡带 `785` 个、外臂/外区 `83` 个；另有 `CRUCIFORMCUT-1.5` DOF 2/3 两条外角数值奇异警告。求解完成、0 个错误和负特征值警告不等同质量通过。
- 判定：实际表面插值闭合了本候选 FE 网格上的空间覆盖，但样件身份和物理坐标变换、实测材料、加载边界及中心畸变风险未闭合；不作为正式 FE-DIC 验证或材料/代理模型标签。旧真实 STEP 的 100% 表面覆盖仍为独立报告，不与本候选混合。
- 更新：[载荷匹配诊断报告](Agents/PA12双轴试样仿真/验证/2026-09-28_S16_FE-DIC载荷匹配位移候选诊断.md)、100% 覆盖图、运行清单、实际表面插值及畸变位置审计脚本、`index.md` 和阶段计划；C3D10 插值/审计 CSV 与 JSON 均在 `D:\PA12_Stage2\g4_s16_peak_field_candidate_20260928\`。
- 下一步：按 G1 执行实物坐标/身份标定并取得夹持端位移；基于真实 STEP 和校准材料/边界再做表面场与网格敏感性检查。

## [2026-09-28] refine | S16 同口径实际表面终点帧对照

- 范围：从同一 21 帧 ODB 提取 `frame_index=20`、`t=1.00` 的中心上表面 U；沿用 450 个 C3D10 实际外表面面片、961 个节点、Z 平移 `-1.5 mm` 和同一候选 DIC 坐标映射。
- 结果：终点帧覆盖 `10098/10098` 点；原始偏置 U1/U2 为 `2.5145/2.6129 mm`，原始 RMSE `2.5569/2.6471 mm`，去偏 RMSE `0.4636/0.4236 mm`。与载荷匹配帧比较时，使用相同实际表面插值口径；终点帧原始误差较高而去偏误差较低。
- 判定：FE 位移量级受载荷阶段影响，但偏置、坐标注册、材料与边界不确定性仍未闭合；只作候选诊断，不做 FE-DIC 正式验收。
- 更新：诊断报告和阶段计划补充同口径终点帧结果；终点帧 CSV/JSON/PNG 在 `D:\PA12_Stage2\g4_s16_peak_field_candidate_20260928\`。

## [2026-09-28] experiment | S16 面外约束敏感性探针

- 来源：S16 候选输入卡/ODB `D:\PA12_Stage2\g4_s16_peak_field_candidate_20260928\`；DIC 峰值帧 `Agents/PA12实验数据处理/MatchID_VFM准备/S16_XY_0.2/merged/000256_DIC全场—力.csv`。
- 方法：从原始 INP 副本仅增加 YMIN 与 XMAX 参考点 `U3=0`，生成独立 Abaqus 2025 作业；固定 `frame_index=8`，沿用原载荷匹配、坐标映射和 C3D10 实际表面插值。
- 结果：21 帧正常完成；`.msg` 数值奇异警告由 2 条降为 0，负特征值/分析错误为 0；`.dat` 仍报告 884/110,952 个畸变四面体。载荷匹配反力为 `1609.839/1623.487 N`；DIC 覆盖 `10098/10098`；RMSE 变化小于 `6×10⁻⁹ mm`，表面节点 U1/U2 最大差 `1.19×10⁻⁷ mm`。
- 更新：[探针报告](Agents/PA12双轴试样仿真/验证/2026-09-28_S16_FE-DIC面外约束敏感性探针.md)、图、`index.md`、阶段计划；输入、ODB、求解日志、CSV/JSON/PNG 均保存在 `D:\PA12_Stage2\g4_s16_out_of_plane_probe_20260928\`。
- 结论/待验证：面外约束可移除候选模型数值奇异且对面内峰值响应影响极小；真实夹具是否对应此约束未知，畸变单元问题仍在。需取得夹具/试样面外运动证据，再确定正式边界；物理注册、材料校准和源 STEP 复算仍未完成。

## [2026-09-28] experiment | TC3000 竖直位移比矩阵补全

- 输入：只读 TC3000 `3.0 mm` 源 STEP；复用既有竖直 `r=1` H6 基准，新增 `r=0.5/2` 两个工况。
- 方法：同一临时正交线弹性卡、`vertical_z_in_plane` 候选、H6/C3D10 网格和中心 `±14 mm` IVOL 统计；三份 INP 核对均为 `84,784` 节点、`54,612` 单元，ROI 各 `138,588` 个积分点。
- 结果：`r=1` 的 PrimaryScore/K 最低（`0.059993/0.034930`）；`r=0.5/2` 分别为 `0.161496/0.627267` 与 `0.099121/0.543874`。三档 `G_transition=2.4128–2.5599`；三份作业均正常结束，但各有 2 条数值奇异警告，负特征值和错误消息为 0。
- 判定：只补齐 TC3000 的诊断加载比行；网格仅 H6，材料和边界为临时假设，不证明应变均匀目标、断裂控制或 VFM 可辨识性，不形成正式选型。
- 更新：[验证报告](Agents/PA12双轴试样仿真/验证/2026-09-28_TC3000竖直位移比补全.md)、CSV/截图、`index.md`；完整 Abaqus 工件在 `D:\PA12_Stage2\g0_tc3000_vertical_ratio_20260928\`。
- 关联核对：只读盘点 `XY\data-20250529\20250529` 下 12 个工作簿；表头仅对应 X1/X2/Y1/Y2 的 Pos/Speed/Press 通道，未形成 Z 向应力—应变或 S16/TC3000 样件身份依据；原始表格未改动。
- 下一步：用同一几何和口径增加比值矩阵的网格敏感性，继续闭合样件—打印任务—STEP、机器—DIC 坐标与真实夹具边界。

## [2026-09-28] experiment | TC3000 竖直位移比 H6/H8 网格对照

- 来源：TC3000 `3.0 mm` 只读源 STEP；H6/H8 `r=1` 基准及 H6/H8 新增 `r=0.5/2` Abaqus 工件，均位于 `D:\PA12_Stage2\`。
- 方法：沿用临时正交线弹性卡、`vertical_z_in_plane` 候选映射、同一边界条件和中心 `±14 mm` 的 IVOL 统计；对每份 INP 统计 C3D10 连通节点和单元，并核对 `.msg/.sta`。
- 网格：H6 为 `84,779` 个实体连接节点、`54,612` 个 C3D10 单元、`138,588` 个 ROI 积分点；H8 为 `31,818` 个实体连接节点、`18,762` 个单元、`37,344` 个 ROI 积分点。两档 INP 节点记录分别另含 4 个参考点节点。
- 结果：两档 `PrimaryScore/K` 排序均为 `r=1 < r=2 < r=0.5`；H6/H8 的 `r=1` PrimaryScore 为 `0.059993/0.060756`。`G_transition` 在六案为 `2.2590–2.5599`，H6 到 H8 随比值变化约下降 `4.18%–11.75%`。六案均正常结束，每案 2 条数值奇异警告、0 条负特征值警告和 0 条错误消息。
- 判定：比值排序在这两档全局网格间保持，但过渡峰值比有网格敏感性；两档且无预设容差不构成网格收敛。临时弹性材料和候选坐标映射不支持塑性、断裂、实物打印方向、DIC/VFM 可辨识性或最终设计结论。
- 更新：[H6/H8 验证报告](Agents/PA12双轴试样仿真/验证/2026-09-28_TC3000竖直位移比补全.md)、六工况 CSV、H8 网格截图、`index.md`；模型与 ODB 文件均留在 D 盘 `g0_tc3000_vertical_ratio_20260928` 及原有 H8 基准目录。
- 下一步：按 G1 取得绑定样件的打印方向、实测材料与夹具边界；再定义收敛容差补做第三档网格，不能仅凭现有线弹性指标启动正式优化。

## [2026-09-28] experiment | TC3000 竖直位移比 H4/H6/H8 三网格矩阵

- 来源：TC3000 `3.0 mm` 只读源 STEP；复用 H4/H6/H8 的 `r=1` 基准，新增 H4 `r=0.5/2` 工况；全部 Abaqus 工件位于 `D:\PA12_Stage2\`。
- 方法：使用相同参数化脚本、临时正交线弹性材料、`vertical_z_in_plane` 候选坐标映射、运动学端部耦合、位移比定义和中心 ROI IVOL 统计；H4/H6/H8 全局种子分别为 `4/6/8 mm`。
- 网格：三档的实体连接节点/C3D10 单元/ROI 积分点分别为 H4 `253,255/171,411/467,916`、H6 `84,779/54,612/138,588`、H8 `31,818/18,762/37,344`。每档内三种比值保持同一网格。
- 结果：九案均正常结束，每案 2 条数值奇异警告、0 条负特征值警告和 0 条错误消息。`PrimaryScore/K` 的比值排序在三档下均为 `r=1 < r=2 < r=0.5`。H4→H8 的 `PrimaryScore` 变化为 `-3.12%/+2.00%/+0.57%`（按 `r=0.5/1/2`），`G_transition` 变化为 `-12.23%/-7.23%/-11.03%`。
- 判定：比值排序在临时线弹性模型的三档全局网格间保持，但过渡带指标变化明显且未预登记收敛容差，不构成网格收敛或正式设计选择；物理打印方向、材料参数和夹具边界仍待 G1 核实。
- 更新：[三网格验证报告](Agents/PA12双轴试样仿真/验证/2026-09-28_TC3000竖直位移比补全.md)、九工况 CSV、H4 网格截图、`index.md`；九案模型、输入卡、ODB、清单和求解记录均在 D 盘 `g0_tc3000_vertical_ratio_20260928` 及既有网格基准目录。
- 下一步：优先完成绑定实样—打印方向—坐标变换—夹具边界证据；随后按预先登记的主指标和过渡带指标容差决定是否加密。

## [2026-09-28] experiment | S19 Voce-I 双域 100% 窗口完成

- 输入：S19_X_0.2 已同步 DIC—力输入、完整 Job ROI 与 DIC subset 内缩敏感性域；使用 `configs/pa12_finite_j2_s19_voce_i.json`。原始照片、DAT、力学数据和 Job 文件未修改。
- 方法：固定 `nu=0.375`，主域/内缩域分别使用既定诊断候选 `E=2577.8864/2267.3227 MPa`，中心厚度 `1 mm` 仍为工作假设；分别拟合峰前 `000002–000126.jpg` 的 Voce-I `Y0/Q/b`，各 125 帧。
- 结果：主域 `Y0/Q/b=395.5698 MPa / 14.2983 MPa / 0.239940 应变⁻¹`，拟合窗/全历程 RMS `285.7882/285.4081 N`，支持率 `84.8667%`，`REVIEW_REQUIRED`；内缩域 `Y0/Q/b=347.9235 MPa / 37.4481 MPa / 0.911011 应变⁻¹`，RMS `306.7447/306.0310 N`，相对内缩分析域覆盖率 `100%`，`DIAGNOSTIC_ONLY`。两域逐帧 126 行的照片、时间和 X/Y 外虚功完全一致。优化器均以 `ftol` 终止，主域 18 次评估/10 次接受迭代，内缩域 110 次评估/91 次接受迭代；两条轨迹的 RMS 改善均很小。
- 判定：内缩域沿用完整 Job ROI 机器合力，不能解释为内缩域边界闭合。两域拟合误差和参数随积分域变化；主域支持率不足 95%，内外虚功未闭合，且窗口稳定性与边界物理证据未完成。因此不发布正式材料参数、不作为代理模型训练标签。两域工件均未保存缩放 Jacobian 秩/条件数，局部可辨识性未知。
- 更新：[S19 双域诊断记录](Agents/PA12实验数据处理/VFM自建/有限变形J2VoceI诊断/S19_X_0.2/S19有限变形J2VoceI双域100pct诊断.md)、内缩域自动摘要、`index.md`；主域摘要已含模型参数名和 Jacobian 未记录说明。
- 下一步：先补足 S19 单轴实物几何/厚度、边界位移与机器—DIC 有向坐标证据；随后开展 Voce-I 窗口稳定性和可辨识性分析，再决定是否进入跨实验验证。

## [2026-09-28] experiment | XZ 候选 Z 向数据身份与关联审计

- 来源：只读目录 `D:\C盘迁移\Desktop\yuan\data\XZ\xz_tu数据`；未改写图片、DAT、CSV 或 MatchID 配置。
- 方法：按四组目录统计扩展名；读取三个 CSV 的表头、字段值范围和重复/缺失 X 值；核对三份 M2INP 图像路径、像素导出选项与 `Conversion`；解压读取第四组 81 份 DAT 的头部图像字段并与本地 JPG 逐一核对；在外部数据根目录按样件/打印关键词和候选编号检索文件名。
- 结果：共 1,122 个文件（1,032 JPG、81 DAT、3 CSV、3 M2INP、3 CIHX）。三组配置引用分别有 227/227、546/546、178/178 个 basename 对应本地 JPG；三份 M2INP 的导出单位选项为 `0`（文件注释标为 pixels），`Conversion` 分别为 `0.057911/0.064381/0.066113`，尚无独立标定。第三组 CSV 的 334 行只覆盖 167 个不同 X 值，缺少 X=131–141。第四组 81 份 gzip 压缩 DAT 的图像字段与本地 JPG 全部对应；共同参考图在原始 `data` 目录内未找到，字段 ID `11` 均为 `0.063251`、定义与单位待核实。外部数据根目录名称搜索未找到 XZ 树外的打印/构建资料或 `XZ-10-04` 编号引用；未搜索电子表格单元格。
- 判定：`Serie/X/Y` 无单位和物理量定义，文件名 `Z/XZ` 不是打印方向证据；尽管图像—DAT 文件关联已闭合，仍未发现试样 ID—构建布局—STEP—机台力/位移闭环，不建立 `Q_i/R_i`，不发布 `E_Z` 或材料参数。
- 更新：[审计报告](Agents/PA12双轴试样仿真/验证/2026-09-28_XZ候选数据身份与关联审计.md)、G1 坐标矩阵、PA12 数据源登记、`index.md`。
- 下一步：优先追溯打印批次/平台排版及唯一试样 ID，再关联机台通道、单位、实测尺寸和 DIC 标定；对 CSV 缺段和 DAT—JPG 配对仅依据原始记录恢复，不补造、不按顺序推定。

## [2026-09-28] refine | XZ 候选数据与实验机工作簿关联核查

- 来源：只读 `D:\C盘迁移\Desktop\yuan\data\XY\data-20250529\20250529` 中的 12 份登记工作簿；隐藏锁文件排除，原文件未修改。
- 方法：从文件字节流识别并只读解析工作簿；核对工作表/列头，并搜索 `XZ-10-04`、`10-04`、`xz_tu`、sample/specimen、print/build/layout、打印/构建/样件/试样等字符串。
- 结果：12 份工作簿均包含 `Pos`、`Speed`、`Press` 表，记录 `T` 与 X1/X2/Y1/Y2 通道；上述身份关键词命中为 0。不能据此把任何机台数值配给 XZ 图像组。
- 判定：G1 的试样—打印任务—STEP—机台—DIC 身份链仍未闭合；文件名相似、速率标签或方向字母不足以建立配对。
- 更新：[XZ 候选数据身份与关联审计](Agents/PA12双轴试样仿真/验证/2026-09-28_XZ候选数据身份与关联审计.md)、G1 坐标矩阵、PA12 数据源登记、PA12 总目标与阶段计划、`index.md`。
- 下一步：寻找唯一试样 ID、打印平台排版/构建记录和机台—相机共同时间基；在此之前不从 XZ 组提取材料方向参数。

## [2026-09-28] refine | 五档源 STEP 几何变量耦合复核

- 来源：既有五档 STEP 几何回归 CSV、manifest 与 Abaqus 几何族报告；源 STEP 保持只读。
- 结果：TC1000–TC2500 中心厚度每增加 `0.5 mm`，平坦面边长同步增加约 `0.4975 mm`、过渡半径减少 `0.24875 mm`、微壁高度减少 `0.00125 mm`；TC3000 不含减薄平面/微壁且拓扑变化。五例因此定义为离散耦合几何族，不是厚度单因素序列。
- 更新：[几何族报告](Agents/PA12双轴试样仿真/验证/2026-09-28_PA12源厚度STEP族竖直坐标几何库.md)、[PA12 总目标与阶段计划](Agents/PA12实验数据处理/处理记录/PA12总目标与阶段计划.md)、`index.md`。
- 下一步：以五个源 STEP 为固定离散案例推进阶段 2 同条件竖直加载比与几何筛查；不插值/外推或作厚度单因素归因。若需因果识别，再建立固定其余特征的受控 CAD 序列；材料、打印坐标、边界和 DIC/VFM 放行条件仍待闭合。

## [2026-09-28] experiment | TC3000 H1.6 竖直位移比矩阵补齐

- 输入：只读 `D:\PA12_Stage2\source_geometry_inspection\inputs\tc3000.step`；`ΔX=0.05 mm`，`ΔY=0.025/0.05/0.10 mm`，全局种子 `1.6 mm`、C3D10、`vertical_z_in_plane`；材料为既有临时正交线弹性诊断卡。
- 结果：三案均正常完成、0 错误、0 负特征值警告；每案 1 条 DOF 3 数值奇异警告、7 个畸变四面体、中心 ROI 403,516 个积分点。`r=0.5/1/2` 的 PrimaryScore 为 `0.166582/0.060598/0.101470`，K 为 `0.6273427/0.0348744/0.5438776`，G_transition 为 `2.374962/2.323968/2.415179`。当前口径下 `r=1` 的中心均匀性与双轴平衡指标最低，但过渡带峰值仍高于中心峰值。
- 更新：[TC3000 H1.6 矩阵报告](Agents/PA12双轴试样仿真/验证/2026-09-28_TC3000_H1P6竖直位移比矩阵.md)、[15 工况 CSV](Agents/PA12双轴试样仿真/验证/2026-09-28_五档源STEP耦合几何竖直位移比15工况矩阵.csv)、指标 PNG 与网格截图、`index.md`、PA12 阶段计划。
- D 盘工件：`D:\PA12_Stage2\g19_tc3000_vertical_ratio_h1p6_20260928\`，含三案 CAE/INP/ODB/STA/MSG/DAT、manifest、网格图、LE 后处理 JSON 和汇总脚本。
- 限制/下一步：五个源 STEP 是耦合几何案例，不能作中心厚度因果归因；临时材料、数值奇异、畸变单元、夹具面外边界及实物打印方向仍未验证。先完成网格/边界/材料验证，再推进受控 CAD 单变量与 DIC/VFM 评价。

## [2026-09-28] experiment | S19 Voce-I 主域 50%/75% 窗口稳定性

- 输入：S19_X_0.2 已同步 DIC—力输入；使用 [50%/75% 隔离配置](configs/pa12_finite_j2_s19_voce_i_window_stability.json)，完整 Job ROI 主域。100% 基准工件保持原位，原始照片、DAT、力学数据和 Job 文件未修改。
- 方法：固定 `E=2577.8864 MPa`、`nu=0.375`，厚度 `1 mm` 仍为工作假设；分别使用峰前 50%（拟合终点 `000063.jpg`）和 75%（`000094.jpg`）数据拟合 Voce-I `Y0/Q/b`。
- 结果：50% 为 `335.5239/79.7224/2.053223`，拟合窗 RMS `157.8176 N`，Jacobian 秩 `3/3`、条件数 `738.4019`，41 次评估/30 次接受迭代；75% 为 `305.9556/29.3992/0.809928`，拟合窗 RMS `224.4866 N`，秩 `3/3`、条件数 `10822.5232`，54 次评估/42 次接受迭代。两窗口均以 `ftol` 终止，但接受轨迹 RMS 改善约 `0.394/0.405 N`。拟合终点不同，RMS 不作横向优劣比较。
- 判定：与 100% 主域 `Y0/Q/b=395.5698/14.2983/0.239940` 相比，窗口参数明显漂移；50%/75% 满秩但条件数较高且增大，不能据此发布材料参数。完整 Job ROI 覆盖率仍为 `84.8667%`、`REVIEW_REQUIRED`，边界外功与 S19 几何物理证据仍未闭合。100% 基准 Jacobian 未记录，不回填推断。
- 更新：[S19 双域窗口诊断记录](Agents/PA12实验数据处理/VFM自建/有限变形J2VoceI诊断/S19_X_0.2/S19有限变形J2VoceI双域100pct诊断.md)、`index.md`；对应拟合窗和优化轨迹工件保存在 `50_75pct_window_stability/full_job_roi/`。
- 下一步：继续同配置下的 DIC subset 内缩域 50%/75% 独立敏感性窗口；完成后比较两域窗口漂移和条件数，但内缩域仍沿用完整 ROI 外虚功，不作为子域闭合。

## [2026-09-28] audit | S19 Voce-I 计算预算与交接状态同步

- 证据：完整 Job ROI 的 50%/75% 全网格精修分别为 `1868.438/4013.413 s`、`41/54` 次函数评估；DIC subset 内缩域 100% 基准为 `9854.724 s`、110 次评估。代码路径中每次残差调用都会重放拟合窗历史并对全积分网格求解平面应力厚度伸长；暖启动已启用，但小型合成基准端到端收益约 `4–7%`。
- 判定：内缩域 50%/75% 任务在最近检查时仍响应，检查点只完成主域 2/4 窗口；未落盘的窗口不视为结果。既有双域 100% 分支已经保留 126 帧内外虚功数据与图，因此可继续推进其他诊断，不让额外窗口扫描阻断总目标。
- 更新：[阶段计划](Agents/PA12实验数据处理/处理记录/PA12总目标与阶段计划.md)、[GPT 交接文档](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、机器状态 JSON；`index.md` 已有 S19 Voce-I 双域与主域窗口诊断入口。
- 下一步：如内缩域窗口在可承受预算内完成，独立审计其拟合与稳定性；同时继续单轴—双轴自建 VFM 数据闭环及真实几何、坐标、边界证据收集，不发布条件候选为正式参数。

## [2026-09-28] audit | S19 载荷骤降帧对虚功残差的影响

- 输入：S19 完整 Job ROI 的 126 行逐帧有限变形 J2 Voce-I 虚功 CSV；比较拟合窗 `000002–000126.jpg` 与含 `000127.jpg` 的全历程。
- 结果：拟合窗 X/Y 逐轴残差 RMS=`399.3504/62.2013 N`；全历程为 `398.8393/61.9905 N`。最大 X 残差 `637.8412 N` 在 `000126.jpg`；`000127.jpg` 的 X 外虚功由前帧 `1141.6 N` 降至 `178.6 N`，该帧残差为 `+328.7486 N`。
- 结论：载荷骤降帧没有主导总残差，较大的 X 失配在骤降前已经出现；此项不判断末帧 DIC 场是否有效，也不改变拟合窗和参数放行状态。
- 更新：[S19 双域窗口诊断](Agents/PA12实验数据处理/VFM自建/有限变形J2VoceI诊断/S19_X_0.2/S19有限变形J2VoceI双域100pct诊断.md)、[GPT 交接文档](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、机器状态 JSON、`index.md`。
- 下一步：保留当前隔离计算；继续查明骤降前持续失配的主因，优先核实 S19 的实物几何/有效截面、机器—DIC 有向轴与单位虚场边界条件，并等待内缩域 50%/75% 工件落盘后再作独立敏感性比较。

## [2026-09-28] audit | S19 机器 X 单位虚场边界跳差

- 来源：S19 原始 `Job.m2inp` 的 Polygon 顶/底顶点与标定 `0.084746 mm/pixel`；自建 VFM 配置的机器轴映射；S19 `000126.jpg` 内外虚功 CSV。
- 方法：机器 X 映射到 DIC `y/v`，按 Job Polygon 两端的 y 坐标计算 `v*_X=y/L_X` 的端边虚位移差，不假设均布牵引、不重建牵引分布。
- 结果：X 向包络 `777 px = 65.847642 mm`；两端单位场跳差 `0.997426–1.000000`，与单位跳差最大相差约 `0.2574%`。`000126.jpg` 的 X 残差 `637.8412 N`，占外虚功 `1141.6 N` 的 `55.8726%`。
- 结论：几何归一化偏差不足以解释当前残差；机器力是否等于 ROI 切面合力、准静态传力及 DIC 缺失区域应力仍未闭合。没有据此发布参数或改动外功算法。
- 更新：[单轴几何证据缺口](Agents/PA12实验数据处理/处理记录/PA12单轴几何证据缺口.md)、[S19 Voce-I 双域诊断](Agents/PA12实验数据处理/VFM自建/有限变形J2VoceI诊断/S19_X_0.2/S19有限变形J2VoceI双域100pct诊断.md)、[GPT 交接文档](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、机器状态 JSON、`index.md`。
- 下一步：继续按完整 Job ROI 主域与 DIC subset 内缩域敏感性分开处理；优先取得 S19 样件/夹具与载荷截面的直接证据，再判断外虚功闭合条件。

## [2026-09-28] refine | TC3000 四级网格幅值匹配复核

- 来源：既有 TC3000 H4/H6/H8 九案摘要与逐案 manifest、锁定库 `tc3000.step`，以及本轮 H1.6 三案 ODB/manifest。历史 STEP 副本与锁定源经二进制比较一致；材料、坐标、耦合、ROI 及对应加载幅值设置已核对。
- 处理：发现旧 `r=2` 网格组使用 `ΔX=0.025, ΔY=0.05 mm`，与新 15 工况矩阵中的 `0.05/0.10 mm` 不同；在 H1.6 另补匹配幅值重复，保留原 15 工况矩阵不变。合并为 12 行四级网格敏感性数据。
- 结果：H1.6 相对 H8 的 PrimaryScore 变化为 `−0.259%–+3.773%`，K 最大绝对差为 `0.000361`，G_transition 变化为 `−0.124%–+7.639%`；过渡带峰值仍高于中心峰值。
- 更新：[TC3000 H1.6/四级网格报告](Agents/PA12双轴试样仿真/验证/2026-09-28_TC3000_H1P6竖直位移比矩阵.md)、[四级敏感性 12 工况 CSV](Agents/PA12双轴试样仿真/验证/2026-09-28_TC3000_四级网格敏感性12工况.csv)、[网格敏感性图](Agents/PA12双轴试样仿真/验证/2026-09-28_TC3000_四级网格敏感性.png)、`index.md`、PA12 阶段计划。
- 限制/下一步：未预登记网格收敛容差，不判定收敛通过；继续完成边界、材料和局部网格验证，再进入受控 CAD 与 DIC/VFM 指标评价。匹配幅值工件保存在 D 盘 `g19_tc3000_vertical_ratio_h1p6_20260928\R20_MATCHED_LOAD\`。

## [2026-09-28] audit | TC3000 ROI 实际网格密度复核

- 来源：只读 TC3000 四份 Abaqus `.inp` 输入卡（H1.6/H4/H6/H8）；旧求解结果与原始输入卡未改写。
- 方法：按现有后处理脚本的 10 节点算术平均定义元素质心，逐单元统计中心 `±14 mm` 方形 ROI 和 `14–16 mm` 过渡带；用 C3D10 四角节点体积换算等体积边长 `h_eq=(6√2V)^(1/3)`。中心 ROI 单元数乘 4 后与既有积分点数逐档完全一致。
- 结果：按中心 ROI 中位 `h_eq` 的实际细化顺序为 H4 `0.544076`、H1.6 `0.572262`、H6 `0.782779`、H8 `1.250245 mm`。H1.6 全模型有 `190,402` 个单元，虽多于 H4 的 `171,411`，其 ROI 单元却较少（`100,879` 对 `116,979`）；全局总数或名义种子不能代表 ROI 分辨率。H4/H6/H8 相邻 ROI 尺度比约 `1.438/1.597`，但 `r=2` 的 PrimaryScore/G_transition 对网格非单调。
- 更新：[TC3000 网格敏感性报告](Agents/PA12双轴试样仿真/验证/2026-09-28_TC3000_H1P6竖直位移比矩阵.md)、[ROI 实际网格密度 CSV](Agents/PA12双轴试样仿真/验证/2026-09-28_TC3000_ROI实际网格密度.csv)、[可复算 INP 审计脚本](Agents/PA12双轴试样仿真/audit_tc3000_roi_mesh_density.py)、`index.md`、PA12 阶段计划；D 盘输出位于 `D:\PA12_Stage2\g20_tc3000_roi_mesh_density_audit_20260928\`。
- 判定/下一步：此项修正名义网格级别的实际空间顺序，不构成收敛通过。先登记指标容差，再用 H4/H6/H8 三档敏感性结果作判定；若未达标，再建立中心与过渡带局部加密网格。

## [2026-09-28] audit | S15 完整 Job ROI 有限变形运动学门槛

- 输入：S15 CP936 编码 DIC—力索引、全程共同网格 DIC 场、Job Polygon 与既有双轴配置；原始照片、DAT、力文件和 Job 文件只读。
- 方法：按 Job 网格间距 `0.087464 mm` 构建三角网；逐帧计算 `F`、`det(F)` 与正 Jacobian 单元上的 Euler–Almansi 应变，只统计与完整 Job ROI 有正面积交叠的实测三角形，不对未覆盖面积补场。完整 Job ROI 为主域，DIC subset 内缩域不混入本次主域结论。
- 结果：284 帧中，首个非正 Jacobian 出现在 `000206.jpg`，共有 27 帧出现非正单元；首个翻转前为 `000205.jpg`。末帧 `000284.jpg` 有 16 个非正单元，占该帧 ROI 交叠面积 `0.008311%`。ROI 面积/实测支持面积为 `828.038378/736.338412 mm²`，覆盖率 `88.9256%`。早期 `000003.jpg` 在约 `31 N` 载荷下局部应变幅值最大值为 `1.1203`，P99 为 `0.0579`。
- 判定：`000205.jpg` 只表示当前网格下首个翻转前边界，不是可识别材料的拟合终点；低载荷局部极值、ROI 覆盖不足及物理同步/几何/外功门槛未闭合，故不启动 S15 `Y/H` 拟合。J2 runner 读取器复用 CP936 支持，并按照片名定位合并场；`python -m pytest -q tests/test_pa12_finite_j2_runner.py` 为 `12 passed`。
- 更新：[S15 运动学审计](Agents/PA12实验数据处理/VFM自建/有限变形诊断_等双轴生产网格/S15_XY_0.2/S15双轴有限变形J2运动学门槛审计.md)、GPT 交接文档/状态、`index.md`。
- 另记：S19 隔离窗口检查点当前完成主域 50%/75% 和内缩域 50%，内缩域 75% 未完成；2026-09-28 07:06 未发现 runner 进程。未重启作业，未把检查点之外的输出记作结果。

## [2026-09-28] audit | S15 双域运动学与局部热点追踪

- 来源：S15 全程共同网格 DIC—力数据、`Job.m2inp` 标定与原始照片；输入文件只读。
- 结果：完整 Job ROI 与 DIC subset 内缩敏感性使用相同的 `192,508` 个实测三角形，逐帧运动学相同；两域只在 ROI 面积与虚场尺度口径上不同。完整 Job ROI 保持主分析域，内缩域独立报告，不补齐未覆盖场。
- 局部复核：围绕 `(38.921480,40.233440) mm` 目标三角形 `0.5 mm` 内的 `205` 个三角形在 `000002–000020.jpg` 共同可用。`000003.jpg` 的 1 px 三角形最大局部应变为 `1.1203`，同邻域原生 DIC `|exx/eyy/exy|` 最大为 `0.0259`；其余 `000002/000004/000005/000006` 分别为 `0.6866/0.4617/0.4455/1.0282` 对 `0.0320/0.0316/0.0495/0.0353`。同一空间热点在多帧反复出现，`000002/000003` 的 4 个 `|e|>0.5` 三角形完全重合。Job 标定换算至约 `(445,460) px`，原图该处可见固定暗斑。
- 判定：应变极值对 1 px 相邻点差分尺度高度敏感，提示局部位移波动被三角形梯度放大；两种应变口径来自同一 DIC 场，不构成独立测量验证。合并 CSV 未保留逐点相关质量量，DAT `r/sigma` 语义/阈值未确认；不据此删点/删帧。本轮未启动 S15 `Y/H` 拟合，参数及训练标签仍未放行。
- 更新：[S15 运动学审计](Agents/PA12实验数据处理/VFM自建/有限变形诊断_等双轴生产网格/S15_XY_0.2/S15双轴有限变形J2运动学门槛审计.md)、[GPT 交接文档](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、交接状态 JSON、`index.md`。
- 下一步：完整 Job ROI 主分支保持不变，单独开展位移差分尺度敏感性分析，并检查热点暗斑邻域 `000001–000020.jpg` 的 DIC 相关质量图与有效点状态；缺少可解释质量量时保留人工复核项。DIC subset 内缩域继续独立作敏感性分析。

## [2026-09-28] audit | S15 局部位移梯度尺度敏感性

- 输入：S15 参考帧 `000001.jpg` 与 `000002–000020.jpg` 合并 DIC 场、同步力索引、Job 标定间距 `0.087464 mm/px`；只读读取，不改原始 JPG/DAT/CSV。
- 方法：在热点目标三角形质心周围，以共同有效的实测位移点做局部仿射最小二乘；比较 `2/4/6.5 px` 半径。13 px subset 的半宽仅用于定义 6.5 px 尺度，不代表独立观测窗口。
- 结果：抽查 `000002/000003/000004/000005/000006`，6.5 px 拟合局部最大应变为 `0.0201/0.0307/0.0160/0.0094/0.0171`，较 1 px 三角形值低 `96.5%–98.3%`；`000003` 的 `det(F)` 从 `0.5282` 变为 `0.9611`。半径 2/4/6.5 px 分别使用 13/50/133 个实测点，拟合设计矩阵均满秩。
- 结论：局部极值强烈依赖梯度支撑尺度；较大支撑拟合与原生 DIC 应变同量级，但源于同一测量场，不能当作真值、独立验证或删点依据。完整 Job ROI 继续为主域；DIC subset 内缩域继续独立作敏感性，生产结果不替换。
- 更新：[S15 运动学审计](Agents/PA12实验数据处理/VFM自建/有限变形诊断_等双轴生产网格/S15_XY_0.2/S15双轴有限变形J2运动学门槛审计.md)、[逐帧 CSV](Agents/PA12实验数据处理/VFM自建/有限变形诊断_等双轴生产网格/S15_XY_0.2/S15局部梯度尺度敏感性.csv)、GPT 交接文档/状态、`index.md`。
- 下一步：查找热点邻域 `000001–000020.jpg` 是否保留可解释的相关质量图或有效点字段；若没有，则保留人工复核，不按未知 `r/sigma` 阈值删点/删帧。物理 ROI、时序、坐标、外虚功和可辨识性门槛未闭合前不发布 S15 `Y/H`。

## [2026-09-28] audit | S15 DAT 有效标记与邻域支持时序

- 来源：S15 284 份合并 DIC 场、参考帧及原始 DAT `<18>/<53>`；字段映射沿用已通过同版本 Results Viewer 同帧核验的项目映射。
- 结果：目标三顶点坐标出现在全部 284 份合并场中；抽查六个关键帧，DAT `<53>` `valid=True`。目标质心 0.5 mm 邻域点数由 104 变化至最低 84，首降为 `000189.jpg`；6.5 px 邻域由 133 变化至最低 104，首降为 `000153.jpg`。`000205/000206.jpg` 两个尺度分别为 `104/132` 与 `104/133`，而 `000284.jpg` 为 `85/106`。末帧对照参考坐标分别缺 19/27 个邻域记录，重合坐标无 `valid=False`。
- 结论：热点顶点没有被显式标为无效，但这不是相关质量证明。晚期局部支持缩减表现为坐标记录缺失，具体成因未知；缺少可解释的相关质量字段，不删点、不按 `r/sigma` 猜测阈值。
- 更新：[S15 运动学审计](Agents/PA12实验数据处理/VFM自建/有限变形诊断_等双轴生产网格/S15_XY_0.2/S15双轴有限变形J2运动学门槛审计.md)、GPT 交接文档/状态、`index.md`。
- 下一步：在完整 Job ROI 的全历程共同实测网格上继续推进自建 VFM 虚功诊断；DIC subset 内缩域保持独立敏感性，不将其结果并入主域。

## [2026-09-28] audit | S15 阶段1内外虚功曲线与 E 窗口

- 来源：S15 完整 Job ROI 与 DIC subset 内缩域既有 284 帧自建 VFM CSV/JSON；仅读取结果，不重算或覆盖曲线。
- 范围：阶段1线弹性拟合窗 `000002–000049.jpg`，48 帧；窗口外阶段1响应不用于虚功闭合判定。
- 结果：完整域/内缩域 `E=3536.4347/3396.6972 MPa`，相对 RMSE 均约 `0.112`，高于当前 `0.10` 放行线；X/Y 残差 RMS 为 `75.9781/72.5665 N`，相关系数为 `0.992291/0.993246`。前七帧 `000002–000008.jpg` 内外虚功异号；整轴全局反号后的 RMS 恶化到 `776.9921/784.1934 N`，故不支持全局翻轴。两域 284 帧 Stage 1 曲线最大差 `1.01×10⁻⁸ N`，但 E 标度相差 `−3.95%`。
- 判定：阶段1候选仅为同窗标定结果，相关性不是独立验证；完整域仍为主结果，内缩域只作敏感性。RMSE 未达门槛，先不进入 S15 `Y/H`。
- 更新：[S15 运动学审计](Agents/PA12实验数据处理/VFM自建/有限变形诊断_等双轴生产网格/S15_XY_0.2/S15双轴有限变形J2运动学门槛审计.md)、[阶段1复核 CSV](Agents/PA12实验数据处理/VFM自建/有限变形诊断_等双轴生产网格/S15_XY_0.2/S15阶段1虚功窗口复核.csv)、GPT 交接文档/状态、`index.md`。
- 下一步：分析阶段1残差随窗口位置变化及零力参考—起始加载对应，不任意剔除前七帧；再依据已确认的窗口门槛决定能否进入 Y/H。

## [2026-09-28] audit | S15 阶段1端点敏感性与起始响应

- 来源：完整 Job ROI 与 DIC subset 内缩域既有自建 VFM 逐帧曲线、阶段1窗口复核及已筛选的 `000002–000049.jpg` 48 帧；原始 DIC、照片和力数据只读。
- 方法：按现有过原点 `E` 拟合公式，对原有48帧作7/12/24/36/48帧时间前缀扩展；不改拟合窗口，不剔除照片。
- 结果：两域五个前缀的相对 RMSE 均超过 `0.10`；完整 Job ROI 的候选 `E` 为 `−8527.132/6213.888/5179.642/4061.866/3536.435 MPa`，内缩敏感性为 `−8190.194/5968.354/4974.975/3901.366/3396.697 MPa`。零力参考 `000001.jpg` 与力索引对齐；`000002–000008.jpg` 正力下平均机器向应变和内虚功异号，`000009–000010.jpg` 逐步转正，物理成因未区分。
- 判定：窗口端点敏感且所有前缀均未达到阶段1门槛；不挑选较短窗口、不拟合 `Y/H`、不发布参数或训练标签。完整 Job ROI 为主域，DIC subset 内缩域只作独立敏感性。
- 更新：[S15 审计报告](Agents/PA12实验数据处理/VFM自建/有限变形诊断_等双轴生产网格/S15_XY_0.2/S15双轴有限变形J2运动学门槛审计.md)、[端点敏感性 CSV](Agents/PA12实验数据处理/VFM自建/有限变形诊断_等双轴生产网格/S15_XY_0.2/S15阶段1窗口端点敏感性.csv)、GPT 交接文档/状态、`index.md`。
- 下一步：转向核实 S15 物理 ROI 与中心恒厚区的配准、机器—DIC 有向坐标和外功边界证据；该证据闭合前保持阶段1及 `Y/H` 参数门槛关闭。

## [2026-09-28] audit | S15 样件几何来源盘点

- 来源：登记的 S15 原始实验目录、`Job.m2inp`、仓库通用 STEP 资产与既有 tc1000 几何审计；原始照片、DAT、Job、MTI、STEP 均只读。
- 结果：S15 目录有 289 张 JPG、286 个 DAT、`Job.m2inp` 与 `S15_XY_0.2.mti`，无 S15 专属 STEP、图纸或测厚记录。仓库候选 `PA12_tc1000.step` 的中心平坦面为 `28.01×28.01 mm`；Job ROI 为 `28.775656×28.775656 mm`。若假设候选 STEP 与 S15 身份相同且同心，Job ROI 单侧超出 `0.382828 mm`；身份与配准未证实，故这不是实际跨越结论。
- 判定：完整 Job ROI 仍为主域，DIC subset 内缩域仅作独立敏感性；不裁切 ROI，不把全域 `1 mm` 厚度视为已测。S15 阶段1及材料参数仍未放行。
- 更新：[S15 审计报告](Agents/PA12实验数据处理/VFM自建/有限变形诊断_等双轴生产网格/S15_XY_0.2/S15双轴有限变形J2运动学门槛审计.md)、GPT 交接文档/状态、`index.md`。
- 下一步：优先推进已有双域自建 VFM 结果充分且不需覆盖旧输出的等双轴组；S15 物理边界需补充样件—STEP 身份与实际厚度/位置证据。

## [2026-09-28] experiment | S19 Voce-I 内缩域 50%/75% 窗口敏感性

- 来源：S19 已合并 DIC—力数据及完整 Job ROI 外虚功序列；使用 [75% 暖启动配置](configs/pa12_finite_j2_s19_voce_i_inset_075_warmstart.json) 和既有 50% 窗口配置。原始照片、DAT、力学数据和 Job 文件只读。
- 方法：固定 `E=2267.3227 MPa`、`nu=0.375`、厚度 `1 mm` 工作假设和 DIC subset 内缩分析域；分别拟合至 `000063.jpg`、`000094.jpg`。75% 窗口从同域 50% 解初始化。
- 结果：50% 的 `Y0/Q/b=295.1081/160.4223/2.988253`，Jacobian `3/3`、条件数 `1044.6286`、拟合窗 RMS `168.5803 N`，全网精修 `3320.387 s`；75% 为 `269.3340/19.8365/0.571793`，Jacobian `3/3`、条件数 `32261.7112`、拟合窗 RMS `240.4028 N`，全网精修 `3995.945 s`。两窗长度不同，RMS 不作优劣比较；参数随窗口显著漂移，条件数升高约 `30.9` 倍。
- 判定：满秩不等于稳定；内缩域仍使用完整 Job ROI 机器合力作外虚功，不是子域边界闭合。与完整 ROI 支持率 `84.8667%`、实物厚度/坐标/边界证据缺口共同考虑，本轮只作为积分域/虚场敏感性诊断，不发布材料参数或训练标签。
- 更新：[S19 双域窗口诊断](Agents/PA12实验数据处理/VFM自建/有限变形J2VoceI诊断/S19_X_0.2/S19有限变形J2VoceI双域100pct诊断.md)、[阶段计划](Agents/PA12实验数据处理/处理记录/PA12总目标与阶段计划.md)、`index.md`；拟合数据、迭代轨迹和图表位于 `Agents/PA12实验数据处理/VFM自建/有限变形J2VoceI诊断/S19_X_0.2/50_75pct_window_stability/dic_subset_inset_sensitivity/`，D 盘副本位于 `D:\PA12_Stage2\vfm_s19_voce_i_window_sensitivity_20260928\`。
- 下一步：窗口扫描完成，不再重复扩窗；回到 G0 源 STEP 受控几何/网格评估和 G1 样件—打印方向—机台—DIC/夹持边界证据闭合。S19 诊断值不得用作正式材料卡或代理模型训练标签。

## [2026-09-28] audit | S18 原始力表与帧力索引复算

- 来源：S18 配置、原始 `Press` 工作表、现有照片—力索引和处理报告；原始工作簿、照片、DAT、Job、索引和配置均只读。
- 方法：按现行同步器的通道均值、基线/符号、事件区间、帧号时间归一和原始时间列线性插值规则逐行复算。
- 结果：原表 4,679 行，覆盖 `0–4.685 s`；索引 `000003–000128.jpg` 共 126 行。X/Y 最大复算差 `1.59×10⁻¹²/1.36×10⁻¹² N`。照片时间无可靠 EXIF，按 `0.050–2.553 s` 力事件区间映射；因此数值复现通过，物理时间同步未证实。索引显示时间仅到 `0.0001 s`，从显示时间重算会产生最高 `0.64/0.62 N` 的舍入差。
- 更新：[S18 复算审计](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S18原始力表与帧力索引复算审计.md)、GPT 交接文档与状态 JSON、`index.md`。
- 下一步：寻找相机时间戳、触发记录或共同时间基证据；完整 Job ROI 保持主域，DIC subset 内缩域保持独立敏感性，正式参数与训练标签不放行。

## [2026-09-28] audit | S19 Linear J2 与 Voce-I 同窗可区分性

- 来源：S19 Linear J2 与 Voce-I 两组 `50/75/100%` 拟合 JSON、逐帧内外虚功 CSV、两份模型配置及 `tools/pa12_finite_j2.py` 中的硬化律定义；原始实验输入未修改。
- 方法：完整 Job ROI 作为主域、DIC subset 内缩域作为独立敏感性；在各自相同 `E、ν`、相同预峰窗口与同一帧力/DIC输入下比较拟合 RMS。另对 75% 参数解计算 `000095–000126.jpg` 的连续时间留出残差，峰后 `000127.jpg` 单独列示。逐帧 CSV 核对照片键、时间、外虚功、DIC 面积与支持率。
- 结果：六个域—窗口组合的拟合 RMS 差（Voce-I 减 Linear）为 `−0.009203…+0.002089 N`。75% 留出 RMS：主域 Linear/Voce-I=`415.675855/415.673124 N`，内缩域=`446.965368/446.970405 N`；差异小于 `0.006 N`。各域两模型 126 行输入序列完全一致。
- 判定：残差仍为数百牛，当前 S19 数据不能区分 Linear J2 与 Voce-I，也没有依据选定更复杂模型。主域 DIC 支持率 `84.8667%`；内缩域使用完整 Job ROI 外虚功，仍仅作积分域敏感性。正式参数与代理模型标签不放行。
- 更新：[S19 双域诊断与模型对照](Agents/PA12实验数据处理/VFM自建/有限变形J2VoceI诊断/S19_X_0.2/S19有限变形J2VoceI双域100pct诊断.md)、GPT 交接文档/状态 JSON、阶段计划、`index.md`。
- 下一步：不重复高耗时窗口拟合；继续源 STEP 受控几何/网格评估和实体样件—打印方向—机台—DIC/夹持边界证据闭合。

## [2026-09-28] audit | S16 历史 MatchID VFM 试算文件流与 Forces 帧数

- 来源：S16 `S16_XY_0.2_258_3try.vfm`、`S16_XY_0.2_258_4try_step3.vfm`、解析器 `tools/vfm_boundary.py` 与完整基准 `.vfm` 的既有审计；原始文件只读。
- 方法：按 1 MiB 分块流式解压并扫描标签；`3try` 上限 256 MiB，`4try_step3` 上限 1 GiB。解析器把 `<Forces>` payload 第二字段解析为声明帧数。
- 结果：`3try` 解压 `5,242,880 B` 后在 EOF 报缺少 gzip 终止标记，截断前未见 Boundary/Forces，故不能由该文件复算 GUI 报告的 X/Y MAE `26.1206/23.4119 N` 和末帧差 `1452.79/1478.85 N`。`4try_step3` 完整干净 EOF（357,389,595 B），有 4 个 Boundary、4 个 Forces 标签，声明帧数为 `0/0/0/0`，与 GUI Forces count=`0` 一致。完整基准 `.vfm` 每组 258 帧，是独立文件，不替代试算文件。
- 判定：保留 `3try` 力差为用户/GUI 历史报告、不可由该损坏流独立复现；`4try_step3` 是零帧序列而非缺少标签。二者均不可用于参数识别。MatchID 仅作历史审计，自建 VFM 主路径不变。
- 更新：[边界载荷说明](Agents/PA12实验数据处理/MatchID_VFM准备/PA12_VFM边界载荷说明.md)、GPT 交接文档/状态 JSON、`index.md`。
- 下一步：不修补、不替换原始试算文件；保持 S16 物理同步与自建 VFM 门槛独立审查。

## [2026-09-28] experiment | TC2000 源 STEP 中心减薄与竖向位移比

- 来源：只读 `D:\PA12_Stage2\source_geometry_inspection\inputs\tc2000.step`；几何/网格探针及三组同网格 Abaqus 2025 输入、ODB、DAT、MSG、STA；临时线弹性材料参数与竖向材料坐标映射。源 STEP 未修改。
- 方法：由源 STEP 派生中心平台 `28×28 mm`、中心厚度 `1.5 mm` 的对称减薄几何；C3D10/H1.6，同一材料和边界分别计算 `ΔY/ΔX=0.5/1/2`。按中心 `±14 mm` ROI 的 IVOL 加权全局应变/应力计算 CV 和应变平衡指标；检查所有算例终止文件并定位畸变单元。
- 结果：三案 `.sta` 均成功结束、ODB 存在，分析阶段数值警告为 0。`r=1` 的 ROI 应变平衡 `K=0.03002`、四项 CV 和 `0.13191`，低于 `r=0.5` 的 `0.58126/0.19144` 与 `r=2` 的 `0.51066/0.16199`。平均应变仅约 `0.01%–0.08%`。三案均有 `913/85,249` 个初始畸变四面体；其中 `911` 个在 `14–16 mm` 过渡带、2 个在臂/外区，中心 ROI 内畸变单元质心数为 0，另有 2 个包围盒触及 ROI。
- 判定：只保留同一几何/网格/临时材料下的中心区趋势，`r=1` 作为下一轮验证候选；过渡带峰值应力比受畸变单元影响，不作筛选判据。单网格、线弹性与打印/装夹坐标均未正式标定，不代表最终设计、8% 应变目标、断裂位置或 VFM 可识别性结论。
- 更新：[TC2000 试算报告](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000源STEP中心减薄与竖向位移比试算.md)、[指标 CSV](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000竖向位移比指标.csv)、几何/网格/应变截图、几何与比值试算脚本、`index.md`；完整 CAE/INP/ODB/审计文件保存在 `D:\PA12_Stage2\g21_tc2000_source_brep_center_depth_probe_20260928\` 和 `D:\PA12_Stage2\g22_tc2000_center_depth_vertical_ratio_20260928\`。
- 下一步：优先修正线性过渡与网格质量，完成 ROI 局部加密及三档实际网格敏感性；随后闭合打印方向、实验材料卡和夹具边界，再进入目标应变段 FE-DIC/VFM 验证。

## [2026-09-28] audit | TC3000 r=1 H4/H6/H8 探索性 GCI

- 来源：TC3000 四级网格敏感性 CSV 与 ROI 实际网格密度 CSV；只读读取已有 Abaqus 结果。
- 方法：固定等双轴比例 `r=1`，按中心 ROI 四角节点四面体体积换算边长 P50 作为代表网格尺度；使用不等细化比三网格幂律关系估计表观阶数，取三网格 GCI 安全系数 `1.25`。方法参照 [Celik 等（2008）](https://doi.org/10.1115/1.2960953) 与 [NASA Glenn 网格收敛说明](https://www.grc.nasa.gov/www/wind/valid/tutorial/spatconv.html)。
- 结果：H4/H6/H8 的 ROI 尺度为 `0.544076/0.782779/1.250245 mm`，细化比 `1.43873/1.59719`。`PrimaryScore` 的 `p=0.7661`，H4/H6 GCI=`2.8067/3.6821%`；`K` 的 `p=4.7903`，GCI=`0.0129/0.0737%`。`mean LE11` 无正表观阶数，`mean LE22` 振荡，`G_transition` 无正表观阶数。
- 判定：只保留 `PrimaryScore` 与 `K` 的条件性探索估计；不作为网格收敛通过或网格选择依据。每档仍有 2 条数值奇异警告，线弹性材料和夹具边界仍为诊断假设，项目也未预登记验收容差。VFM 继续使用完整 Job ROI 主域，DIC subset 内缩域只作独立敏感性。
- 更新：[TC3000 H1.6 位移比矩阵与 GCI 诊断](Agents/PA12双轴试样仿真/验证/2026-09-28_TC3000_H1P6竖直位移比矩阵.md)、GPT 交接状态 JSON、`index.md`。
- 下一步：不把这次试算升级为正式通过；先解决网格求解奇异性并为目标输出预先确定验收容差，再决定是否补局部网格级。与此同时继续按既定域口径推进 VFM 诊断和 G1 实物坐标/夹持证据闭合。

## [2026-09-28] audit | TC3000 r=1 三网格奇异警告节点核对

- 来源：只读读取 H4/H6/H8 三个 r=1 工况各自的 .msg 与 .inp；工件均位于 D:\PA12_Stage2\g0_tc3000_vertical_mesh_diagnostic_20260926\。
- 方法：逐条对照 solver warning 指出的实例/节点/自由度与 INP 节点坐标，并比较四个运动学耦合和位移/约束卡。
- 结果：H4 CRUCIFORM-1.266，坐标 (11.875, 39.0750008, -1.5) mm，DOF 2/3 ratio=1.E+09 / 10.E+12；H6 CRUCIFORM-1.261，坐标 (11.875, 48.1166649, -1.5) mm，ratio=1.E+09 / 10.E+15；H8 CRUCIFORM-1.39，坐标 (54.5750008, 11.875, -1.5) mm，ratio=100.E+09 / 100.E+12。三份 INP 的四个耦合、零约束及 0.05 mm 位移卡模式一致；每份 MSG 均为 2 条数值问题警告、0 条负特征值警告、0 条错误。
- 判定：警告 DOF 类型相同，但节点号和坐标随网格改变；边界卡一致只排除了输入卡模式不一致这一项，不能确定数值奇异根因。保持根因未定，不更改边界条件。
- 更新：[TC3000 H1.6 矩阵与奇异警告核对](Agents/PA12双轴试样仿真/验证/2026-09-28_TC3000_H1P6竖直位移比矩阵.md)、GPT 交接状态 JSON、index.md。
- 下一步：先确认物理夹具边界证据，再在只读/隔离副本中追踪警告自由度的约束、耦合从属关系及局部刚度；未取得物理依据前不修改正式模型边界。VFM 主域仍为完整 Job ROI，DIC subset 内缩域仅作独立敏感性。

## [2026-09-28] experiment | TC2000 H1.2 网格敏感性复核

- 来源：同一 TC2000 源 STEP 派生中心 1.5 mm 几何；H1.6 三加载比结果与 H1.2 `r=1` 结果。原始 STEP 保持只读，模型与求解文件保存在 D 盘。
- 方法：固定几何、临时正交线弹性卡、竖向坐标映射、边界和中心 `±14 mm` ROI；比较 C3D10 全局种子 1.6/1.2 mm 的 `r=1` 指标。按 `.dat` 的 WarnElemDistorted 表定位单元，并核对 `.sta/.msg` 终止及分析警告。
- 结果：网格由 `85,249` 增至 `144,533` 单元；畸变数 `913→992`，占比 `1.071%→0.686%`。畸变单元均在 ROI 外：过渡带 `911→990`、臂外区各 2 个；ROI 质心计数 `0/0`，包围盒交叠 `2→0`。`r=1` 四项 CV 和 `0.13191→0.13287`（`+0.73%`），最大单项 CV 相对变化约 `2.1%`，K=`0.03002→0.02966`；过渡带峰值比 `G_transition=2.00744→2.30428`（约 `+14.8%`）。两案均成功结束，分析阶段数值警告为 0。
- 判定：中心区均值/CV 在这两档网格呈初步稳定信号，但只有两档且 H1.2 仅有 `r=1`，不满足三档收敛或加载比复核；过渡带应力集中量受畸变影响，不作选型。材料、真实打印方向、夹具和 DIC/VFM 仍未标定。
- 更新：[TC2000 试算报告](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000源STEP中心减薄与竖向位移比试算.md)、[两档网格敏感性 CSV](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000_H1P6-H1P2_r1网格敏感性.csv)、H1.2 网格/应变图、`index.md`；完整 H1.2 CAE/INP/ODB 和审计文件位于 `D:\PA12_Stage2\g24_tc2000_global_h1p2_refinement_20260928\`。
- 下一步：先改用与源 STEP 过渡相容的连续几何，再完成至少三档网格和三种位移比的联合复核；正式材料、装夹与打印坐标门槛关闭前，不生成优化排名或代理模型标签。



## [2026-09-28] audit | S19 Voce-I 优化器迭代图阶段状态

- 来源：S19 Voce-I 有限变形 J2 双域 100% 报告及 50%/75% 窗口工件；逐项核对两分析域各窗口的迭代图、CSV 和 JSON。
- 结果：完整 Job ROI 主域与 DIC subset 内缩敏感性域均已有 50%/75%/100% 六组迭代图和对应 CSV/JSON。100% 窗口主域 CSV 11 行/10 个接受步，内缩域 92 行/91 个接受步；两份 JSON 的参数、域标识和停止信息与报告一致。
- 判定：图件展示的是接受优化迭代，不等于材料参数已收敛或识别通过。主域拟合 RMS 仅由 285.9235 降至 285.7882 N，且支持率 84.8667%；内缩域 RMS 由 307.0172 降至 306.7447 N，仍独立使用完整 Job ROI 机器合力。参数随域和窗口漂移，两个分支均为诊断候选；不据此生成正式屈服面或代理模型标签。
- 更新：S19 双域报告嵌入主域/内缩域 100% 迭代图；四类图路线图更新为“S19 部分实验轨迹已生成、全项目未完成”；更新 index.md。
- 下一步：继续按完整 Job ROI 主域、内缩域独立敏感性逐组生成可支持的图件；屈服面图等待本构定义、支持率、虚功和参数稳定性门槛通过，其他实验迭代图逐项核验后再纳入。

## [2026-09-28] audit | 自建 VFM 双域交付物只读复核

- 来源：`Agents/PA12实验数据处理/VFM自建/` 下 S15–S22 完整 Job ROI 主域及可构造的 DIC subset 内缩敏感性域现有 CSV、JSON、PNG。
- 方法：逐组核对输出文件、帧数、阶段 1 X/Y 内外虚功与残差字段、数值有限性、照片键唯一性及虚功图文件非空；不运行生成器或拟合器。
- 结果：完整 Job ROI 8 组/1127 行；内缩敏感性域 6 组/965 行；14 组共 2092 行。S19、S21 因 DIC 点云外接矩形未完全位于 Job Polygon 内，不构造矩形内缩域。
- 判定：输出可读性和数量一致性通过，但不代表物理边界、同步、虚功闭合或参数识别通过。完整 Job ROI 保持主分析域，subset 内缩域只作独立敏感性；材料参数和训练标签均不放行。
- 更新：`index.md`、[交接状态 JSON](Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json)；修正 S19 迭代图索引的过期状态。
- 下一步：继续推进样件几何/厚度、机器—DIC 坐标与同步、全域外功定义等物理门槛；不因工件完整而提前释放参数。S19 内缩域迭代图横轴标签拥挤，待确定展示刻度后只调整刻度，不删改数据点。

## [2026-09-28] audit | S19 单轴几何证据目录追查

- 来源：`D:/C盘迁移/Desktop/yuan/data/XY/picture-20250529/vertical_all_45°/PAPER/unixal` 实验数据树及 `PAPER` 中含 S19 的文件名检索。
- 方法：逐层确认 `unixal` 下 S19–S24 实验目录，并用大小写不敏感文件名筛选 CAD、图纸、尺寸文档常见扩展名；对 `PAPER` 执行 S19 文件名检索。
- 结果：`unixal` 树内未发现 `.step/.stp/.dxf/.dwg/.pdf/.xlsx/.xls/.docx/.png/.tif/.tiff` 候选文件；`PAPER` 下 S19 专名文件仅检出 `S19_X_0.2.mti`。
- 判定：本次没有发现可关联 S19 样件的几何资料；范围外归档或其他文件命名未排除。单轴实物厚度、有效宽度、标距及 Job ROI 物理关系仍未确认，不使用双轴十字 STEP 补齐。
- 更新：[单轴几何证据缺口](Agents/PA12实验数据处理/处理记录/PA12单轴几何证据缺口.md)、交接状态 JSON、`index.md`。
- 下一步：继续推进不依赖猜测几何的 VFM 诊断；正式 E/Y/H 识别仍等待可追溯的单轴几何及边界证据。

## [2026-09-28] audit | 有限变形 J2 硬化模型覆盖

- 来源：`tools/pa12_self_vfm.py`、`tools/pa12_finite_j2.py`、`tools/run_pa12_finite_j2_vfm.py`、对应测试及总路线图中的截图模型清单。
- 方法：对照通用应力—塑性应变曲线拟合、有限变形 J2 材料点硬化接口与实验 runner 的模型分派；只读源码，不改代码、不运行拟合。
- 结果：通用曲线比较层列出 Linear、Ludwik、Swift、Voce I、Voce II 五种形式；有限变形 J2 核/runner 仅接入 Linear 与 Voce I。Linear 当前实现正斜率 `Y₀+H ε̄p`，与论文式 (2.19) 的负号及正 `H` 数值冲突尚未解开。Voce II/Ludwik/Swift 目前不是有限变形 J2 返回映射模型。
- 判定：通用曲线拟合不等于本构状态更新或 VFM 参数识别；当前 generic Voce I/II 命名也不证明与用户截图/软件内部模型同义。不能据此发布参数或改变 H 符号。
- 更新：总路线图模型覆盖表与 `index.md`；当前无代码改动。
- 下一步：按用户要求把后续工作限定在材料本构，不扩展控制/GUI；先核对目标公式与参数定义，再设计统一硬化增量/切线接口，将缺失模型接入有限变形 J2 核、runner 和合成恢复测试。完整 Job ROI 仍为主域，DIC subset 内缩域仅作独立敏感性；实验候选继续标为诊断，不释放正式 E/Y/H。

## [2026-09-28] implementation | 有限变形 J2 多硬化律接入

- 来源：`tools/pa12_finite_j2.py`、`tools/run_pa12_finite_j2_vfm.py` 与 `tests/test_pa12_finite_j2.py`。
- 更新：接入 Ludwik、Swift、Voce II 候选的有限变形平面应力材料点更新和固定 `E/ν` VFM 拟合；runner 支持 Linear、Ludwik、Swift、Voce I、Voce II 并记录公式、独立参数、逐帧虚功、优化轨迹及 Jacobian 指标。Swift 的屈服值由 `K ε0^n` 派生；Voce II 明确采用 `Y0+R0 ε̄p+Q(1−exp(−b ε̄p))`，不主张与软件同名模型等价。
- 验证：有限变形 J2 核测试 `59 passed`，`tests/test_pa12_finite_j2_runner.py` 为 `13 passed`，合并运行 `72 passed`；覆盖新增模型公式、标量/批量返回映射、合成 VFM 参数恢复、Voce II 报告、真实 Linear runner 合成闭环和 Jacobian 输出。
- 判定：这是本构与软件链路实现/合成验证，不是 PA12 实验拟合。Linear 拟合器现返回参数尺度化 Jacobian 秩/条件数，实际 Linear runner 已合成闭环。完整 Job ROI 保持主域，DIC subset 内缩域只作独立敏感性且仍沿用完整 ROI 机器力；实验参数、屈服面和训练标签不放行。Linear H 公式符号冲突未解决。
- 更新：[总体方法协议](Agents/PA12实验数据处理/处理记录/PA12实验总体方法与防跑偏协议.md)、[GPT/VFM 交接文档与状态](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、[边界载荷说明](Agents/PA12实验数据处理/MatchID_VFM准备/PA12_VFM边界载荷说明.md)、`index.md`。
- 下一步：在隔离的模型配置/输出目录评估可辨识性、噪声与窗口敏感性；真实识别仍先从单轴候选开始，并受几何、同步、坐标及外功门槛约束。

## [2026-09-28] experiment | TC2000 H1.2 位移比与圆角候选网格质量对照

- 来源：只读 `D:\PA12_Stage2\source_geometry_inspection\inputs\tc2000.step`；g24 未圆角 H1.2 CAE/ODB/DAT/MSG/STA、g25 圆角几何、g26 三比例 ODB 与畸变定位、g27 局部网格 r=1 结果。源 STEP 与先前结果未修改。
- 方法：未圆角 28 mm 中心平台 H1.2 网格沿用既有 `r=1`，补算 `r=0.5/2`；圆角候选为中心厚 1.5 mm、16 条边 `R=0.10 mm`，同网格比较三比例；另对其周边 28 条几何边施加 `0.4 mm` 种子，仅复核 r=1。三种几何/网格均用相同临时正交线弹性卡、端面耦合、位移幅值和 `±14 mm` IVOL 加权中心 ROI。检查 `.sta/.msg/.dat`，并将畸变单元质心和包围盒映射至中心/过渡/臂区。
- 结果：未圆角基准 H1.2 三比例的 PrimaryScore 为 `0.19601/0.13287/0.15973`，K 为 `0.58054/0.02966/0.51053`；三案各有 `992` 个畸变单元，但中心 ROI 质心数和包围盒交叠均为 0（过渡带 990、臂外 2）。圆角 H1.2 网格有 `2,354` 个畸变单元，其中中心质心 28、过渡带 2,325、臂外 1，包围盒与 ROI 相交 658；局部 `0.4 mm` 网格有 `5,357` 个，其中中心 161、过渡带 5,194、臂外 2，包围盒相交 1,359。各算例正常终止，分析阶段数值警告、负特征值警告和错误均为 0。未圆角 r=1 中心平均 `LE11/LE22` 约 `0.0342%/0.0322%`，全部比例的最大分量均值仍低于 `0.08%`。
- 判定：未圆角 H1.2 的 `r=1` 只作为同一临时模型下的比例筛查参考，不是最优设计；单网格、材料/打印坐标/夹具未标定，且过渡带仍有畸变。圆角及其局部细化分支未通过中心 ROI 网格质量门槛，不据其低 PrimaryScore 或峰值比判为改进。塑性、断裂、DIC/VFM 参数可识别性和代理模型标签均未验证。
- 更新：[本轮对照报告](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000竖直位移比与圆角网格质量对照.md)、未圆角比例矩阵与圆角诊断 CSV、四张截图、相关生成/后处理脚本及 `index.md`。Abaqus 原生工件在 `D:\PA12_Stage2\g26_tc2000_rounded_transition_vertical_20260928\`、`g27_tc2000_rounded_local_h0p4_20260928\`、`g28_tc2000_taper_h1p2_vertical_ratio_20260928\`。
- 下一步：保留未圆角 H1.2 工件作比例参考；先建立匹配源 STEP 曲率且能保持中心 ROI 网格质量的过渡几何，再做至少三档网格及预登记容差复核。正式提高位移至塑性目标前，需闭合实物打印方向、材料本构和夹具边界；之后才进入 FE-DIC/VFM 验证。

## [2026-09-28] implementation | 有限变形 J2 Jacobian 秩与条件数分别报告

- 来源：`tools/pa12_finite_j2.py`、`tools/run_pa12_finite_j2_vfm.py` 及对应 runner 回归测试。
- 方法：报告状态按缩放 Jacobian 秩、参数数目和条件数三项分别判读；使用秩亏、满秩有限条件数、满秩非有限条件数三种 runner 输出用例验证。
- 结果：只有秩低于参数数目时 Markdown 才标记“Jacobian 秩亏”；满秩但条件数不可用时单独标示。JSON 保留 rank/参数数目，非有限 condition 记为 `null`。现有有限变形 J2 Markdown 摘要未命中旧误标文案，未重生成实验派生曲线。核心测试 `59 passed`，runner `15 passed`，合并 `74 passed`。
- 判定：秩与条件数是不同诊断量，不能由非有限条件数单独推出秩亏。该报告修正不改变实验拟合状态；当前仍未运行真实实验参数识别。
- 更新：[runner](tools/run_pa12_finite_j2_vfm.py)、[回归测试](tests/test_pa12_finite_j2_runner.py)、[总体方法协议](Agents/PA12实验数据处理/处理记录/PA12实验总体方法与防跑偏协议.md)、[GPT/VFM交接文档](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、[机器状态](Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json)、`index.md`。
- 下一步：为候选硬化律隔离配置和输出目录，继续评估合成数据下的参数可辨识性、噪声与窗口敏感性；真实实验拟合仍受单轴几何、同步、坐标和外功门槛约束。

## [2026-09-28] experiment | TC2000 W32 中心平台竖直位移比试算

- 来源：只读 `D:\PA12_Stage2\source_geometry_inspection\inputs\tc2000.step`；W32 几何、H1.2 网格以及三组竖直位移比 Abaqus 工件均保存在 `D:\PA12_Stage2\g34_tc2000_w32_taper_candidate_20260928\` 至 `g37_tc2000_w32_vertical_ratio_matrix_20260928\`。
- 方法：构造名义 `32×32 mm`、中心厚 `1.5 mm` 的对称直线过渡减薄几何；同一 C3D10 H1.2 网格上取 `ΔX=0.05 mm`、`ΔY/ΔX=0.5/1/2`。以固定 `±14 mm` ROI、IVOL 加权计算应力/应变 CV 和均值平衡，另统计 `14–16 mm` 过渡带峰值比；检查 `.sta/.msg/.dat` 并把畸变单元映射到 ROI。
- 结果：中心平台名义边长 `32 mm`、厚 `1.5 mm`，单一连通实体；网格 `303,646` 节点、`186,574` 个 C3D10。每案 ROI 有 `142,552` 个积分点。`r=0.5/1/2` 的 `PrimaryScore` 为 `0.138956/0.071110/0.096097`，`K=0.578718/0.029178/0.509735`，`G_transition=2.6442/2.5563/2.5961`；三案分析阶段均 0 数值 warning、0 负特征值、0 错误。全网格有 1,136 个输入畸变单元，四角质心代理分类为过渡带 1,134、外区 2、中心 ROI 0，且无 XY 包围盒与 ROI 相交。
- 判定：本轮唯一网格上 `r=1` 的三项筛查指标较低，可作为后续参考工况；不构成优化排名。平均应变仍低于 `0.08%` 数量级，模型仅为临时正交线弹性与未校准端面耦合；过渡区畸变、网格收敛、塑性/断裂、DIC/VFM 参数识别均未关闭。用户此前约 `8%` 为初步观察，与本次阶段和载荷不可直接比较。
- 更新：[W32 试算报告](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000_W32中心平台竖直位移比试算.md)、[三比例 CSV](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000_W32竖直位移比指标.csv)、几何/网格/云图截图、W32 几何/网格/渲染脚本及位移比求解脚本参数、`index.md`；三比例计算数据及原生 CAE/INP/ODB 保留在 D 盘 `PA12_Stage2`。
- 下一步：在同一 W32 几何下补足多档网格敏感性并改进过渡区网格；之后才开展中心厚度、平台宽度、过渡形状参数扫描，待材料和夹具标定后进入塑性及 DIC/VFM 验证。

## [2026-09-28] audit | PA12 全有效区间应力—应变交付物清点

- 来源：`Agents/PA12实验数据处理/应力应变/` 下逐实验 CSV、应力—应变 PNG 与 `完整曲线/` PNG；对照[应力—应变曲线审计](Agents/PA12实验数据处理/处理记录/PA12应力应变曲线审计.md)。
- 方法：只读核对 S15–S23 的逐组文件和 S24 状态，不重算曲线、不覆盖原始 JPG/DAT/XLS。
- 结果：S15–S23 九组均有应力—应变 CSV 与逐组图，且各有完整有效区间曲线图；S24 为预载释放记录，按现行分类不生成拉伸曲线。S15、S22、S23 保留报告中的事件复核状态。
- 判定：用户要求的逐组全区间曲线已有交付，没有发现需要补生成的实验；曲线齐全不代表照片—力物理同步或正式材料参数门槛通过。
- 更新：仅追加本日志记录；现有报告与图表未改。
- 下一步：继续处理自建 VFM 的可执行诊断；正式识别仍需物理 ROI/厚度、轴向标定、相机—力共同时间基和外功边界证据。未发现单独命名为 camera/trigger/timecode/sync/clock/metadata 的 S16/S18 文件，不能据此推断同步成立。

## [2026-09-28] experiment | TC2000 W32 r=1 网格敏感性

- 来源：W32 中心厚 1.5 mm 几何在 H1.2/H1.6/H2.0 的 C3D10 CAE/ODB/DAT/MSG/STA；对应网格与求解目录为 `D:\PA12_Stage2\g35/g36`、`g38/g40`、`g39/g41`。
- 方法：固定几何、材料、边界、`r=1` 位移和 `±14 mm` ROI；按同一 IVOL 加权后处理提取中心指标，并依据 Abaqus `.dat` 畸变表将单元映射到中心/过渡/外区。未对名义种子作 Richardson/GCI 收敛外推。
- 结果：H1.2/H1.6/H2.0 分别为 `186,574/138,390/127,741` 个 C3D10 单元，ROI 积分点 `142,552/139,348/155,380`。`PrimaryScore` 相对 H1.2 为 `0/−1.54%/−0.99%`，`K=0.029178/0.029190/0.029366`，`G_transition=2.55630/2.52844/2.53457`。畸变单元 `1,136/1,227/1,692`，三档中心 ROI 质心数和 XY 包围盒交叠均为 0；分析阶段 warning、负特征值和错误均为 0。
- 判定：名义网格下中心均值和筛查指标变化较小，但 ROI 积分点数不单调、过渡带畸变随粗化增加，且未预登记容差；仅记录为网格敏感性观察，不认定网格收敛。
- 更新：[W32 试算报告](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000_W32中心平台竖直位移比试算.md)、[三网格 CSV](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000_W32_r1网格敏感性.csv)、H1.6/H2.0 网格截图、`index.md`；三档原生工件及完整审计数据保留在 `D:\PA12_Stage2\` 的 g35–g42 目录。
- 下一步：先登记有效网格质量/收敛容差和 ROI 实际尺寸口径，再针对过渡带畸变做局部几何与网格改进；通过后再推进几何参数扫描。

## [2026-09-28] audit | 自建 VFM 运行状态与 GUI 历史交接复核

- 来源：Windows 进程快照、[GPT 交接文档](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)及[机器状态](Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json)。
- 方法：只查旧 PID `45360` 和执行 PA12 J2 runner 的 Python 进程；核对 S16 `3try`、`4try_step3` 与第 16 轮 GUI 候选是否已明确记录。
- 结果：未发现 PID `45360` 或匹配 runner。交接文档/JSON 已记载 `3try` 力序列不同步（X/Y MAE `26.1206/23.4119 N`，末帧差 `1452.79/1478.85 N`）、`4try_step3` Forces count 为 `0`，以及第 16 轮 `Y=63.93 MPa、H=41.55 MPa` 仅为 GUI 中间候选；本轮未重复写入这些既有事实。总阶段计划的“当前直接执行项”仍引用旧进程状态，索引已标注待同步。
- 判定：当前无需要续跑或清理的活动 VFM 进程。已完成的主域/内缩域结果不重跑；GUI 候选均不是正式识别结果。完整 Job ROI 继续作为主分析域，DIC subset 内缩域只作独立敏感性分析，且不视为自身边界闭合。
- 更新：修正 `index.md` 与交接状态 JSON 中过期的进程描述；历史日期记录保留。
- 下一步：在计划文件进入可修改范围后同步其当前执行指针；继续推进不依赖 MatchID GUI 的自建 VFM 证据闭环，参数发布仍受几何、时间同步、坐标及独立虚功/稳定性门槛约束。

## [2026-09-28] audit | S19 新硬化模型运行目录隔离

- 来源：`tools/run_pa12_finite_j2_vfm.py`、`configs/pa12_finite_j2_s19.json`、`configs/pa12_finite_j2_s19_voce_i.json`、`configs/pa12_finite_vfm_s19_production.json` 与 S19 现有诊断目录。
- 方法：只读核对 runner 参数、两份 S19 硬化配置的输出目录，以及目标目录现有文件；不启动拟合、不改配置、不覆盖产物。
- 结果：Linear 与 Voce-I 配置都指向 `Agents/PA12实验数据处理/VFM自建/有限变形J2VoceI诊断/S19_X_0.2`，目录内已有窗口稳定性 CSV、虚功诊断 JSON、运行检查点 JSON 和诊断报告。runner 只提供 `--config`、`--domain`、`--fraction`，没有单独的输出目录参数。
- 判定：现有 S19 产物不能作为新模型的输出目录直接复用；本轮未运行新增模型的真实实验拟合。后续必须先建立独立配置/输出位置，完整 Job ROI 作为主域，DIC subset 内缩域保持独立敏感性；所有拟合仍是诊断候选，不能绕过几何、同步、坐标及外功门槛。
- 更新：[GPT/VFM 交接文档](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、[机器状态 JSON](Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json)、`index.md`。
- 下一步：进入允许修改独立模型配置/输出目录的范围后，再按候选硬化律运行同一单轴窗口；先比较完整 Job ROI 主域，内缩域另做敏感性，不触碰既有 S19 输出。

## [2026-09-28] audit | S19 新模型配置可复用性清点

- 来源：`configs/pa12_finite_j2_s19.json`、`configs/pa12_finite_j2_s19_voce_i.json`、`configs/pa12_finite_j2_s19_voce_i_inset_075_warmstart.json`、`configs/pa12_finite_j2_s19_voce_i_window_stability.json`。
- 方法：搜索配置树中引用 S19 生产数据源的文件，再逐份核对 `hardening_model`、`analysis_domains` 和 `output_directory`；不修改配置、不启动拟合。
- 结果：共四份 S19 配置，分别为默认 Linear 与 Voce-I，另两份为 Voce-I 窗口/warm-start。未发现 Ludwik、Swift 或 Voce II 的 S19 实验配置。前述配置输出位于既有 S19 诊断目录或其窗口敏感性子目录。
- 判定：当前无新增硬化律可直接复用的 S19 实验配置。要继续模型比较，需先为每个候选建立独立配置和输出位置；完整 Job ROI 为主分析，DIC subset 内缩域单独作敏感性。参数仍受几何、同步、坐标和外功门槛约束。
- 更新：[GPT/VFM 交接文档](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、[机器状态 JSON](Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json)、`index.md`。
- 下一步：在可修改独立配置/输出目录时，先运行一个新增硬化律的完整 Job ROI 单轴诊断窗口，再评估是否需要内缩敏感性复算；不得复用既有 S19 输出路径。

## [2026-09-29] implementation | G1 坐标标定采集包与候选计算

- 来源：既有 [G1 实体试样坐标标定执行单](Agents/PA12双轴试样仿真/验证/2026-09-27_G1下一件实体试样坐标标定执行单.md)、逐样件采集总表及 `D:\PA12_Stage2\g1_coordinate_mapping_20260927\`；只读盘点未发现逐标记点输入表或坐标标定求解器。
- 方法：新增同平面标记点仿射拟合、机器 X/Y 实测微动与同事件 DIC 像素位移的独立残差核验；以已知映射、共线拟合点和超过预登记误差限三类用例验证。拟合阈值不自动推定，原始照片/测量/控制器文件未修改。
- 结果：3 项测试通过。求解器输出像素到机器平面 `B_i`、分离尺度/剪切后的方向因子 `R_i`、静态与运动留出残差及摘要；退化拟合会失败，已登记限值超限会标为 `HOLDOUT_FAILED`，整体 G1 放行固定为 `NOT_AUTOMATED`。四张空白输入模板和说明位于 [G1 坐标标定工具](Agents/PA12双轴试样仿真/验证/G1坐标标定工具/README.md)；D 盘工件为 `D:\PA12_Stage2\g1_coordinate_mapping_20260929_calibration\`。
- 判定：这是采集/计算工具链准备，不是实体标定；S16 及新样件 `Q_i/R_i`、独立尺度、共同时间基和构建身份链仍未闭合。当前仿射模型只适用于留出误差符合事先登记的不确定度范围的平面成像。
- 更新：[求解器](tools/g1_coordinate_calibration.py)、[测试](tests/test_g1_coordinate_calibration.py)、输入模板、`index.md`。未修改 `raw/` 原始资料。
- 下一步：对一件具唯一编号且可追溯构建记录的实体样件按模板采集真实点位与 X/Y 微动，登记不确定度限值后运行；随后继续基于已核实方向的 Abaqus 几何/网格诊断。无实测数据前不发布标定矩阵、材料参数或设计排名。

## [2026-09-28] correction | G1 标定工具工件日期

- 更正：前一条 G1 工具实现记录误用 `2026-09-29`。本机时间核对为 `2026-09-28 13:21`（Asia/Shanghai）；按追加式日志约定保留原记录，不改写历史。
- 更新：本轮创建的 D 盘目录已在 `D:\PA12_Stage2\` 内更名为 `g1_coordinate_mapping_20260928_calibration`；工具说明和 `index.md` 已同步更正。工具内容、空白模板和未标定状态不变。
- 下一步：继续执行 PA12 阶段计划中不依赖真实打印/标定记录的源 STEP 几何与网格评估；实体 G1 仍等待可追溯样件数据。

## [2026-09-28] audit | TC2000 W32 中心 ROI 实际网格尺度

- 来源：W32 `r=1` 的 H1.2/H1.6/H2.0 Abaqus 输入卡；只读复算 C3D10 节点与单元几何，不重新网格或求解。
- 方法：沿用 TC3000 ROI 审计解析器，以 10 节点坐标均值作为质心代理，固定 `max(|x|,|y|)≤14 mm` ROI；计算四角四面体等体积边长 `h_eq`、角边长度和 `14–16 mm` 过渡带尺度。
- 结果：实际 ROI `h_eq` P50 顺序为 H2.0 `0.622383 mm`、H1.2 `0.647523 mm`、H1.6 `0.651003 mm`；H1.2→H1.6 仅增加约 `0.54%`，名义较粗 H2.0 比 H1.2 细约 `3.88%`。积分点数复现既有 ODB 汇总。
- 判定：三档属于全局种子变化下的网格生成差异，不构成有序局部细化序列，也不构成网格收敛结论。
- 更新：[审计报告](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000_W32_ROI实际网格密度审计.md)、[ROI 尺度 CSV](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000_W32_ROI实际网格密度.csv)、`index.md`、阶段计划、GPT 交接文档与状态 JSON；CSV 的 D 盘副本位于 `D:\PA12_Stage2\g42_tc2000_w32_mesh_sensitivity_20260928\`。
- 下一步：固定 W32 几何和 `r=1`，先做 mesh-only 尺度标定，目标 ROI `h_eq` P50 约 `0.78/0.62/0.50 mm`；以实际 INP 复算排序后再决定是否运行正式网格敏感性求解。

## [2026-09-28] experiment | S19 Ludwik 完整 ROI 与内缩域敏感性

- 来源：S19 合并 DIC—力索引及逐帧场、既有同域 Linear 100% 窗口结果；原始 JPG/DAT/力学表未修改。
- 方法：为完整 Job ROI 主域和 DIC subset 内缩敏感性域分别建立独立配置/输出目录；固定各自前序条件 E、`ν=0.375`、配置厚度 `1 mm`，以各域 Linear 解构造 `n=1` Ludwik 初值；拟合 `000002–000126.jpg` 共 125 帧，保留至 `000127.jpg` 的 126 帧全历程。两域沿用同一完整 Job ROI 机器力序列。
- 结果：主域 `Y₀/K/n=395.4963/25.2870/2.69178`，Jacobian `3/3`、条件数 `98,367.3`、拟合 RMS `285.7881 N`、覆盖率 `84.8667%`；subset 敏感性域 `347.9327/16.7058/1.00002`，Jacobian `3/3`、条件数 `6,893.15`、拟合 RMS `306.7443 N`、域内覆盖率 `100%`。Ludwik 相对同域 Linear 的 RMS 改善仅 `0.001253 N` 和 `4.38×10⁻⁷ N`。两份 CSV 各 126 行且照片/时间/X/Y 外虚功逐帧一致，数值均有限。主域 X/Y 拟合残差 RMS 为 `399.350/62.203 N`；Y 外虚功为零而 Y 内虚功非零。
- 判定：数据不能区分 Linear 与 Ludwik。主域支持率低于 `95%`；subset 100% 只表示 subset 内覆盖，并仍使用完整 ROI 外力，不是子域自身边界闭合。参数均为条件诊断，不发布正式材料值或训练标签。
- 更新：[S19 双域报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S19_Ludwik双域诊断.md)（含四张图）、两份独立配置、总体方法协议、GPT 交接文档/状态 JSON、`index.md`。runner CLI 标准输出改为 UTF-8，回归测试覆盖 Windows GBK 控制台；J2 核 59 项、runner 16 项、联合 `75 passed`。
- 下一步：先核实完整 Job ROI DIC 支持缺口、S19 实物有效截面、边界虚位移和机器—DIC 有向坐标，再决定是否对该数据扩展其他硬化律。

## [2026-09-28] experiment | TC2000 W32 mesh-only 实际尺度标定

- 来源：只读 W32 几何 CAE `D:\PA12_Stage2\g34_tc2000_w32_taper_candidate_20260928\TC2000_SOURCE_CENTER_DEPTH_PROBE.cae`；网格、输入卡和截图写入 `D:\PA12_Stage2\g43_tc2000_w32_mesh_scale_probe_20260928\`，没有生成材料/载荷或提交求解。
- 方法：使用 Abaqus C3D10 自由四面体网格，测试全局 seed `0.6/0.8/1.2/3.2/4.8/6.4 mm`；复用 ROI 单元几何审计口径，中心 ROI `max(|x|,|y|)≤14 mm`，按四角四面体计算 `h_eq`。H1.2 网格节点/单元/ROI 数及拓扑与既有 W32 基线一致，坐标差小于 `5×10⁻⁸ mm`。
- 结果：六档 ROI `h_eq` P50 依次为 `0.492519/0.571882/0.647523/0.638481/0.642235/0.882863 mm`。全局 seed 与 ROI 尺度明显非单调；735,799 单元的 0.6 mm 档对应 `0.492519 mm`，6.4 mm 档 37,242 单元、对应 `0.882863 mm`。
- 判定：候选粗/中/细档取 seed `6.4/1.2/0.6 mm`，实际 ROI P50 `0.882863/0.647523/0.492519 mm`，相邻尺度比 `1.36/1.32`。仅为网格敏感性候选；未检查求解畸变、未求解，不形成收敛或几何排名。
- 更新：[实际尺度预试报告](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000_W32实际网格尺度预试.md)、[六档 CSV](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000_W32实际网格尺度预试.csv)、三张中心网格截图、网格生成宏与 `index.md`、阶段计划、GPT 交接文档/状态 JSON。D 盘 Abaqus CAE、mesh-only INP、manifest、PNG 和脚本副本均在 `D:\PA12_Stage2\` 下。
- 下一步：评估细档求解资源并核查畸变分布；若 735,799 单元全局细网格不可承受，先通过 ROI 局部尺寸控制降低域外单元数，再运行固定 W32、`r=1` 的线弹性网格敏感性。

## [2026-09-28] experiment | TC2000 W32 seed 5.6 尺度补档

- 来源：W32 mesh-only 全局 seed 扫描的既有六档 INP，以及本次新增 seed 5.6；源 CAE 只读，所有网格均未赋材料、未施加载荷或求解。
- 方法：沿用 C3D10 自由四面体及同一 ROI 审计口径；max(|x|,|y|)≤14 mm，按十节点坐标均值分区，并用四角节点体积计算 h_eq。manifest 节点/单元数与 INP 相符，逐单元连接均可映射到节点表。
- 结果：seed 5.6 有 93,318 节点、55,731 单元、ROI 23,401 单元；ROI h_eq P10/P50/P90=0.626010/0.729312/0.869827 mm，角边 P50=0.787563 mm，过渡带 P50=0.751365 mm。全七档中更接近 0.78/0.62/0.50 mm 目标的粗/中/细候选为 5.6/3.2/0.6，但粗/中 ROI 尺度区间重叠约 0.107 mm；保留分布分离度更好的 6.4/1.2/0.6 作为待质量核查的诊断序列。
- 数据质量：初次 seed_1p2 INP 的 13 个单元引用不存在的节点标签 0，已排除；同 seed seed_1p2_verified 的节点/单元数相同且无缺失引用，纳入尺度表。
- 判定：全局 seed 与 ROI 实际尺度非单调；mesh-only 尺度映射已扩展，但未检查单元畸变/求解稳定性，不构成网格收敛或材料/几何结论。
- 更新：[预试报告](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000_W32实际网格尺度预试.md)、[尺度 CSV](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000_W32实际网格尺度预试.csv)、阶段计划、交接文档/状态与 index.md。
- 下一步：检查 6.4/1.2/0.6 mm 三档的网格畸变位置和严重度，评估 735,799 单元细档资源后再决定是否建立同口径线弹性敏感性求解。

## [2026-09-28] experiment | TC2000 W32 R=1 实际网格尺度敏感性

- 来源：W32 中心平台候选及 g43 实际尺度网格；G44 datacheck、G45 新增网格的 Abaqus 文件；H1.2 复用既有 G36/G37 基准。源 STEP 保持只读。
- 方法：对 6.4/1.2/0.6 mm 网格完成 datacheck 并将 `WarnElemDistorted` 单元映射至输入卡节点坐标；固定 `r=1`、临时正交线弹性卡、载荷和中心 ROI，按积分点 `IVOL` 加权计算场指标。H1.2 节点/单元拓扑与 G36 基准一致，故复用 ODB，不重复求解。
- 结果：实际 ROI `h_eq` P50 为 `0.8829/0.6475/0.4925 mm`；畸变单元数为 `1,526/1,136/1,844`，中心 ROI 质心均为 0。`PrimaryScore` 相对 H1.2 为 `+11.14%/0/−2.22%`，`G_transition` 为 `2.35075/2.55630/3.20402`，细档相对 H1.2 增加 `25.34%`。两新增求解均正常完成，0.6 mm 案有 1 条一般分析 warning，无数值 warning、负特征值或错误。
- 判定：中心均值变化较小不代表整体收敛；过渡带指标仍明显随网格变化。结果仅支持网格敏感性诊断，不支持材料塑性、断裂、DIC/VFM 或设计排名。
- 更新：[敏感性报告](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000_W32实际网格尺度敏感性.md)、[汇总 CSV](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000_W32实际网格尺度敏感性.csv)、三档中心 LE11 截图、[复现宏](Agents/PA12双轴试样仿真/验证/run_tc2000_w32_mesh_sensitivity_r1.py)、`index.md`；汇总 CSV 副本已放入 `D:\PA12_Stage2\g45_tc2000_w32_actual_mesh_sensitivity_20260928\mesh_sensitivity_summary.csv`。
- 下一步：改善 `14–24 mm` 外缘带畸变四面体并针对 `G_transition` 做局部网格敏感性；先预登记指标容差，再复算。完整阶段限制与执行指针见[PA12 总目标与阶段计划](Agents/PA12实验数据处理/处理记录/PA12总目标与阶段计划.md)。

## [2026-09-28] experiment | S18 Linear 与 Voce-I 双域窗口对照

- 来源：S18_XY_2 的 126 帧 DIC—力合并场、既有有限变形 J2 Linear 结果；新增 Voce-I 配置和拟合产物。原始 JPG、DAT、Press 力表未修改。
- 方法：固定 `ν=0.375`、厚度工作值 `1 mm`，完整 Job ROI 主域与 DIC subset 内缩敏感性域分别固定各自阶段1 E；对 `000003–000063/000094/000125.jpg` 的 50/75/100% 窗口拟合 Voce-I。内缩域沿用完整 Job ROI 机器力，只作独立积分域敏感性。
- 结果：六窗均收敛、Jacobian 秩均为 3/3，但条件数 `7.58×10⁷–2.62×10⁸`；`Q、b` 均趋近零，`Y₀` 与同域 Linear 差小于 `4.5×10⁻⁷ MPa`，拟合 RMS 差小于 `2.5×10⁻⁹ N`。四份逐帧 CSV 各 126 行，照片/时间键、外虚功与同域 Linear 相同，全部数值有限。
- 判定：当前 S18 窗口数据不能区分 Voce-I 与 `H≈0` 的 Linear 响应，也未识别可发布的塑性硬化参数。完整 Job ROI 覆盖率 `89.1147%` 仍需复核；物理同步、坐标与边界虚位移证据未闭合，参数及代理模型标签不放行。
- 更新：[S18 Linear/Voce-I 交接结果](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、机器状态 JSON、`index.md`；新增[50%配置](configs/pa12_finite_j2_s18_voce_i_50pct.json)与[75/100%配置](configs/pa12_finite_j2_s18_voce_i_75_100pct.json)及两域逐帧工件。
- 下一步：优先核实 S18 Job ROI 支持缺口、物理时间同步、机器—DIC 轴映射和单位虚位移边界条件；这些门槛通过后再扩展同窗硬化模型比较。

## [2026-09-28] experiment | TC2000 W32 过渡网格与 C30 几何候选

- 来源：W32 源 STEP 派生 CAE、G46 过渡边清单、G47 局部网格、G48/G49 datacheck、G50 R1 线弹性场，以及 G51 C30 源 STEP 布尔几何回归；源 STEP 保持只读。
- 方法：审计坡面/相邻边，比较全局 1.2、坡面局部 0.4/0.2 和边界 0.4+坡面 0.2 mm 网格；按固定 ROI 与 IVOL 口径后处理 G50；另将中心平台改为 30 mm、外半宽保持 16.5025 mm，执行 C30 几何回归。
- 结果：分级网格共 341,067 个 C3D10，datacheck 报告 1,373 个畸变单元，其中中心 ROI 0、过渡带 1,363；最小质量值 `7.40×10⁻⁸`、最小角 `0.0763°`。G50 R1 求解完成，`PrimaryScore=0.06926335`、`G_transition=2.57576`，材料仍为暂定线弹性卡。G51 C30 中心厚 1.5 mm、名义平台边长 30 mm、过渡宽 1.5025 mm、总包络与源 STEP 相同，15 项几何回归全部通过。
- 判定：局部/分级网格没有消除过渡带质量问题，G50 中心指标不用于网格收敛或设计排序；C30 仅通过几何级门槛，尚未划网格、加载或求解。竖直 Datum 不是实物打印方向验证，当前无 C30 加载比结果。
- 更新：[W32 过渡网格与 C30 几何报告](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000_W32_过渡网格诊断与C30几何候选.md)、[C30 几何回归](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000_C30几何回归.csv)、截图、manifest、`index.md` 与阶段计划。C30 CAE、日志和几何宏副本在 `D:\PA12_Stage2\g51_tc2000_c30_taper_geometry_20260928\` 与 `D:\PA12_Stage2\tools\`。
- 下一步：对 C30 做几何特征定位的网格预试和 datacheck，重点审查微边及过渡带质量；通过后再建立竖直 `r=0.5/1/2` 同口径工况。正式排名仍依赖经验证的材料、打印方向、夹具边界及 FE–DIC/VFM 证据。

## [2026-09-28] experiment | TC2000 C30 全局与局部网格 datacheck

- 来源：G51 C30 派生几何、G52 全局 H1.2 网格、G53 全局 R1 datacheck、G54 C30 B-rep 边清单、G55 局部播种网格与 G56 局部 R1 datacheck。源 STEP 未修改。
- 方法：C3D10 自由四面体；全局方案 seed `1.2 mm`。局部方案在 192 条坡面边播种 `0.2 mm`、256 条上下边界边播种 `0.4 mm`；两组均以相同暂定正交线弹性材料、竖直坐标映射、四端运动学耦合和 `ΔX=ΔY=0.05 mm` 执行 datacheck。对畸变清单按 C30 实际过渡外半宽 `16.5025 mm` 重新分区。
- 结果：G52 有 `149,182` 个单元和 `1,083` 个畸变单元（`0.7260%`），中心 ROI 质心 0、包围盒交叠 3，过渡区质心 1,082。G54 共 976 条边，辨认出 192 条坡面候选边、8 条内边界边、248 条外边界候选边及 8 条 `0.0025 mm` 微边。G55 局部方案增至 `349,329` 个单元（`+134%`）；G56 有 `4,428` 个畸变单元（`1.2676%`），全部在 C30 过渡带，中心 ROI 质心和包围盒交叠均为 0。局部网格质量虽略改善最差质量/角度，仍有 4,361 个质量值低于 `0.02`、2,943 个最小角低于 `10°`；未提交结构求解。
- 判定：C30 几何回归通过，但全局与局部网格质量均不放行；局部播种降低中心邻接风险的同时恶化畸变比例并大幅增加单元数。没有 C30 应力/应变场或加载比分析结果。
- 更新：[W32 过渡网格与 C30 几何报告](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000_W32_过渡网格诊断与C30几何候选.md)、全局/局部网格截图、G53/G56 datacheck manifest、失真单元 CSV/JSON、G54 边清单，以及 C30 网格、边清单与 datacheck 宏。完整 Abaqus 工件位于 `D:\PA12_Stage2\g51_tc2000_c30_taper_geometry_20260928\`、`g52_tc2000_c30_mesh_probe_20260928\`、`g53_tc2000_c30_r1_datacheck_20260928\`、`g54_tc2000_c30_transition_edge_inventory_20260928\`、`g55_tc2000_c30_transition_mesh_20260928\`、`g56_tc2000_c30_local_r1_datacheck_20260928\`。
- 下一步：在只读源 STEP 的派生副本上检查平面过渡连接和微边与畸变网格的关系；新的几何候选须先过 B-rep 与 datacheck 质量门槛，再进入竖直 `r=0.5/1/2` 分析。正式材料、打印方向、夹具边界和 FE–DIC/VFM 证据门槛保持不变。

## [2026-09-28] experiment | S18 全采集候选时轴虚功诊断

- 来源：S18 原始 JPG/DAT、现行 Press 力表及候选照片—力索引；原始 JPG、DAT、Press 表保持只读。
- 方法：在既有 `000003–000128.jpg` 映射锚点上以 `0.020024 s/frame` 向后延伸，新增 `000129–000234.jpg` 106 帧；使用完整 Job ROI 主域，并按用户确认的 DIC subset 内缩域独立敏感性口径运行有限变形诊断。
- 结果：总计 232 帧，9,312 个固定共同 DIC 点；前 126 帧可复现现有力索引，新增候选帧完成双域虚功计算。Job ROI 支持率 `89.1147%`；延伸段 X/Y 残差 RMS `10169.42/10414.88 N`，远高于此前区间的 `1091.64/1134.01 N`。抽查 `000125/000128/000129/000234.jpg` 未确认中心裂纹。
- 判定：向后延伸的帧时轴未经相机时间戳或共同触发证实，不能把后段当作已同步材料响应；外功骤降点也不是照片确认的断裂点。完整 Job ROI 为主域，subset 内缩域仅作独立敏感性；不发布参数或代理模型标签。
- 更新：[S18 候选时轴诊断报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S18全采集候选时轴虚功诊断.md)、[候选时轴配置](configs/pa12_finite_vfm_biaxial_s18_full_capture_candidate.json)、照片—力索引及双域逐帧 CSV/曲线、`index.md` 与 GPT 交接状态。
- 下一步：继续查找相机触发/控制器时间戳等独立共同时间基；若无记录，不将算法复现当作物理同步证明，并优先转向具备独立同步记录的实验批次。

## [2026-09-28] experiment | S18 配置同步源只读复核

- 来源：S18 图像目录和 `configs/pa12_rotated_batch.json` 指向的 Press 工作簿；原始文件保持只读。
- 方法：枚举 S18 目录非 JPG/DAT 旁文件，并检查工作簿可见/隐藏表、定义名称、时间列和相机/触发/帧号相关文本字段。
- 结果：目录旁文件为 `Job.m2inp`、`xy_2.mti`、`xy_2.vfm`。工作簿有 `Pos/Speed/Press` 三张可见表，各 4,679 条数据记录；Press `T` 覆盖 `0–4.685 s`，中位步长 `1 ms`，含 7 个 `2 ms` 间隔。未发现相机时间戳、触发、帧号或日期型字段，也未发现隐藏表或定义名称。候选末帧距力记录末端 `9.456 ms` 的计算正确。
- 判定：现有本地 S18 目录和关联工作簿没有独立相机—机台共同时间基证据。既有 126 帧映射的数值复现与 106 帧延伸仍不能证明物理同步；正式参数/训练标签继续不放行。
- 更新：[S18 全采集候选时轴诊断](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S18全采集候选时轴虚功诊断.md)、总目标阶段计划、GPT 交接文档/状态、`index.md`。
- 下一步：继续推进其他现有可分析实验的自建 VFM 诊断；若要将 S18 升级为物理同步数据，需取得独立相机/控制器共同时间基或新的同步采集记录。

## [2026-09-28] experiment | TC2000 C30 微边、虚拟拓扑与内侧圆角诊断

- 来源：只读 TC2000 源 STEP、C30 尖角派生体、G57 微边审计、G59/G60 虚拟拓扑网格与 datacheck、G61–G63 同尺寸内侧 `R0.1` 几何/网格/datacheck；所有原生 Abaqus 工件保存在 `D:\PA12_Stage2\g57_tc2000_c30_microedge_source_audit_20260928\` 至 `g63_tc2000_c30_round_r0p1_datacheck_20260928\`。
- 方法：核对源 STEP 与 C30 的 8 条角点微边；在派生 C30 上尝试忽略微边的虚拟拓扑；另只对 8 条内侧过渡边加 `R0.1 mm`，保持名义中心平台 30 mm、厚度 1.5 mm 和过渡宽度 1.5025 mm，再用全局 seed 1.2 mm 的 C3D10 执行 datacheck。仅提交输入检查，不提交结构分析。
- 结果：微边在源 STEP 中已存在。虚拟拓扑方案有 `1,288/148,586` 个畸变单元（`0.8668%`），全部处于过渡带，中心 ROI 无包围盒交叠，但劣于尖角全局基线 `1,083/149,182`（`0.7260%`）。内侧圆角几何回归 11 项通过，但 datacheck 有 `1,947/149,524` 个畸变单元（`1.3021%`），其中 1 个包围盒触及 ROI。失真热点集中在 `r∞=15–15.5 mm`。
- 判定：虚拟拓扑与内侧 `R0.1` 均未通过网格质量门槛；几何回归通过不代表网格可用。没有 C30 结构场、竖直加载比、塑性、断裂、DIC 或 VFM 结果。
- 更新：[W32/C30 过渡网格报告](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000_W32_过渡网格诊断与C30几何候选.md)、[R0.1 几何截图](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000_C30_R0P1_geometry.png)、[R0.1 网格中心图](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000_C30_R0P1_mesh_center.png)、几何/网格/datacheck manifests 与失真单元清单、`index.md` 和阶段计划。Abaqus 原生 CAE/STEP/INP/ODB/DAT/MSG 与运行日志保留在 D 盘对应 G57–G63 目录。
- 下一步：聚焦 `r∞=15–15.5 mm` 的内侧过渡 B-rep 连续性与网格拓扑，用可解释的单因素方法检验过渡几何或网格方法；不重复微边忽略、内侧简单圆角或当前边集播种。只有 datacheck 网格质量通过，才进入竖直 `r=0.5/1/2` 场分析。

## [2026-09-28] experiment | S19 五种硬化律双域条件诊断

- 来源：S19_X_0.2 已有完整 Job ROI 自建有限变形 J2 数据；本轮对照五种硬化律各自独立的拟合摘要、逐帧 CSV、配置和输出。原始 JPG/DAT/力表未修改。
- 方法：对 `000002–000126.jpg` 的 125 帧峰前窗口拟合，并将全历程审计至 `000127.jpg`；固定 `ν=0.375`、厚度 `1 mm`，主域与 DIC subset 内缩敏感性域各自固定阶段 1 的 E。完整 Job ROI 为主结果域，内缩域独立计算且仍使用完整 ROI 机器合力。
- 结果：Linear、Ludwik、Swift、Voce I、Voce II 共 10 支诊断。主域 RMS 跨度 `0.001253 N`，内缩域 `0.000418 N`，相对约 `285.8/306.7 N` 残差均不足以区分本构；主域 DIC 覆盖率 `84.8667%`，需复核。逐模型数值见[双域比较报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S19有限变形J2五种硬化律双域比较.md)。
- 判定：Swift `n≈1`；Voce II 虽满秩但条件数高。内缩域不是自身边界外功闭合；复用帧—力索引不构成独立物理同步证明。当前不选择硬化模型，不发布正式材料参数或代理模型训练标签。
- 更新：总方法协议、GPT 交接文档/状态、`index.md`；保留五种模型独立配置和结果文件。
- 下一步：先闭合主 ROI DIC 支持与实物几何/有效截面、机器—DIC 有向坐标和同步证据、边界虚位移及内外虚功检查；这些门槛通过前不追加同一 S19 数据的拟合。

## [2026-09-28] experiment | C30 自由四面体 NON_DEFAULT 算法适用性

- 来源：TC2000 C30 尖角源几何、G59 忽略 8 条微边的虚拟拓扑几何、Abaqus 2025 `setMeshControls` 官方 API，以及 10 mm 立方体烟测模型。
- 方法：在同一 Abaqus 环境以自由四面体 `algorithm=NON_DEFAULT` 和 C3D10 对简单立方体作可用性对照；再对尖角 C30 与 VT8 C30 分别使用 seed `1.2 mm` 复测。C30 试验未提交结构分析。
- 结果：立方体生成 `4,926` 节点、`3,087` 单元；尖角 C30 与 VT8 C30 两次均未生成节点或单元。忽略 8 条既有微边仍不能使该算法在 C30 上工作。
- 判定：旧算法在当前环境可用，但与当前 C30 几何/拓扑组合不兼容；不对失败的 C30 网格做质量或力学解释，也不再重复该算法分支。
- 更新：[W32/C30 过渡网格报告](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000_W32_过渡网格诊断与C30几何候选.md)、[立方体烟测 manifest](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000_NONDEFAULT_tet_smoke_manifest.json)、`index.md`、阶段计划及 C30 网格预试宏。D 盘烟测/运行目录：`D:\PA12_Stage2\g64_nondefault_tet_smoke_20260928\`、`g64_tc2000_c30_nondefault_tet_mesh_20260928\`、`g65_tc2000_c30_nondefault_vt8_mesh_20260928\`。
- 下一步：审计 `r∞=15–15.5 mm` 的 B-rep 面与边拓扑、尺寸和相邻面连续性；依据审计结果选取新的几何级/网格级单因素测试。

## [2026-09-28] experiment | 源 STEP 薄面审计与 C30 VT24 网格

- 来源：G51 CAE 中未修改源件 `TC2000_SOURCE_LOCKED` 与 C30 派生件；VT24 网格 CAE/INP；G69 datacheck ODB/DAT。源 STEP 保持只读。
- 方法：对源件和 C30 同口径统计过渡带 B-rep 面/边；在 VT8 之外再忽略 8 个狭长面的 16 条长边，总计虚拟忽略 24 条边；维持 C3D10、默认四面体算法、全局 seed `1.2 mm`。G69 使用既有暂定材料、竖直坐标映射和四端运动学耦合，只提交 datacheck。
- 结果：源件/C30 均含 8 个面积约 `0.075 mm²` 的狭长面，每个面有两条 `0.0025 mm` 短边、两条约 `30 mm` 长边；指标一致至 `1e-8`。VT24 网格 `250,227` 节点、`151,253` 单元；datacheck 畸变数从 VT8 的 `1,288` 降至 `164`（`0.1084%`，下降 `87.3%`），全部在过渡带，ROI 质心和包围盒交叠均为 0。剩余 120 个在 `r∞=14–15 mm`，44 个在 `15–15.5 mm`；仍有 137 个质量值低于 `0.02`，最小角 `0.20273°`。
- 判定：源 STEP 狭长面是网格退化的重要促成因素；VT24 为目前最佳诊断网格，但 datacheck 仍有质量告警，不放行场求解、加载比比较或设计排名。没有 C30 结构场、塑性、断裂、DIC 或 VFM 结果。
- 更新：[W32/C30 过渡网格报告](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000_W32_过渡网格诊断与C30几何候选.md)、[VT24 网格中心图](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000_C30_VT24_mesh_center.png)、源/C30 B-rep 面边 CSV/manifest、VT24 mesh/datacheck manifest 与失真清单、`index.md` 和阶段计划。原生 Abaqus 工件保存在 `D:\PA12_Stage2\g66b_tc2000_c30_transition_brep_audit_20260928\`、`g67_tc2000_source_step_brep_audit_20260928\`、`g68_tc2000_c30_vt24_mesh_20260928\`、`g69_tc2000_c30_vt24_datacheck_20260928\`。
- 下一步：把剩余畸变单元映射到源/候选 B-rep 相邻面，随后仅对派生几何开展一个薄面消除或过渡面重构的单因素测试；质量门槛通过前不启动竖直 `r=0.5/1/2` 矩阵。

## [2026-09-28] experiment | S19 残差分解与支持域复核

- 来源：S19_X_0.2 自建有限变形 J2 完整 Job ROI Linear 100% 窗口逐帧虚功 CSV、125/126 帧 DIC—力索引及现有 Job Polygon 几何；原始 JPG/DAT/力表保持只读。
- 方法：分别按拟合帧 000002–000126.jpg 与全历程 000002–000127.jpg 重建全程共同 DIC 支持和相邻网格三角形；复核 ROI 交叠面积，并按 X/Y 方向分解拟合窗内外虚功残差。
- 结果：两段都得到 9,143 点、17,708 个三角形；三角面积总和与 Job ROI 交叠面积同为 572.295649542 mm²，相对 ROI 面积 674.346637572 mm² 的覆盖率 84.8666869%。000127.jpg 不改变支持网格。125 帧中 X/Y 残差 RMS 为 399.354535/62.185739 N；X 内功对机器力回归斜率 0.414790、截距 12.241 N、R²=0.997418。000126.jpg 的 X 内/外虚功为 503.759/1141.600 N。
- 判定：支持网格和三角交叠积分口径不能解释 S19 残差；X 向差距随载荷系统性增长，根因尚未确定。五种硬化律间的 RMS 差远小于残差，不继续用同一数据追加模型拟合；不发布正式参数或代理模型训练标签。
- 更新：S19 双域比较报告、GPT 交接文档/状态、index.md。
- 下一步：取得 S19 有效截面/厚度和 Job ROI 与受力截面的对应证据，核对机器—DIC 有向坐标、照片—力独立同步证据及边界虚位移；继续保持完整 Job ROI 主域和 DIC subset 内缩域独立敏感性。

## [2026-09-28] audit | S19 照片—力时间基来源核查

- 来源：S19 批处理配置、S19 处理报告、候选力源工作簿登记及现有照片—力匹配表；原始 JPG 与控制器工作簿保持只读。
- 方法：对照相机帧率来源、处理报告中的照片时间算法、有效力区间和设备 Pos 位移。
- 结果：当前配置关联 x-05-0.1 状态工作簿；相机 10 fps 是历史候选，原始相机元数据未找到。处理报告记载无可靠 EXIF，时间按帧号间隔归一化到力数据有效区间；有效照片频率 9.861155 Hz、区间 12.676 s。名义速度推算照片位移 2.5352 mm，Pos 设备位移 2.795 mm，差 0.2598 mm。
- 判定：力源文件具备配置关联，但没有独立相机时间戳/触发证据；帧—力表不是严格同步已证实。旧文件配对或 VFM_READY 标签只表示数据链路就绪，不构成物理同步验收。当前虚功残差仍不能归因于此时间差。
- 更新：S19 双域比较报告、GPT 交接文档/状态、index.md。
- 下一步：寻找相机原始时间戳或触发/同步记录；若不存在，则该数据继续作为候选同步条件诊断，并优先核实有效截面、ROI边界、方向映射和外功边界条件。

## [2026-09-28] audit | S19 力源工作簿复算

- 来源：S19 配置关联的状态工作簿 Press 表、S19 照片—力匹配 CSV；原始工作簿只读。
- 方法：按匹配表保存的照片时间和处理报告中的 X 基线/符号对原始 Press 双通道均值重新插值，并与 126 行匹配表逐帧比较。
- 结果：Press 表 14,735 行，时间 0–14.754 s，中位间隔 1 ms；X 力重算最大差 0.072 N，120/126 行精确到 1 μN。Y 通道依单轴配置归零。
- 判定：现有 X 力表与登记的控制器 Press 源序列及插值一致；该结果只证明力值来源链，不证明相机照片与力时间严格同步。相机时间仍由无 EXIF 的帧号区间归一化得到。
- 更新：S19 双域比较报告、GPT 交接文档/状态、index.md。
- 下一步：继续寻找相机原始时间戳/触发记录；取得前，S19 仅用于候选同步条件下的诊断，不放行正式识别。

## [2026-09-28] audit | S19 Pos—DIC 位移趋势与断裂末帧复核

- 来源：S19 配置关联工作簿 `Pos` 表、当前 126 行候选照片—力索引、完整 Job ROI 几何及共同 DIC 位移场；工作簿和原始 DIC/JPG 保持只读。
- 方法：按候选照片时刻插值 X1/X2_Pos，计算两夹头相对位移；在候选 `机器 X→DIC y/v` 映射下拟合 DIC 轴向位移梯度，并分别乘完整 Job ROI 长度与 DIC 支持跨度。只作运动趋势/尺度核对，不用于拟合材料参数或替代边界虚位移审查。
- 结果：完整 Job ROI/DIC 支持轴向跨度为 `65.847642/64.322214 mm`。断裂前 `000002–000126.jpg` 的 Pos—DIC 全 ROI 趋势回归 `R²=0.999585`、RMSE `0.014924 mm`，仿射尺度约 `1.7014`；`000126.jpg` Pos/DIC 全域趋势量为 `2.5183/1.520935 mm`。`000126→000127.jpg` Pos 突增 `0.2767 mm`，高于断裂前单帧中位/最大增量 `0.0204/0.0235 mm`；X 力同时由 `1141.6` 降到 `178.6 N`，DIC 趋势量仅增 `0.0128568 mm`。
- 判定：断裂前趋势与候选时轴相容，但 DIC 与机台绝对位移口径未闭合；末区间的 Pos 突跳与掉载同现，不能分辨断裂后夹头运动、真实断裂变形和帧时刻误差。没有独立相机时间戳/触发证据，严格同步仍未证实；这也不验证 VFM 外功边界位移。
- 更新：S19 双域比较报告、GPT 交接文档/状态、`index.md`。
- 下一步：寻找独立相机/触发时基，并核实 S19 实物标距、Job ROI 与加载边界关系及机器—DIC 有向坐标；保持完整 Job ROI 主域和 DIC subset 内缩敏感性，不再用同一 S19 窗口追加拟合，不发布正式参数或训练标签。

## [2026-09-28] audit | S19 Job ROI 相对可见试样边界复核

- 来源：S19 原始参考图 `000000.jpg`、Job 五点 Polygon、既有完整 Job ROI/DIC 支持叠加图；原图只读。
- 方法：把 Job Polygon 顶/底端线投回参考图，核对其与连续可见试样区域及可辨认夹持/加载接触线的位置关系。
- 结果：端线位于可见长条试样中段，未与可辨认夹持端/加载接触线重合；当前 ROI 是内部 DIC 域的图像证据增强。照片不能证明 Polygon 两侧覆盖完整承载宽度，也不能证明机台力等于内截面合力。
- 判定：使用机台力作为 ROI 内部截面合力只能作为依赖完整截面覆盖与准静态轴向力传递的工作口径；本轮没有重建牵引分布、没有假设均布应力，也没有改变完整 ROI 主域或内缩敏感性域。
- 更新：单轴几何证据缺口、GPT 交接文档/状态、`index.md`。
- 下一步：若要把 S19 外虚功升级为闭合结果，需补齐样件实测宽度/厚度、全截面覆盖与机器力传递/加载方向证据；在此之前保留为条件诊断，不发布材料参数或训练标签。

## [2026-09-28] audit | S19 掉载末端原图复核

- 来源：S19 原始 JPG 与 DAT 文件名序列、当前照片—力索引；原始文件只读。
- 方法：对照最后两张有力值配对照片 `000126/000127.jpg`，并检查其后 `000128/000129.jpg` 是否存在及其 DAT/力配对状态。
- 结果：目录有 130 张 JPG、128 份 DAT；`000127.jpg` 的 X 力为 `178.6 N`，画面仍有连续散斑试样、未见明确宏观断口。`000128/000129.jpg` 无 DAT/力值；分别出现试样纹理离开视场和模糊亮斑。
- 判定：`000127.jpg` 是最后力配对掉载照片，不是已确认断裂照片；后续原图提示末端显著光学事件，但无法确定断裂帧/时间。没有补配力值、重建 DAT 或将未配对图像纳入 VFM，严格同步未证实。
- 更新：S19 双域报告、单轴几何证据缺口、GPT 交接文档/状态、`index.md`。
- 下一步：若需判断具体失效时刻，需获得后续帧的控制器共同时间基或新增同步采集；现有数据继续只用 126 个配对帧，正式参数仍不放行。

## [2026-09-28] audit | PA12 论文式(2.19)符号复核

- 来源：本地《3D打印尼龙材料的双轴拉伸测试方法与力学性能》PDF 首页、印刷第 11–12 页；MinerU 标准解析及原页图；Abaqus 官方等向塑性材料说明。
- 方法：对照公式文本和原页图，核对参数页单位换算；检索精确题名、作者及宁波大学域名；只读检查论文关联目录和既有六份几何扫描 `.inp` 的材料卡状态。
- 结果：原页图确认式 (2.19) 为 `σy=σy0−H ε̄p`，参数同时给 `σy0=21 MPa`、`H=0.18 GPa=+180 MPa`。正 H 按字面对应软化，外推约 `ε̄p=0.1167` 时屈服应力为零，与正文“等向线性硬化”冲突。公开检索未找到可核验官方原文或勘误；论文关联目录未检出 `.inp`，六份既查几何扫描输入只有 provisional `*Elastic`、无 `*Plastic`。
- 判定：冲突已确认存在但来源未裁定。自建 VFM `Linear` 保持代码明示的正斜率 `σy=Y0+H ε̄p`，不宣称复现论文公式；不把论文 `H=180 MPa` 当实验识别值，不生成相关训练标签。完整 Job ROI 仍为主分析域，DIC subset 内缩域独立作敏感性。
- 更新：总体方法与防跑偏协议、GPT 交接文档/状态、`index.md`。
- 下一步：取得作者确认/正式勘误或其实际 Abaqus `*Plastic` 材料表后再裁定论文符号；在此之前继续按自建 VFM 已明示本构公式推进，不混用两域结果。

## [2026-09-28] experiment | TC2000 C30 过渡宽度与网格尺度筛选

- 来源：只读源 STEP `D:\PA12_Stage2\source_geometry_inspection\inputs\tc2000.step`；G82–G98 与 G100–G103 的几何、网格、datacheck manifest 与畸变位置审计。
- 方法：固定 C30 平台 30 mm、中心厚 1.5 mm、C3D10、自动 STAIR 虚拟拓扑；先扫描过渡宽 1.5025/2.0/2.25/2.5/2.75/3.5 mm，后固定 2.5 mm 比较 seed 1.2/0.8/0.6 mm。datacheck 使用临时线弹性卡，仅做输入检查。
- 结果：宽度 2.5 mm、seed 1.2 mm 在已测宽度中畸变数最低，为 125/147384；原始宽度 1.5025 mm 的最小质量值和最小角更好，指标存在权衡。固定 W2.5 后，H0.8 有 61/356348 个畸变单元（0.0171%），ROI 包围盒交叠 0；H0.6 升至 202/697029（0.0290%），质量指标也劣于 H0.8。
- 判定：C30/W2.5/H0.8/STAIR 是当前网格筛选候选，不是通过验收的分析网格。仍有 61 个 datacheck 畸变单元，未预登记质量容差；本轮未提交结构场求解，也没有竖直位移比、应变均匀性、塑性、断裂、DIC 或 VFM 结果。
- 更新：[筛选报告](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000_C30_过渡宽度与网格尺度筛选.md)、[数据 CSV](Agents/PA12双轴试样仿真/验证/2026-09-28_TC2000_C30_过渡宽度与网格尺度筛选.csv)、几何及网格截图、index.md 和[PA12 阶段计划](Agents/PA12实验数据处理/处理记录/PA12总目标与阶段计划.md)。Abaqus 原生工件和日志位于 D:\PA12_Stage2\g82–g98 与 g100–g103；源 STEP 未改写。
- 下一步：先为中心 DIC/VFM 目标预登记网格质量验收标准，并决定对 ROI 外残余畸变的处理规则；验收前不启动竖直 r=0.5/1/2 场分析。验收后再按竖直坐标做加载比筛选，并以实验/DIC/VFM 证据评价试样设计。

## [2026-09-28] experiment | S21 DIC subset 与 Job ROI 交集敏感性

- 来源：S21_X_20 的 DIC—力索引、首个有效帧 `000010.jpg`、Job Polygon 与既有完整 Job ROI 阶段 A 结果；原始 JPG/DAT/力表及 Job 文件保持只读。
- 方法：保持完整 Job ROI 为主域；将独立敏感性域定义为首帧 DIC 点云外接矩形与 Job Polygon 的交集。使用相同 36 帧、力序列、机器轴映射、中心厚度 `1 mm` 和固定 `ν=0.375`，结果写入隔离目录。
- 结果：交集敏感性域面积 `595.267671 mm²`，完整 ROI 面积 `617.689774 mm²`；阶段 1 `E` 从 `17419.148949` 变为 `16989.358627 MPa`（`−2.4673%`），两域相对 RMSE 均为 `0.048532`。阶段 2 分别只有 14/10 个候选点，低于 20 点门槛，未计算 `Y/H`。完整域/敏感性域最低 DIC 支持面积比为 `0.841189/0.872874`，均低于 `0.95`。
- 几何审计：S19 与 S20 的 Job Polygon 分别存在自交；现有多边形三角化面积与 Job 多边形有向面积不一致，相关全域积分暂不作为有效几何结论。原始 Job 文件未改写，修复口径待确认。
- 更新：[S21 独立敏感性报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S21_DICsubsetJobROI交集敏感性.md)、[Stage A 双域对照](Agents/PA12实验数据处理/VFM自建/汇总/PA12自建VFM阶段A完整JobROI与DICsubset内缩域网格拓扑复算对照.md)、自建 VFM 裁切几何/逐组 runner、定向测试、`index.md`。
- 下一步：在 S19/S20 Job Polygon 几何意图未核实前，不用这两组 Stage A 主域结果作参数比较；继续检查其他 VFM 放行门槛，不发布正式材料参数或训练标签。

## [2026-09-28] experiment | S19/S20 Job ROI 自交门禁复核

- 来源：原始 S19/S20 `Job.m2inp` 的 `<Shape>` 五点序列；文件只读。
- 发现：非相邻边在约 `(462.0001,184.0084) px` 与 `(471.0071,222.0002) px` 相交。旧耳切器未拒绝自交轮廓，三角片绝对面积和不等于有向轮廓面积，不能解释为有效 ROI 面积。
- 修改：自建 VFM Polygon 三角化入口新增自交边拒绝；新增两组真实顶点回归测试。未删除控制点、未重建 ROI、未重算单轴参数。
- 验证：`python -m pytest tests/test_pa12_finite_kinematics.py -q`，18 passed；测试同时覆盖既有简单凹多边形裁切行为。
- 扩展验证：运动学/J2 相关测试 93 passed；全仓 `python -m pytest -q` 为 287 passed。
- 更新：[S19/S20 ROI 复核](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S19-S20原始ROI自交与积分门禁复核.md)、[阶段 A 对照](Agents/PA12实验数据处理/VFM自建/汇总/PA12自建VFM阶段A完整JobROI与DICsubset内缩域网格拓扑复算对照.md)、[总目标计划](Agents/PA12实验数据处理/处理记录/PA12总目标与阶段计划.md)、[GPT 交接](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、`index.md`。
- 后续：取得 MatchID 控制点定义或实物几何依据后，才可建立独立派生 ROI 并重算 S19/S20；其余可用实验与 G0/G1 工作继续推进。正式材料参数仍未放行。

## [2026-09-28] experiment | S19 make_valid_linework 双域重算

- 来源：S19_X_0.2 原始 Job Shape、126 帧 DIC—力合并索引与首帧 DIC 点云；原始 Job、JPG、DAT 和力表只读。
- 方法：按用户明确授权，仅对 S19 采用 Shapely 2.1.2 `make_valid(method="linework")`；完整 Job ROI 主域保留全部两个面片，DIC subset 外接框与修复后 Job ROI 的交集作为独立敏感性域。S20 未加修复配置。
- 结果：主域面积 `674.346698 mm²`、DIC 交集面积 `637.609461 mm²`；两域均为 126 帧，最低支持率 `0.848619/0.897514`。固定 `ν=0.375` 的 `E=5517.118/5389.308 MPa`（变化 `−2.32%`）；`Y` 从 `7.197` 变为 `−38.561 MPa`，`H` 从 `21665.929` 变为 `85333.666 MPa`。参数对域高度敏感，主域状态仍为 `SELF_VFM_REVIEW_REQUIRED`，敏感性域仅作对照，不发布参数或训练标签。
- 更新：[S19 双域重算审计](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S19_make_valid_linework双域重算审计.md)、[Stage A 对照](Agents/PA12实验数据处理/VFM自建/汇总/PA12自建VFM阶段A完整JobROI与DICsubset内缩域网格拓扑复算对照.md)、[自交几何历史审计](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S19-S20原始ROI自交与积分门禁复核.md)、方法协议、GPT 交接与状态 JSON、`index.md`。
- 验证：`python -m pytest -q`，`287 passed`。S20 原始几何仍待独立授权/边界证据，新流程保持阻断。

## [2026-09-28] refactor | PA12 总目标拆分与 Stage 2 独立性门禁

- 来源：PA12 总目标/阶段计划、`tools/run_pa12_self_vfm.py`、现有 Stage 2 虚功独立性审计；原始实验资料未修改。
- 结论：旧 Stage 2 先由 Press 力计算名义等效应力并拟合硬化曲线，再将拟合应力缩放回同一 Press 力；矩形 ROI 下内部虚功满足 `Wint=F·σeq,fit/σeq,force`，残差不是独立平衡检验。相关数值仅保留为力耦合曲线诊断。
- 目标调整：拆成软件无关 VFM 数值内核验收、现有实验诊断/条件参数候选、正式 PA12 参数发布三层。MatchID 不可接入不再阻断项目；物理证据不足仅阻止正式发布。
- 更新：[总目标与阶段计划](Agents/PA12实验数据处理/处理记录/PA12总目标与阶段计划.md)、[GPT 交接文档](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、`index.md`。
- 下一步：复用解析/合成已知解验证独立 VFM 内核与外功定义；逐项审查实验外功是否独立于待识别本构，再推进可审计诊断和候选参数，不重复旧 Stage A 或已完成窗口拟合。

## [2026-09-28] experiment | 单位伸长虚场边界外功条件

- 来源：`tools/pa12_finite_j2.py` 的参考构形虚功积分、现有解析常 Piola 应力/边界牵引测试、PA12 四路 Press 与 Pos/夹爪证据边界。
- 方法：实现 `integrate_external_virtual_work_from_nodal_forces`，计算全部边界节点 `Σ f·v*`，其中 `v_x*=(X/Lx,0)`、`v_y*=(0,Y/Ly)`。解析矩形回归分别验证满足零其他边界功时 Press resultants 与广义外功一致，以及顶边自平衡切向力导致两者不等。
- 结果：定向解析测试 4 passed；满足条件的例子为 X/Y=`12/15 N`，反例中右边 X Press 合力=`12 N` 而全边界 `Wext,x=14 N`。再对默认 6×6 非均匀 FE 的全体边界节点反力逐帧求和，25 帧与原右/上边合力最大差 `1.124×10⁻⁹ N`，自由节点平衡残差最大 `3.180×10⁻⁹ N`。全仓 `python -m pytest -q` 为 290 passed。外功需计入全部受力边界，不能只凭单边合力宣称闭合。
- 限制：PA12 工作簿仅有通道合力，未提供分布边界节点力；机器—DIC 有向坐标及各边界虚位移也未全部独立确认。新增函数目前用于离散外功定义/基准验证，不自动重建实验牵引或升级物理证据状态。
- 更新：[Stage 2 虚功独立性审计](Agents/PA12实验数据处理/VFM自建/汇总/PA12Stage2现行实现与虚功独立性审计.md)、[总目标计划](Agents/PA12实验数据处理/处理记录/PA12总目标与阶段计划.md)、[GPT 交接文档与状态](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、`index.md`。
- 下一步：审查四路 Press、Pos 和夹爪图像运动证据对单位虚位移加载边界及其余边界零功条件的支持；无法证明时继续输出条件化外功候选与 DIC 内场诊断，不以合力分布猜值。

## [2026-09-28] compile | PA12 项目全景与总控指令

- 来源：当前 Obsidian 的 index.md、log.md、PA12 总目标与阶段计划、总体方法与防跑偏协议、GPT 交接文档及状态 JSON；第一阶段盘点报告；Stage 2 虚功独立性审计；S19/S20 ROI 门禁与 S19 双域重算报告；XY-0.1-02 DIC 导出审计及三项相关 Codex 任务的最新进展。
- 更新：wiki/PA12项目全景与总控指令.md、index.md。
- 结论：汇总项目目标、工作区、关键时间线、数据与文献处理、DIC/力映射、VFM/J2、Abaqus/FE–DIC、机器学习准备及证据边界；补入 S19 make_valid 双域数值结果、旧 Stage 2 循环依赖审计、独立边界外功接口，以及三项任务的当前状态。正式参数、最终设计、网格收敛、FE–DIC 和机器学习训练仍未放行。
- 待验证：VFM 端到端独立节点力外功基准；S20 自交几何继续阻断；XY/XZ 样件身份、坐标、字段、导出版本和同步证据；G0/G2 网格质量门槛；正式材料参数及独立验证依赖。

## [2026-09-28] experiment | PA12 应力—应变图事件标记复核

- 来源：9 组现存应力—应变 CSV、批量处理清单中的有效终点状态、`tools/pa12_sync.py`。
- 结果：图表同时保留原始采样淡线和 5 点显示平滑；峰值及已确认掉载终点按原始 CSV 值定位。S16 原始末帧 X/Y 名义应力为 `5.077/4.209 MPa`，未被平滑曲线的约 `37 MPa` 终点替代；S15、S23 的断裂照片缺少可配对完整场/力值，不标为已确认断裂。
- 影响：只重绘 9 张 PNG；CSV、VFM 力值和原始 JPG/DAT/XLS 未改。
- 更新：应力—应变绘图代码与回归测试（`tests/test_pa12_sync.py`：42 passed）、应力—应变图、S16 分析说明、总目标、GPT 交接、`index.md`。
- 下一步：继续逐实验审查外虚功边界条件与 DIC 内场积分；正式参数仍需几何、坐标、边界和独立验证门槛。

## [2026-09-28] audit | S15–S18 候选等双轴 Press 四通道统计

- 来源：configs/pa12_rotated_batch.json 中登记的四个候选双轴工作簿，Press 工作表；候选关联尚未证明为对应样件的正式原始记录。原始工作簿只读。
- 方法：各通道减去首个采样值、不翻转符号；在信号峰值 5% 以上区间计算对置通道相关/差值 RMS，并以 X/Y 对置均值计算跨轴相关、相对差中位数/P95 和峰值差。5% 是分析窗口，不是验收阈值。
- 结果：对置相关系数为 0.99830781–0.99999477，对置差值 RMS 为峰值的 0.17249%–2.67475%；跨轴相关为 0.99968137–0.99997230，峰值相对差为 0.28016%–2.41241%。S17 跨轴相对差 P95 为 10.62030%。逐组统计见[边界载荷说明](Agents/PA12实验数据处理/MatchID_VFM准备/PA12_VFM边界载荷说明.md)。
- 判定：保留用户确认的名义等双轴试验前提，不按瞬时通道差异改标为非等双轴，也不采用未预登记的阈值判定通过/失败。统计不证明样件—工作簿映射、照片同步、机器—DIC 有向轴或其他边界零虚功；实验外虚功仍为条件候选。完整 Job ROI 为主域，DIC subset 内缩域仅作独立敏感性并沿用完整 ROI 合力。
- 更新：总体方法与防跑偏协议、GPT 交接文档/状态、边界载荷说明、index.md。
- 下一步：继续 DIC 内场虚功和应变测度诊断；若要升级实验外虚功结论，再取得样件—工作簿对应、独立时间基、机器—DIC 方向/符号和其余边界运动证据。

## [2026-09-28] audit | PA12 Press/Pos 边界运动证据量化

- 来源：`configs/pa12_rotated_batch.json` 关联的只读 Press/Pos 工作簿、既有试验加载区间及 S16 夹爪图像追踪报告。
- 结果：活动轴 Press 两路 RMS 差为峰值平均力的 `0.16%–2.70%`，最大差 `4.78–71.86 N`；Pos 两侧位移幅值不对称率 `0.08%–13.78%`。S16 图像四夹爪均向外，候选 Pos/图像幅值差 `1.7%–5.1%`。
- 判定：仅支持候选记录中通道/运动近似对称；工作簿—样件身份、相机—力严格同步、单位虚位移边界及其余边界零功均未证实。外虚功保持条件候选，不恢复牵引分布，不发布正式材料参数。
- 更新：Stage 2 虚功审计、GPT 交接文档/状态、`index.md`。
- 下一步：继续输出可追溯的 DIC 内场虚功和条件外功残差；针对正式闭合补齐可追溯样件/夹具边界和独立时基证据。

## [2026-09-28] experiment | S19 DIC 运动学测度复核

- 来源：S19 正式 DIC—力索引、六个配对合并场及原始 DAT；原始 JPG/DAT/Job 保持只读。
- 方法：比较 DAT 的 Exx/Eyy/Exy 与 x/y/u/v 局部位移拟合重建的 Euler–Almansi 应变；拟合半径 15 px（1.27119 mm），与既有 S16 复核保持同一设置。逐帧覆盖 000002、000003、000015、000064、000126、000127。
- 结果：6 帧各 9,144 点；Exx/Eyy/Exy 相关系数范围分别为 0.7782–0.8590、0.6779–0.7245、0.7535–0.7989。Exy 张量 RMSE `0.000960–0.001334`，工程剪切对照 RMSE `0.002219–0.002943`；gamma 与主方向角最大差 `0.9444°`。支持 Exy 张量剪切和 gamma 主方向角的经验解释，但不证明 MatchID 内部滤波语义、严格同步或边界虚功闭合。
- 更新：总体方法与防跑偏协议、GPT 交接文档/状态、`index.md`。
- 下一步：按同一测度交叉核验方法逐组审计 S20–S22；外虚功继续标记为条件候选，正式参数不放行。

## [2026-09-29] experiment | S15–S22 DIC 运动学测度代表帧复核

- 来源：S15–S22 的原始 DAT、逐帧合并场及正式 DIC—力索引；S16 复用既有六帧审计。原始 JPG/DAT/Job/力表只读。S15 索引为 GBK 四列文件，merged 场为 UTF-8；按照片编号关联现有文件，没有改写源文件或配置。
- 方法：以 15 px 局部位移拟合半径重建 Euler–Almansi 张量应变，比较 DAT Exx/Eyy/Exy 的空间相关和 RMSE；gamma 对比应变主方向角。S15 取首末两帧，S16–S22 各取六帧；对 S22 的 001776/001784 另外比较 7.5/15/30 px 半径。该抽样检查不是全帧分析或 MatchID 滤波复现。
- 结果：S16–S22 抽样帧的 Exy 张量剪切 RMSE 均低于工程剪切对照；S15 两端帧工程剪切 RMSE 略低、但差值很小，不能决定字段约定。若干 Job 中 gamma 与导出分量计算的主方向角在数值精度内一致，不能把 gamma 当作独立跨组校验。S22 001784 的 Exy 相关系数随半径为 `0.044/−0.604/0.295`，张量 RMSE 为 `0.09931/0.08806/0.01929`，显示局部支持尺度敏感；尾段失配在 001744/001760 等仍有约 1.35 kN 载荷的帧已出现，不限于掉载末帧。
- 判定：该结果用于标记场测度约定和支持尺度的不确定性，不据此判定 PA12 材料行为，不改变完整 Job ROI 主域与 DIC subset 内缩独立敏感性，也不宣称严格同步、外虚功闭合或参数识别通过。
- 更新：总体方法与防跑偏协议、GPT 交接文档/状态、`index.md`。
- 下一步：停止重复已完成的参数窗口拟合；继续闭合实物厚度/ROI 包含、机器—DIC 有向坐标、独立相机时间基和边界虚位移证据，再评估现有逐帧 VFM 诊断能否进入条件参数验证。

## [2026-09-28] audit | PA12 Stage 2 均匀应力近似与局部虚功对照

- 来源：S15/S16/S18/S22 Stage A 内外虚功 CSV 与结果 JSON、用户授权的 S19 `make_valid_linework` 派生结果、S16 局部有限变形 J2 逐帧虚功 CSV；原始 JPG/DAT/XLS 只读。
- 方法：按 Stage 2 模型输出非空帧，比较逐点积分系数与 DIC 支持域均值应变系数；另按照片名连接 S16 两份逐帧结果，复核相同外力和残差差异。
- 结果：5 个分支共 1,384 个帧—方向记录；支持域系数差中位数 `0.018%–0.353%`，最大值 `0.222%–28.827%`；完整 Job ROI 支持率 `84.75%–92.19%`。S16 配对 222 帧的外力最大差 `0 N`；旧 Stage 2 与局部 J2 的内虚功差 RMS 为 X/Y `240.823/235.352 N`。
- 判定：低支持域积分系数差不等于应力场均匀；完整 ROI 基线差包含未支持区域影响。S16 局部 J2 残差较低不是独立验证，因为算法/拟合窗口不同且共用 Press 外力。正式材料参数与真实外功闭合仍未放行。
- 更新：[定量审计](Agents/PA12实验数据处理/VFM自建/汇总/PA12Stage2均匀应力近似与局部虚功对照审计.md)、[逐组 CSV](Agents/PA12实验数据处理/VFM自建/汇总/PA12Stage2均匀应力近似定量对照.csv)、总目标、GPT 交接文档/状态、`index.md`。
- 下一步：在不丢失断裂事件信息的前提下，将 S15 不完整 `000285.jpg.dat` 排除于正式 DIC/VFM 积分；以 `000284.jpg` 作为最后完整场帧，再审查 S23 力记录早于视觉断裂结束等数据资格问题。

## [2026-09-28] audit | S15 DAT 门禁与 S23 断裂—力记录边界

- 来源：`configs/pa12_rotated_batch.json`、S15 帧力索引/DIC 合并索引/DAT 审计/Stage A 虚功表、S23 原始 Press 工作簿和断裂前后照片；原始资料只读。
- 结果：S15 `000285.jpg` 已在配置排除；四类派生索引均为 284 帧并止于完整场 `000284.jpg`。S23 Press 工作簿虽为 `.xls` 后缀，实际为 OOXML/XLSX 容器；只读解析得到末时刻 `15.347 s`，最后有力照片为 `001528.jpg`（Y=`1259.37 N`）。`001545/001546.jpg` 仍连续，`001547.jpg` 首次明确断开；该断裂时刻无力记录，不外推、不补造。
- 判定：S15 断裂照片保留作事件证据但不进入正式 DIC/VFM；S23 只能保留断裂前有力区间，不能生成包含断裂载荷的完整闭合结果。两者均不阻止其他合格实验的条件性局部 VFM 诊断。
- 更新：S23 处理报告、Stage 2 均匀应力近似审计、GPT 交接文档/状态、总目标、`index.md`。
- 下一步：继续对输入合格的实验推进局部有限变形 VFM 逐帧诊断；保持物理门槛和正式参数发布门禁，不复拟合旧 Stage 2。

## [2026-09-29] audit | S15–S18 完整 Job ROI 仿射单位虚位移边界核算

- 来源：四组 `pa12_finite_vfm_biaxial` 配置、各自 `Job.m2inp` Shape、有限变形 VFM 虚场长度与机器轴映射；原始 Job/DIC/力表只读。
- 方法：读取 Job Polygon 后按机器 X=`DIC y/v`、机器 Y=`DIC x/u` 重排，检查 ROI 是否为轴对齐矩形及其 X/Y 跨度是否等于虚场归一化长度。
- 结果：S15/S16/S17/S18 的 `(L_X,L_Y)` 分别为 `(28.775656,28.775656)`、`(27.906880,27.209208)`、`(28.075944,27.638624)`、`(26.763984,26.326664) mm`；四者均为机器坐标轴对齐矩形，两方向相对边虚位移差均为 1。对完整 Job ROI，按用户确认的纯轴向机器合力边界前提，合力可直接给出仿射虚场外功，不需要重建牵引分布；subset 合力沿用只作为内场敏感性对照。
- 判定：此项关闭 S15–S18 的 Job 几何—仿射虚场归一化代数关系核算；不证明 Job 与真实减薄区/受力边配准、机器—DIC 正负号、实际 ROI 力路径或相机—力物理同步。实验外虚功仍为条件候选，正式参数/训练标签不放行。
- 更新：GPT 交接文档与状态、`index.md`。
- 下一步：核实逐件 ROI/1 mm 厚度物理位置、机器—DIC 有向坐标和独立相机/控制器时基；单轴 Job Polygon 另行核算边界虚场关系。不重复本轮全域几何核算或既有拟合窗口。

## [2026-09-29] audit | S19–S22 单轴完整 Job ROI 仿射边界虚位移核算

- 来源：S19–S22 有限变形 VFM 配置、`pa12_self_vfm.json` 中 S19 几何修复授权及各自原始 `Job.m2inp` Shape；原始 Job/DIC/力表只读。
- 方法：按每组机器轴映射重排多边形；比较加载轴包围盒长度与虚场长度，并逐边计算 `q/Lq` 的端边内变化。没有接受阈值，不把小幅非零变化当成自动通过。
- 结果：S19/S20/S21/S22 的加载轴长度分别为 `65.847642/59.580106/60.436324/44.333156 mm`。四组包围盒跳变量均为 1；S19 授权 linework 修复得到两个连通片，主片两条横向短边场变化约 `0.001276/0.001287`；S21 为 `0.004354/0.007257`；S22 为 `0/0.003759`。S20 原始 Polygon 自交且当前未授权修复，仍不作有效域积分。
- 判定：现用 `q/Lq` 虚场并非在 S19/S21/S22 的实际 Job 端边处处恒定；仅有机器合力不能精确给出该场的边界虚功。该结论限定于“当前虚场—Job Polygon”关系，不否定用户给定的机器合力前提；S20 维持阻断。外虚功和既有参数继续标记为条件诊断，完整 Job ROI 主域及 subset 独立敏感性不变。
- 更新：[单轴边界虚位移报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12单轴完整JobROI仿射边界虚位移核算.md)、GPT 交接文档/状态、`index.md`。
- 下一步：在有效的 S21/S22 Job Polygon 上验证端边恒为 0/1 的边界适配虚场并积分内部功；复核 S19 修复连通片的物理意图；S20 等待 ROI 意图核实或修复授权。同步、物理 ROI/厚度配准和有向坐标仍未闭合。

## [2026-09-29] experiment | S15 全历程逐帧运动学质量复核

- 来源：S15 有效 DIC—力索引、全程共同网格合并场、`tools/run_pa12_finite_vfm_diagnostic.py`；原始 JPG/DAT/Job/力数据只读。
- 方法：对 284 帧、192,508 个共同网格三角形逐帧计算 `det(F)` 极值、非正 Jacobian 数、最小 `|det(F)|` 和最大绝对 Euler–Almansi 分量；另核对已完成的 000261/000278 局部梯度尺度与 DAT 应变对照。
- 结果：000261 有 2 个非正三角形，最小 `|det(F)|=0.001630`、最大绝对应变分量 `236,539.5`；000278 分别为 10、`0.002168`、`152,675.7`。6.5 px 局部拟合令异常处 `det(F)` 约为 `1.234/1.294`，但该尺度并非已验证真值。九帧弹性候选 `E=4444.699 MPa`、固定 `ν=0.375` 未变；自由 ν 1% 残差带 `[0.47045,0.499]`，不能辨识。
- 判定：异常主要由近奇异三角形和空间梯度尺度敏感性触发；证据不足以断定是材料局部化还是 DIC 失配。未删帧/点、未平滑、未更改主域；S15 `Y/H` 与正式参数继续关闭。
- 更新：[S15 运动学门槛审计](Agents/PA12实验数据处理/VFM自建/有限变形诊断_等双轴生产网格/S15_XY_0.2/S15双轴有限变形J2运动学门槛审计.md)、[逐帧质量 CSV](Agents/PA12实验数据处理/VFM自建/有限变形诊断_九帧弹性候选/S15_XY_0.2/逐帧运动学质量.csv)、GPT 交接文档/状态、`index.md`。
- 验证：S15 诊断命令成功；目标测试 `8 passed`；全仓测试 `293 passed`。
- 下一步：继续推进输入合格实验的独立内外虚功与参数可辨识诊断；不重复 S15 的同一拟合，物理 ROI/厚度、独立时基、机器—DIC 有向轴和真实边界功仍待证据。

## [2026-09-29] experiment | S16 逐帧运动学与线弹性全程残差复核

- 来源：S16 正式 DIC—力索引、257 个合并 DIC 场、Job、Press 力索引；原始资料只读。索引帧与合并场一一对应，000000 在索引外、000258 无 DAT。
- 方法：按固定共同网格逐帧计算 `det(F)`、非正 Jacobian 数及 Euler–Almansi 极值；九帧弹性参数拟合与全历程残差单独报告，检查图复核双轴内外虚功趋势。
- 结果：10,098 点/19,796 三角形，`det(F)=0.56447–2.37447`，无非正 Jacobian；最大绝对应变分量 `1.04551`（000235）。Job ROI 覆盖率 `89.2248%`。九帧 E 候选 `3507.540 MPa`，固定 ν `0.375`，拟合相对 RMS `9.64%`，自由 ν 1% 残差带 `[0.32769,0.499]`；全历程虚功残差 RMS `4968.352 N`，后段内功约 `12.6 kN`、外功候选约 `1.6 kN`。既有全窗 J2 候选 `E/Y/H=3507.812/88.770/13.385 MPa`，仅为 REVIEW_REQUIRED 候选、未正式放行。
- 判定：早期线弹性候选不能代表全程；网格未翻转不等同于局部应变已验证。ν 未辨识，ROI 覆盖不足，Press 外功边界条件和样件物理映射仍待证。不同模型/窗口的残差不直接横向比较。
- 更新：[S15/S16 综合复核](Agents/PA12实验数据处理/VFM自建/汇总/PA12有限变形运动学与弹性候选_S15_S16复核.md)、S16 逐帧输出与检查图、GPT 交接文档/状态、`index.md`。
- 下一步：审核既有 S16 J2 窗口稳定性和留出证据，不重复九帧 E/ν 拟合；继续维持物理边界与正式参数门禁。

## [2026-09-29] design | S21/S22 完整 Job ROI 边界适配虚场

- 来源：S21/S22 有限变形配置与原始 Job Shape、正式 DIC—力索引、S22 三个早期加载合并场，以及现存有限变形逐帧虚功 CSV；源文件只读。
- 结果：现有 S21 主域/subset 各 36 帧、S22 各 223 帧 CSV 均含 X/Y 内虚功、机器力外虚功及残差；均属 Euler–Almansi 线弹性诊断基线，不是 J2 拟合曲线。当前机器轴映射为 S21 X=`DIC y/v`、Y=`DIC x/u`；S22 X=`DIC x/u`、Y=`DIC y/v`。S22 早期 Y 力从 175.3 N 增至 356.3 N 时，`dv/dy` 从 0.002822 增至 0.005800，`du/dx` 为相反符号，支持现配置方向。
- 方法：以完整 Job ROI 两条轴向切边的直线定义 `φ=(q−q0(p))/(q1(p)−q0(p))`。S21/S22 两轴在横向包络端点的归一化分母最小值分别为 60.055726/10.191727 mm、9.832666/44.083157 mm；11 点端边恒值误差最大 `6.96×10⁻¹⁶`。subset 敏感性复用 Job ROI 虚场、单独改变积分域，不视为 subset 自身边界闭合。
- 判定：几何适配场定义可进入实现审阅；仍需把一般节点虚场传入有限 J2 内虚功与拟合目标。力路径/符号/独立同步、实物厚度与 ROI 配准及 <0.95 支持率仍限制正式参数发布；S19 双组件修复和 S20 自交 ROI 不在本设计范围。
- 更新：[边界适配虚场设计](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S21_S22完整JobROI边界适配虚场设计.md)、`index.md`、GPT/VFM 机器状态。
- 下一步：审核设计；通过后按测试驱动扩展 J2 积分与拟合接口，再生成 S21/S22 主域和 subset 敏感性 J2 曲线，不重跑现存线弹性基线。

## [2026-09-29] experiment | S17/S18/S21/S22 全索引帧运动学质量复核

- 来源：四组正式 DIC—力索引、全程合并 DIC 位移场、Job ROI 与现有有限变形诊断 runner；原始 JPG、DAT、Job 和力工作簿保持只读。
- 方法：按全程共同 DIC 网格计算逐帧 `det(F)`、非正 Jacobian 三角形数、最小 `|det(F)|` 和最大绝对 Euler–Almansi 应变分量；输出到独立新目录，不覆盖既有结果。
- 结果：S17/S18/S21/S22 分别为 12/126/36/223 帧；索引、运动学质量 CSV、虚功 CSV 照片键及顺序一致，全部运动学质量数值有限。共同点/三角形数为 10,403/20,400、9,312/18,240、7,765/15,007、5,425/10,062；Job ROI 覆盖率为 90.5004%、89.1147%、84.1189%、71.1951%。S22 有 15 个非正 Jacobian 事件，分布于 7 帧；极值应变 `2228.046` 位于 `001776.jpg`。
- 判定：四组均低于 95% 覆盖门槛，保持 `REVIEW_REQUIRED`。S17/S18/S21 的 `det(F)` 为正；S22 极端值保留为运动学质量警报，不解释为材料局部化，不删帧、不筛三角形、不平滑。阶段 1 条件 E 及 ν 网格仅为诊断候选，不发布正式材料参数。
- 更新：[四组质量复核报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12全组逐帧运动学质量_S17_S18_S21_S22.md)、四个独立配置、GPT 交接文档/状态、阶段计划、`index.md`。
- 验证：四组质量 CSV 行数分别与索引和逐帧虚功 CSV 完全匹配；照片顺序一致；各质量数值列均无空值、NaN 或无穷值。复现命令见报告。
- 下一步：不重复四组运动学审计；继续不依赖待审设计的 VFM 诊断。S19/S20 自交 ROI 不使用原始全域积分；S21/S22 边界适配虚场设计经审核后再实现，正式参数发布门槛继续独立执行。

## [2026-09-29] audit | PA12 应力—应变图与屈服候选判读

- 来源：`tools/pa12_sync.py`、`PA12应力应变曲线审计.json` 及批处理清单引用的逐组主图；未改写 PNG 或 CSV。
- 判定：规范主图由 `pa12_sync.py` 生成，包含有效曲线、线性拟合、峰值、屈服候选及经确认的终点标记；`应力应变/完整曲线/` 下的旧静态图没有仓库内对应生成命令，不作为最新批处理图。
- 结果：候选屈服判据为前段线性拟合偏差达到峰值应力 5% 并连续 3 个样点。S17 两轴候选都与峰值重合于索引 8（全程 12 帧）；S21 候选距峰值 1 帧；S22 线性拟合 `R²=0.8229`。图上继续标候选，但这些情形不构成独立确认屈服值。
- 更新：[全组运动学质量复核报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12全组逐帧运动学质量_S17_S18_S21_S22.md)、GPT 交接文档/状态。
- 下一步：曲线应以清单 `stress_strain_plot` 指向的规范主图为准；人工复核屈服候选后，才用于模型窗口选择。

## [2026-09-29] audit | S21/S22 边界适配虚场 J2 接口状态

- 来源：`tools/run_pa12_finite_vfm_diagnostic.py`、`tools/run_pa12_finite_j2_vfm.py`、有限 J2 积分器、现有边界适配设计及 4 项定向测试。
- 结果：节点级边界适配虚场已贯通 J2 预拟合、全网格精修和全历程积分路径；ROI/subset 分域与一般节点虚场积分相关测试 `4 passed`。环境检查通过，自建 VFM 依赖、实验路径及 MatchID 可执行文件均可用。
- 限制：尚无 S21/S22 边界模式配置或新 J2 实验输出；矩形等价与该模式下合成已知参数回收尚未验收。单轴覆盖率低于 95%，Press 外功仍为条件候选，正式参数不放行。
- 更新：边界适配设计报告、阶段计划、GPT 交接文档/状态、`index.md`。
- 下一步：用户确认后再生成独立 S21/S22 配置和结果，保留仿射基线；不把 S19/S20 自交域纳入本分支。

## [2026-09-29] experiment | S21 边界适配虚场 J2 双域窗口诊断

- 来源：`configs/pa12_finite_j2_s21_job_boundary.json`、S21 正式 DIC—力索引和合并场；原始 JPG、DAT、Job 与力文件只读。
- 方法：固定 `ν=0.375` 与阶段 1 `E=9042.042 MPa`，分别对完整 Job ROI 主域及 DIC subset 内缩敏感性域拟合 Linear J2；窗口为峰前时程的 50%/75%/100%，峰前终点 `000035.jpg`；状态历史保留 36 帧至 `000045.jpg`。
- 结果：完整域/内缩域覆盖率为 84.1189%/100%。Y0/H 随窗口漂移：完整域从约 `(0,55.52 GPa)` 到 `(2.104 GPa,37.10 GPa)` 再到 `(0.970 GPa,≈0)`；subset 从约 `(0,55.52 GPa)` 到 `(0,200.65 GPa)` 再到 `(0.970 GPa,2.879 GPa)`。完整域 75% Jacobian 秩为 0；全窗内缩域条件数较低但未消除参数漂移。全窗拟合 RMS 几乎相同（119.292/119.325 N）。
- 判定：两域全部保留为条件诊断，不是正式材料参数；完整 Job ROI 仍为主域，subset 只作独立敏感性，沿用完整域机器力不构成自身边界闭合。Press 外功、实物 ROI/厚度、同步及机器—DIC 有向轴仍待物理证据。
- 更新：[S21/S22 设计与结果页](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S21_S22完整JobROI边界适配虚场设计.md)、GPT 交接文档/状态、`index.md`。
- 验证：六窗口参数、残差、秩/条件数、覆盖率与逐域 JSON/CSV 对照；核心代码既有定向测试记录为 `107 passed`，本轮未改代码、未重跑测试。
- 下一步：等待 S22 已有双域运行结束，再记录其窗口结果；随后补矩形仿射等价和边界适配模式下合成参数回收验证。

## [2026-09-29] audit | 边界适配虚场矩形等价与合成参数回收

- 方法：直接调用边界适配虚场构造器与有限变形 J2 拟合接口；未修改实验输入或生产代码。先比较矩形 ROI 边界适配场与仿射场，再在非平行轴向切边的梯形网格上检查端值与参数回收。
- 合成域：`x∈[0,4] mm`，`q0(x)=0.2+0.1x`、`q1(x)=3.8−0.05x mm`；25 个参数网格节点、32 个三角形，厚度 1 mm。端边场值最大误差 `1.1×10⁻¹⁶`，矩形场与仿射场最大误差为 0。
- 合成历程：固定 `E=2100 MPa, ν=0.35`，给定 Linear J2 真值 `Y0=18 MPa, H=120 MPa`，41 帧等效塑性应变历程覆盖至 0.02；外部合力按均匀 `Pyy` 乘 4 mm 投影宽度和 1 mm 厚度生成。
- 结果：拟合回收 `Y0=18.0000000000 MPa, H=120.0000000000 MPa`；虚功残差 RMS `3.13×10⁻¹² N`。
- 判定：矩形退化关系、梯形端边归一化及一般节点场 J2 拟合链路在解析均匀场中自洽。该检查不含 Abaqus 解，不验证实验外功边界、物理 ROI、照片—力同步、坐标符号或 PA12 参数。
- 更新：边界适配设计/结果页、交接文档/状态、`index.md`。
- 下一步：等待 S22 双域三窗口运行完成，再审查实验敏感性结果；不据合成回收发布实验参数。

## [2026-09-29] experiment | S22 边界适配虚场 J2 双域窗口诊断

- 来源：`configs/pa12_finite_j2_s22_job_boundary.json`、S22 正式 DIC—力索引与合并场；原始 JPG、DAT、Job 和力工作簿只读。
- 方法：固定 `ν=0.375` 与阶段 1 `E=7749.576 MPa`，分别对完整 Job ROI 主域和 DIC subset 内缩敏感性域拟合 Linear J2；峰前拟合截止 `001120.jpg`，用 50%/75%/100% 前缀窗口；有限 J2 状态历史截止 `001504.jpg`。
- 结果：223 个索引帧中，拟合窗含 140 帧，状态历史含 188 帧，截止后排除 35 帧。完整域/subset 覆盖率为 71.1951%/100%。两域三窗的 Y0 分别为 `257.100/260.781/260.150 MPa` 与 `257.046/260.856/260.148 MPa`；H 分别为 `126.266/199.518/265.061 MPa` 与 `127.373/198.721/265.069 MPa`。拟合 RMS 为约 `276.7/286.0/274.7 N`，秩均为 2/2。
- 判定：Y0 窗口变化较小，但 H 随窗口变化，不能称为稳定识别。subset 参数与主域近似重合只是同一数据/力口径下的积分域敏感性结果；完整域支持率低于 95%，Press 外功的物理边界条件仍未验证。结果不发布为正式材料参数或训练标签。
- 更新：[S21/S22 设计与结果页](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S21_S22完整JobROI边界适配虚场设计.md)、GPT 交接文档/状态、`index.md`。
- 验证：六个窗口的 CSV 与汇总 JSON 在 E/Y0/H/拟合 RMS 上逐项一致；双域报告均已生成。未重跑已完成拟合。
- 下一步：按同口径继续其他输入合格的速率/等双轴实验，并先闭合物理 ROI/厚度、同步、有向轴与外虚功边界证据。

## [2026-09-29] experiment | S18_XY_2 边界适配虚场 J2 双域诊断

- 来源：`configs/pa12_finite_j2_s18_job_boundary.json`、S18 DIC—力索引与合并场、既有仿射阶段 1 E 候选；原始 JPG、DAT、Job 和力工作簿只读。
- 方法：固定 `ν=0.375`、厚度假设 1 mm 和阶段 1 E 候选，对完整 Job ROI 主域及 DIC subset 内缩敏感性域分别做 Linear J2 50%/75%/100% 峰前拟合；Job ROI 场供两域共用，外虚功沿用完整 ROI Press 合力。
- 结果：126 帧（000003–000128），拟合截止 000125（123 帧）；完整 ROI 支持率 89.1147%，subset 100%。主域三窗 Y0/H 为 88.610/≈0、86.318/≈0、85.065/≈0 MPa；subset 为 89.656/1636.090、86.078/≈0、84.315/≈0 MPa。逐帧 X/Y 内外虚功 CSV 均 126 行且数值有限，六条优化轨迹 RMS 单调不增；最大绝对残差均在 000128.jpg。
- 判定：主域矩形边界适配结果复现仿射基线；subset 的窗口结果不同，但其 E 沿用旧仿射阶段 1 候选，虚场、积分域与 E 口径差异尚未隔离。H 不稳定、完整 ROI 支持率不足、峰后残差骤增；不发布正式参数或训练标签。Press 外功及 ROI/厚度、时序、有向轴物理证据仍未闭合。
- 更新：[S18 双域诊断报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S18_XY_2边界适配虚场J2双域诊断.md)、[逐帧主域曲线](Agents/PA12实验数据处理/VFM自建/有限变形J2边界适配诊断/S18_XY_2/Linear/full_job_roi/逐帧有限变形J2虚功.png)、[逐帧 subset 曲线](Agents/PA12实验数据处理/VFM自建/有限变形J2边界适配诊断/S18_XY_2/Linear/dic_subset_inset_sensitivity/逐帧有限变形J2虚功.png)、交接文档/状态、`index.md`。
- 验证：结果 JSON 与运行检查点均列出六窗；两域虚功 CSV 各 126 帧，数值列有限；六个优化轨迹的 RMS 均单调不增。未修改生产代码，未重跑单元测试。
- 下一步：先在边界适配虚场口径下重新识别 S18 阶段 1 E，再继续其他等双轴速度组；物理边界、同步、实测厚度/ROI 和有向轴门槛保持独立。

## [2026-09-29] experiment | S18 阶段1边界适配 E 复核与 subset J2 重算

- 来源：`configs/pa12_finite_vfm_biaxial_s18_job_boundary.json`、`configs/pa12_finite_j2_s18_subset_job_boundary_e_refit.json`、S18 DIC—力索引及合并场；原始 JPG、DAT、Job 和力工作簿只读。
- 方法：固定 `ν=0.375`、厚度假设 `1 mm`，用 Job ROI 边界适配虚场在 `000004–000036.jpg` 识别阶段 1 E；仅重算受旧 E 口径影响的 DIC subset Linear J2 50%/75%/100% 窗口，主域结果保留。
- 结果：阶段 1 完整 ROI/subset E 分别为 `4636.145391883104/4636.145391883215 MPa`。旧 subset 仿射 E `4376.946936991783 MPa` 高估差约 `5.9219%`，已不用于当前阶段 2。新 subset 三窗 `(Y0,H)` 为 `(88.610,≈0)`、`(86.318,≈0)`、`(85.065,≈0) MPa`；J2 全窗历史 RMS 为 `170.032/155.189/150.186 N`。
- 判定：Job ROI 面积 `704.606414 mm²`，DIC 支持面积 `627.908002 mm²`；完整 ROI 覆盖率 `89.1147%`，subset 为 `100%`，但两个分支的实际三角积分支持面积相同。当前 subset 分支改变覆盖率基准，不构成不同空间积分支持的敏感性对照。H 三窗均贴近 0 下界；不放行正式材料参数或代理训练标签。Press 边界、物理 ROI/厚度、方向与独立同步门槛仍未闭合。
- 更新：[S18 双域报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S18_XY_2边界适配虚场J2双域诊断.md)、阶段 1/阶段 2 配置、GPT 交接文档/状态、`index.md`。
- 验证：两个分析命令均退出码 0；Stage 2 汇总含 3 个 subset 窗口；窗口稳定性 CSV 与汇总 JSON 参数逐项一致；逐帧虚功 CSV 为 126 行且数值列全有限。生产代码未改，未运行单元测试。
- 下一步：以 S15_XY_0.2 为下一组按同口径推进；S16 力同步问题未解除前不拟合。继续独立执行物理边界、ROI/厚度、同步与坐标门槛。

## [2026-09-29] audit | S18 当前帧力索引全 ROI 与 subset 复核

- 来源：S18 当前 DIC—力索引、阶段 1 E 边界适配复核及全 ROI/subset 有限变形 J2 逐帧 CSV；原始 JPG、DAT、Job 和力工作簿只读。
- 方法：逐行比较照片键、时间、X/Y 外力；检查所有数值列有限，并核对输出图和汇总 JSON 存在。
- 结果：两域各 126 帧，照片键、时间、X/Y 外力与索引完全一致；首帧 `000003.jpg` 为 X=`3.54 N`、Y=`3.87 N`。全 ROI/subset 三个峰前窗口使用相同阶段 1 `E=4636.145392 MPa`，`H` 均贴近 0 下界，拟合与全历程残差数值一致。
- 判定：旧全 ROI 路径首帧外功为零，与当前帧力索引不一致，已从当前报告/状态的正式引用中移除，但原文件保留。新结果仍是条件诊断：完整 ROI DIC 覆盖率 `89.1147%`，ν 固定为 `0.375`，物理 ROI/厚度、有向轴、照片同步与 Press 边界外功证据未闭合，不发布正式参数。
- 更新：[S18 双域报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S18_XY_2边界适配虚场J2双域诊断.md)、GPT 交接文档/状态、`index.md`。
- 验证：只读数值一致性核对通过；未修改生产代码，未重跑单元测试。
- 下一步：转入 S15_XY_0.2，围绕已有阶段 1 超限和起始窗口内外虚功异号做证据限定的根因核对；不靠删帧或无依据的符号翻转解锁拟合。

## [2026-09-29] experiment | S23_Y_2 预断裂有限变形 VFM 阶段 1 窗口诊断

- 来源：S23 DAT 重构全场、191 帧 DIC—力索引及三组阶段 1 配置；原始 JPG、DAT、Job 和力工作簿只读。
- 方法：固定 ν=0.375 和 1 mm 中心厚度工作值，比较最早 3/7/12 个配对帧的条件 E；完整 Job ROI 为主域，DIC subset 内缩域单独作敏感性。
- 结果：条件 E 为 3423.085/5445.339/5996.844 MPa，拟合相对 RMS 为 51.70%/30.01%/24.02%，Job ROI DIC 覆盖率 83.1892%。ν 粗网格候选随窗口从 0.470449 变为 0.413347，1% 残差带各只有一个网格点。虚功及运动学质量输出均覆盖 191 帧并与索引逐行一致。
- 判定：窗口与参数不稳定、残差和面积支持门槛未通过；不发布 E/ν，不进入 S23 的 Y/H 拟合。001547.jpg 首次明确断裂，力记录止于 001528.jpg，不补造断裂力。
- 更新：[S23 阶段 1 诊断报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S23_Y_2预断裂有限变形VFM阶段1窗口稳定性诊断.md)、GPT 交接文档/状态、MatchID 输入状态、`index.md`。
- 下一步：按交接状态转至 S15，统一力基线和应变/虚功口径调查 Stage 1 超限；原始资料保持只读。

## [2026-09-29] experiment | S15 有限变形 Stage 1 窗口敏感性

- 来源：S15 完整 Job ROI 与 DIC subset 内缩域 284 帧逐帧虚功、当前 DIC—力索引、旧 Stage A 窗口表；原始照片、DAT、Job 与力工作簿只读。
- 方法：固定 `ν=0.375`、厚度工作值 `1 mm`。固定 ν 时内部虚功对 E 线性；从已完成的 48 帧全历程曲线恢复单位 E 响应，解析重拟合 7/12/24/36/48 帧前缀。完整 Job ROI 为主域，subset 单独作敏感性并沿用完整 ROI 合力。
- 结果：主域 E 候选 `0/0/4778.044/4817.946/4137.466 MPa`，相对 RMS `1.0000/1.0000/0.7828/0.4437/0.3117`。7/12 帧 X/Y 单位 E 虚功—外力相关系数均为负，24 帧起转正。48 帧回代与原直接拟合 E 差 `1.16×10⁻¹⁰ MPa`；subset 回代差 `−9.46×10⁻¹¹ MPa`。旧 Stage A 同五窗相对 RMS 全部高于 `0.10`，但应变/虚功模型和归一化分母不同，不作同模型误差比较。
- 判定：短窗 `E=0` 是非负约束下界，不是材料模量；24–48 帧参数仍随窗口变化，48 帧相对 RMS 为 31.17%，完整 Job ROI DIC 支持率为 88.9256%。S15 阶段 1 不通过，不识别 `Y/H`，不发布材料参数或训练标签；不翻转符号、不自动扣基线、不删早期帧。
- 更新：[S15 窗口敏感性报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S15有限变形Stage1窗口敏感性.md)、窗口 CSV、GPT 交接文档/状态、总目标阶段计划、`index.md`。
- 验证：48 帧回代复现原直接 E；受保护的 check 脚本、测试及共享 boundary config 未改；生产代码未改。
- 下一步：仅在已有配对和参考场证据支持下，对 S15 `000000.jpg`/`000001.jpg` 参考基线做单独敏感性分析；外功边界、时序和有向坐标仍需独立证据，不以参考帧选择替代物理验证。

## [2026-09-29] experiment | S15/S17 有限变形 Stage 1 双域复核

- 来源：`configs/pa12_finite_vfm_biaxial_s15_job_boundary.json`、`configs/pa12_finite_vfm_biaxial_s17_job_boundary.json`、S15/S17 当前 DIC—力索引与合并场、既有 Stage A 结果；原始 JPG/DAT/Job/Press 数据只读。
- 方法：固定 `ν=0.375`；完整 Job ROI 为主域，DIC subset 内缩域独立输出。S15 复核同一 `000002–000049.jpg` 拟合窗的旧 Stage A 与有限变形边界适配虚功公式；S17 按 `000004–000007.jpg` 拟合，并额外计算 `F−F_ref` 基线敏感性。
- 结果：S15 有限变形主域 `E=4137.466178 MPa`、拟合 RMS `123.303568 N`；旧 Stage A `E=3536.434746 MPa`、RMS `74.291878 N`。拟合照片、时间、力一致，但两路应变/虚功模型和相对 RMSE 分母不同；Stage A 相对 RMSE `0.111998` 超过 `0.10` 门槛。S17 原始力主域 `E=5050.231948 MPa`、RMS `56.058542 N`；参考图 `000003.jpg` 力为 `84.45/83.45 N`，扣参考帧力的敏感性 `E=4443.938518 MPa`（−12.0053%）、RMS `38.285190 N`。S15/S17 Job ROI 支持率分别为 `88.9256%/90.5004%`，低于 `0.95`；各组 subset 支持面积均与主域实测积分支持面积相同，未对未覆盖区域外推。
- 判定：S15 两种 E 不是同模型复算差；S17 参考帧预载/力零点口径未确认。S15/S17 均不放行正式 E，不进行本轮 `Y/H` 识别，不生成材料训练标签。参考力敏感性只是诊断，不自动扣基线。S16 的 `3try` 不同步、`4try_step3` Forces=0、第 16 轮 GUI `Y=63.93/H=41.55 MPa` 与残差显示 `1214`（定义/单位未知）继续只作历史 MatchID 审计。
- 更新：[S15 审计](Agents/PA12实验数据处理/VFM自建/有限变形诊断_等双轴生产网格/S15_XY_0.2/S15双轴有限变形J2运动学门槛审计.md)、[S15 边界适配摘要](Agents/PA12实验数据处理/VFM自建/有限变形诊断_等双轴生产网格_JobROI边界适配/S15_XY_0.2/诊断摘要.md)、[S17 边界适配摘要](Agents/PA12实验数据处理/VFM自建/有限变形诊断_等双轴生产网格_JobROI边界适配/S17_XY_20/诊断摘要.md)、总体方法协议、边界说明、GPT 交接文档/状态、`index.md`。
- 验证：S17 主域/subset CSV 各 12 行；状态 JSON 可解析且 S15/S17 E 与诊断摘要一致；新增文档链接存在。受保护的 check 脚本、测试和共享 boundary config 未改。生产代码未修改，未运行单元测试。
- 下一步：核实 S17 参考图对应的预载及力零点；以共同力基线和应变测度设计 S15 Stage A/有限变形口径的可比性检查。物理 ROI/厚度、同步、有向轴、外虚功边界与参数稳定性门槛继续独立保留。

## [2026-09-29] analysis | S15 原始力与 DIC 参考场敏感性

- 来源：S15 当前 DIC—力索引、S15 配置/处理报告、原始 Press 工作簿、`000000.jpg.dat`、两套有限变形逐帧虚功输出；原始 JPG/DAT/工作簿只读。
- 方法：用首 50 ms 基线与既有符号复现 0.105/0.205 s 力；固定现有 284 帧索引，比较以 `000001.jpg` 和原始 DIC 参考场 `000000.jpg.dat` 计算的完整 Job ROI 主域及 subset 敏感性，并按同一过原点 E 公式复核 7/12/24/36/48 帧窗口。
- 结果：0.105 s 原始四通道校正为 X/Y=`4.68/5.33 N`，0.205 s 为 `17.18/17.83 N`，支持当前索引而非零力。以 DIC 来源参考场重算的 48 帧 E=`4211.375 MPa`、残差 RMS=`133.481 N`、相对 RMS=`0.337441`；旧参考场结果为 `4137.466 MPa/0.311713`。主域与 subset 外力序列相同。
- 判定：DIC 参考场不等同于力索引首行；不将首个受力帧强制归零，也不给 `000000.jpg` 补造力。切换参考场未消除早期反向对齐，且 48 帧相对 RMS 略增；阶段 1 不通过，不发布 E，不识别 Y/H。Job ROI 支持率为 `88.9256%`；subset 虽全覆盖，但使用同一 DIC 网格支持和完整 ROI 合力。时间关系仍是图像帧映射，不等于硬件触发同步证明。
- 更新：总体方法协议、边界载荷说明、GPT 交接文档/状态、`index.md`。
- 验证：敏感性输出与索引的 284 帧照片顺序、时间、X/Y 力逐行一致；主域/subset 外力数组相同；独立重算 48 帧 E 与直接结果之差小于 `2×10⁻¹⁰ MPa`。原始工作簿、照片、DAT 以及受保护的 check/config 文件未改。
- 下一步：以 `000000` 为 DIC 参考场检查 S15 早期 DIC 场、机器轴映射与边界虚场方向；正式生产重算前再对齐 S15 配置中的参考场定义。

## [2026-09-29] analysis | S15 早期 DIC 轴向方向复核

- 来源：S15 原始 DIC 参考场 `000000.jpg.dat`、现有 `000001–000049.jpg` 合并 DIC 位移/应变场、当前 284 行 DIC—力索引、Job ROI 几何与有限变形诊断虚场定义；原始资料保持只读。
- 方法：按配置 `X=(DIC y,v)`、`Y=(DIC x,u)`，对齐参考点坐标，在完整 Job ROI 内拟合轴向位移梯度；力仅从当前索引读取，不使用合并 DIC CSV 内嵌的旧力列。核对首帧应变中位数及 ROI 内空间标准差，并比较早期符号与后续力—梯度趋势。
- 结果：参考点 100,489 个。首个受力帧的 ROI 应变中位数 X/Y=`−0.000197/−0.000181`，空间标准差=`0.005646/0.005705`。`000002–000008.jpg` 的 X 梯度 7/7 为负、Y 梯度 6/7 为负；`000013.jpg` 两轴转正，`000049.jpg` 梯度=`0.004928/0.005048`；`000002–000049.jpg` 窗口内力—梯度 Pearson r=`0.9926/0.9946`。
- 判定：早期负号相对 ROI 场内离散很弱，不能稳健解释为真实压缩；后续正向梯度与正向载荷一致，不支持全程统一反号。等双轴条件不能独立识别 X/Y 标签互换；单位虚场的符号一致性不等于传感器物理轴或实验边界外功已独立验证。完整 Job ROI 保持主域，subset 保持独立敏感性；不翻转力、不删帧、不发布 E/Y/H。
- 更新：总体方法协议、边界载荷说明、GPT 交接文档/状态、`index.md`。
- 验证：按参考/当前坐标键逐点匹配，首帧及代表帧各 100,489 个参考点（末代表帧 100,488 个）；力值来自现行索引。此前确认主域/subset 输出各 284 行，与索引照片、时间及力逐行对应。生产代码、受保护 checker/test/shared config 及原始 JPG/DAT/Press 未改。
- 下一步：独立取得机器或夹具上 X1/X2/Y1/Y2 与照片坐标的标记证据；确认后将 S15 生产配置位移参考统一到 `000000.jpg.dat`，再做隔离复跑。物理轴标签确认前，不作正式参数识别。

## [2026-09-29] analysis | S15 机器—DIC轴映射证据范围复核

- 来源：用户提供的[原始方向与旋转标定照片](raw/assets/PA12原始方向与旋转标定方向.jpg)、[S16 FE–DIC 坐标映射预检](raw/PA12_Stage2_Evidence/阶段2_G4_S16_FE-DIC坐标映射预检.md)、[G1 材料—试验机—DIC 坐标变换矩阵](Agents/PA12双轴试样仿真/验证/2026-09-26_G1材料-机器-DIC坐标变换矩阵.md)及现行方法协议。
- 结果：现有资料已登记原机四执行器象限和旋转后顶/底/左/右边界对应，支持将 `X=(DIC y,v)`、`Y=(DIC x,u)` 作为双轴诊断的工作轴置换；G1 矩阵仍将完整有向变换列为未标定。S15 高载荷 DIC 梯度支持当前映射下的正向拉伸符号，但等双轴响应本身不能独立识别 X/Y 标签互换。
- 判定：保留既有用户方向映射，不要求重复提供；不把本次趋势升级为逐样件有向标定或外功闭合。正式标定仍按 G1 规程使用可辨识的单轴小位移/带轴标记记录。
- 更新：总体方法协议、边界载荷说明、GPT 交接文档/状态、`index.md`。
- 下一步：诊断阶段继续使用现有轴置换工作映射；S15 下次隔离重算前统一使用原始 DIC 参考场 `000000.jpg.dat`，正式参数放行前完成有向坐标与边界功门槛。

## [2026-09-29] analysis | S16 预加载参考帧与零载候选审计

- 来源：S16 `Job.m2inp`、`000000/000001.jpg` MatchID 全场导出、当前 257 行照片—力索引、原始 Press 表；原始照片、DAT、Job 和工作簿只读。
- 方法：核对 Job 参考图、全场点键/位移/应变；按当前有效帧端点 `000001–000257` 和实际帧率向前外推一帧，再与首 50 ms Press 基线均值及标准差比较。
- 结果：目录含 `000000–000257` 共 258 组 JPG/DAT 配对，另有无 DAT 的 `000258.jpg`。参考图导出 10,098 点，U 为零、V 最大绝对值 `3×10⁻⁶ mm`、应变为零。候选时刻 `0.001484 s` 的基线校正力为 X/Y=`+0.32/−0.24 N`，小于基线标准差 `0.426/0.431 N`；现索引首帧力仍为 `4.82/4.26 N`。
- 判定：`000000.jpg` 具有作为预加载参考态的证据，但时间依赖帧率外推。当前 257 行索引与正式输出目录未改；是否把该参考态作为 VFM 零载行及其噪声门限尚未确认。正式输出继续阻断。
- 更新：[S16 参考帧审计](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S16预加载参考帧与零载候选审计.md)、GPT 交接文档/状态、`index.md`。
- 下一步：保持当前同步结果不变，按方法确认后再决定是否实现可选参考行；继续独立的样件坐标/边界诊断。

## [2026-09-29] experiment | S17 重同步与 Stage 1 窗口敏感性

- 来源：S17 当前同步报告/照片—力索引、3/6 帧边界适配 Stage 1 输出及 `000013–000020.jpg` 原图；原始 JPG、DAT、Job 和 Press 工作簿只读。
- 方法：核对当前同步表 13 行与两窗口配置；按 `000013–000020` 顺序检查可见断裂，结合帧号—力时间映射核对掉载前后 Press 值。
- 结果：自动事件起点/峰值/掉载为 `0.026/0.218/0.268 s`；3/6 帧条件 E 为 `3300.967/4278.855 MPa`，差 29.63%，ν 不可辨识，完整 Job ROI DIC 覆盖率 90.5004%。`000013–000019.jpg` 外观仍连续，`000020.jpg` 首次明显断裂且无同名 DAT；外推时间约 `0.409167 s`。掉载后力在约 `0.288 s` 降至近基线，不能据现有时钟证据把力掉载与可见断裂视为同一时刻。
- 判定：当前 13 帧索引和已有两窗口结果保留为诊断候选；不扩窗追参、不纳入后续近零力照片、不补造断裂 DAT/力，不释放 E/ν/Y/H。
- 更新：[S17 重同步与 Stage 1 报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S17重同步与Stage1窗口敏感性.md)、GPT 交接文档/状态、阶段计划、`index.md`。
- 下一步：不重复 S17 拟合；继续独立的实验坐标与边界证据核验，不据此自动放行正式参数。

## [2026-09-29] analysis | 用户方向与旋转标定照片的轴标签证据边界

- 来源：`raw/assets/PA12原始方向与旋转标定方向.jpg`、用户给出的方向/旋转说明、现有 S16 FE–DIC 预检及 G1 坐标变换矩阵页；不修改原始图片。
- 方法：目视核对归档照片中是否存在能对应 `X1/X2/Y1/Y2` 与 DIC x/y 的可读标签或方向标记，并与现有边界方向审计中的工作轴映射对照。
- 结果：照片可辨认四臂夹具与十字试样构型，但没有可读的机台通道标签，也不足以单独确定正负号、镜像或精确旋转。结合用户说明和 S16 预检，机器 X→DIC y、机器 Y→DIC x 保留为工作轴置换；完整有向变换仍未独立标定。
- 判定：不改力符号、边界映射或生产配置；不将照片当作正式轴标定。正式材料轴 `Q_i` 与机器—DIC 有向变换继续阻断参数发布。
- 更新：[边界载荷说明](Agents/PA12实验数据处理/MatchID_VFM准备/PA12_VFM边界载荷说明.md)、S17 报告、GPT 交接文档/状态、阶段计划、`index.md`。
- 下一步：取得可读的机台/夹具 X1/X2/Y1/Y2 标记，或对 X、Y 方向分别执行小位移校准并记录同帧 DIC 响应；证据齐全后再考虑 S15 生产参考场隔离复跑。

## [2026-09-29] analysis | 应力—应变图末端保真与回归

- 范围：只调整应力—应变 PNG 的显示平滑边缘，并修正依赖已失效历史 VFM CSV 的状态快照测试夹具；原始 JPG/DAT/XLS、同步力表、VFM 力文件和应力—应变 CSV 保持不变。
- 绘图规则：5 点居中平滑仅用于内部显示；首尾各 3 个样点保留 CSV 原值，使首行近零和末端掉载不被均值模糊。9 张主图由对应 CSV 与各组处理报告重绘；S15/S17/S23 仍不标记未确认终点。
- 检查器测试：状态快照测试使用现存照片—力表构造对齐力值，不依赖已撤出正式目录的 `.invalid` 历史结果；断言分别核对报告快照和当前首力门禁。
- 验证：应力—应变/同步定向回归 `55 passed, 2 subtests passed`；全仓 `304 passed, 2 subtests passed`。S15 双轴及 S19 单轴图已目视检查，端点掉载保留实测值。
- 下一步：继续可复用数据支持的 VFM 内外虚功、残差、覆盖率与参数稳定性诊断；物理轴标定、参考帧、边界外功和几何门槛未通过前不发布正式参数。

## [2026-09-29] refactor | 自建 VFM 阶段 A 汇总口径澄清

- 来源：阶段 A 一致性审计 JSON、旧 Stage A 汇总报告和最新有限变形 J2 逐组交接。
- 结论：1127 是含 S20 63 帧失效旧几何工件的历史总量；当前阶段 A 一致性审计覆盖 7 组、1064 帧，S20 阻断。旧 Stage A 表保留作方法对照，旧 Stage 2 的 Y/H 与 Press 力耦合，不作为独立材料参数。
- 更新：阶段报告、`index.md`、GPT 交接文档及机器状态 JSON 已明确有效/历史帧计数和参数口径；没有重写 VFM 数值工件。
- 验证：审计 JSON 计数与三份交接文档一致；链接存在；`compileall`、目标文件 `git diff --check` 通过；全仓 `304 passed, 2 subtests passed`。
- 下一步：沿当前工作轴映射继续仅做诊断；正式放行仍需实体有向标定、ROI/厚度、同步、边界功及参数稳定性/独立留出闭合。

## [2026-09-29] analysis | S16 自建有限变形 Stage 1 参考场敏感性

- 来源：S16 当前 257 行 DIC—力索引、Job 几何、合并 DIC 场、原始 `000000.jpg.dat` 与已有预加载参考帧审计；原始 JPG/DAT/Job/Press 和力索引只读。
- 方法：使用相同 Job ROI 边界适配虚场、固定 `ν=0.375` 和 1 mm 中心厚度，分别以 `000001.jpg` 与 `000000.jpg.dat` 作位移参考；两次均保留原始 257 行力序列和 `000002–000042.jpg` 拟合窗，分别输出完整 Job ROI 主域与 subset 分支。
- 结果：参考 `000001` 下完整 ROI 条件 E=`3524.822863 MPa`、拟合 RMS=`33.136512 N`；参考 `000000.dat` 下为 `3498.487479 MPa`、`31.350824 N`，变化 `−0.7471%/−5.3889%`。ROI 面积 `759.324103 mm²`，DIC 支持面积 `677.505105 mm²`，支持率 `89.2248%`。
- 判定：两种参考的全 ROI 结果均低于 95% 支持门槛；E 为固定 ν 的诊断候选，不发布 E、不拟合 Y/H。`000000` 候选时刻来自帧率外推，不是硬件同步证据；未补力行、扣力基线或更改生产索引。S16 subset 与 Job ROI 实际积分三角形支持相同、且复用 Job 边界虚场，故结果退化为数值重复，不构成独立敏感性或闭合证据。
- 更新：[S16 参考帧交接记录](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、[状态 JSON](Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json)、[方法协议](Agents/PA12实验数据处理/处理记录/PA12实验总体方法与防跑偏协议.md)、[边界载荷说明](Agents/PA12实验数据处理/MatchID_VFM准备/PA12_VFM边界载荷说明.md)、`index.md`；生成的两组隔离摘要/逐帧输出仅供诊断。
- 验证：两次主域与 subset CSV 各 257 行，首尾帧 `000001/000257.jpg`；外力与索引最大差 `0 N`，拟合窗口一致。状态 JSON 语法解析通过；生产配置、索引和受保护 check/config 文件未改。
- 下一步：保持 S16 诊断状态；待参考时序/零点语义和 ROI 实测支持证据解决后再评估 Stage 1 是否放行，不将 subset 重复结果当作独立证据。

## [2026-09-29] analysis | S16 预加载参考行的 Stage 1 统计量影响

- 来源：S16 参考 `000000.jpg.dat` 隔离诊断、当前 257 行 DIC—力索引及逐帧虚功残差 CSV；原始数据和生产索引只读。
- 结论：`000000.jpg` 在当前 `000002–000042.jpg` 拟合窗之外；保持窗口时 Stage 1 E/RMS 不变。把候选行额外并入 pooled RMS 会将样本从 82 个残差标量扩大至 84 个，RMS 表观下降约 1.20%，属于均方分母稀释，不是拟合改善；零位移参考行的单位模量内功为零，不增加 E 信息。
- 更新：[S16 参考行敏感性报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S16预加载参考行Stage1影响敏感性.md)、预加载参考审计、GPT 交接文档/状态及 `index.md`。未增加正式参考行，未强制归零候选力，未发布 E 或 `Y/H`。
- 验证：以逐帧 CSV 复算当前和两个 pooled-RMS 算术情形；报告值分别为 `31.350824`、`30.975382`、`30.975352 N`。
- 下一步：维持 S16 诊断候选状态，继续处理独立外功/实体几何与机器—DIC 有向轴证据；参考时序和基线门限确认前不改正式索引。

## [2026-09-29] analysis | S16 Stage 1 力—照片相位一帧偏移敏感性

- 来源：S16 完整 Job ROI 逐帧虚功诊断和当前全场—力索引；原始力、DIC 场、照片索引及生产配置只读。
- 方法：固定 DIC 场、参考态、Job ROI、厚度、泊松比与 `000002–000042.jpg` 拟合窗；比较现行同帧力值及索引前/后一行力值，偏移绝对时间为 `0.100500–0.100600 s`。基准复算与已有条件 E/RMS 一致。
- 结果：现行 E/RMS 为 `3524.823 MPa/33.1365 N`；早一行 `3408.617 MPa/25.2773 N`；晚一行 `3640.777 MPa/41.2622 N`。E 跨度为基准的 `6.5864%`。早移力值降低残差只表示后验拟合对时间相位敏感，不能识别真实同步延迟。
- 更新：[S16 力相位敏感性报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S16Stage1力相位一帧偏移敏感性.md)、GPT 交接文档/状态及 `index.md`；未选定偏移，未修改生产同步数据或释放参数。
- 验证：零偏移复算回到报告基准 E/RMS；三种情形均使用 41 帧、82 个残差标量。状态 JSON 和相对链接后续验收。
- 下一步：在继续诊断前，保持目前照片—力配对；优先获取硬件同步/相机时间证据，若无则将该偏移幅度作为条件不确定性，而不通过最小化同窗残差“校准”时间。

## [2026-09-29] analysis | S21/S22 subset 内缩敏感性域与力索引新鲜度

- 来源：S21/S22 Job 元数据、当前 DIC—力索引、有限变形 J2 域构造代码及已生成的双域窗口结果。源 Job、DIC、照片和力资料只读。
- 方法：按用户决定固定完整 Job ROI 为主域，检查现有 subset 域的三角形交叠权重；将新敏感性定义为以 Job subset 支持半宽内缩 Job Polygon 后与共同有效 DIC 三角网格求交。两域保留相同的完整 Job ROI 边界适配虚场，敏感性外功沿用完整 ROI 机器合力。
- 结果：S21/S22 Job 均记录 subset size `15 px`、step `3 px`，半跨度 `7 px`，标定后半宽约 `0.614012/0.583331 mm`。旧有限变形 J2 主/子域分别有 `15,007/10,062` 个非零积分三角形，最大面积权重差仅 `7.01×10⁻¹³/5.84×10⁻¹³ mm²`，因此旧分支不构成独立内缩域敏感性。当前索引相较 HEAD 将 S21 `000010.jpg` 从 `0/0` 改为 `78.95/0 N`，将 S22 `000008.jpg` 从 `0/0` 改为 `0/80.8 N`；Stage 1 E 窗口未包含这些行，已有 Stage 2 拟合包含这些行，旧 Y/H 输出过期。
- 更新：总体方法协议、边界载荷说明、GPT 交接文档/状态、`index.md`。未修改 VFM runner、checker/test、配置、力索引或旧拟合工件。
- 下一步：按 Job subset 支持半宽实现真正内缩域，再用现行 S21/S22 力索引重跑 Stage 2；分开报告主域与敏感性域，不发布正式参数或训练标签。

## [2026-09-29] analysis | S16 原始 Press 亚帧时间偏移敏感性

- 来源：S16 原始 `Press` 工作表、现行全场—力索引、完整 Job ROI 逐帧虚功诊断及同步时间公式；全部只读。
- 方法：按事件起止 `0.102–25.834 s` 和帧号 `000001–000257` 重建完整精度时间轴；对原始 X/Y Press 通道基线校正后，在 `t_photo+δ` 处线性插值，扫描 `δ=−50…+50 ms`、步长 5 ms。
- 零偏移核对：原始曲线插值与索引力最大差 `5.0000017×10⁻⁷ N`，拟合窗内与虚功诊断外力最大差 `4.9999954×10⁻⁷ N`；基准 E/RMS 复现。CSV 时间显示舍入误差最多 `50 μs`，解释了为何不能直接从 4 位小数时间重插值。
- 结果：`±5 ms` 时条件 E 变化 `−0.1649%/+0.1451%`，RMS 变化 `−1.3397%/+1.5194%`；`±50 ms` 时 E 约 `±1.64%`，RMS `−11.52%/+12.42%`。±1 个精确照片间隔 `0.100515625 s` 的原始 Press 重采样与相邻索引行结果一致。
- 更新：[亚帧偏移报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S16原始Press亚帧时间偏移敏感性.md)、一帧敏感性报告、GPT 交接文档/状态及 `index.md`。未修改原始数据、现行同步、VFM 力值或生产配置；未选取最小 RMS 偏移。
- 下一步：将亚帧偏移仅作为条件同步敏感性；需要真实相机时钟/触发证据确定绝对配对，不从同窗 VFM 残差反推同步。

## [2026-09-29] query | PA12 名义应力的截面积口径

- 来源：批次配置、`tools/pa12_mechanics.py`、`tools/pa12_sync.py`、S15–S23 九份应力—应变 CSV 与 REV B 几何尺寸记录；原始试验资料保持只读。
- 结论：现有 CSV 的应力为各轴同步力除以 `30 mm × 1 mm = 30 mm²`，不是除以 `30×30 mm²`。图纸中的 `30×30 mm` 是减薄区的平面外边界，中心平坦区约 `28×28 mm`；这些平面尺寸不能直接当作截面积。若要报告中心截面的名义应力，应使用载荷法向上的实际净承载宽度乘局部厚度；狭缝穿过截面时按剩余韧带宽度计。现有配置没有单独的狭缝净宽字段，所以该曲线口径尚不能称为逐件验证的狭缝净截面应力。十字双轴试样中，狭缝/减薄几何及载荷比例还可能影响中心应力，`F/A` 应标作名义近似，局部应力需用对应几何的 VFM/有限元场确定。
- 更新：[PA12 实验总体方法与防跑偏协议](Agents/PA12实验数据处理/处理记录/PA12实验总体方法与防跑偏协议.md)、`index.md`。
- 后续：如需把曲线改为中心平坦区或狭缝净截面口径，先依据对应样件的图纸/实测几何确认截面，再重算派生曲线；当前诊断曲线不回写原始力数据。

## [2026-09-29] analysis | S16 MatchID 工程文件同步时间元数据复核

- 来源：S16 `Job.m2inp`、`xy_0.2_289.mti`、`xy_2try_step1.mti`，本机 MatchID 2019 安装说明；全部只读。
- 方法：检查 Job 文本中有语义的时间/帧率/触发字段，读取两份 MTI 的帧名及数值标签，并用 MinerU 标准解析五页安装说明。
- 结果：Job 只见相机内参块；两份 MTI 有 `000000–000257.jpg` 帧名，但 `<19>=0.001`、`<22>=100` 等标签没有本地字段定义；安装说明不包含 MTI 时钟字段说明。未获得相机硬件时钟、真实 FPS 或触发证据。
- 判定：不把未定义数字标签推断成采样间隔/FPS，不改变 S16 时间轴或 VFM 数据；当前照片时刻仍由力事件起止和帧序号推算。
- 更新：[S16 亚帧时间偏移敏感性报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S16原始Press亚帧时间偏移敏感性.md)、GPT 交接文档/状态、`index.md`。
- 下一步：需要独立相机时间戳、触发/共同时间基记录，或带标记的低载荷微动试验才能提升同步状态；在此之前仅保留条件敏感性，不以拟合残差校准时间。

## [2026-09-29] query | 截图中的 PA12 拍摄—力传感器表与后续数据入口

- 来源：用户截图；`force_inventory.csv`；`PA12实验数据处理/实验概览/`、`处理记录/` 输出目录。原始 JPG、DAT、XLS 保持只读。
- 结论：截图没有在当前工作区保存为同名独立表格；其中 `36244/36.300 s`、`27980/28.049 s`、`511/0.510 s`、`4570/4.576 s` 四组力计数和结束时间分别对应 `xy-1-0.1`、`xy-2-0.1`、`xy-3-10` 和 `xy-04-1 ...113003.xls` 原始状态文件。截图照片数属于早期摘要口径，不等于当前配对帧或 VFM 行数。
- 更新：[PA12 照片—力同步与 VFM 生成](wiki/PA12照片力同步与VFM生成.md)、`index.md`；记录当前汇总 Excel/CSV、批量清单和报告的直接入口。未修改原始试验数据。
- 待验证：若需要重建截图的实际频率和照片位移四列，还需确认当时使用的照片时间戳/帧间隔口径；当前仅凭 JPG 数量和力文件终点不能唯一重建这些数值。

## [2026-09-29] query | PA12 照片数量口径

- 来源：`PA12批量处理清单.csv`、`旋转序列—力文件映射.csv`、DIC 清单 `dic_inventory.csv`。
- 结论：相机 JPG 总数、同名 JPG+DAT 配对数和当前同步/诊断窗口内的有效照片数不是同一指标。`photo_count` 使用第三种口径；例如 S15 为 `289/286/284`，S18 为 `267/249/126`。减少来自缺 DAT、参考帧、断裂证据帧、力学事件窗口和稀疏 DIC 配对，不代表相机少拍。
- 更新：[PA12 照片—力同步与 VFM 生成](wiki/PA12照片力同步与VFM生成.md)、`index.md`；补充十组试样的三种照片数量和解释。原始照片、DAT、XLS 未修改。
- 下一步：后续主表默认只展示当前有效照片数；需要核对实际拍摄量时单独查看 JPG 总数。

## [2026-09-29] query | 核心照片数量采用实际拍摄口径

- 来源：用户确认“只需要核心的照片数量”，并指出其与实际拍摄数量不一致。
- 结论：核心照片数量改用正式来源目录中的 `JPG 总数`；`JPG+DAT 配对数`和`当前有效照片数`只作为 DIC/同步分析说明，不再替代拍摄总数。
- 更新：补充照片数量口径说明；原始照片、DAT、XLS 和既有分析输出未修改。

## [2026-09-29] query | 单轴虚位移图片、数据与拟合原理

- 来源：S19–S22 当前有限变形 VFM 诊断摘要、逐帧虚功 CSV/PNG、仿射虚场实现和用户展示需求。
- 结论：当前主拟合使用仿射单位虚位移场 `φq=q/Lq`；阶段 1 返回条件 `E`，阶段 2 只保留诊断候选。四组主域条件 `E` 为 S19/S20/S21/S22=`2577.886/7540.211/9498.399/7816.754 MPa`，均未解除 `REVIEW_REQUIRED`。
- 更新：[PA12 单轴虚位移 VFM 展示](wiki/PA12单轴虚位移VFM展示.md)、四组虚位移场展示图、虚位移场数据 CSV 和拟合摘要 CSV；原始 JPG、DAT、XLS 与既有逐帧结果未修改。
- 限制：展示图是单位虚场/虚功诊断图，不是试样实测位移图；DIC 支持率、边界虚位移等价、机器—DIC 有向坐标和 S22 Jacobian 质量仍未通过正式门槛。

## [2026-09-29] query | 内外虚功相等性解释

- 来源：用户对单轴 VFM 内外虚功图的追问；`wiki/PA12单轴虚位移VFM展示.md`。
- 结论：在准静态平衡、虚场可接受、边界力完整计入且积分域/坐标正确时，内虚功应等于外虚功；当前残差是数值与边界闭合诊断量，不代表原理失效。
- 更新：补充内外虚功相等条件、拟合残差含义和横向内虚功不为零的解释；未修改原始数据和拟合结果。

## [2026-09-29] analysis | 单轴 Stage 1 拟合门槛复算

- 来源：`configs/pa12_self_vfm.json`、S19/S20/S21/S22 当前 DIC—力索引、合并 DIC 场、Job 文件和 Stage 1 结果 JSON；原始 JPG、DAT、XLS 保持只读。
- 方法：按项目主入口自建 VFM 重算 S19、S21、S22，并运行阶段 A 逐帧一致性审计；只在活动加载轴上使用 `ν=0.375`、弹性应变窗和零截距虚功拟合，验收阈值为相对 RMS `≤10%`。
- 结果：S19 `E=5517.118 MPa`、相对 RMS `2.01%`；S21 `E=17419.149 MPa`、`4.85%`；S22 `E=10585.486 MPa`、`8.09%`，三组 Stage 1 均为 `PASS`。S20 的 Job ROI 在 `(39.5806067, 18.6555632)` 自交，既有协议没有授权修复，保持阻断。
- 更新：[单轴虚位移 VFM 展示](wiki/PA12单轴虚位移VFM展示.md)、[Stage 1 拟合验收 CSV](Agents/PA12实验数据处理/VFM自建/汇总/PA12单轴阶段1拟合验收.csv)、`index.md`；保留有限变形支线为独立诊断，不把其未通过/旧结果混入主拟合。
- 验证：S19/S21/S22 的逐帧自建 VFM 一致性审计无失败；全批审计仅报告 S20 几何阻断。Stage 1 通过不等于单轴物理边界和材料参数正式放行。
- 下一步：后续阶段可从 S19/S21/S22 的 Stage 1 条件 `E` 继续；S20 需用户授权具体 ROI 修复方法或提供有效 Job ROI。

## [2026-09-29] experiment | TC1000 H0.35 竖直加载比矩阵与 U3 约束诊断

- 来源：D:\PA12_Stage2\g0_tc1000_h0p35_vertical_ratio_matrix_20260929\ 的参数化 Abaqus INP、ODB、原始矩阵结果；D:\PA12_Stage2\g0_tc1000_h0p35_u3_fixture_diagnostic_20260929\ 的三案输入、求解日志与 IVOL/局部峰值后处理。
- 方法：基于同一网格和临时正交弹性卡建立 r=ΔY/ΔX 为 0.5/1/2 的统一诊断矩阵，固定 ΔX=0.05 mm，仅改变 ΔY；四个夹持参考点 U3=0。每案 506,171 节点、316,201 个 C3D10 单元、中心 28×28 mm ROI。
- 结果：三案均 1 增量、3 次平衡迭代完成；分析数值警告、负特征值和错误均为 0，仍各有 60 个畸变单元。PrimaryScore/K 分别为 r=0.5: 0.150687/0.538864、r=1: 0.108882/0.0000463、r=2: 0.153564/0.538604。r=1 仅在当前候选诊断中最均衡，不作最终试样排名。
- 对照：在同一 r=0.5 输入上补齐三个夹持参考点 U3 后，1 条数值奇异与 1 个负特征值警告均消失；中心面内指标变化接近数值精度，畸变单元数不变。该结果支持奇异模态与面外自由度有关，但不能证明真实夹具采用 U3=0。
- 更新：[研究报告](Agents/PA12双轴试样仿真/验证/2026-09-29_TC1000_H0P35_竖直加载比矩阵与U3约束诊断.md)、索引、三比例 CSV/JSON、对比图和模型截图。完整 Abaqus 工件均保存在上述 D 盘目录。
- 限制与下一步：显式草图尚未通过源 STEP 回归，材料仅为临时弹性卡，60 个畸变单元未解决；先核实真实夹具面外运动并处理几何/网格门槛，再讨论正式载荷比、塑性响应和 DIC/VFM 参数可识别性。

## [2026-09-29] experiment | S21/S22 Job ROI 与 subset 支持内缩复算

- 来源：S21_X_20、S22_Y_0.2 当前 DIC—力索引、Job 几何与 subset 元数据；`configs/pa12_finite_vfm_s21_subset_support_20260929.json`、`configs/pa12_finite_vfm_s22_subset_support_20260929.json`、`configs/pa12_finite_j2_s21_subset_support_20260929.json`、`configs/pa12_finite_j2_s22_subset_support_20260929.json`。
- 更新：按完整 Job ROI 主域和 DIC subset 支持内缩敏感性域，分别完成 Stage 1 固定 `ν=0.375` 的条件 E 及 Stage 2 Linear J2 三窗口复算；新增[复算报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S21_S22_JobROI与subset支持内缩敏感性复算_20260929.md)，更新交接文档、状态 JSON 与索引。旧输出保留未覆盖。
- 结论：S21 的 `Y0/H` 对窗口高度不稳定且 75% 窗口 Jacobian 秩为 0/2；S22 的 `H` 随峰前窗口明显变化。完整 ROI 与 S22 内缩域支持率不足，所有参数保持诊断候选。
- 待验证：完整 ROI 实测覆盖、机器—DIC 有向坐标及外虚功边界等价；当前不释放正式参数或代理模型标签。

## [2026-09-29] maintenance | Abaqus 派生工件归档与 D 盘运行约定

- 来源：C 盘 Abaqus 派生目录、根目录运行工件、D 盘 G0 求解目录与 `run_scan.ps1`；原始实验数据保持只读。
- 更新：108 个 Abaqus 派生文件集中归档到 `D:\PA12_Stage2\migrated_from_C_20260929\`，旧路径保留为 D 盘目录联接；将 `run_scan.ps1` 的运行副本、输入、输出、工作目录和临时目录统一到 D 盘，并更新全流程协议、GPT 交接文档及状态、索引。
- 结果：归档后 C/D 可用空间分别为 `25.56/127.93 GB`。Windows 自动分页文件仍在 C 盘，C 盘 `50 GB` 目标尚未达到；当前未改分页文件/转储设置，未重启。详见[Abaqus D 盘归档与空间核查](AGENTS/PA12双轴试样仿真/验证/2026-09-29_Abaqus生成数据D盘归档与空间核查.md)。

## [2026-09-29] experiment | S21/S22 精确 15×15 像素 subset 支持内缩复核

- 来源：S21/S22 Job subset 元数据、当前 DIC—力索引、当前阶段 1 条件 E、有限变形 J2 runner 与隔离复算输出；原始 JPG/DAT/XLS 保持只读。
- 方法：按用户选定的完整方形 subset 支持定义，将完整 Job Polygon 与 `15×15` 像素中心的全部 `−7…+7 px` 整数偏移求交，再与共同有效 DIC 三角形支持域求交；完整 Job ROI 仍为主域，内缩敏感性仍沿用完整 ROI 机器合力。
- 结果：S21/S22 各完成主域及内缩域 50/75/100% 三窗口 Linear J2 复算。S21 75% 窗口 Jacobian 秩为 `0/2`，其他窗口参数不稳定；S22 的 `H` 随历史窗口从约 `127–128` 增至约 `265 MPa`。Stage 1 覆盖率 S21 主/内缩 `84.12%/97.84%`、S22 `71.20%/82.85%`。结果不释放正式材料参数或训练标签。
- 更新：[S21/S22 复算报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S21_S22_JobROI与subset支持内缩敏感性复算_20260929.md)、隔离输出和配置、GPT 交接材料、`index.md`。
- 下一步：继续逐组核实实际 ROI 覆盖、机器—DIC 有向坐标与边界外功证据；不以高支持率内缩域替代完整 Job ROI。

## [2026-09-29] analysis | S19 E量级与厚度/积分域复核

- 来源：S19 Stage 1 结果 JSON、逐帧内外虚功 CSV、`tools/pa12_self_vfm.py`、`PA12实验总体方法与防跑偏协议.md`，以及两篇本地 PA12 论文的 MinerU 定位结果。
- 方法：按 `000003–000026.jpg` 的 24 个弹性点复现零截距拟合；检查虚功系数中的厚度因子；量化 Job Polygon 等效宽度和 DIC 积分覆盖率；对照论文报告的 PA12 弹性模量量级。
- 结论：`E=5517.118 MPa` 在当前输入下数值可复现，但属于 `t=1 mm` 的条件值。因 `E∝1/t`，若仅把厚度改为 `3 mm`，结果为 `1839.039 MPa`；这不是对真实厚度的自动判定。当前 Polygon 几何等效宽度约 `10.241 mm`，最低积分支持率约 `84.86%`，单轴有效宽度、完整受力域和外功边界仍未闭合。论文结果主要在 `900–2300 MPa` 范围，典型值约 `1620–1680 MPa`，因此暂不把 `5517.118` 发布为材料模量。
- 更新：修正 Stage 1 汇总中 S19 的拟合帧数为 `24`，在[单轴虚位移 VFM 展示](wiki/PA12单轴虚位移VFM展示.md)登记厚度敏感性和文献量级对照；原始 JPG、DAT、XLS 和原始论文未修改。
- 待验证：S19 实测厚度、垂直加载方向的有效宽度、Job Polygon 是否代表完整受力域，以及对应的外功边界。

## [2026-09-29] analysis | S19 厚度 3 mm 条件重算

- 来源：S19 弹性段 `000003–000026.jpg`、逐帧内外虚功 CSV、项目厚度协议和 S19 原始目录文件清单。
- 方法：仅将 Stage 1 虚功系数按厚度从 `1 mm` 线性改为 `3 mm`，重新进行零截距拟合；不覆盖 1 mm 主结果。
- 结果：条件 `E=1839.039 MPa`，RMS `5.257 N`，最大残差 `9.188 N`，相对 RMS `2.01%`，数值门槛 `PASS`。该量级落在两篇本地 PA12 文献的报告范围内，但仍依赖 S19 实物确为 `3 mm`、当前积分域和外功边界成立。
- 更新：[S19 厚度 3 mm 条件重算 CSV](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S19_t3mm条件重算.csv)及[单轴虚位移 VFM 展示](wiki/PA12单轴虚位移VFM展示.md)；原始 JPG、DAT、XLS、`.vfm` 和论文未修改。
- 待验证：由样件实测或对应图纸确认 S19 单轴厚度；当前原始目录未见独立厚度证据。

## [2026-09-29] experiment | S19 实测厚度确认后的 3 mm 主口径重算

- 来源：用户确认 S19 实物厚度为 `3 mm`；`configs/pa12_self_vfm.json` 的实验级厚度覆盖；S19 DIC—力索引、Job 几何和原始 JPG/DAT。
- 更新：新增 `S19_X_0.2: 3.0 mm` 实验级厚度覆盖；S19 独立重算输出保存于 `实验结果_S19_t3mm重算_20260929`，未改变 S21/S22 的 `1 mm` 工作值。
- 结果：S19 Stage 1 `E=1839.039 MPa`，25 帧弹性窗口/24 个非零回归点，RMS `5.257 N`，最大残差 `9.188 N`，相对 RMS `2.01%`，数值门槛 `PASS`。E 的量级与本地 PA12 文献报告相符。
- 状态：S19 厚度门槛已关闭；单轴有效宽度、Job Polygon 是否代表完整受力域、DIC 覆盖率和外功边界仍使结果保持 `SELF_VFM_SENSITIVITY_ONLY`，不发布正式材料卡或正式 Y/H。

## [2026-09-29] rule | 同一模型的共享参数拟合口径

- 来源：用户确认的项目拟合规则；单轴/双轴 VFM 结果页和总体方法协议。
- 规则：同一数据集、同一模型、同一窗口、同一输入和同一目标函数必须复现同一组参数；若要发布一个单轴或双轴材料常数，应将通过准入的该类数据合并后做一次共享参数拟合。不同试样的分别拟合只作诊断，不并列称为最终材料值；同一数据集换模型才用于模型差异比较。
- 当前状态：S19/S21/S22 的逐试样 E 暂保留为诊断值；统一单轴/双轴共享拟合待几何、坐标和外功门槛闭合后执行。

## [2026-09-29] analysis | S19 有效宽度、积分域与外功边界敏感性

- 来源：S19 `t=3 mm` 重算 JSON/逐帧 CSV、Job Polygon 几何和当前 Stage 1 虚功公式。
- 结果：逐点积分等效宽度约 `8.691 mm`，完整 Polygon 面积折算宽度约 `10.241 mm`，最低 DIC 积分覆盖率 `84.86%`。若在均匀应变假设下补足当前漏区，E 约为 `1560.643 MPa`；若错误地把总力对应的有效宽度直接取为 `30 mm`，敏感性值约为 `532.752 MPa`；这些都不是正式修正。
- 外功边界：当前 X 外虚功直接取同帧机器总力，Y 外虚功取零；若真实广义外力为当前输入的 `0.8/1.2` 倍，E 线性变为约 `1471.2/2206.8 MPa`。三项口径相互耦合，不能用单一比例同时修正。
- 结论：S19 `E=1839.039 MPa` 仅表示当前厚度、积分域、有效宽度和外功假设下的条件结果；正式共享参数拟合前必须确认三项物理口径。

## [2026-09-29] analysis | S21/S22 输入与 15 px subset 内缩域审计

- 来源：[S21/S22 照片—力表、帧—力—时间索引、DIC 全场—力索引、DIC 元数据、DAT 逐帧审计和原始 Press 工作簿](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S21_S22输入与subset内缩域门禁审计_20260929.md)。
- 更新：[S21/S22 输入与 15 px subset 内缩域审计](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S21_S22输入与subset内缩域门禁审计_20260929.md)。
- 结论：力值可从原始 Press 数据复算；照片时间仍由候选频率和力事件端点推算，首张有效照片力不接近零；机器—DIC 有符号变换未独立确认。15 px subset 半宽 7 px 的敏感性域及共同 DIC 网格支持面积已单独核算；旧 `.50/.75` 结果不作为新域证据。
- 下一步：取得可靠相机时间戳/硬件同步事件和有符号坐标标定；完成前不启动新的 Stage 2 拟合。

## [2026-09-29] analysis | S21/S22 旧 J2 输出与现行力索引差异复核

- 来源：S21/S22 当前 DIC—力索引、早期完整 Job ROI 与精确 15 px subset 内缩复算的逐帧虚功 CSV，以及对应 J2 摘要。
- 方法：逐照片对照当前活动轴力与早期/现行输出的外虚功；核对两次复算使用的边界适配虚场、厚度、固定 E/ν 和拟合窗口。
- 结果：S21 `000010.jpg` 当前 X 力为 `78.95 N`，早期输出该帧 X 外虚功为 `0 N`，现行输出为 `78.95 N`；S22 `000008.jpg` 当前 Y 力为 `80.8 N`，早期输出为 `0 N`，现行输出为 `80.8 N`。早期拟合使用过期力输入，其 Y/H 与残差不得作为现行索引结果；后续精确内缩复算报告为当前双域诊断的依据。两组照片—力绝对同步和有向坐标仍未证实，参数继续诊断-only。
- 更新：[输入与内缩域审计](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S21_S22输入与subset内缩域门禁审计_20260929.md)；原始数据与历史输出均保留。
- 下一步：不重复 S21/S22 三窗口拟合；先取得独立同步/坐标证据并核实完整 Job ROI 的实测覆盖，再决定正式参数识别放行。

## [2026-09-29] analysis | S21/S22 合并场力列与 Pos—DIC 时序对照

- 来源：S21/S22 现行 DIC—力索引、全部合并场 CSV、原始 Press 工作簿 Pos 页、`000000.jpg.dat` 参考场、当前 VFM runner 与 `.mti` 工程文件。
- 方法：逐照片比较合并场 CSV 首行 X/Y 力与索引；读取各 VFM runner 的力值来源；在索引候选时轴上比较两夹头相对 Pos 位移与 DIC ROI 两端 2 mm 条带的 `v` 中位数差。
- 结果：合并场 CSV 与索引仅两帧力列不一致：S21 `000010.jpg` 为 `0/0` 对 `78.95/0 N`，S22 `000008.jpg` 为 `0/0` 对 `0/80.8 N`；其余行差小于 `1×10⁻⁶ N`。三个自建 VFM runner 均从正式索引取力，现行 VFM 诊断使用了更新值，但合并场显示列尚未刷新。Pos—DIC 轴向开口趋势 R² 为 S21 `0.97066`、S22 `0.99949`，两组无唯一时间事件锚点；这些结果支持趋势相容，不证明绝对同步。
- 更新：[S21/S22 输入与内缩域门禁审计](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S21_S22输入与subset内缩域门禁审计_20260929.md)。未改写原始文件、索引或合并场 CSV。
- 下一步：将两份合并场 CSV 的力列刷新列入数据输出维护；在取得硬件触发/相机时间记录前，照片—力绝对同步继续标为未证实，所有参数保持诊断候选。

## [2026-09-29] maintenance | S21/S22 合并场重复力列与索引对齐

- 来源：S21/S22 当前 DIC—力索引及对应派生合并场 CSV；原始 JPG/DAT 未改写。
- 更新：按索引更新 S21 `000010.jpg` 的 7,769 个点行至 `78.95/0 N`，S22 `000008.jpg` 的 6,166 个点行至 `0/80.8 N`；DIC 坐标、位移、应变、时间、行数和索引均保持不变。更新审计页，并从已索引的复算报告链接到该审计页。
- 结论：此前合并场与索引的两处重复力列差异已消除；VFM runner 仍以正式索引为力值来源。照片—力绝对同步及机器—DIC 有向坐标未因此得到证明，S21/S22 参数继续保持诊断候选。
- 下一步：继续优先闭合相机时间/共同触发证据、机器—DIC 有向标定和完整 Job ROI 实际覆盖门槛；不重复已完成的 S21/S22 双域三窗口拟合。

## [2026-09-29] analysis | S15 完整 Job ROI 与 13 px subset 内缩双域复核

- 来源：S15 Job subset/step 元数据、现行 284 帧 DIC—力索引、完整 Job ROI 边界适配配置与自建有限变形 VFM 输出。
- 方法：保持基准配置的原始输入、参考场和拟合窗，仅隔离输出目录；主域为完整 Job ROI，独立敏感性域按 subset 中心偏移 `−6…+6 px` 内缩，并与共同有效 DIC 三角形精确求交。两域使用完整 ROI 边界适配虚场与机器合力。
- 结果：主域覆盖率 `88.9256%`，内缩域 `95.7856%`；两域 DIC 支持面积相同、各有 284 帧，虚功序列一致至 `5.83×10⁻¹¹ N`。固定 `ν=0.375` 的条件 `E=4137.466 MPa`，相对 RMS `31.17%`，不放行参数；拟合窗 48 帧无非正 Jacobian，全历程 27 帧有非正事件。
- 更新：[S15 双域复核报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S15完整JobROI与13pxsubset内缩域敏感性复核_20260929.md)、[边界载荷说明](Agents/PA12实验数据处理/MatchID_VFM准备/PA12_VFM边界载荷说明.md)、[GPT 交接文档](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)及交接状态 JSON；`index.md` 新增报告入口。方法协议已含相同域定义，本次未改写。
- 下一步：核实完整 ROI 实际几何/厚度 containment、机器—DIC 有向坐标、绝对同步与外功边界物理证据；定位全历程非正 Jacobian 事件，再判断后续参数识别窗口。

## [2026-09-29] analysis | S15 Jacobian 与全历程虚功适用性复核

- 来源：S15 当前双域逐帧虚功 CSV、逐帧运动学质量 CSV、自建 VFM runner/积分器，以及既有仅统计正 Jacobian 单元的运动学审计。
- 方法：追踪最大 Euler–Almansi 质量列与内虚功积分的单元筛选条件；按首个 `det(F)≤0` 帧分段汇总现有残差，仅作输出诊断。
- 结果：runner 两处均未对非正 Jacobian 单元作筛选。首个翻转在 `000206.jpg`；27 帧含 154 个非正事件。拟合窗 `000002–000049.jpg` 无事件，最小 `det(F)=0.528218`，条件 `E=4137.466 MPa` 的数值不因该门槛变化，但相对 RMS=`31.17%`，仍不放行。末帧全单元应变最大值 `3503.578` 与旧审计正 Jacobian 子集值 `1249.0717` 是筛选口径差异。`000261.jpg` 的残差峰 `178724 N` 与最小 `|det(F)|=0.001630`、2 个非正单元同帧出现；无单元级功贡献分解，未据此断定单一根因。后段全域虚功曲线和残差不作为物理闭合证据；正但近退化单元仍待定量门控。
- 更新：[总体方法协议](Agents/PA12实验数据处理/处理记录/PA12实验总体方法与防跑偏协议.md)、[GPT 交接记录/状态](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、[边界载荷说明](Agents/PA12实验数据处理/MatchID_VFM准备/PA12_VFM边界载荷说明.md)和 `index.md`。未改 runner、检查脚本、配置、原始数据或 S15 输出。
- 下一步：全 ROI 含非正 Jacobian 的帧须先标为运动学无效；不静默删单元或自设正 Jacobian 截断值。恢复全历程物理解释前，需实现并验证帧级门槛及近退化单元敏感性；`Y/H` 与训练标签保持未发布。

## [2026-09-29] audit | 自建线弹性 VFM Jacobian 影响范围

- 来源：`VFM自建/` 下 25 份现存逐帧运动学质量 CSV、自建线弹性有限变形 runner/积分器，以及既有 S15、S22 运动学审计。
- 方法：按实验和输出版本读取非正 Jacobian 帧数、事件数、首发帧及最小 `|det(F)|`；不重跑 DIC/VFM，不把重复输出计为独立样本。
- 结果：S15 的四份输出均含异常；三个标准参考版本各为 27 帧/154 事件，参考 `000000.jpg.dat` 的版本为 24 帧/149 事件。S22 的四份输出各为 7 帧/15 事件，首帧 `001512.jpg`。现行 runner 将异常单元纳入全域内虚功和应变极值；S15、S22 的 Stage 1 拟合照片未含非正事件。S16、S17、S18、S19、S21、S23 的已存 CSV 未见非正事件。该结论只涵盖线弹性有限变形 runner，不涵盖 J2 runner。
- 更新：[总体方法协议](Agents/PA12实验数据处理/处理记录/PA12实验总体方法与防跑偏协议.md)、[交接文档/状态](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、[边界载荷说明](Agents/PA12实验数据处理/MatchID_VFM准备/PA12_VFM边界载荷说明.md)与 `index.md`。S22 原有位置和 DIC 时序报告未重做或覆盖。
- 下一步：确定无效帧物理列与原始诊断值的输出契约；完成后以回归测试验证帧级门槛，仅隔离重跑受影响的 S15/S22 线弹性 VFM 输出。J2 runner 另行盘点，不先外推此结论。

## [2026-09-29] audit | 有限变形 J2 非正 Jacobian 门槛

- 来源：`tools/pa12_finite_j2.py` 的批量平面应力更新器与历史虚功积分器、`tests/test_pa12_finite_j2.py`、S22 当前 Linear J2 主域/内缩域摘要，以及 S22 逐帧运动学质量审计。
- 结果：J2 更新器对参与积分的面内 `det(F)≤0` 直接抛错；积分器逐帧传递参与单元，不静默删单元。异常帧没有单独的无效输出行，遇到异常将停止该次 J2 积分。当前 S22 两域 J2 历史均为 188 帧、终点 `001504.jpg`，早于线弹性质量审计的首个非正事件 `001512.jpg`。当前 J2 测试未见专门验证该拒绝门槛的断言。
- 更新：[总体方法协议](Agents/PA12实验数据处理/处理记录/PA12实验总体方法与防跑偏协议.md)、[GPT 交接文档/状态](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、`index.md`。未改 J2 源码、测试、配置、实验输入或已有输出。
- 限制：源码门槛只证明实现拒绝非正 Jacobian，不证明正但近退化三角形稳定，也不补足 DIC 覆盖、几何、同步、坐标或外虚功证据。
- 下一步：线弹性 VFM 的无效帧物理输出契约仍待确认；确认后按获批口径增加回归测试并隔离重算 S15/S22。若 J2 之后要扩展到已知异常帧，按 J2 当前失败快停行为单独处理，不把失败帧误记为有效残差。

## [2026-09-29] analysis | S15 000261 单元虚功贡献与局部位移复核

- 来源：S15 完整 Job ROI 条件诊断、284 帧 DIC—力索引、逐帧质量 CSV、13 px 内缩敏感性输出。
- 方法：保持完整 Job ROI 主域和生产边界适配虚场，固定条件 E/ν、厚度及精确三角交叠权重；对六个代表帧分解单元 `P:grad(v*)` 虚功并与现有逐帧 CSV 回加核对；对照 284 帧完整域与内缩域。
- 结果：单元回加最大差 `5.30×10⁻⁹ N`。`000261.jpg` Y 残差 `−178724.416 N` 中，三角形 48081（正 `detF=0.0016304854`）单元贡献 `−191387.290 N`，占单元绝对贡献 `91.9586%`；两枚非正 Jacobian 单元仅占 `0.0109%`。该单元两个顶点的机器 Y 位移在中间帧跳变并于下一帧回落，物理/算法来源仍未确定。完整 ROI 与内缩域 284 帧虚功差最大 `5.82×10⁻¹¹ N`，外力序列相同，因此当前内缩分支不改变数值积分结果。
- 更新：[双域与单元分解报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S15完整JobROI与13pxsubset内缩域敏感性复核_20260929.md)、[单元摘要 CSV](Agents/PA12实验数据处理/VFM自建/有限变形诊断_S15_13pxsubset有效支撑复算_20260929/S15_XY_0.2/单元虚功贡献分解摘要_20260929.csv)、[Top-5 CSV](Agents/PA12实验数据处理/VFM自建/有限变形诊断_S15_13pxsubset有效支撑复算_20260929/S15_XY_0.2/单元虚功贡献Top5_20260929.csv)、方法协议、GPT 交接文档/状态、边界载荷说明及 `index.md`。
- 下一步：核查主导三角形三个节点在 `000260–000262.jpg` 的 DIC 相关结果和位移导出来源；不删点、不设 Jacobian 截断值，不放行 E、Y/H 或训练标签。

## [2026-09-29] audit | S15 000261 DAT 位移与原图局部相关核验

- 来源：S15 原始 `000000/000260/000261/000262.jpg` 与同名 `.dat`、当前合并 DIC CSV、完整 Job ROI 生产网格及三角形 48081。
- 方法：按 97,422 点共同网格复现三角形节点；核对原始 DAT 与合并 CSV 的逐点 `u/v`；以 Job 参考图 `000000.jpg` 锚定像素坐标，再以 13×13 模板检查 `000000→000260` 和 `000260→000261→000262` 的局部相关峰。未写出或修改任何图像、DAT、CSV或VFM输入。
- 结果：`000000→000260` 三节点图像位移与 DAT 预测一致至 `0.71–0.94 px`；但 `000261.jpg` 两异常节点的相邻帧 DAT 位移预测约为正负 `2.1–2.5 px`，局部高 NCC 峰偏离预测 `2.1–3.0 px`。证据支持两节点 DAT 位移与原图局部纹理不一致；不确定来源，不是 DIC 算法错误定论。完整 Job ROI 保持主域，subset 内缩仍独立作敏感性。
- 更新：[S15 双域与 000261 审计报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S15完整JobROI与13pxsubset内缩域敏感性复核_20260929.md)、[总体方法协议](Agents/PA12实验数据处理/处理记录/PA12实验总体方法与防跑偏协议.md)、[GPT 交接文档/状态](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、`index.md`。
- 限制：局部模板重叠且峰值只定位到整数像素，未重跑 DIC；结果只用于局部图像一致性审计。不得据此删点、截断 Jacobian、识别 `Y/H` 或生成训练标签。
- 下一步：核对异常节点邻域 MatchID 原始质量字段和逐点位移（在字段语义确认前仅记录原值），然后继续完成实物 ROI/厚度 containment、机器—DIC 有向坐标、绝对同步和外功边界核验。

## [2026-09-29] analysis | S15 000261 邻域场与同步力对照

- 来源：S15 原始 DAT `000259–000263.jpg.dat`、76 个共同有效邻域点、同一照片—力索引。
- 方法：统计局部 11×11 像素窗口的逐点 `Δu/Δv`、DAT 原始 `r/sigma` 数值分位和 `000260–000262.jpg` 对应同步力；未将未核准字段解释为质量指标。
- 结果：异常节点的 `Δu` 在 76 点邻域中位于最极端的 1–3 位；`r/sigma` 数值相对局部分布持续偏离但语义未证实。同期 X/Y 力增量平滑（`0→+1.5 N`、`+1→+1 N`），没有对应整体力脉冲。局部 DAT/原图不一致得到进一步支持，根因仍未定。
- 更新：[S15 双域与 000261 审计报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S15完整JobROI与13pxsubset内缩域敏感性复核_20260929.md)、[总体方法协议](Agents/PA12实验数据处理/处理记录/PA12实验总体方法与防跑偏协议.md)、[GPT 交接文档/状态](Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md)、`index.md`。
- 下一步：核实 MatchID 同版本 `r/sigma` 字段定义，再继续完成实物 ROI/厚度 containment、机器—DIC 有向坐标、绝对同步及外功边界证据；不删点、不设无依据阈值、不放行 `Y/H` 或代理训练标签。

## [2026-09-29] query | S15 DAT `r/sigma` 字段语义

- 来源：项目 `raw/`、PA12 MatchID 准备记录及 S15 DIC 元数据。
- 结果：本地仅找到 `<18>` 第 13/14 字段位置映射及其与同版本 Results Viewer 的数值交叉验证记录，没有 `r/sigma` 的定义文档。字段值继续按原始数值记录，不解释为相关质量或不确定度。
- 更新：[S15 双域与 000261 审计报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12_S15完整JobROI与13pxsubset内缩域敏感性复核_20260929.md)、[GPT 交接状态](Agents/PA12实验数据处理/处理记录/PA12_GPT交接状态.json)。
- 待验证：如需解释该字段，取得 MatchID 2D 19.2.2.0 同版本定义或 Results Viewer 字段说明；在此之前不对字段语义作判断。

## [2026-09-29] decision | 两方向紧急目标分配

- 来源：用户关于“根据规划和目标，按紧急程度分配两个方向目标”的最新要求；`wiki/PA12项目全景与总控指令.md`、单轴 VFM 展示页、双轴阶段盘点和项目参数合并规则。
- 更新：将当前执行方向固定为 P0 单轴 VFM 闭合与 E/Y/H 合并验收、P1 双轴数据与边界闭合；向“双轴优化参数”和总调度对话发送同一任务入口。
- 结论：单轴先统一 `t=3.000 mm` 并闭合有效宽度、积分域、坐标/单位和外功边界；双轴先统一中心 ROI `t=1.000 mm`、方向/载荷映射和边界口径。两方向均只在门禁通过后合并拟合，各自最终只输出一组 `E/Y/H`；逐试样结果仅作诊断。
- 待验证：单轴 S21/S22 的 `t=3 mm` 重算、S20 ROI 自交、单轴/双轴有效域和外功边界证据，以及各方向合格数据集合。
## [2026-09-29] refactor | 当前任务方向锁定与两个对话纠偏

- 来源：当前用户关于“更新已有方向、避免继续跑偏”的要求；`AGENTS.md`、`wiki/PA12项目全景与总控指令.md`；两个执行对话和总控对话的最新状态。
- 更新：向 `PA12数据合理性独立审计` 发出收束指令，只保留四项 MatchID 人工确认门槛；向 `系统|Wiki搭建` 发出收束指令，只读核对第一阶段六个交付物，不做 VFM 或跨副本同步；更新项目总控页和 `index.md`。
- 结论：当前不创建新的 `.vfm`，不运行虚功/参数识别，不发布 E/Y/H，不修改原始资料、代码、配置或测试；`D:\2026.9.21_finally` 与当前打开的 `D:\C盘迁移\Desktop\yuan\second brain` 是两个独立且均有未提交改动的副本，不能自动同步或覆盖。
- 待验证：S15 的四项 MatchID 人工证据；`D:\C盘迁移\Desktop\yuan\PA12_biaxial_project` 第一阶段六个交付物的齐全性和阶段状态；用户对两个副本后续合并/同步方式的明确选择。

## [2026-09-29] decision | 单轴厚度与合并参数唯一性规则

- 来源：用户最新明确要求；`configs/pa12_self_vfm.json`、PA12 总体方法协议、单轴 VFM 展示页和项目总控页。
- 更新：S19–S22 单轴实物厚度统一登记为 `3 mm`；配置补齐四组单轴厚度覆盖；更新单轴/双轴合并拟合和唯一可复现参数规则，并将 S21/S22 旧 `t=1 mm` E 标为待重算。
- 结论：所有合格单轴数据合并后只输出一组单轴 `E/Y/H`；所有合格双轴数据合并后只输出一组双轴 `E/Y/H`；逐试样拟合只能作诊断；同一数据集、模型、窗口、目标函数、几何/厚度/单位和求解设置必须得到唯一可复现参数，只有更换本构模型才允许不同。
- 待验证：单轴有效宽度、标距、积分域、机器—DIC 坐标和外功边界；S21/S22 按 `t=3 mm` 的重算；合格单轴/双轴数据集成员和合并拟合的最终输出。

## [2026-09-29] decision | 暂停两个执行目标并冻结旧方向

- 来源：用户要求停止无用功、清理过期方向并让两个目标回到正确路线；两个目标的暂停指令和总调度监控状态。
- 更新：两个执行对话改为暂停；总调度仅监控是否继续工作；总控页、阶段计划和首页明确旧的“立即执行/下一步”只作历史计划，不自动恢复。
- 结论：当前不运行 VFM、虚功、参数识别、模型扫描、skill 阅读、代码/配置/测试修改、跨副本同步或删除操作。最新有效规则仍是单轴 `3 mm`、单轴/双轴分别合并拟合各输出一组 `E/Y/H`、逐试样仅诊断、同口径唯一可复现。
- 待验证：两个目标已确认空闲并归档；派生文件清理已完成，原始数据与当前规则保留。

## [2026-09-29] refactor | 清理过期仿真输出并归档执行目标

- 来源：用户授权自行删除不影响总体方向和数据的过期模型、VFM 派生物和文档。
- 更新：删除 `D:\PA12_Stage2` 下 223 个可重新生成的 Abaqus 仿真/诊断输出目录，释放约 66.32 GB；保留 `inputs`、`source_geometry_inspection`、`configs`、`tools`。两个已暂停执行对话归档，历史仍可恢复。
- 保留：`raw/`、`Agents/PA12实验数据处理/MatchID_VFM准备`、`_matchid_export`、当前配置、方法协议、总控页和索引未删除。
- 结论：删除不改变实验原始数据、DIC 数据、当前单轴 3 mm 规则或单轴/双轴分别合并拟合规则；两个执行目标不再自动运行。
- 已知问题：仓库与 Obsidian 当前打开的是两个独立副本，本次未覆盖或删除 Obsidian 副本中的用户改动。

## [2026-09-29] summary | 缺失日期回填与周期总结

- 来源：log.md 中 2026-09-21 至 2026-09-29 的已落盘记录，以及对应 Wiki/验证报告；未把聊天计划作为完成证据。
- 更新：新增 wiki/daily/2026-09-21.md 至 2026-09-29.md、wiki/weekly/2026-W39.md、wiki/weekly/2026-W40.md、wiki/monthly/2026-09.md；在 index.md 增加周期总结入口。
- 结论：日志覆盖的九个日期均已建立日报；W40 与 9 月月报明确标注为截至 2026-09-29 的未完结汇总。原始资料未改写，未触及另一份 Second Brain 副本。
- 待验证：日报只归纳日志和可核实报告中的内容；各条待验证问题仍按原状态保留，不代表相关实验门槛已通过。

## [2026-09-29] refactor | 技术主工作区路径与派生物边界整理

- 来源：`D:\2026.9.21_finally` 的 Git 状态、Markdown 内部链接、`second brain` 副本结构及 PA12 当前任务规则。
- 更新：修正现行入口和协议中把实际目录 `Agents/` 写成 `AGENTS/` 的路径；在 `.gitignore` 中把 `VFM自建` 逐次诊断明细标记为可重建本地输出，仅保留 `VFM自建/汇总` 可追踪；删除两个未被引用的根目录临时 `.sat` 文件和 `S15_XY_0.2/.merge-*` 合并缓存。
- 结论：`D:\2026.9.21_finally` 继续作为 PA12 技术主工作区；`D:\C盘迁移\Desktop\yuan\second brain` 仅作 Obsidian 整理参考。当前执行方向仍锁定为单轴 `t=3 mm`、双轴 `t=1 mm`，分别在门禁通过后合并拟合，每个方向只输出一组 `E/Y/H`。
- 待验证：对现行入口执行大小写敏感内部链接扫描；对代码、配置和测试执行语法/回归验证；确认剩余可追踪新增文件是否纳入版本控制。

## [2026-09-29] environment | PA12 本地 Python 隔离环境

- 来源：`requirements-pa12-vfm.txt`、`AGENTS/科研工具环境.md` 和本机 Python/工具入口。
- 更新：在主工作区创建 `.venv/`，使用 Python `3.12.10` 安装 PA12 VFM 直接依赖；将 `.venv/` 加入 `.gitignore`，补充环境重建和使用入口。
- 结论：8 个直接依赖版本全部匹配，18 个已安装包通过 `uv pip check`。MinerU `4.0.5` 与标准解析所需 Torch/GGUF 模型就绪；Abaqus `2025` 可启动并报告版本。MinerU ONNX 模型仓库缺失，但当前后端为 Torch，不影响现行流程，未为未使用后端下载额外模型；本地解析服务当前未运行。
- 待验证：实际执行 PA12 脚本时应调用 `.venv\Scripts\python.exe`；需要 MinerU 解析时再启动本地服务。

## [2026-09-29] audit | VFM 0.2-258 序列来源待核

- 来源：`VFM专用力值/X方向/X-0.2-258.csv`、`VFM专用力值/Y方向/Y-0.2-258.csv`，与已有 `0.1-258` 文件逐行比较。
- 更新：确认四份序列均为 258 行；X 方向 `0.2` 与 `0.1` 数值逐行完全一致，Y 方向也完全一致，差异仅在换行编码。两份 `0.2` 文件保留在工作区，但不加入正式追踪输入。
- 结论：`0.2-258` 文件名与内容的速度/试样来源尚未闭合，当前不得据此进行正式 VFM 拟合；这两个未跟踪路径已识别，非临时缓存。
- 待验证：回溯对应原始 Pos/Press 工作簿及同步记录，确认其来源后再决定重建、追踪或删除。

## [2026-09-29] query | 力—位移与 VFM 力文件位置

- 来源：用户询问仓库内力—位移 CSV/Excel 与 VFM 力 CSV 的位置。
- 更新：定位至 `Agents/PA12实验数据处理/实验概览/` 与 `Agents/PA12实验数据处理/VFM专用力值/`；记录于本日志。
- 结论：概览汇总 CSV/XLSX 在仓库内；配置引用的原始 Pos/Press XLS 路径当前不存在；VFM X/Y CSV 位于对应方向目录，S15–S22 的旧同名文件在 `历史失效输入/` 且后缀为 `.invalid`。
- 待验证：如需原始 Pos/Press 工作簿，需从归档或数据源恢复到配置引用位置。

## [2026-09-29] query | XY-0.1-02 VFM 力文件帧数

- 来源：用户追问对应文件应为 231 条还是 258 条。
- 更新：核对 `XY-0.1-02_处理报告.md` 与 VFM 力值目录；记录于本日志。
- 结论：该组有效照片与 X/Y VFM 力值各为 258 条，应对应 `X-0.1-258.csv`、`Y-0.1-258.csv`；231 条文件不对应这份工作簿。
- 待验证：无。

## [2026-09-29] experiment | S16_XY_0.2 VFM3 DIC 导出可读化

- 来源：`D:/C盘迁移/Desktop/yuan/data/XY/picture-20250529/vertical_all_45°/PAPER/biaxal/S16_XY_0.2/VFM3/000000.jpg.csv`。
- 更新：生成 `AGENTS/PA12实验数据处理/MatchID_VFM准备/S16_XY_0.2_VFM3可读化/S16_XY_0.2_VFM3_DIC简明查看.xlsx` 和说明；更新 `index.md`。
- 结论：原表包含 258 条连续记录、每条 10,098 个测点；核心位移和应变字段无缺失。简版含 258 条全场统计及 3 条记录的 30,294 个点位数据。
- 待验证：`u/v` 单位与物理标定、`File` 到 JPG/实验时间的对应关系、应变字段的具体定义。

## [2026-09-29] environment | 补齐 PA12 隔离测试依赖

- 来源：`requirements-pa12-vfm.txt`、PA12 工具导入项及完整回归测试。
- 更新：项目 `.venv/` 安装 `opencv-python==5.0.0.93` 与 `pytest==9.1.1`；将版本写入依赖文件，并记录可复建安装命令。
- 结论：24 个隔离环境包通过 `uv pip check`；全量测试 318 项通过、2 项失败、2 个子测试通过。环境现可运行 PA12 工具并完成全量测试；失败项仍待数据/测试夹具处理。
- 已知问题：S22 合成测试的载荷仍按 1 mm 厚度设置，却从配置读取用户确认的 3 mm 厚度，因此其 E 期待值与夹具不一致；同步配置测试引用的 S16 力工作簿 `D:\C盘迁移\Desktop\yuan\data\XY\data-20250529\20250529\xy-2-0.1_state_20250529104919_20250529104947.xls` 当前不存在。两项均不通过伪造数据或放宽测试处理。

## [2026-09-29] experiment | XY-2-0.2-258-DIC 全量按帧整理

- 来源：`C:\Users\Administrator\Desktop\单双轴-DIC-VFM\双轴\XY-2-0.2-258-DIC.csv`。
- 更新：生成 `AGENTS/PA12实验数据处理/MatchID_VFM准备/XY-2-0.2-258-DIC整理/XY-2-0.2-258-DIC_全量按帧整理.zip` 和说明；更新 `index.md`。
- 结论：258 条连续记录拆为 258 个逐帧 CSV，共 2,605,284 个测点行；每点 27 个源字段值全部保留。每帧 10,098 行、29 列；首、中、末帧全点与源数据一致。
- 待验证：`u/v` 单位和物理标定、`File` 到 JPG/实验时间的映射、DIC 与 X/Y 力的同步关系。

## [2026-09-29] experiment | XY-2 模板来源确认与 S19_X_0.2 全量整理

- 来源：用户提供的 `C:\Users\Administrator\Desktop\XY-2-0.2-258-DIC.csv`；S19 原始目录 `D:\C盘迁移\Desktop\yuan\data\XY\picture-20250529\vertical_all_45°\PAPER\unixal\S19_X_0.2`；S19 配置引用的 Press 工作簿及现有同步索引、MatchID 导出和 DAT 审计。
- 更新：确认新模板 CSV 与此前整理来源逐字节一致，沿用现有 258 帧整理包并更新来源说明；生成 `AGENTS/PA12实验数据处理/MatchID_VFM准备/S19_X_0.2整理/S19_X_0.2_全量按帧整理.zip` 和中文说明；修正工作区派生合并表 `000002.jpg` 的 X 向力值，并更新 `index.md`。
- 结论：S19 整理包含 126 帧、1,152,141 个点位行，每帧保留 15 个 MatchID 原始字段；123 帧有 9,144 点，3 帧有 9,143 点。Press 原始记录在 `0.169 s` 的 X1/X2 为 20/22 N，按基线 31.6 N 和符号系数 -1 得到 `000002.jpg` 的 X 力 10.6 N，故合并表同步更正。压缩包逐项读取、帧/行数、源字段抽查和力时间一致性检查通过。
- 已知问题：首个有效照片已有 10.6 N 载荷，正式 VFM 近零起载门槛未通过；相机无可靠 EXIF 时间，照片时间按有效力区间映射。原始 JPG/DAT、Press 工作簿未改写。
## [2026-09-29] experiment | XY-2 与 S19 应力字段及 VFM 分量核对

- 来源：XY-2-0.2-258-DIC 原始 CSV；S19_X_0.2 的 MatchID Results Viewer 导出和 X_0.2.vfm。
- 更新：XY-2 说明确认全部 27 个源字段（含 sxx/syy/sxy）及逐点数值已保留；S19 说明列出 15 个源字段且注明不含 Sxx/Syy/Sxy。将 S19 .vfm 中可解出的 ReconstructedMatCont 数值另存为 VFM_ReconstructedMatCont_原始分量.csv，并加入整理包；未知分量保持原序号，源末尾不完整行单独标记。
- 结论：XY-2 已有小写 sxx/syy/sxy 源列，单位未注明。S19 .vfm 仅提供前 14 帧完整的未命名分量，帧索引 14 后在源文件末尾中断；不能据此命名为应力。S19 正式 VFM 输入仍受首帧 10.6 N 的零载起始门槛阻塞。
- 待验证：取得完整且有字段名/单位的 S19 应力重建导出，或确定应力重建材料模型；确认 S19 可接受的近零参考帧与力值零点。

## [2026-09-29] experiment | PA12 自建有限变形 VFM 全历程诊断批次

- 来源：S19、S21、S22、S15–S18 的现有 DIC—力索引、合并场、Job.m2inp 和已登记有限变形 VFM 配置；单轴厚度采用已确认的 3 mm，双轴中心区采用 1 mm。
- 更新：本机可重建输出至 `Agents/PA12实验数据处理/VFM自建/有限变形诊断_全历程物理有效_20260929_r2/`，保留各样本双域逐帧 CSV、曲线、泊松比剖面及摘要；在 `AGENTS/PA12实验数据处理/VFM自建/汇总/` 保存版本可追踪的[批次摘要](AGENTS/PA12实验数据处理/VFM自建/汇总/PA12自建有限变形VFM全历程诊断批次_20260929.md)，更新 `index.md`。
- 结论：7 组完成，S15 两域各 284 帧中 27 帧非正 Jacobian，S22 两域各 223 帧中 7 帧非正 Jacobian；无效帧物理虚功/残差留空、代数诊断另列、有效帧 RMS 单独统计。S20 Job ROI 自交且配置未授权修复，未生成。结果是线弹性诊断，不作为最终 `E/Y/H`。
- 验证：`tests/test_pa12_finite_vfm_diagnostic.py` 17 项通过；7 组 JSON 严格解析、逐帧行数/有效性计数、物理字段屏蔽、厚度和输出文件核对通过。
- 下一步：按冻结规则检查合格单轴数据的合并参数可辨识性；不平均逐样本拟合，S20 排除，未闭合的本构符号/几何门槛继续作为发布限制。

## [2026-09-29] refactor | PA12 Obsidian 工作区合并与唯一事实源

- 来源：旧 Obsidian Vault `D:\C盘迁移\Desktop\yuan\second brain`；原 PA12 项目目录中的第一阶段盘点交付。
- 更新：将 83 个旧 Vault 独有稳定文件和 6 个盘点文件导入 `D:\2026.9.21_finally`，不覆盖已有同路径文件；更新 Abaqus 运行入口、PA12 工作区索引和项目总览；将 Obsidian 默认 Vault 登记切换到 `D:\2026.9.21_finally`。
- 结论：`D:\2026.9.21_finally` 是唯一事实 Vault；旧目录及其文件保持不变，作为恢复副本。新资料、Wiki 和派生输出均在主库继续维护。
- 验证：导入文件存在且源/目标长度相同；新并入 Markdown 的相对链接检查通过；运行脚本 PowerShell AST 解析通过；Obsidian 登记 JSON 解析通过并仅将主库标记为默认打开。未运行 Abaqus。
- 限制：本轮未重新启动 Obsidian 做界面确认；默认 Vault 选择以已核验的应用登记为准。

## [2026-09-29] refactor | PA12 Obsidian 工作区合并与唯一事实源

- 来源：旧 Obsidian Vault `D:\C盘迁移\Desktop\yuan\second brain`；原 PA12 项目目录中的第一阶段盘点交付。
- 更新：将 83 个旧 Vault 独有稳定文件和 6 个盘点文件导入 `D:\2026.9.21_finally`，不覆盖已有同路径文件；更新 Abaqus 运行入口、PA12 工作区索引和项目总览；将 Obsidian 默认 Vault 登记切换到 `D:\2026.9.21_finally`。
- 结论：`D:\2026.9.21_finally` 是唯一事实 Vault；旧目录及其文件保持不变，作为恢复副本。新资料、Wiki 和派生输出均在主库继续维护。
- 验证：导入文件存在且源/目标长度相同；新并入 Markdown 的相对链接检查通过；运行脚本 PowerShell AST 解析通过；Obsidian 登记 JSON 解析通过并仅将主库标记为默认打开。未运行 Abaqus。
- 限制：本轮未重新启动 Obsidian 做界面确认；默认 Vault 选择以已核验的应用登记为准。

## [2026-09-29] experiment | S19_X_0.2 逐点弹性应力候选补充

- 来源：S19_X_0.2 全量逐帧 DIC 整理包、1 mm 阶段一结果、3 mm 厚度敏感性结果、原始 X_0.2.vfm 厚度记录。
- 更新：生成 `Agents/PA12实验数据处理/MatchID_VFM准备/S19_X_0.2整理/S19_X_0.2_VFM应力候选_全量按帧整理.zip`；另存参数 JSON、逐帧摘要 CSV 和说明；在 `index.md` 登记。
- 结论：126 帧共 1,152,141 个点位均保留原始 MatchID 字段，并按平面应力公式追加 1 mm（E=5517.117882 MPa）和 3 mm（E=1839.039294 MPa）两套 Sxx/Syy/Sxy 候选值；拟合窗口为 000002–000026，后续帧标为线弹性外推。Exy 按张量剪切应变处理。两种厚度口径对应的应力相差 3 倍，尚需按有效 ROI 实物厚度定版。
- 验证：压缩包 CRC 完整；126 帧逐帧 CSV 的全部原始字段、值及行顺序与基础包一致；总点数 1,152,141（9,144 点×123帧、9,143点×3帧）；有限应变缺失 0；六列候选公式最大舍入误差 `5.0×10⁻¹⁰ MPa`；逐帧摘要 126 行。
- 已知问题：候选应力是模型推算，不是实测应力或正式材料参数。正式 VFM 仍受首帧 10.6 N、DIC/机器轴映射未核准、厚度口径未定及原始 `.vfm` 尾部不完整限制。

## [2026-09-29] experiment | PA12 按加载模式共享有限变形 J2 双域诊断

- 来源：S19/S21/S22 与 S15–S18 的已登记有限变形 J2 配置、完整 Job ROI 和 DIC subset 内缩域 JSON/CSV、照片—力索引及对应表。
- 更新：生成 `Agents/PA12实验数据处理/VFM自建/汇总/PA12按加载模式共享有限变形J2双域诊断_20260929.md`；在 `index.md` 登记。
- 结论：按加载模式合并为单轴一组与等双轴一组，速度只作残差分层；完整 Job ROI 为主域，内缩域独立作敏感性。单轴候选 `E=2123.66 MPa、Y₀=92.19 MPa、H≈0 MPa`，等双轴候选 `E=4294.15 MPa、Y₀=62.93 MPa、H=2260.25 MPa`。完整 ROI 七组支持率均低于 95%，结果不正式放行；MatchID 门槛 1–4 按用户确认通过，S20 因 Job ROI 自交排除。S19 使用两组件修复几何；S16/S19 与其余样本虚场模式不同。单轴源配置厚度字段为 1 mm，而单样本 J2 配置及已生成输出为 3 mm，未修正源配置前不可直接重跑。
- 验证：报告 21 个 Markdown 链接均有效；四组 full/inset 参数、目标值、覆盖率与 JSON 一致，E 与固定 `ν=0.375` 的弹性 profile 点一致；主域逐样本 RMSE 与 JSON 一致。
- 待验证：七组 Press 源文件与速度标签对应；S16 精确源工作簿缺失；单轴源配置厚度字段统一；自建 VFM 外功边界条件的独立验证；论文与代码硬化符号定义。现有等双轴 J2 输出中关于 S15/S17 未纳入的限制文案与结果数组冲突。

## [2026-09-30] experiment | 单轴有限变形 VFM r3 跨速度共享 E 与 pooled J2

- 来源：用户确认单轴实物厚度 `3 mm`、MatchID 人工证据门槛 1–4 通过；S19/S21/S22 的 r2 pool-source 与 J2 配置、DIC—力索引、合并场及 Job 文件。
- 更新：新增隔离 r3 配置：`configs/pa12_vfm_pool_source_s19_r3.json`、`s21_r3.json`、`s22_r3.json`，对应三份 `configs/pa12_finite_j2_*_r3.json`，以及单轴专用共享 E/J2 配置。r2 文件未覆盖；未改代码、原始数据、双轴配置或旧 Obsidian 副本。
- 方法：S19/S21/S22 均用 `t=3.0 mm`、`job_roi_boundary_adapted` 和完整 Job ROI；加载轴保留 X/X/Y。固定 `ν=0.375` 的共享弹性 profile 按每试样归一化残差平方等权，得到唯一共享 `E=2230.725903 MPa`。随后只运行一次 pooled Linear 有限变形 J2：同一 E/ν、拟合终点前 `0.5` 前缀窗口、每样本 512 个分层预拟合三角形、`Y0/H` 每试样归一化残差平方等权；初值 `35/500 MPa`、`max_nfev=100`、`ftol=1e-7`。
- 结果：唯一诊断解 `E=2230.725903 MPa`、`ν=0.375`、`Y0=93.519664 MPa`、`H=0.000262 MPa`；Jacobian 秩 `2/2`、条件数 `4.0108`，但 H 贴近零下界。S19/S21/S22 Job ROI DIC 覆盖率为 `84.8667%/84.1189%/71.1951%`，均 `REVIEW_REQUIRED`；发布标志 `formal_parameter_release=false`。固定 ν profile 的自由扫描最低误差位于网格边界 `ν=-0.9`，不构成 ν 的独立识别。Stage 1 沿用各样本既有弹性帧窗，分别 24/17/3 帧；J2 实际拟合分别 62/13/70 帧。逐帧 J2 CSV 共 350 行，与摘要历程帧数一致。
- 输出：固定 ν [共享 E 报告](Agents/PA12实验数据处理/VFM自建/共享弹性参数诊断_单轴_r3_20260929/单轴/诊断报告.md)；[pooled J2 报告](Agents/PA12实验数据处理/VFM自建/共享参数J2诊断_单轴_r3_20260929/单轴/诊断报告.md)、[结果摘要 JSON](Agents/PA12实验数据处理/VFM自建/共享参数J2诊断_单轴_r3_20260929/单轴/共享线性J2诊断摘要.json)、[逐帧虚功 CSV](Agents/PA12实验数据处理/VFM自建/共享参数J2诊断_单轴_r3_20260929/单轴/共享线性J2逐帧虚功.csv)、[残差图](Agents/PA12实验数据处理/VFM自建/共享参数J2诊断_单轴_r3_20260929/单轴/共享线性J2逐帧残差.png)。
- 已知问题：ROI 覆盖低于 95%、有效宽度/积分域/Press 外功边界未闭合，不能发布正式材料参数；S19 修复几何为两个组件；S20 排除；S16 力源缺失仍作为独立 REVIEW 项，不纳入单轴队列。r2 的 pool-source 厚度字段为 1 mm、J2 字段为 3 mm，且 S19/J2 虚场模式不同，故 r2 的共享 E→J2 不作当前结果，历史产物保留不删。Stage 1 弹性拟合帧窗仍是逐样固定列表（24/17/3），并非相同帧数；本次 pooled J2 的统一设置是相同 50% 窗口比例。

## [2026-09-30] experiment | PA12 共享有限变形 J2 完整 Job ROI 与 subset 内缩双域 r3

- 来源：S19/S21/S22 单轴及 S15–S18 等双轴的 r3 共享弹性 profile、pooled J2 摘要、逐帧 CSV 和残差图；完整 Job ROI 与 DIC subset 内缩域使用同一组样本和拟合窗口规则。
- 更新：新增[双域 r3 汇总](Agents/PA12实验数据处理/VFM自建/汇总/PA12按加载模式共享有限变形J2双域诊断_r3_20260930.md)，更新 `index.md` 的 P1 状态并将 20260929 汇总标为历史；保留 r2、原始 DIC/力数据和其他进行中的 check/config 文件不变。
- 结论：完整 Job ROI 为主域，内缩域只作独立敏感性；单轴与等双轴分别 pooled。单轴完整域/内缩域候选为 `E=2230.725903/2233.525999 MPa、Y0=93.519664/93.464390 MPa、H≈0/≈0 MPa`；等双轴为 `E=4294.148944/4294.148944 MPa、Y0=62.926614/62.951238 MPa、H=2260.249495/2259.835956 MPa`。四组均 `DIAGNOSTIC_ONLY`，不正式释放参数。主域七样本覆盖率均低于 95%；内缩域 S22 覆盖率 82.85%。S17 与 S21 分别主导等双轴与单轴内缩域目标，且只有 6/13 个拟合帧；ν profile 边界、窗口外残差、本构 H 符号、S16 力源追溯、S22 帧数差异及外功条件继续列为限制。
- 验证：汇总所引 4 份 J2 摘要与 4 份 Stage 1 报告均存在；全域/内缩域逐帧 CSV 行数分别为单轴 350、等双轴 601，与各 JSON 历程帧数总和一致；报告 Markdown 本地链接逐项检查通过。未运行代码测试，因为本次只更新分析文档、索引和日志。
- 待验证：独立闭合广义外功边界虚位移条件；核对 S22 的 188 与既有 223 历程帧差异；恢复/确认 S16 原始力工作簿；解决论文和当前代码的硬化符号冲突；取得足以解除主域 REVIEW 状态的 DIC 支持证据。

## [2026-09-30] refactor | PA12 项目总览与总控交接指令同步 r3 状态

- 来源：用户确认的实验固定口径；[PA12 共享有限变形 J2 双域 r3 汇总](Agents/PA12实验数据处理/VFM自建/汇总/PA12按加载模式共享有限变形J2双域诊断_r3_20260930.md)及其链接的阶段 1 profile、J2 JSON/CSV/报告；现有 PA12 项目全景页、`index.md` 和本日志。
- 更新：修订 `wiki/PA12项目全景与总控指令.md` 的快照日期、当前执行状态、时间线、VFM 证据摘要和可复制交接指令；更新 `index.md` 的首页与目录摘要；保留历史诊断内容和项目冻结范围，不改暂存删除的交接页、原始数据或检查/配置文件。
- 结论：单轴 S19/S21/S22 与等双轴 S15–S18 已完成 r3 pooled J2 的完整 Job ROI 主域及 DIC subset 内缩敏感性诊断。七个主域样本均低于 95% DIC 覆盖，全部结果仍为 `DIAGNOSTIC_ONLY`；总览明确保留用户口径：等双轴、ROI 边界合力、主域/敏感性域分离，不要求非等双轴或重建四边牵引。
- 验证：总览页所引 r3 汇总报告存在；更新后的首页与目录入口均指向现有总览；已确认 P1 不再显示“双轴范围未触碰”，当前限制和交接顺序与 r3 报告一致。未运行数据拟合或代码测试。
- 待验证：有效宽度/积分域和外功边界虚位移条件；S16 原始力源追溯、S22 历程帧数差异；本构硬化符号冲突、窗口外残差与 DIC 覆盖门槛。

## [2026-09-30] audit | S22 DIC—力输入 223 帧与 J2 历史 188 帧口径核对

- 来源：S22 原始 JPG/DAT 目录、`S22_Y_0.2_配置.json`、DIC—力索引与状态 JSON、r2/r3 J2 配置和逐帧 CSV、S22 局部 Jacobian/DIC 时序诊断、共享 J2 runner。
- 更新：在[PA12 r3 双域诊断报告](Agents/PA12实验数据处理/VFM自建/汇总/PA12按加载模式共享有限变形J2双域诊断_r3_20260930.md)补充帧数定义与逐帧筛选链；更新 `index.md` 的当前 r3 摘要。本次只读追溯，未重跑 VFM/J2，也未修改 JPG/DAT/XLS、源码或配置。
- 结论：原始目录有 1,825 张 JPG、233 对同名 JPG/DAT；223 行 DIC—力索引是有效输入列表，区间 `000008–001784.jpg`、步长 8。8 个 DAT 质量帧被显式排除，另 `000000/000001.jpg` 不在索引中，现有处理报告仅记录从 `000008.jpg` 起始，未单列这两帧的原因。r2/r3 配置都显式将 `history_end_photo` 设为 `001504.jpg`；该键是索引第 188 帧，runner 按此截取，所以两个版本的 J2 CSV 均保留相同前 188 帧，并截去 `001512–001784.jpg` 共 35 帧。首个被截帧是首个已知非正 `det(F)` 帧；异常审计只报 7 个异常帧/15 个三角形—帧事件，因此不得把整段 35 帧都称作无效帧，也不得把 188 解释为完整输入数。
- 验证：233 个 DAT 均找到同名 JPG；223 个索引帧与状态 JSON 数量一致；r2/r3 CSV 的 S22 帧键均与输入索引前 188 项完全一致；配置截止帧、索引位置和被截尾数量分别为 `001504.jpg`、188、35。报告新增本地链接指向现有证据文件。
- 待验证：补充 `000000.jpg`、`000001.jpg` 未进入有效索引的具体来源/筛选记录；S22 仍因主域覆盖率和异常运动学保持 `REVIEW_REQUIRED`，本次不延伸有限变形 J2 状态历史。

## [2026-09-30] query | S19_X_0.2 前两帧同步状态核查

- 来源：S19 原始 000000–000127 JPG/DAT、`_matchid_export/S19_X_0.2`、Press 工作簿、帧—力—时间索引、原始 `.vfm` 与 DIC 元数据。
- 更新：在 `index.md` 标明原始序列 128 帧、当前已同步交付 126 帧；未生成或交付含未同步前两帧的同步包。
- 结论：000000/000001 均有 Results Viewer CSV，且各有 9,144 个有效 DAT 点；但现有帧—力索引仅覆盖 000002–000127。两张 JPG 无 EXIF 拍摄时刻，源目录文件时间均为迁移时间；Force 工作簿只有 T、Press、Pos、Speed 通道，无相机触发通道；配置的 10 Hz 仅为历史候选值。S19 `.vfm` 解压内容未发现逐帧 Forces 记录。因此不能可靠确定两帧的相机时刻及同步力值，不能标记为已同步。
- 待补资料：相机触发/起始时刻相对 Force `T` 时间轴的记录，或明确包含 000000/000001 的原始逐帧同步表。取得后才能把两帧加到 128 帧同步包。


## [2026-09-30] query | S19_X_0.2 全 128 帧时基映射复核

- 来源：S19 `000000–000127` 的 128 份 Results Viewer 全场 CSV、原始 Press/Pos 工作簿、`S19_X_0.2.mti` 和现行 `000002–000127` 帧—力索引；原始文件只读。
- 方法：每帧按其自身坐标取 DIC `V` 在上下各 2 mm 条带的中位数差，和 Pos 两夹头相对起点位移绝对值之和比较；在多组帧起点和帧间隔下做仿射趋势对齐。该比较用于判断能否唯一恢复时基，不把相关性当作触发证据。
- 结果：128 帧均有 CSV，每帧 9,143–9,144 个点；3 帧为 9,143 点。`000000↔T=0`、`000127↔T=12.845 s` 线性映射的趋势拟合 `R²=0.999431`、RMSE `0.017704 mm`；现行索引起点附近的替代映射也得到 `R²=0.999442`、RMSE `0.017303 mm`。多组候选起点/间隔均保持近似拟合，不能唯一确定时间原点和帧间隔。若采用前一种映射，`000002.jpg` 会由现行 `10.6 N @ 0.1690 s` 改为约 `13.1 N @ 0.2023 s`，并会重算全体 128 行。`mti` 列出 000000–000127 图像及无字段定义的数值标签，没有逐帧时间戳或力触发记录。
- 判定：不能据趋势拟合把新表标为已同步；现有 126 帧索引保持不变，未输出未核实的 128 帧同步包。
- 下一步：取得相机起始时刻相对力表 `T` 的触发/时间戳，或由用户确认可采用指定的人工映射；人工映射只能标明按约定对齐，不能称为硬件同步已验证。
## [2026-09-30] query | S16 力数据来源追溯

- 来源：主 Vault 第一阶段 force/DIC/experiment inventories、S16 配置和处理报告、现有帧—力—时间索引及合并派生表；`D:\C盘迁移\Desktop\yuan\data` 中现存 12 个非锁定 XLS/XLSX 工作簿。
- 更新：新增 [S16 力数据来源追溯](AGENTS/PA12实验数据处理/数据盘点/S16力源追溯.md)，记录只读内容比对、候选误差和剩余证据缺口；不改原始工作簿、配置或派生力数据。
- 结论：`xy-2-0.2.xls` 是唯一与现有 S16 X/Y 力序列接近的现存候选（RMSE 0.019580/0.016941 N），但未逐值精确复现且无法证明等同于配置指向的缺失 `xy-2-0.1...xls`。Press 作为力及 N 单位采用项目约定；现存候选表内部没有单位声明。来源维持 `source-unverified`。
- 待验证：找回配置所指工作簿或归档改名证据、S16—工作簿实验映射记录、明确 Press 工程单位为 N 的设备资料。


## [2026-09-30] experiment | S19_X_0.2 128 帧人工映射包

- 来源：用户确认的人工时基锚点、S19 `000000–000127` Results Viewer 全场 CSV、Press 工作簿、原 126 帧整理包；原始 DIC/力文件只读。
- 更新：新增 `Agents/PA12实验数据处理/MatchID_VFM准备/S19_X_0.2整理_128帧人工映射/`，含全量逐帧 ZIP、快速查看工作簿、128 行索引、逐帧摘要、单列 X/Y 力值和状态说明；旧 126 帧包及既有诊断目录未覆盖。更新 `index.md` 指向新版本。
- 方法：按用户确认 `000000=T0.000 s`、`000127=T12.845 s`，对 128 帧作线性映射，间隔 `0.101141732283 s/frame`；沿用 `F_X=−(mean(X1_Press,X2_Press)−31.6 N)`，单轴非加载 Y 力置零。逐帧保留 15 个 MatchID Results Viewer 源字段。
- 结果：128 帧，共 `1,170,429` 点位行；每帧 9,143–9,144 点。首/次/第三/末帧 X 力为 `0.6/3.1/13.1/178.6 N`，对应时间 `0/0.101142/0.202283/12.845 s`。状态写为“人工映射已确认；硬件同步未验证”。首帧 0.6 N 未额外归零，本地正式 VFM 门禁仍阻断。
- 验证：ZIP 完整性、连续帧号、全部逐点行与索引时间/力对应、128 行单列力文件及查看工作簿行数均核对一致。旧版输出保持不变。
- 已知限制：人工映射不是硬件触发验证；首行非严格零力，因此该版本是映射下的 VFM 输入候选，不是正式 VFM 放行结果。

## [2026-09-30] query | PA12 数据可用性初审

- 来源：`Agents/PA12实验数据处理/数据盘点/manifests/` 中的实验、DIC、力、路径级清单；当前 `index.md`、PA12 双轴/单轴交接与 S15–S24 样品处理报告；XY-2 模板与 S19 新映射包。
- 更新：新增 `Agents/PA12实验数据处理/数据盘点/PA12数据可用性初审_20260930.md` 和 Excel 工作簿；在 `index.md` 登记。
- 结论：路径级清单 55,246 条（未按文件内容去重）；59 条 DIC 目录记录中 11 条全配对、12 条不完整/不连续、36 条图片无 DAT；15 条力文件记录中 12 个工作簿可读、3 个为 Excel 临时锁文件。源实验登记共 38 条且同步状态均为 `NOT_STARTED`，其中有派生/排除帧目录和力文件独立记录，不能当作独立样本数量。当前 S15–S24 工件多为诊断候选；S20 几何阻断、S23 缺断裂时力、S19 新映射首行不满足正式 VFM 零力门禁。临时锁文件仅从分析范围排除；未删除数据。
- 下一步：优先闭合各样品的力文件—图像关联、物理/人工时间锚点和有效数据域；确认历史派生工件仍未被引用后，再决定归档范围。

## [2026-09-30] audit | S22 首两帧未进入有效力索引的原因补证

- 来源：S22 原始 `000000/000001.jpg` 与 DAT、MatchID Job/MTI、现有照片—力索引和 S22 处理报告。
- 更新：在 [r3 双域诊断汇总](Agents/PA12实验数据处理/VFM自建/汇总/PA12按加载模式共享有限变形J2双域诊断_r3_20260930.md) 写明首端帧筛选依据，并同步更新 `index.md` 和项目总览；原始 JPG/DAT 保持只读。
- 结论：`000000.jpg` 是 Job 参考图，DAT 有 `<18>/<53>` 字段，但按记录的加载起点 `0.159 s` 与相机 `10 fps` 口径位于有效加载区间前；`000001.jpg` 也在区间前，且 DAT 缺 `<53>`、MTI 标记未选。两帧文件存在，不代表有可映射的有效加载力值。现有说明闭合了首两帧不在 223 行索引的原因；`223` 与 `188` 仍分别是有效输入和配置截止后的 J2 历史长度。
- 验证：S22 处理报告与原始帧/DAT/Job/MTI 记录相互对应；未重跑 DIC、VFM 或 J2，未修改原始资料。

## [2026-09-30] audit | r3 VFM 积分面积与外功边界条件

- 来源：S15/S19 r3 配置、既有 J2 摘要与力索引，以及有限变形虚场和积分实现。
- 更新：新增 [r3 面积与外功边界证据审计](Agents/PA12实验数据处理/VFM自建/汇总/审计/2026-09-30_r3面积与外功边界证据审计.md)，并在 `index.md` 登记。
- 结论：内虚功按完整 Job ROI 与 DIC 三角网的交叠面积乘厚度积分，不额外乘 30/28 mm 宽度；未覆盖 ROI 区域没有外推。机器 Press 合力作为广义外功输入符合当前用户口径，但其与完整 ROI 外虚功物理等价仍需单位共轭边界位移及其他边界功项证据。S19 修复 ROI 的两个组件均纳入面积积分，而当前虚场由最大组件构造，场在第二组件上的相容性未闭合。S15/S19 主域支持率分别 88.93%/84.87%，维持 `REVIEW_REQUIRED`。
- 验证：报告引用的配置、实现和摘要路径存在；未重跑 VFM/J2/拟合，未修改原始数据、共享代码或配置。

## [2026-09-30] audit | r3 拟合窗内、窗外与全历程逐帧残差

- 来源：现有单轴 S19/S21/S22 与等双轴 S15–S18 r3 逐帧 J2 CSV、摘要 JSON、配置和共享汇总；S22 照片—力索引。
- 更新：新增 [拟合窗外残差审计](Agents/PA12实验数据处理/VFM自建/汇总/审计/2026-09-30_r3拟合窗外逐帧残差审计.md)，补齐逐样本逐方向拟合窗、窗外、全历程的 RMS、MAE、偏差、最大残差位置和载荷；在 `index.md`、r3 汇总及项目总览登记链接。
- 结论：S15/S16 窗外 RMS 约为拟合窗的 14/20 倍，S17 约 2.3 倍、S18 约 3.5–3.7 倍；单轴 S21/S22 约 3.1/2.2 倍。S19 窗外 MAE 为 27.74 N，但 `000127.jpg` 的 962.19 N 末帧残差主导其 RMS。S22 的 223 行力索引对应配置截断后的 188 行 J2 历史；其余 35 帧没有现成残差输出。
- 验证：统计只读取既有逐帧 CSV，未重跑 VFM/J2/拟合；报告所引 8 个链接存在，逐样本计数符合各 CSV 与 S22 配置历程边界。残差仅用于诊断，不作独立验证或材料结论。

## [2026-09-30] audit | S16 力源改名副本确认

- 来源：用户确认文件只改名；原配置所指工作簿缺失，现存 `xy-2-0.2.xls` 的内容、工作表和 S16 力序列已完成比对。
- 更新：将 S16 活动配置、批次映射和力追溯页指向现存改名副本；修正报告中的旧候选指标。原工作簿与派生力数据未改，未重跑同步、VFM 或拟合。
- 结论：257 点 X/Y Press 重采样 RMSE 为 `0.011007/0.008716 N`、相关系数为 `0.999999999735/0.999999999829`；来源身份由用户确认及内容比对支持。单位元数据缺失，N 仍为项目约定。
- 验证：[S16 力源追溯](AGENTS/PA12实验数据处理/数据盘点/S16力源追溯.md)已去除与最终比较结果冲突的旧表述。

## [2026-09-30] audit | S19–S22 曲线标距与 Job 虚引伸计

- 来源：S19–S22 Job `Extensometer` 点、像素标定、现行曲线配置和曲线生成代码。
- 更新：新增[Job 虚引伸计与曲线标距核查](Agents/PA12实验数据处理/处理记录/PA12_S19-S22_Job虚引伸计与曲线标距核查.md)，并登记于 `index.md`。
- 结论：现有曲线使用配置中的 30 mm 标距与设备 Pos 夹头相对位移；未使用 Job 虚引伸计点。S20/S21/S22 点距为 `44.0358/43.0098/20.3339 mm`，S19 无点对记录。图纸采用项目统一 30 mm 标距段。

## [2026-09-30] audit | S19 ROI 双组件虚场适配

- 来源：S19 原始 Job 五点顺序、授权 `make_valid_linework` 的双组件几何、现有 DIC 原图和 r3 虚场实现。
- 更新：新增[S19 ROI 双组件与边界适配虚场审计](Agents/PA12实验数据处理/VFM自建/汇总/审计/2026-09-30_S19ROI双组件与边界适配虚场审计.md)，并登记于 `index.md`。
- 结论：第二组件面积约 `3.02×10⁻⁵ mm²`，占比 `4.48×10⁻⁸`；虚场值有限连续，组件影响可忽略。缺少带 ROI 叠加的原软件图，物理边界归属未直接确认；机器力边界功条件仍独立待核。
- 限制：未运行 VFM/J2/拟合，未改 Job、原图或配置。

## [2026-09-30] decision | 单轴实体尺寸统一定稿

- 来源：S19/S20/S21/S22 四件 `000000.jpg` 的三处横截面宽度读数、各 Job `Conversion` 与用户确认的单轴厚度。
- 更新：定稿单一单轴结构图 [SVG](Agents/PA12实验数据处理/处理记录/单轴实体尺寸图/PA12单轴试样_实体尺寸图.svg)、[PNG](Agents/PA12实验数据处理/处理记录/单轴实体尺寸图/PA12单轴试样_实体尺寸图.png)、[SCAD](Agents/PA12实验数据处理/处理记录/单轴实体尺寸图/PA12单轴试样_实体几何.scad)；更新[宽度证据复核](Agents/PA12实验数据处理/处理记录/PA12单轴样件30mm宽度证据追溯_20260930.md)、[单轴几何证据页](Agents/PA12实验数据处理/处理记录/PA12单轴几何证据缺口.md)、方法页、项目总览与 `index.md`。既有 90 mm² 派生文件保留并标记为不适用。
- 结论：采用统一标距段 `30×10×3 mm`，名义截面积 `30 mm²`；厚度 3 mm 为用户确认实测值，宽度 10 mm 由四件三截面图像标定值收敛，30 mm 使用项目标距口径。既有单轴 `30 mm²` 曲线数值不变，几何解释改为 `10×3 mm²`；整件总长未记录，不作外推。
- 验证：SCAD 已编译为 `30×10×3 mm`，SVG/PNG 已生成并目视核对；未重算应力曲线或运行 VFM/J2 拟合。
- 环境变更：制图线程安装 OpenSCAD 2021.01 用于 SCAD 编译验证。

## [2026-09-30] update | S19–S22 单轴曲线几何解释

- 更新：将 [S19](Agents/PA12实验数据处理/应力应变/S19_X_0.2_应力应变分析.md)、[S20](Agents/PA12实验数据处理/应力应变/S20_X_2_应力应变分析.md)、[S21](Agents/PA12实验数据处理/应力应变/S21_X_20_应力应变分析.md)、[S22](Agents/PA12实验数据处理/应力应变/S22_Y_0.2_应力应变分析.md) 的当前口径改为单轴宽 `10 mm`、厚 `3 mm`、标距段 `30 mm`、名义面积 `30 mm²`。
- 结论：原页面中的 `30×1 mm²` 仅是历史配置字段，面积数值与当前 `10×3 mm²` 相同；既有曲线数值保持不变，`90 mm²` 派生曲线不适用。双轴曲线未改。
- 验证：四页计算口径均与单轴实体尺寸图一致；未改 CSV、同步力数据或原始资料。

## [2026-09-30] update | 当前执行规则与历史口径对齐

- 更新：将 [PA12 总目标与阶段计划](Agents/PA12实验数据处理/处理记录/PA12总目标与阶段计划.md)、[批量照片—力处理报告](Agents/PA12实验数据处理/处理记录/PA12批量处理报告.md) 和 [照片—力同步与 VFM 页面](wiki/PA12照片力同步与VFM生成.md) 中的暂停状态及旧 MatchID 主线标记为历史；更新 `index.md` 中的入口说明。
- 当前规则：单轴使用标距段 `30×10×3 mm`；双轴使用中心厚 `1 mm`、外围厚 `3 mm` 的单一 TC1000 结构。MatchID 人工门槛 1–4 已确认，不重复索取；当前主线为自建 VFM。
- 结论：旧批次单轴应力分母 `30×1 mm²` 与当前 `10×3 mm²` 数值相同，单轴应力曲线无需重算；正式参数仍需 DIC 支持、外功边界、窗外残差和本构符号证据。

## [2026-09-30] audit | S16 Press 导出单位证据边界

- 来源：S16 力源追溯页中的源工作簿字段核查，以及本地论文设备量程记载。
- 更新：明确区分传感器量程与 XLS 导出单位，并列出闭合 S16 单位所需的采集通道字典/导出配置、通道映射和传感器校准记录。
- 结论：源表 `Press` 列没有单位或换算系数；论文的 `0–10 kN` 只说明设备量程，不能确定该 XLS 的导出单位。`N` 仍是项目处理约定，源表单位未核实。
- 限制：未改原始工作簿、派生力数据或处理配置；未重跑同步、VFM 或拟合。

## [2026-09-30] artifact | PA12 双轴试样实体尺寸图

- 来源：只读 `raw/assets/PA12_几何STEP/PA12_tc1000.step`、`raw/assets/PA12_几何STEP/PA12_tc1000_source_topology.json` 与[源 STEP 几何族回归](Agents/PA12双轴试样仿真/验证/2026-09-28_PA12源厚度STEP族竖直坐标几何库.md)。
- 更新：新增 [SVG 尺寸图](Agents/PA12双轴试样仿真/图纸/PA12双轴试样实体尺寸图/PA12双轴试样实体尺寸图.svg)、[PNG 预览](Agents/PA12双轴试样仿真/图纸/PA12双轴试样实体尺寸图/PA12双轴试样实体尺寸图.png) 和 [1:1 可编辑 DXF](Agents/PA12双轴试样仿真/图纸/PA12双轴试样实体尺寸图/PA12双轴试样实体尺寸图_可编辑几何.dxf)，并登记于 `index.md`。
- 结论：TC1000 外包络 `150.4×150.4×3.0 mm`；加载臂宽 `30.0 mm`；减薄区边界 `30×30 mm` 与中心平坦面 `28.01×28.01 mm` 分开标注；中心平坦区厚 `1.0 mm`、外围实体厚 `3.0 mm`；28 条圆头槽，单槽 `40.0×1.25 mm`、同臂中心距 `3.75 mm`。DXF 按源 B-rep 平面投影轮廓离散为可编辑闭合多段线，标称弦差不超过 `0.01 mm`。
- 验证：PNG 为 `1800×1280` 且已目视检查；SVG 可解析；DXF 包含 31 条闭合多段线、4 个预期图层，外边界 ±75.2 mm、减薄边界 ±15 mm、中心平坦面 ±14.005 mm 分层正确；索引和来源链接可解析。本次 `index.md`/`log.md` 补丁通过空白检查。源 STEP 未改，未运行 Abaqus/VFM/J2。

## [2026-09-30] refactor | PA12 唯一执行路线

- 来源：用户要求只保留一条清晰路线；核对首页、项目总控页、方法页、阶段计划、GPT 交接页和机器状态 JSON 中现存的行动指针。
- 更新：以 `wiki/PA12项目全景与总控指令.md` 为唯一行动入口；将单轴/等双轴 P0/P1 拆分改为同一路线，将其他页面改为方法口径或历史证据，并在 GPT 机器状态中写入唯一当前步骤。
- 结论：当前第一步是按内容而非文件名完成原始来源—试样身份对应；后续依次过数据资格、曲线、虚功、E/ν、J2、独立验证和正式发布门槛。既有诊断保留、不重复运行。
- 待完成：逐项补齐来源身份表及各实验数据资格；正式材料参数仍未放行。

## [2026-09-30] decision | 双轴概念图尺寸按实物尺寸定稿

- 来源：用户明确确认“概念图属性就是实物尺寸”；对应[双轴试样实体尺寸图](AGENTS/PA12双轴试样仿真/图纸/PA12双轴试样实体尺寸图/PA12双轴试样实体尺寸图.svg)及只读源 STEP `raw/assets/PA12_几何STEP/PA12_tc1000.step`。
- 更新：定稿双轴实体几何及名义应力截面积，更新[当前执行方法](wiki/methods/PA12当前执行方向.md)、[项目总览](wiki/PA12项目全景与总控指令.md)和 `index.md`。
- 结论：整体 `150.400×150.400×3.000 mm`；加载臂宽 `30.000 mm`；减薄区边界 `30×30 mm`；中心平坦区 `28.010×28.010 mm`、厚 `1.000 mm`；外围厚 `3.000 mm`；狭缝 28 条，每条 `40.000×1.250 mm`、同臂中心距 `3.750 mm`。双轴名义截面积是 `30×1=30 mm²`；30×30 和 28.010×28.010 是平面尺寸。既有双轴名义应力曲线分母已为 30 mm²，数值保持不变。
- 验证：核对尺寸图及相对路径目标存在；不运行 VFM、拟合或测试，不改源 STEP、原始资料和现有曲线。

## [2026-09-30] ingest | 独立 PA12 本构与公开实验曲线证据

- 来源：Puttonen 等（2021）公开 Zenodo 原始拉伸数据及论文；Zadeh 等（2025）SLS PA12 多机制本构论文；Psarros 等（2025）开放论文与补充数据目录。
- 更新：归档只读原始来源，整理 [Puttonen 六组 PA2200 曲线长表](Agents/PA12实验数据处理/文献数据/Puttonen2021_SLS_PA2200_noUV_tensile_curves.csv)，更新[独立本构与公开曲线证据页](Agents/PA12实验数据处理/VFM自建/汇总/审计/2026-09-30_独立PA12本构与公开实验曲线证据.md)、方法页、项目总览和 `index.md`。
- 结论：Puttonen 整理表保留 27,279 行原始载荷、横梁位移、引伸计应变与应力；完整量是应力—横梁位移，引伸计应变只覆盖初始段。独立 SLS PA12 研究支持正硬化增量对应硬化方向，但不能直接提供本项目 `Y/H`。Psarros 补充表 S9–S10 是完整工程应力—应变候选来源。
- 验证：六组分别为 X/XY-01 7,311、X/XY-02 5,446、X/XY-03 5,522、Z-01 3,007、Z-02 2,915、Z-03 3,078 行；所有六个原始曲线源文件、整理表链接和本地论文文件均存在。
- 限制：未重算曲线、VFM 或参数拟合；Psarros 补充材料仍以出版方链接登记，未纳入本地原始资料。

## [2026-09-30] update | 双轴 VFM 面积审计采用实物厚度

- 更新：[r3 面积与外功边界审计](Agents/PA12实验数据处理/VFM自建/汇总/审计/2026-09-30_r3面积与外功边界证据审计.md) 将表头和尺寸依据更新为用户确认的实体厚度，并补入双轴名义截面积口径。
- 结论：S15 实物中心厚度 `1 mm`、S19 实物厚度 `3 mm`；双轴名义截面积 `30×1=30 mm²`。原报告中按这些厚度计算的虚功积分体积不变；30×30 与 28.010×28.010 仍是平面尺寸。
- 待闭合：DIC 支持面积与完整 ROI 的覆盖，以及机器合力对应的外功边界运动学；本次尺寸定稿不代替这两项检查。

## [2026-09-30] audit | S15–S18 ROI 与中心厚度几何门槛

- 来源：四组 MatchID DIC 元数据与只读 Job/参考图、用户确认的 TC1000 实体尺寸、等双轴 r3 完整 Job ROI 摘要。
- 更新：扩展[阶段 H 双轴 ROI 与厚度几何门槛](Agents/PA12实验数据处理/VFM自建/汇总/PA12自建VFM阶段H双轴ROI与厚度几何门槛.md)至 S15–S18；同步 `index.md`。未修改原始 JPG/DAT、Job、STEP、力表或结果文件。
- 结论：Job ROI 面积为 `828.038/759.324/775.980/704.606 mm²`；r3 DIC 支持积分面积为 `736.338/677.505/702.266/627.908 mm²`，支持率为 `88.93%/89.22%/90.50%/89.11%`。S15 完整 ROI 面积超过 `28.01×28.01 mm` 中心面；S17 同向投影有约 `0.066 mm` 临界超出；S16 仅 `0.05156 mm` 单侧居中余量；S18 尺寸可容纳但未注册。四组都没有定量图像—CAD 平移/旋转配准，故完整积分支持域的空间厚度分布仍不能确认。
- 厚度口径：用户确认的几何基准为中心平坦区 `1.000 mm`、外围 `3.000 mm`；r3 全域使用 `1.000 mm` 仍是条件性参考厚度。只有映射到中心平坦面的支持区可确认采用 1 mm，不能把过渡区/外围一概套用 1 mm 或 3 mm。
- 待验证：逐样本 CAD—图像配准残差、Job ROI 与积分三角网在平坦区/过渡区/外围的交面积、STEP/打印批次身份关联；四组 DIC 支持率均未达到 95% 门槛。

## [2026-09-30] experiment | S19 128 帧机器曲线与 VFM 口径诊断

- 来源：S19 原始 1000 Hz Press/Pos 工作簿、128 帧人工映射包、现有 S19 r3 单样本弹性 profile、共享 J2 诊断及 ISO 527-1:2019 官方预览。
- 更新：新增 [S19 128 帧机器曲线与 VFM 口径诊断](Agents/PA12实验数据处理/处理记录/S19_128帧机器曲线与VFM口径诊断_20260930.md)，并在 `index.md` 登记。原始工作簿和既有 VFM 输出未修改。
- 结果：人工映射力值与原始 Press 按映射时间重算最大差 `4.3×10⁻⁷ N`，但硬件同步未验证。原始 Pos 在 `0.05%–0.25%` 应变窗得 `504.02 MPa`（297 点，基于项目 30 mm 标距）；同帧全场 DIC 平均 `Eyy` 斜率为 `1754.27 MPa`，旧 126 帧 r3 的 S19 条件 E 为 `1683.97 MPa`（厚度 3 mm）。S19 pooled J2 的 50% 窗口在 `000063.jpg` 结束、最大应力约 `21.04 MPa`；机器曲线残差阈值候选在 `000088.jpg`、`28.42 MPa`，故现有窗口未覆盖候选屈服点。
- 待验证：实际帧同步时轴、初始夹持距离/应变标距及论文屈服定义。确认前不重跑 Y₀ 拟合，不把诊断候选发布为材料参数。

## [2026-09-30] audit | r3 机器合力与单位虚场边界映射

- 来源：S15–S19 r3 与 pool-source 配置、各自 MatchID Job ROI Shape、边界适配虚场及 ROI 积分实现。
- 更新：扩展[面积与外功边界证据审计](Agents/PA12实验数据处理/VFM自建/汇总/审计/2026-09-30_r3面积与外功边界证据审计.md)；同步 S19 双组件结论、固定方法页、项目总览和 `index.md`。
- 结论：S15–S18 的 X/Y 加载切边与配置中的机器力方向一致，S19 的 X 切边亦一致；代码在对应对边上定义虚场值 `0→1`。按用户确认的 ROI 边界合力口径，外虚功等于该轴 Press 合力乘单位差，不需要同帧实测边界位移或四边牵引分布。S19 第二组件约 `3.02×10⁻⁵ mm²`，与主组件共用同一连续场公式，积分权重可忽略。
- 待闭合：双轴 ROI 到中心 1 mm / 外围 3 mm 厚度区的空间注册；主域 DIC 支持率均低于 95%；S16 力表工程单位/设备标定、各组照片—力时序与参考预载定义。
- 验证：以源 Job 多边形、现有配置轴映射和代码中的边选择公式逐样本核对；未运行 VFM/J2/拟合，未改原始文件或配置。

## [2026-09-30] refactor | 科研论文六阶段工作流与技能分类

- 来源：用户提供的六阶段科研流程图和“6 大类 → 25 个 Skill → 交付目录”映射截图。
- 更新：新增 `AGENTS/科研论文SOP与工作流.md`；更新 `AGENTS/技能分类与调用协议.md`、`AGENTS.md`、`index.md`；原图归档于 `raw/assets/科研论文工作流参考/`。
- 技能：从 `Yuan1z0825/nature-skills` 下载 18 个 Skill 目录及 `nature-shared` 参考依赖；`literature-review` 为既有安装。四个图示名称未找到同名安装包，其余无同名项在 SOP 中注明可用映射。
- 结论：按图 1 标清六阶段与节点，按图 2 标清全部 25 项、六类、参考交付目录和本机状态；PA12 路线继续服从现有项目证据门槛。
- 待验证：新 Skill 的运行依赖、API、浏览器会话和外部服务未配置；需在新 Codex 会话加载后按具体任务调用。

## [2026-09-30] audit | S16 工作簿格式与力单位元数据

- 来源：现存 `xy-2-0.2.xls` 工作簿、S16 257 点帧—力索引及既有力源追溯报告。
- 更新：补充 [S16 力数据来源追溯](Agents/PA12实验数据处理/数据盘点/S16力源追溯.md) 的工作簿格式和内嵌属性；同步 `index.md` 与 PA12 项目总览。
- 结论：文件后缀为 `.xls`，实际内容为 XLSX/OOXML；含 3 个可见表 Pos、Speed、Press。Press 表没有单位、量程、校准、传感器型号或缩放信息。内嵌核心属性为创建者 `Bi-Axial Testing`，创建于 `2025-05-29 02:51`，修改于 `2025-08-13 23:46:24`；这些属性不说明工程单位，修改时间也不单独证明数据值改变。原配置文件仍未找到，身份链依据用户确认和现存 257 点索引吻合度。
- 待补证：采集软件导出单位/缩放配置、Press 通道到传感器序列号的映射、有效校准证书。设备量程 `0–10 kN` 不能代替这些记录；N 继续作为项目约定，正式单位门槛未闭合。
- 验证：使用只读工作簿解析检查 3 个工作表结构、全部表内文本及核心属性；未修改原始工作簿或派生力序列。

## [2026-09-30] audit | S15–S18 槽距配准候选与 ROI 厚度权重

- 来源：S15–S18 只读 `000000.jpg`、`Job.m2inp`、MatchID 元数据及首个有效合并 DIC 全场；固定几何基准为 TC1000：中心平坦区 `28.01×28.01×1 mm`、过渡边界 `30×30 mm`、外围 `3 mm`。
- 更新：阶段 H 新增狭缝节距中心候选、尺度偏差、Job ROI 与首帧支持三角网的 1 mm 平坦区/过渡区/外围分区及厚度积分权重上下界；同步 `index.md`。仅修改 Wiki/索引/日志，未修改原始照片、DAT、Job、STEP 或合并表。
- 结果：Job ROI 平坦区/过渡区面积 (mm²)：S15 `781.809/46.230`、S16 `757.168/2.156`、S17 `772.590/3.391`、S18 `704.606/0`。首帧 DIC 支持分区 (mm²)：S15 `756.939/6.955/0`、S16 `677.505/0/0`、S17 `702.266/0/0`、S18 `627.908/0/0`（顺序为 1 mm/过渡/3 mm）；对应支持域 `∫t dA` 分别为 S15 `763.894–777.803 mm³`、S16 `677.505`、S17 `702.266`、S18 `627.908`。S15 首帧支持面积与 r3 全历程共同支持面积不同，已分开标记。
- 限制：槽距反算尺度相对 MatchID 标定偏差 `0.46%–2.03%`，槽线残差最高 `3.32 px`；仅估平移中心，旋转/剪切/镜像/透视及中心定位误差未闭合。配准仍为候选，不作为精确物理注册；r3 全历程支持率继续低于 95%。没有进行 VFM/J2 拟合或参数发布。

## [2026-09-30] audit | 独立 SLS PA12 硬化符号口径

- 来源：[独立 PA12 本构与公开实验曲线证据](Agents/PA12实验数据处理/VFM自建/汇总/审计/2026-09-30_独立PA12本构与公开实验曲线证据.md)及当前有限变形 J2 实现。
- 更新：修正 `wiki/PA12项目全景与总控指令.md` 的当前未闭合事项与时间线；`index.md` 已有该独立文献报告入口。
- 结论：独立 SLS PA12 多机制研究定义 `Q>0` 为硬化、`Q<0` 为软化；当前 J2 `σ_y=Y0+H·ε̄p` 中正 H 同样表示硬化，符号方向一致。文献的 `(Q,b)` 不转换为 `(Y0,H)`；现有 pooled H 数值和正式参数发布仍受覆盖率、残差、数据资格及可辨识性门槛约束。
- 验证：核对来源报告中的模型公式与当前代码定义；未重新拟合、未发布参数。

## [2026-09-30] refactor | S19 人工 128 帧主路线整理

- 来源：[S19 128 帧人工映射包](Agents/PA12实验数据处理/MatchID_VFM准备/S19_X_0.2整理_128帧人工映射/)、[主序列逐帧对照](Agents/PA12实验数据处理/MatchID_VFM准备/S19_X_0.2整理_128帧人工映射/S19_X_0.2_128帧主序列对照旧诊断.csv)、Stage 1 有限变形虚功诊断及项目确认的单轴 `3 mm` 厚度口径。
- 更新：[唯一执行路线](wiki/PA12项目全景与总控指令.md)、`index.md`、[S19 主报告](Agents/PA12实验数据处理/处理记录/S19_X_0.2_处理报告.md)；修正有限变形 J2 runner 将 `geometry_repair` 配置传入 Job ROI 读取，并更新相应测试夹具和单轴厚度期望。
- 结论：S19 唯一主序列定为 128 帧人工映射，硬件同步仍未验证；旧 126 帧只保留逐帧时间/力对照。共同帧 DIC 点位逐点一致。完整 Job ROI 支持率 `84.8667%`，固定 `ν=0.375` 的条件 `E=1713.651696 MPa`；`ν` 未识别，Press 合力外功共轭未验证，因此当前不进入有效 J2 参数识别，不发布 `Y/H`。
- 整理：移除旧 126 帧重复 DIC 包、未验证应力候选包及其冗余摘要、重复的 `.vfm` 分量副本和两份失效 126 行 VFM 输入，共 9 个派生/失效文件。共同帧 DIC 数据仍在 128 帧包中，旧时间/力值仍在对照表中；原始 JPG、DAT、XLS 未修改。
- 验证：主索引、人工索引、逐帧对照、X/Y 力文件及 ZIP 均为 128 帧；有效 DIC—力帧 `128`，源目录登记为 `130` 张 JPG / `128` 个 DAT；有限变形 J2 专项测试 `17` 项通过，全库 `327` 项及 `2` 个子测试通过。
- 待闭合：人工时轴的物理同步、首帧 `0.6 N` 残余按统一基线规则处理、完整 Job ROI 支持率、外功边界共轭和 `E/ν` 可辨识性。门槛通过后再进入 J2 `Y/H` 与独立验证。

## [2026-09-30] refactor | PA12 科研论文六阶段工作台

- 来源：现有 PA12 文献研读、总控页、方法页、VFM 诊断汇总及已确认的六阶段 SOP。
- 更新：新增 `wiki/PA12科研论文六阶段工作台.md`；更新 `index.md` 与 `AGENTS/科研论文SOP与工作流.md` 的入口和阶段状态。
- 结论：文献检索与阅读已有首轮成果；研究与数据阶段仍处于 S19 128 帧主序列及 VFM 门槛闭合；写作目前搭建结构，尚未形成正式初稿；审稿与成果转化尚未启动。
- 待验证：硬件时序、完整 ROI DIC 支持、载荷/虚功和厚度区注册、E/ν 可辨识性、本构符号及后续 J2 独立验证。

## [2026-09-30] refactor | 六阶段 Skill 映射入工作台

- 来源：用户提供的图 2 Skill 分类表与 `AGENTS/科研论文SOP与工作流.md` 的安装状态和替代路线。
- 更新：在 `wiki/PA12科研论文六阶段工作台.md` 增加 25 项 Skill 到六个工作阶段的映射；更新 `index.md` 页面说明。
- 结论：工作台可按论文阶段直接定位对应 Skill；安装状态、未找到同名包的项目及替代路线继续以 SOP 总表为准。
- 待验证：新 Skill 的外部 API、运行依赖和机构访问配置仍按各 Skill 的配置说明单独核实。

## [2026-09-30] diagnostic | S19 128 帧机器 E 与 Y₀ 口径复核

- 来源：S19 原始 1000 Hz Press/Pos 工作簿、128 帧人工映射索引、S19 128 帧 VFM profile、r3 ROI/外功边界审计及 ISO 527-1 官方预览。
- 更新：修订 [S19 128 帧机器曲线与 VFM 口径诊断](Agents/PA12实验数据处理/处理记录/S19_128帧机器曲线与VFM口径诊断_20260930.md) 和 `index.md`；原始工作簿、人工映射及 VFM 配置未修改。
- 结论：用户确认初始夹持距 `30 mm`、试样厚度 `3 mm`，并确认 `000000=0 s`、`000127=12.845 s` 线性映射继续用于诊断。原始机台名义 E=`504.02 MPa`；同一 24 帧窗口 Pos/DIC/VFM 斜率为 `518.72/1754.27/1713.65 MPa`，表明机台名义应变与全场 DIC/VFM 应变当前不等价。完整 ROI 覆盖率 `84.87%` 未过 95% 门槛。128 帧曲线在断裂前未观测到应力平台，`28.42 MPa` 只作残差阈值候选，不作为标准 Y₀。
- 待反馈：确认论文 E 的应变基准及 Y₀ 定义；定义确认和完整 ROI 覆盖门槛解决前不继续参数拟合、不发布 E/Y₀。

## [2026-09-30] refactor | 六阶段 Skill 实施路径

- 来源：用户提供的六阶段科研工作流图、25 项 Skill 分类图、本 Vault 科研论文 SOP 与 PA12 项目总控资料。
- 更新：在 `wiki/PA12科研论文六阶段工作台.md` 增加逐阶段输入、调用顺序、交付物、放行条件和 PA12 当前推进优先级；更新 SOP 与索引入口。
- 结论：Skill 以阶段交付和证据门槛驱动；当前 PA12 主线仍在阶段 3，阶段 4 可保留结构准备，阶段 5 待完整初稿，阶段 6 按需启动。
- 待验证：第三方 Skill 的外部 API、运行依赖、机构访问权限及单独部署配置按调用前置条件核实。

## [2026-09-30] update | 阶段 H 实物尺寸口径统一

- 来源：用户定稿的概念图实物尺寸口径、[双轴试样实体尺寸图](AGENTS/PA12双轴试样仿真/图纸/PA12双轴试样实体尺寸图/PA12双轴试样实体尺寸图.svg)和 TC1000 源 STEP/B-rep 拓扑。
- 更新：阶段 H 证据页及 `index.md`，删除将逐样本 STEP/打印记录身份链作为尺寸放行条件的表述。
- 结论：S15–S18 直接采用已定稿的 TC1000 实物几何；后续 VFM 几何门槛是 DIC 图像到试样平面的配准与支持域覆盖率。
- 记录核对：图纸链接存在，阶段页、索引和日志中的整体尺寸一致；尺寸真实性不再列为待确认项。

## [2026-09-30] refactor | Obsidian 双库收敛与日常整理规则

- 来源：用户确认合并方案；对当前 Vault、旧 second brain、Git 状态和 Obsidian Vault 注册表进行内容级核对。
- 更新：新增根目录 `README.md`、[双库合并与归档说明](AGENTS/PA12实验数据处理/处理记录/Obsidian双库合并与归档说明.md)及[今日摘要](wiki/daily/2026-09-30.md)；收敛 `index.md` 与 PA12 总控页的旧库表述、入口和大小写链接；从 Obsidian 注册表移除旧 Vault 条目。
- 结论：`D:\2026.9.21_finally` 是 PA12 项目唯一活动工作库；旧 `second brain` 目录、旧 Git 状态和 Abaqus 工件保留为只读恢复档案。PA12 仍只有 S19 128 帧人工映射这一主序列，后续按总控页的单一路线推进。
- 待处理：旧库中 47 个主库未找到同路径文件的资料继续留档；其研究价值尚未逐项裁定。既有 Git 暂存变更不纳入本次整理提交。

## [2026-09-30] ingest | DIC-VFM 目录入库与初始处理链路

- 来源：`D:\C盘迁移\Desktop\yuan\DIC-VFM`，含 S15–S24 的 DIC/VFM 导出和配套项目文件。
- 更新：按原结构复制至 `raw/DIC-VFM/`；新增 [目录与初始处理链路](wiki/methods/PA12_DIC-VFM目录与初始处理链路.md)，并更新 `index.md`。
- 结论：共 1,526 个文件、8,014,026,403 字节，源与副本逐相对路径的文件数及大小一致；索引含十组样品、1,486 个逐帧导出条目。目录展示了 DIC 点场、照片力索引、X/Y 力数组及 MatchID/VFM 导出之间的关系。
- 待验证：该目录不含完整 DAT、十组原始 Press 工作簿或同步脚本；S19 照片 ZIP 比覆盖表少 1 张；S16 应力单位、所有样品的力时钟来源和部分坐标单位仍需对应原始来源记录。

## [2026-09-30] update | r3 VFM 外功与硬化符号证据状态

- 来源：S22 原始 DIC—力索引、S22 r3 配置、共享单轴 J2 逐帧 CSV、S16 力源追溯、r3 面积/外功审计、窗外残差审计及独立 SLS PA12 本构文献。
- 更新：修正 [r3 共享 J2 汇总](Agents/PA12实验数据处理/VFM自建/汇总/PA12按加载模式共享有限变形J2双域诊断_r3_20260930.md)中过时的外功边界和硬化符号状态，并同步 `index.md`。
- 结论：S22 的 223 个输入帧与共享 J2 CSV 中 188 帧逐一对齐到 `001504.jpg`；后 35 帧从 `001512.jpg` 起被配置整体截断。VFM 按 DIC 三角形与完整 ROI 的交叠面积乘厚度积分，无额外宽度因子；按用户确认的 ROI 合力口径，`0→1` 单位虚场的外功映射已闭合。当前线性 J2 中正 H 表示硬化的符号方向获独立 SLS PA12 来源支持，但文献参数不直接换算为项目 `Y0/H`。S16 工作簿身份及派生时序匹配已确认，工程单位仍无原始采集/校准证据。
- 待验证：全 ROI DIC 支持、双轴 ROI 到中心 1 mm/外围 3 mm 厚度区的注册、各样本力单位与照片时序、参数稳定性和独立验证。未重跑拟合，未发布 E/Y/H。


## [2026-09-30] ingest | PA12 S15–S24 全量模板人工映射整理

- 来源：S15–S24 的 PAPER DIC JPG/DAT、配置中对应的 Press 工作簿、已确认人工映射及现有逐帧索引。
- 更新：新增全量整理包、样品 ZIP、全量索引、源映射、数据覆盖与 XZ 未同步清单；更新数据可用性报告、样品—力映射表、index.md 和初审工作簿。
- 结论：10 个 XY 样品包共 1,486 个真实逐点帧，全部从 000000.jpg 开始；用户确认人工映射，硬件触发未验证。S16 258 帧 sxx/syy/sxy 压缩源包逐字节保留；S19 仅收 128 帧版本且无这三列。其他 XY 样品不从应变反算应力。XZ 有 81 个配对 DAT 均无应变记录、951 张图片无 DAT，无已确认力—时间映射。
- 首帧口径：S15、S17、S18、S20–S23 的 000000 由真实 DAT 重建；时间从首个既有映射帧按配置帧率回推，若早于力表起点则取 T=0；力按源 Press、既有基线/符号规则插值。S24 按帧号/500 fps，保留约 1555.5 N 预载释放力。原始 JPG/DAT/Press 未修改。
- 验证：10 个样品 ZIP 和总 ZIP CRC 检查通过；逐点帧数、索引和 X/Y 力数组逐样品一致；所有包含 000000；S16 原应力 ZIP 与源完全相同；S19 恰为 000000–000127；总包不含 126 帧旧候选包。
- 待验证：硬件触发时基、源力/应力单位与校准、各样品正式 VFM 的力零点/ROI/边界门槛；XZ 的应变 DAT 与力—时间映射。
## [2026-09-30] ingest | 三篇 VFM/FEMU 方法论文与公式解析

- 来源：三篇原始 PDF，分别为有限应变弹塑性 FEMU/VFM 灵敏度比较、FEniCS 非均质超弹性 VFM、机器学习 VFM 各向异性超弹性；原件归档于 raw/papers/力学反问题与VFM-FEMU标定/。
- 解析：使用本机 MinerU 全文解析 56 页；原始 PDF 保留，解析稿位于同目录的 mineru/。关键目标函数、局部状态灵敏度、虚应变参数更新、ICNN 参考态修正和多虚场损失已对照渲染页核读。
- 更新：新增三篇 16 节论文卡、PA12 方法迁移与六阶段执行路线、核心公式索引及 LaTeX 源稿；同步 PA12 六阶段工作台与 index.md。
- 结论：Kumar et al. 的弹塑性合成基准最接近当前材料模型；Deng、Meng 两篇研究超弹性，只迁移虚场、参数更新和变形模式验证思路。当前 PA12 同步、完整 ROI 支持和相关识别门槛未放行，论文方法不构成正式参数证据。
- 待核：Meng et al. 正文称主动脉训练数据有七个压力级，但明确列出的压力值为六个；卡片按列出的值登记，实际级数待原始数据或补充材料确认。Kumar 论文卡采用结构/公式号定位，公式索引保留 MinerU 页 locator。
- 下一步：按 PA12 项目总控页继续关闭当前数据资格门槛；只有放行后再决定是否进行同条件 FEMU/VFM 对照与跨加载模式留出验证。

## [2026-09-30] update | 固定 S19 机台—DIC—VFM 单一路线

- 来源：用户确认的 S19 30 mm 实测夹持距、3 mm 厚度和 128 帧诊断映射；原始 1000 Hz Press/Pos；S19 DIC 位移场与 Job ROI。
- 更新：收敛 `wiki/PA12项目全景与总控指令.md` 与本索引的唯一执行顺序；新增并更新 [S19 机器曲线与 VFM 口径诊断](Agents/PA12实验数据处理/处理记录/S19_128帧机器曲线与VFM口径诊断_20260930.md)；修正有限变形 J2 诊断生成器关于数学虚位移的说明并加回归测试；新增 S19 128 帧诊断配置和内外虚功结果。
- 结论：机台名义 `E=504.02 MPa` 与当前 VFM 条件 `E=1713.65 MPa` 属不同应变口径，不能强制相等；全 ROI 覆盖率 `84.87%` 未过 `95%` 门槛，内外虚功合并 RMS `119.7749 N`，J2 参数 Jacobian 秩 `0/2`。当前不发布最终 `E/Y₀`，不继续调参追数值。
- 下一步：只补齐实际 30 mm 夹持段两端在 DIC 图像/坐标中的注册，再进行同窗虚拟引伸计对照并处理缺失的 ROI 支持面积；从机器力/位移和 DIC 标尺校准建立误差预算后，按虚功、可辨识性、独立验证顺序放行或停止。

## [2026-09-30] ingest | Wu2023 SLS PA12 直接机台曲线

- 来源：Wu 等 2023 *International Journal of Solids and Structures* 论文、ORBi 论文/数据记录、公开 GitLab 仓库与 Zenodo 数据集 DOI 10.5281/zenodo.7792804；仓库 README 和 25 个单试样 CSV。
- 更新：归档作者后印本及原始曲线文件；新增 [Wu2023 曲线长表](Agents/PA12实验数据处理/文献数据/Wu2023_SLS_PA12_public_curves.csv)，更新[独立本构与曲线证据页](Agents/PA12实验数据处理/VFM自建/汇总/审计/2026-09-30_独立PA12本构与公开实验曲线证据.md)、方法页与 `index.md`。
- 结论：25 件 PA2200 SLS 拉伸记录合计 11,795 行，列含 Time(s)、Extension(mm)、Load(N)、Eng.strain、Eng.stress(MPa)，为公开机台导出而非图像数字化。H=打印层面垂直加载方向，V=平行加载方向；速率为 `7.37×10⁻⁴`、`7.37×10⁻³`、`7.37×10⁻² s⁻¹`。每件实际厚度、宽度和高度在长表逐行保留；应力应变原值未重算。Wu 的拉伸硬化率定义和 Zadeh 的 Q 符号为当前正 J2 H 的独立方向依据，不构成参数数值映射。
- 限制：Eng.strain 与 Extension/Height 一致到 5×10⁻⁶ 舍入误差，是全局机台应变；H/V×速率组合不平衡。Psarros 补充曲线 SI 当前仍未取得；外部文献参数不替代本项目正式 E/Y/H。

## [2026-09-30] update | VFM/FEMU 公式排版与来源审计

- 来源：三篇原始 PDF、对应 MinerU 全文解析稿、核心公式索引与三张论文卡。
- 更新：编译并逐页检查 `wiki/methods/PA12_VFM-FEMU核心公式复现.pdf`；为三张论文卡保存审计报告至各自 `mineru/*_support/audit-report.json`。
- 结果：公式稿共 3 页，文献原式与待验证的 PA12 适配表达分开标注。Deng、Meng 卡片通过章节和方程覆盖审计；Kumar 卡片通过结构定位审计，其来源清单覆盖因 MinerU source bundle 不可用未执行。
- 下一步：按六阶段路线先关闭 PA12 数据同步与全场支持门槛，再评估同条件 FEMU/VFM 对照和跨加载模式留出验证。

## [2026-09-30] lint | S15–S24 人工映射模板包自查

- 发现：首轮交付中 S24 的 DAT 质量审计表只有表头；10 个 XY_RAW 目录曾被写成“重复数据”，但其与 PAPER 的映射尚未核实；需确认单样品 ZIP 独立使用时确有逐点场、帧索引及 X/Y 力数组，并解释源目录中未入包的配对帧。
- 修改：从 S24 原始 DAT 重新生成 157 帧质量审计，均含 `<18>` 位移与 `<53>` 应变记录，点数范围 7,024–7,064；更新 S24 ZIP。修正 XY_RAW 范围说明，新增 10 个来源目录、5,280 对 JPG/DAT 的待匹配清单。更新覆盖清单、自查说明、总 README 和全量包；逐样品包共 1,486 帧，首帧、索引行及 X/Y 力数组行数一致；S16 的 258 帧保留 `sxx/syy/sxy`，S19 仅保留 128 帧。源中 252 对未入包帧均在覆盖清单列明来源与排除依据。
- 限制：XY_RAW 与 S15–S24/PAPER 的关系和力映射未确认，因此 5,280 对未纳入当前包；硬件触发同步仍未验证，当前包不是正式 VFM 放行结果。
- 下一步：按自查说明复核本次总 ZIP 和 10 个样品 ZIP 的 CRC、帧/索引/力数组一致性及源覆盖关系；后续若要纳入 XY_RAW，先完成其样品对应及力时轴映射。

## [2026-09-30] ingest | PA12 可辨识性与加载路径方法文献

- 来源：Ricciardi et al. 期刊论文的 arXiv v2 开放全文及 DOI/出版社记录；补充筛选 Marek、Grama、Jones、Martins、Zhang、Jafari 等原始研究。
- 更新：归档 Ricciardi PDF；完成 MinerU standard 全文 41 页解析及第 8–10 页公式原页核对；新增 16 节论文卡、可辨识性/跨模式验证路线、公式 Markdown 与 LaTeX 源稿；更新 index.md 与三篇论文迁移路线。
- 结论：本文可迁移的是以后验不确定性和 EIG 规划下一加载步；PA12 已有数据应先比较单轴、等双轴和联合数据的灵敏度谱、参数协方差及独立跨模式预测。2025 年已有 FE-VFM 与 sensitivity-based VFM 集成成果，不能把方法拼接本身写作新颖性。
- SI：未发现 Ricciardi 期刊论文的独立 SI 文件；算法附录 A 和结果附录 B、C 已包含在所解析的 arXiv 全文中。
- 待验证：其余重点候选完成全文获取与 MinerU 精读；PA12 同步、ROI 支持与本构参数可辨识性门槛通过；完成跨模式留出结果后再判断候选新颖性。
- 下一步：严格按 PA12 总控页关闭数据资格门槛，再执行 U、B、U+B 的可辨识性和整试样/整模式留出预测比较。

## [2026-09-30] audit | Psarros SI 公开获取核查

- 来源：Psarros 等（2025）Wiley 开放论文页面及出版方补充材料下载入口。
- 核实：出版方页面确认完整工程应力—应变曲线位于表 S9–S10，附件名 `adem70164-sup-0001-SuppData-S1.pdf`，标示大小 816.9 KB；官方补充材料下载请求返回 HTTP 403。公开检索未发现可核验的作者仓库副本。
- 结论：补充表的存在及定位已确认，文件仍未取得、读取或数字化。现有 Wu2023 公开 SLS PA12 曲线保持为可用完整工程应力—应变来源；不将 Psarros 表记为本地数据。
- 更新：[独立 PA12 本构与公开实验曲线证据](Agents/PA12实验数据处理/VFM自建/汇总/审计/2026-09-30_独立PA12本构与公开实验曲线证据.md)及 `index.md`。

## [2026-09-30] lint | S19 128 帧 DAT 审计补齐

- 发现：S19 最终 128 帧的逐点场和源 JPG/DAT 配对完整，但样品包原 DAT 质量审计只列出 `000002–000127` 的 126 帧。
- 修改：按最终 128 帧索引重新审计源 DAT，将完整质量表更新到 S19 样品 ZIP，并放入配套文件目录；同步更新总 ZIP、README 与自查说明。未改动原始 JPG/DAT 或对应 126 帧历史索引。
- 结论：128 份 DAT 均含 `<18>/<53>` 记录；`000000` 与 `000001` 各有 9,144 点，整组点数范围 9,143–9,144。
- 下一步：复核更新后的总 ZIP、10 个样品 ZIP、源配对覆盖清单和索引/力数组行数。硬件触发同步仍未验证。

## [2026-09-30] refactor | 六阶段工作台接入可辨识性路线

- 来源：现有六阶段工作台与 PA12 单轴/等双轴可辨识性路线。
- 更新：在阶段 03 加入补充路线入口，明确该路线在数据门槛通过后执行，并保留原六阶段框架和项目总控门槛。
- 结论：主工作台可从研究设计阶段直接进入 U、B、U+B 的辨识性与跨模式预测比较。
- 待验证：PA12 同步、ROI 支持、虚功残差和参数识别门槛通过后再执行比较。

## [2026-09-30] lint | S15–S24 交付复核收尾

- 发现：最终自查确认 S19 128 帧配套 DAT 审计最初缺少 `000000/000001` 两行；这两帧的原始 DAT 均完整，且已补入最终样品包审计。
- 修改：更新 S19 包与配套目录，补充审计说明并同步总 ZIP；索引登记本次审计结论。
- 结果：10 个样品共 1,486 帧；索引和 X/Y 力数组逐样品行数一致；S16 258 帧均保留 `sxx/syy/sxy`；S19 128 份 DAT 均含 `<18>/<53>`；S24 157 份 DAT 均含对应记录；252 对未入包源配对帧全部列明。总 ZIP 与 10 个样品 ZIP CRC 检查通过。
- 待验证：硬件触发同步未验证；10 个 XY_RAW 来源目录的样品身份及力时轴对应未核实。
- 下一步：仅在完成 XY_RAW 样品映射及力时轴来源核对后纳入其他来源；当前人工映射包不等于正式 VFM 放行。

## [2026-09-30] update | Stage H 双轴 B-rep 厚度积分与注册复核

- 来源：[阶段 H 双轴 ROI 与厚度几何门槛](Agents/PA12实验数据处理/VFM自建/汇总/PA12自建VFM阶段H双轴ROI与厚度几何门槛.md)、TC1000 STEP B-rep、S15–S18 只读参考图/Job 与 r3 支持索引。
- 更新：报告以四臂七槽中心线拟合候选四参数相似变换，并将 TC1000 B-rep 局部厚度积分到首帧及 r3 全历程共同支持域；同步 `index.md`。
- 结论：15,345 个厚度查询点与支持网格完整对应，查询厚度为 `1.0000000002–1.3269820854 mm`；八个支持域均未进入外围 3 mm 区。S15 等效厚度首帧/全历程为 `1.001694/1.001275 mm`，S16–S18 为 `1.000000 mm`。候选注册的最大残差为 `5.01–10.96 px`。
- 限制：全历程 DIC 覆盖率 `88.9256%–90.5004%`，低于 95% 门槛；候选注册未经过独立留出点验证。本次只更新几何/支持域报告，不重跑 VFM/J2、不拟合或发布参数。

## [2026-09-30] update | S19/S16 成对主样本路线与 S16 258 帧虚功诊断

- 来源：用户确认的 S19 128 帧和 S16 258 帧人工映射；S16 逐帧 DIC 合并场、参考 DAT 及 `configs/pa12_finite_vfm_biaxial_s16.json`。
- 更新：S16 参考照片帧复用已加载的 `000000.jpg.dat` 位移场，其余帧读取既有合并场；人工映射列名在读取时规范化，不改源索引。新增 S16 258 帧诊断汇总，并将唯一执行路线明确为 S19 单轴 + S16 等双轴这一对。
- 结果：S16 输出与输入索引 258 行逐行一致，照片顺序、时间及 X/Y 力相同；共同网格每帧 10,098 点。完整 Job ROI 支持率 89.2248%，低于 95% 门槛；虚功状态 `BLOCKED_INCOMPLETE_DIC_SUPPORT`。固定 ν=0.375 的条件 E 为 3498.487479 MPa，自由 ν 的 1% 残差带为 0.27059–0.499，均为诊断值，不作参数放行。
- 限制：S19 全 ROI 支持率为 84.87%；两组人工时轴不是硬件触发验证。S16 Press 单位/标定、实际厚度区注册和完整域外功等价仍未闭合。S16 每次运行的逐帧 CSV、质量表和图片保留在由配置生成的本机派生目录，不纳入本汇总页。
- 下一步：按唯一主路线补闭合 S19/S16 的时间、坐标、厚度、ROI 与力单位资格，再完成完整曲线和虚功/E/ν 评估；仅当这些门槛通过后才进入 J2 Y/H 与独立验证。
