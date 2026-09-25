# PA12 单轴/双轴拉伸：GPT → 自建 VFM / MatchID 历史审计交接文档

> 下一次 GPT 必须先读本文件、`PA12实验总体方法与防跑偏协议.md`、`PA12_GPT交接状态.json`、`PA12批量处理清单.json`、`PA12数据合理性审计报告.md`、`PA12数据合理性审计结果.json`、`MatchID_VFM准备/PA12_MatchID_VFM闭环状态.md`、`MatchID_VFM准备/PA12_环境检查.md`、`MatchID_VFM准备/PA12_DIC_DAT质量审计.md`、`MatchID_VFM准备/PA12_VFM边界载荷说明.md` 和 `configs/pa12_vfm_boundary.json`。主流程使用自建 VFM；历史 MatchID 资料只作格式、方向、边界和 GUI 试算审计证据。用户确认外围机器力直接作为 ROI 边界合力，不重建四边牵引分布。

## 1. 用户意图和当前边界

用户不是只要若干 CSV，而是要一条可重复的 PA12 实验处理链：

1. 按真实受力起点和断裂掉载点选择有效照片。
2. 用同一照片时间轴插值 X/Y 力。
3. 生成照片—力对应表、单列 VFM 力值 CSV、检查图和名义应力—应变审核结果。
4. 将同一帧的 DIC 全场位移/应变和边界载荷接入自建 VFM 主路径；保留历史 MatchID 输入作为审计对照。
5. 在单位、标定、几何和边界条件确认后，再识别材料参数。

当前已完成同步力值、逐帧 DAT 质量审计、同版本 MatchID 字段交叉验证和 8 组 DIC 全场—力合并；自建 VFM 阶段 A 已对四组等双轴数据完成逐点内外虚功和两阶段候选计算。历史 MatchID GUI 试算仅作审计证据：S16 的试算分别有载荷不同步和 Forces 缺失问题。同步力 CSV、DIC 合并、自建 VFM 候选和 GUI 中间迭代都不是最终材料参数识别结果。

## 1.1 最新验证状态

- 自建 VFM 与全量回归测试：`100/100` 通过，包含旋转后机器轴映射与 E–ν 剖面合成数据测试。
- Python 编译检查：`python -m compileall -q tools tests` 于 2026-09-26 通过。
- 力值/概览审计：10 组概览和 10 组 MatchID 实验索引齐全；8 组正式力值三文件通过数量与数值契约，S23 为诊断状态，S24 为预载释放记录。
- 输出契约审计：通过（`audit_passed=true`）；8 组正式力值三文件的照片/X/Y 行数分别一致；整体 `formal_vfm_ready=false` 仅由 S23、S24 状态门禁导致。
- 语义复核：历史 `PA12数据合理性审计结果.json` 的实验级 `formal_vfm_ready:true` 和 `PA12批量处理报告.md` 的“正式 VFM 已完成”表示同步力值/输出契约通过，不表示 MatchID `.vfm` 工程或虚功/参数识别完成。当前以 `PA12_MatchID_VFM闭环状态.json` 的 `formal_matchid_vfm_ready=false`、实际 `.vfm` 文件和人工 VFM 审计为准。
- 应力—应变审计：6 组通过，3 组需要曲线/事件人工复核，S24 为预载释放记录；尚未对原始派生 CSV 平滑或补点。最终曲线需保持完整连续、中文标注，X/Y 同图；若显示层使用平滑，必须与计算数据分离。
- MatchID 闭环审计：8 组为 `MATCHID_VFM_INPUT_READY`；S23 为 `FORCE_REVIEW_REQUIRED`；S24 为 `PRELOAD_RELEASE_ONLY`；`formal_matchid_vfm_ready=false`。
- 当前版本 MatchID 2D 19.2.2.0 的 DAT 字段映射、Results Viewer 导出列、分隔符和单位已经本地同帧交叉验证；更换版本时必须重新验证。
- 方向/边界格式审计：完整 `S16_XY_0.2_258.vfm` 为 4 个 `Boundary`、4 组 `Forces`、每组 258 帧、中心厚度 `1 mm`，首帧为零且后续力值为正；旋转后边界映射为顶部=X2、底部=X1、左侧=Y2、右侧=Y1。该审计不等于已完成 VFM 识别。
- 自建 VFM 阶段 A（旋转后机器轴映射修正并重算）：S15/S16/S17/S18 分别输出 284/257/12/126 帧；逐帧积分为 `pointwise_triangle`，最低面积比约 0.895428、0.892248、0.905004、0.891147，四组均为 `REVIEW_REQUIRED`。固定 `ν=0.375` 条件候选依次为 S15 `E=3536.45/Y=34.06/H=154.56 MPa`、S16 `3410.42/39.49/156.39 MPa`、S17 `E=4997.67 MPa`（Y/H 未计算）、S18 `4605.76/43.77/632.27 MPa`；ν 剖面未能独立识别 ν，这些均不是最终材料参数。
- 自建 VFM 阶段 B：S19–S22 已接入真实 Job Polygon 和逐点三角形积分；旋转方向修正后的固定 `ν=0.375` 结果为 S19 `E=5389.40/Y=8.94/H=23357.94 MPa`、S20 `17600.49/41.74/18526.97 MPa`、S21 `16912.33 MPa`（Y/H 点数不足）、S22 阶段 1 模量非正，阶段 2 阻断。四组均保持 `REVIEW_REQUIRED`；单轴实际厚度、有效宽度、标距、积分域和外部虚功边界仍无独立证据，因此这些值只是诊断候选，不是材料参数或代理模型标签。详见 [阶段 B 单轴 Polygon 复核](../VFM自建/汇总/PA12自建VFM阶段B单轴Polygon复核.md)。
- 最新 GUI 试算（用户报告及当前截图）：S16 `3try` 的 X/Y 力 MAE 为 `26.1206/23.4119 N`，末帧绝对差为 `1452.79/1478.85 N`，载荷不同步；`4try_step3` 的 Forces count 为 `0`。两次均不进入参数识别。S16 第 16 轮界面显示约 `70%` 进度、`Y=63.93 MPa`、`H=41.55 MPa`、残差栏 `1214`、迭代 `16`；`E`、`ν` 未显示，残差定义/单位未核实。上述只列作 GUI 中间候选，不是最终识别结果。
- 并行流程只读快照补充：受保护的 `configs/pa12_vfm_boundary.json` 及其当前 Markdown/CSV 报告还记录了第 `28` 轮 `Y=61.94 MPa`、`H=139.60 MPa`、界面值 `1655` 的另一份 GUI 中间候选；该快照不覆盖本交接状态中按用户要求保留的第 `16` 轮记录。两份候选均不是最终识别结果，且当前报告/配置不在本次修改范围内。
- 论文本构公式待核验：第 2.3.2 节式 (2.19) 原页为 `σ_y=σ_y0−H ε̄p`，参数页列 `σ_y0=21 MPa`、`H=+180 MPa`。按字面是软化斜率，外推约到 `ε̄p=0.1167` 时屈服应力降至零；不能默认是论文排版笔误，也不能据此猜 MatchID 的 H 定义。官方 Abaqus 资料说明等向塑性屈服应力可随等效塑性应变增加或降低；当前六份可查几何扫描 `.inp` 均为 provisional Elastic 卡，没有 `*Plastic` 材料表。
- 检查器最新状态：`test_pa12_vfm_check.py` 定向测试 `4/4` 通过；只读调用 `build_current_check(configs/pa12_rotated_batch.json)` 成功返回四组结果，并从相邻 `configs/pa12_vfm_boundary.json` 读入 S16 候选快照及 ROI 状态。当前 Markdown/CSV 已由并行流程更新，随后经只读逐字段比对与当前 builder 结果一致；本轮未调用 writer。该检查器和配置仍属于 MatchID 历史审计分支，不改变自建 VFM 主路径。

### 当前检查器与报告一致性审计

- 上一轮发现的候选参数字段与单一配置入口错误已在当前代码中修正：构建器以 `configs/pa12_rotated_batch.json` 为批次输入，并读取同目录的 `pa12_vfm_boundary.json` 状态快照；定向测试从 `3/4` 更新为 `4/4` 通过。测试仍是单元级，未覆盖完整生产配置构建。
- 只读生产构建现可返回 S15/S16/S17/S18 四行；受保护并行配置/报告快照带入 S16 第 28 轮候选值，而本交接状态另保留用户要求的第 16 轮候选值。两者都只属于 GUI 中间快照，不解除 Force 序列门槛，也不构成最终参数。直接把边界配置作为批次主输入仍不支持；批次配置才是当前入口。
- `summarize_check()` 将 `vfm_force_status` 仅追加到“结论”备注，不参与 `reasons` 或“时间同步”列判定。因此 S16 可同时显示“时间同步：通过”和“VFM Forces 与同步序列不一致”；前者只说明预处理照片—力表一致，后者说明具体 MatchID VFM 输入序列未闭合，报告需要明确分开表达。
- 当前 Markdown/CSV 已各有 4 行，并与当前 builder 的 `REPORT_FIELDS` 全字段逐行逐字段一致（CSV 4 行、Markdown 4 行、差异 0）。S15 已区分视觉断裂帧与末有效帧；S16 已分别表达预处理同步和 VFM Forces 未闭合状态。
- S15 的 `000284.jpg` 同步力表末行与两轴单列力 CSV 一致：X=`1608.18 N`、Y=`1603.33 N`。Markdown 中 Y 峰值 `1603.83 N` 是峰值统计值，不是末帧值，应按不同字段含义呈现。
- 当前报告文件的最后修改来自并行流程；本轮仅做只读一致性比对，没有调用 writer，也没有修改 Python、测试、配置或报告文件。
- S15 帧数复核：照片—力表 284 条数据记录；X/Y 单列力 CSV 各 284 行；DIC—力状态与索引均为 284 帧，排除无效场点 568 个。`000285.jpg` 虽有同名 DAT，但仅约 5,277 点（前帧完整场约 98,000 点），作为视觉断裂证据保留且排除出正式 DIC/VFM；`000284.jpg` 是最后有效帧。原 GPT 机器状态中的 285 帧/570 个排除点及“合并保留 000285”的描述过时。
- GUI 只读核验（2026-09-24）：最近截图显示 Virtual Fields Module 打开的是 S16 `4try_step3` 工程（此前曾观察到 S16 `3try`），不是 S15；可见中间迭代和虚功/残差曲线，不能作为 S15 首试输入核验。MatchID 2D 窗口反复显示 `000000.jpg: Not a TIFF or MDI file`，当前 GUI 环境/工程未处于可用的 S15 Results Viewer 观察状态。未点击保存、导出或参数运行；当前截图作为候选值证据保留。
- GUI 环境复核（2026-09-25）：MatchID 可执行文件存在且窗口进程可枚举，但当前桌面状态捕获不可用，未取得新的可信画面或控件状态；没有点击保存、导出或运行识别。S15 的 ROI、参考帧、零力场和虚功门槛保持未通过。
- S15 原始实验目录文件清单审计（只读）：存在 `Job.m2inp`、`S15_XY_0.2.mti` 和 JPG/DAT，未发现 `.vfm` 文件。因此 S15 当前只是 DIC Job/同步力输入候选，尚未建立 MatchID VFM 工程；不能直接进入内外虚功检查。
- S19 `.vfm` 补充核验（只读）：原始目录实际存在 `X_0.2.vfm`，但用 `tools/vfm_boundary.py::parse_matchid_vfm_metadata` 解析时未发现 `Boundary` 和 `Forces` 记录。此前“未发现 `.vfm`”修正为“存在文件但不是完整边界输入”；S19 仍不能进入单轴 VFM 虚功或阶段 1 `E` 识别。
- 单轴几何检索封口（只读）：对 `PA12_biaxial_project` 内排除 `PAPER/CHECK` 图像目录后的 65 个文本型文件做定向检索，未发现 S19–S22 独立厚度、有效宽度、标距、VFM 积分域或外功边界；仅发现双轴十字模型厚度说明。不得从这些双轴说明反推单轴几何。
- S15 `.mti` 内容审计（只读）：参考图为 `000000.jpg`；有效 DIC 条目为 `000000–000284.jpg` 共 285 条（含参考帧），`000285.jpg=False`；标定 `0.087464 mm/pixel`；ROI 为起点 `(395,413)`、尺寸 `329×329 px`。这与当前 284 个非参考有效合并帧和视觉断裂帧排除相符，可作为建立 S15 VFM 工程时的 DIC 输入核对依据。
- S15 原始 `Press` 表包含四个独立通道 `X1_Press/X2_Press/Y1_Press/Y2_Press` 和 36,244 个采样点。按现有同步规则重采样到 284 个有效照片时刻后，四通道平均值与当前 X/Y 单列 CSV 的最大差分别为 `4.93×10⁻⁷ N`、`4.79×10⁻⁷ N`；末帧为 X1=`1601.36`、X2=`1615.00`、Y1=`1607.70`、Y2=`1598.96 N`。这证明四边力数据层可复用，但尚未写入 S15 `.vfm` 工程。
- S15 VFM 帧契约：每个 Boundary/Forces 序列应为 `285` 个值，顺序为 `000000` 参考帧零值、`000001–000284` 四通道同步力；`000285` 不进入 VFM。现有 X/Y CSV 的 284 行只覆盖非参考有效照片，不能直接作为完整 `.vfm` Forces 序列。
- S16 完整 `S16_XY_0.2_258.vfm` 的 Forces 数值审计与当前原始 Press 不一致：四个 Boundary 的 MAE 为约 `24.65–29.80 N`，末帧差为约 `1.43–1.49 kN`。因此它只保留为格式/方向证据，不能作为当前同步力序列或 S15 Forces 模板。
- 终点敏感性补充：将当前 Press 按 S16 峰值终点 `25.751 s` 映射时，旧 `.vfm` 各 Boundary 最大差约 `38–67 N`，比掉载终点映射显著接近但仍不完全一致；可能存在峰值截断或另一时间映射，未解除同步审计门槛。
- 共同仿射时间拟合补充：四个 Boundary 共用网格搜索起止时刻的最佳点约 `0.2044–25.7870 s`，MAE 仍为 `16.7–21.5 N`、最大偏差 `39–58 N`。因此差异不能仅由共同起止时间解释，旧文件还可能来自不同力源版本、通道映射或偏置；不将拟合当同步通过。
- 已生成 [S15 四边力蓝图 CSV](../MatchID_VFM准备/S15_XY_0.2/S15_XY_0.2_BoundaryForces_blueprint.csv)：285 行、Boundary0=X2、Boundary1=Y2、Boundary2=Y1、Boundary3=X1；经核验无 `000285`，非参考行平均值与现有 X/Y CSV 最大差约 `5.0×10⁻⁷ N`。该文件是人工建立 `.vfm` 的输入核对表，不是 `.vfm` 工程文件。

## 2. 唯一事实来源

| 内容 | 路径 |
| --- | --- |
| 当前 Second Brain Vault | `D:\2026.9.21_finally` |
| 原始资料根目录 | `D:\C盘迁移\Desktop\yuan` |
| 正式 JPG/DAT | `D:\C盘迁移\Desktop\yuan\data\XY\picture-20250529\vertical_all_45°\PAPER` |
| Press/Pos XLS | `D:\C盘迁移\Desktop\yuan\data\XY\data-20250529\20250529` |
| 批量配置 | `configs/pa12_rotated_batch.json` |
| 同步程序 | `tools/pa12_sync.py` |
| 批量入口 | `tools/run_pa12_batch.py` |
| MatchID 索引入口 | `tools/matchid_prepare.py` |
| 结果审计入口 | `tools/audit_pa12_outputs.py` |
| 机器清单 | `Agents/PA12实验数据处理/处理记录/PA12批量处理清单.json` |
| 审计 JSON | `Agents/PA12实验数据处理/处理记录/PA12数据合理性审计结果.json` |
| MatchID 实验索引 | `Agents/PA12实验数据处理/MatchID_VFM准备/PA12_MatchID_VFM实验级索引.csv` |
| DAT 逐帧质量审计 | `Agents/PA12实验数据处理/MatchID_VFM准备/PA12_DIC_DAT质量审计.md` |
| MatchID 闭环状态 | `Agents/PA12实验数据处理/MatchID_VFM准备/PA12_MatchID_VFM闭环状态.md` |
| 环境检查 | `Agents/PA12实验数据处理/MatchID_VFM准备/PA12_环境检查.md` |
| 导出字段模板 | `configs/matchid_export_example.json` |
| 原始方向证据 | `raw/assets/PA12原始方向与旋转标定方向.jpg` |
| VFM 边界配置 | `configs/pa12_vfm_boundary.json` |
| VFM 边界审计 | `Agents/PA12实验数据处理/MatchID_VFM准备/PA12_VFM边界载荷审计.json`、`PA12_VFM边界载荷说明.md` |

正式 DIC 只能使用旋转后的 `vertical_all_45°/PAPER`。不要切回 `CHECK` 或早期 `orginal_all`，也不要修改原始 JPG、DAT、XLS。

## 3. 已确认的处理规则

- `Press` 按力使用；用户已确认工程单位为 `N`，后续同步、VFM 力值和应力计算均按 N 处理。
- 默认等双轴：`X=(X1_Press+X2_Press)/2`，`Y=(Y1_Press+Y2_Press)/2`。单轴实验只保留主动方向，非加载方向按配置置零。
- 零点为加载前基线均值，输出公式是 `F_corrected=-(F_raw-F_baseline)`；第一行强制为零。
- X/Y 使用同一组有效照片时间点插值，不能按照片序号直接抽取力数据行。
- 照片主索引是同名 JPG+DAT 配对帧。缺 DAT 的 JPG 不删除、不补造。
- 正式同步力值门禁：照片数 = X 行数 = Y 行数、无 NaN、时间严格递增、第一行归零、主动方向第一行之后为正、终点已确定。
- 设备位移使用加载方向两侧位置增量绝对值之和。概览同时保留“速度×有效时间”的照片位移和 Pos 设备位移。
- 名义应力—应变审核固定使用中心有效宽度 30 mm、中心 ROI 厚度 1 mm、标距 30 mm，即名义截面积 30 mm²；整体厚度 3 mm 只作为几何记录，不用于该截面积。
- VFM 厚度规则固定为：中心 ROI 有效厚度 1 mm，试样整体大厚度 3 mm；整体厚度不能替代中心 ROI 厚度。若后续获得新的实测几何，只能新增版本并重新生成派生结果。
- 双轴 REV B 图纸证据：总尺寸 150.4×150.4 mm，臂宽/减薄区外边界约 30×30 mm，中心平坦测量区约 28×28 mm，中心厚度 1.00 mm；模型采用总厚 3.00 mm，但图纸将总厚标为比例/截面推定值；DAT/照片实测的是有效点外接范围约 27.64×28.08 mm。S15 `Job.m2inp` 的 Shape 为 329×329 px、标定 0.087464 mm/pixel，换算为 28.775656×28.775656 mm，与当前约 28.78×28.78 mm 的 MatchID ROI 一致；差异来自 Job ROI 矩形与 DAT 有效点外接框的不同口径，实际边界仍需人工核对。来源为 `PA12_biaxial_project/04_geometry/drawings/moxing/moxing.pdf`（MinerU `doc:7535ee9/tier:standard/page:1` 至 `page:4`）、`简易版.pdf`（MinerU `doc:953d05c/tier:standard/page:1`）和 S15 `Job.m2inp`。该证据只支持双轴十字试样，不解锁 S19 等单轴长条试样的 VFM 几何。
- S15 ROI 几何筛查：若 Job ROI 与试样名义中心同心，`28.775656 mm` 相对 `30 mm` 减薄区外边界每侧约余 `0.612172 mm`，相对 `28 mm` 平坦测量区每侧超出约 `0.387828 mm`。因没有真实厚度过渡边界和 ROI 中心偏移实测，当前状态为“同心条件下位于外边界内、平坦区潜在重叠，需人工核对”，不能写成 ROI 通过或越界。
- S15 Job 坐标补充：ROI 中心为 `(559.5,577.5) px`，初始子集为 `(531,591) px`，引伸计标记为 `(575,483)` 与 `(573,711) px`；这些是 DIC Job 控制点，不是已确认的 1 mm 厚度边界中心，不能用来直接判定 ROI 偏移。
- 当前默认等双轴同步力约定为 `X=(X1_Press+X2_Press)/2`、`Y=(Y1_Press+Y2_Press)/2`。用户已确认外围力传感器值可直接作为 ROI 边界合力；自建 VFM 主路径和历史 MatchID 审计均不据此另行构造四边牵引分布或均布应力。
- 原始机器方向固定为右上/左下=`Y1/Y2`、右下/左上=`X1/X2`；旋转后的 ROI 边界固定为顶部=`X2`、底部=`X1`、左侧=`Y2`、右侧=`Y1`。
- MatchID Boundary 顺序固定为 `0=顶部、1=左侧、2=右侧、3=底部`；双轴用 X 顶/底和 Y 左/右，单轴只用受力方向两边；拉伸力为正。
- 厚度分开记录：外围整体结构 `3 mm`，中心 ROI `1 mm`；MatchID VFM 的中心 ROI 使用 `1 mm`。
- 四组等双轴数据分别拟合：`S15_XY_0.2`、`S16_XY_0.2`、`S18_XY_2`、`S17_XY_20`；S15/S16 即使同速率也不合并。阶段 1 固定 `ν=0.375` 识别 `E`；阶段 2 固定该 `E` 和 `ν=0.375` 识别 `Y、H`。
- 论文第 3.3 节把“单轴拉伸和等双轴拉伸”写在同一双轴实验方案中，第 4.6 节把单轴与等双轴屈服点共同用于屈服面；但论文未给出 S19/S20/S21/S22 长条单轴试样的独立几何、积分域或外功边界。当前 S19–S22 的长条 Job/参考图证据不能与论文中的单轴路径静默合并（MinerU：`doc:b39265e/tier:standard/page:31`、`page:37`、`page:38`）。
- 论文速率标签为 `0.1/1.0/10 mm/s`，当前目录标签为 `0.2/2/20 mm/s`；当前配置已说明前者是单个执行通道速度、后者是两侧相对加载速度，S19 报告的照片/Pos 位移计算也支持该口径。当前处理保留真实配置标签，不重命名、不混合拟合；仍需核对论文“加载速率”的术语口径。论文第 3.1 节确认四个力传感器位于四个加载方向的夹具与驱动单元之间，但这不替代当前机器力—MatchID ROI 边界合力规则（MinerU：`doc:b39265e/tier:standard/page:28`）。

## 4. 当前十组实验状态

这里的 `VFM_READY` 只表示同步后的单列 X/Y 力值 CSV 通过数量和数值门禁，不表示 DIC 全场和 MatchID VFM 已完成。

| 实验 | 力值状态 | 有效帧数 | 起始—结束照片 | 力索引：起点/峰值/终点 | Job 覆盖 | MatchID 合并状态 |
| --- | --- | ---: | --- | --- | --- | --- |
| S15_XY_0.2 | VFM_READY | 284 | 000001—000284 | 105 / 28387 / 28463 | Job 不覆盖 000285；其 DAT 虽存在但场不完整并排除 | `MATCHID_VFM_INPUT_READY`：284 帧由 DAT 重构，排除 568 个 `valid=False` 点；000285 为视觉断裂帧，不进入合并 |
| S16_XY_0.2 | VFM_READY | 257 | 000001—000257 | 102 / 25690 / 25773 | 完整 | `MATCHID_VFM_INPUT_READY` |
| S17_XY_20 | VFM_READY | 12 | 000003—000014 | 50 / 209 / 273 | 完整 | `MATCHID_VFM_INPUT_READY` |
| S18_XY_2 | VFM_READY | 126 | 000003—000128 | 50 / 2473 / 2550 | 完整 | `MATCHID_VFM_INPUT_READY`：126 帧由 DAT 重构，排除 252 个 `valid=False` 点 |
| S19_X_0.2 | VFM_READY | 126 | 000002—000127 | 169 / 12749 / 12827 | 完整 | `MATCHID_VFM_INPUT_READY` |
| S20_X_2 | VFM_READY | 63 | 000005—000067 | 105 / 1266 / 1341 | 完整 | `MATCHID_VFM_INPUT_READY`：63 帧由 DAT 重构，排除 126 个 `valid=False` 点 |
| S21_X_20 | VFM_READY | 36 | 000010—000045 | 50 / 167 / 227 | 完整 | `MATCHID_VFM_INPUT_READY`：36 帧由 DAT 重构，排除 72 个 `valid=False` 点 |
| S22_Y_0.2 | VFM_READY | 223 | 000008—001784 | 159 / 109550 / 178732 | 已排除 8 个无 `<53>` DAT 帧；223 帧均有可用 DIC 字段 | `MATCHID_VFM_INPUT_READY` |
| S23_Y_2 | DATA_LIMITED | 191 | 000008—001528 | 51 / 9053 / 15327 | 完整；终点不是掉载 | `FORCE_REVIEW_REQUIRED` |
| S24_Y_20 | PRELOAD_RELEASE_ONLY | UNKNOWN | UNKNOWN | UNKNOWN | 已确定为约 1555 N 预载释放记录，不代表完整拉伸加载 | `PRELOAD_RELEASE_ONLY` |

### 已生成的用户结果

- 8 组 `VFM_READY` 的 X/Y 单列、无表头、UTF-8 力值 CSV；每组均通过照片数=X 行数=Y 行数门禁。
- 9 组已进入处理的照片—力表、检查图和名义应力—应变结果；S24 按预载释放记录排除。
- 10 组 MatchID Job/DAT 元数据登记；S22 已完成 223 帧 DIC—力合并，S23 有帧—力—时间索引，S24 仅保留状态记录。
- 已审计 1319 个当前选定照片对应 DAT，全部为 `DIC_FIELDS_AVAILABLE`；S15 的 `000285.jpg.dat` 有 `<18>/<53>` 记录，虽然当前 Job 未列出该帧。
- 已确认 MatchID 2D 19.2.2.0 Results Viewer 导出表头、分号分隔符、mm 坐标/位移和无量纲 `Exx/Eyy/Exy`；配置在 `configs/matchid_export_example.json`。
- 已完成 DIC 全场—同步力合并：S15 284 帧、S16 257 帧、S17 12 帧、S18 126 帧、S19 126 帧、S20 63 帧、S21 36 帧；每帧保留照片时间、X/Y 力、x/y、u/v、Exx/Eyy/Exy。S15 的 000285.jpg 保留为视觉断裂证据，但其 DAT 场不完整，不进入正式合并。
- S15/S18/S20/S21 的导出存在缺失、非有限值或与 DAT 点数不一致；程序按已验证的 DAT 映射重构，状态和帧索引均标记 `DAT_RECONSTRUCTED`，只排除 DAT 明确标记 `valid=False` 的点，不填零、不插值、不静默删点。
- DAT `<18>/<53>` 字段映射已由 MatchID 2D 19.2.2.0 Results Viewer 与同帧数据交叉验证；该证据是本地版本验证，不是官方 DAT 格式文档。
- 汇总概览 CSV/XLSX 按配置顺序包含 10 行；S24 行的未知结果写为 `UNKNOWN`。
- 批量输出由持久化审计工具检查，审计结果在 `处理记录/PA12数据合理性审计结果.json`。

## 5. 输出位置

- 实验概览：`Agents/PA12实验数据处理/实验概览/`
- 照片—力表：`Agents/PA12实验数据处理/照片力匹配/`
- X/Y 力值：`Agents/PA12实验数据处理/VFM专用力值/X方向/` 和 `Y方向/`
- 检查图：`Agents/PA12实验数据处理/检查图/`
- 名义应力—应变：`Agents/PA12实验数据处理/应力应变/`
- 批量报告和审计：`Agents/PA12实验数据处理/处理记录/`
- MatchID 准备包：`Agents/PA12实验数据处理/MatchID_VFM准备/`
- DAT 审计明细：`Agents/PA12实验数据处理/MatchID_VFM准备/<实验编号>_DAT逐帧质量审计.csv`
- MatchID 已合并帧：`Agents/PA12实验数据处理/MatchID_VFM准备/{S16_XY_0.2,S17_XY_20,S19_X_0.2}/merged/`
- MatchID 合并状态：`Agents/PA12实验数据处理/MatchID_VFM准备/<实验编号>/<实验编号>_DIC全场—力状态.json`
- MatchID 合并入口：`tools/merge_matchid_exports.py`

## 6. 尚未完成的短板

1. S23 没有记录到峰值后的明显持续掉载，分析终点索引为 `15327`，但不能称为断裂点或发布正式 VFM。
2. S24 文件开头已有约 1555 N Y 向预载，已确定为预载释放记录；没有加载前零点，因此不作为完整拉伸实验处理。
3. S16 `3try` 力序列不同步（X/Y MAE=`26.1206/23.4119 N`，末帧绝对差=`1452.79/1478.85 N`），不可用于识别；`4try_step3` Forces count=`0`，输入不完整。
4. S16 第 16 轮界面显示候选为 `Y=63.93 MPa`、`H=41.55 MPa`、残差栏 `1214`（定义/单位 UNKNOWN）；`E`、`ν` 未显示。它们是 GUI 中间候选，不是最终识别值，不得迁移到其他实验或写成材料结论。
5. 当前双轴 VFM 工作几何固定为中心 ROI 厚度 1 mm、外围整体厚度 3 mm、有效宽度 30 mm、标距 30 mm；REV B 图纸另给出中心平坦区约 28×28 mm、DAT/照片 ROI 约 27.64×28.08 mm。单轴长条的厚度、有效宽度、标距和外功边界仍须独立证据。按已确认的机器通道—DIC 方向映射，将机器力直接用于自建 VFM 主路径；MatchID 只作历史审计，不恢复牵引分布。
6. 论文中的 `E=1800 MPa`、`ν=0.375`、初始屈服强度 `21 MPa`、硬化模量 `180 MPa` 是试样优化阶段的 Abaqus 工作参数，不是本实验已经识别出的材料参数。式 (2.19) 的负斜率与正 H 需向原始 Abaqus 塑性卡/作者核实，不能用于推断 MatchID 的 H 约定。
7. 完整 `S16_XY_0.2_258.vfm` 是既有 `.vfm` 格式证据；它不能证明后续 GUI 的 `3try` 力序列同步，也不能弥补 `4try_step3` 缺少 Forces。
8. 当前环境没有保存任务开始前的原始文件时间戳基线；不能仅凭现有时间戳反推更早历史是否有外部改写。
9. 论文将单轴与等双轴写入同一双轴实验方案，但没有给出 S19/S20/S21/S22 长条单轴的独立几何和外功边界；当前配置已解释 `0.1/1/10`（单个执行通道）与 `0.2/2/20`（两侧相对速度）的本地标签差异，但论文术语口径和单轴路径对应的具体试样/文件仍须确认，不能直接启动 S19 阶段 1。
10. S15 Job ROI 相对名义 30 mm 减薄区外边界每侧余 0.612172 mm，但相对名义 28 mm 平坦测量区每侧超出 0.387828 mm；当前标为潜在过渡区重叠，须人工确认真实厚度边界和 ROI 中心偏移后，才能进入虚功检查。
11. 名义 `05_a1p1.00mm.step` 使用 mm；所有几何控制点的坐标包络为 `x/y=±75.2 mm、z=±5 mm`，但实体拓扑顶点包络为 `150.4×150.4×3.0 mm`、`z=-1.5…1.5 mm`。当前 STEP 是单一实体，中心顶点位于 `z=±0.5 mm`、`x/y=±14.005 mm`，对应约 `28.01×28.01 mm`、`1.0 mm` 中心平面；全局控制点范围不能当作实体厚度，实物厚度仍须独立核验。
12. 两份 `verification.json` 都记录名义中心 `1.0 mm`、总厚 `3.0 mm`、过渡半径约 `0.995 mm`；虽然引用的长文件名 STEP 及同族模型在原始资料根目录均不存在，当前短文件名 STEP 的实体拓扑已独立复核相同名义包络、中心平面和 `0.995 mm` 圆柱面记录。文件名映射仍是血缘待补证项，但名义 CAD 几何不再是阻塞，不等于实物厚度或 S15 ROI 已通过。

## 7. 下一次 GPT 的执行顺序

0. 保留 STEP、`verification.json` 与实际厚度口径的证据分界；当前短 STEP 已独立复核名义几何，长文件名映射只作为血缘补证项。下一步取得实际截面/厚度或 MatchID 几何证据，在此之前不把 CAD 名义值写成实物测量，也不解除 S15 ROI containment 门槛。

**本构定义核验项**：项目优化论文第 2.3.2 节式 (2.19) 原页写为 `σ_y=σ_y0−H ε̄p`，第 2.3.2 节材料参数页给 `H=+180 MPa`、`σ_y0=21 MPa`。按该式正 H 表示屈服应力随等效塑性应变下降，线性外推约在 `ε̄p=0.1167` 时降至零；因此原文“线性硬化”与方程/参数符号存在软化—硬化冲突。Abaqus 官方允许等向塑性表中的屈服应力随塑性应变增加或降低；现存几何扫描 `.inp` 仅有 provisional Elastic 卡，没有 `*Plastic` 表可核实论文实际求解输入。识别/解释 MatchID 的 `Y、H` 前，先核实 MatchID 模型定义及原始 Abaqus 材料卡；不得直接将论文符号约定套到 MatchID。

1. 读取本文件、机器可读状态、总体方法协议和阶段 A–F 报告；将 `STAGE_F_COMPLETE_REVIEW_REQUIRED` 视为当前状态。
2. 自建 VFM 是唯一当前计算主线；MatchID `.vfm`、Boundary/Forces 和 GUI 参数仅作格式、方向和历史审计，不作为计算依赖。
3. 保持原始 JPG、DAT、XLS 只读。双轴重算使用已确认的旋转后 DIC 映射（机器 X=`Eyy`、机器 Y=`Exx`）和 DIC 全场—Press 合并数据；单轴方向映射须逐试样核实后方可用于正式识别。边界力按用户确认的机器合力规则输入。
4. 四组等双轴主结果均低于面积比 `0.95` 门槛；完整 Job ROI 是主口径，DIC subset 内缩域只作独立敏感性分析。不要自动用内缩域解锁正式参数。
5. 阶段 1 的 E 是固定工作假设 `ν=0.375` 的条件结果。阶段 F 全区间剖面显示 ν 不稳定或最优点在边界；先补独立 ν 约束和真实 ROI/中心 1 mm 区域边界，再重新识别 E 并评估 J2。
6. S19–S22 只允许真实 Job Polygon 诊断，必须维持 `REVIEW_REQUIRED`；除单轴实际厚度、有效宽度、标距、积分域含义和外功边界外，还须逐试样核实机器 X/Y 与 DIC `Exx/Eyy` 的映射。当前代码沿用双轴旋转映射，不能视为单轴方向已确认。
7. S23 视觉断裂帧缺力，禁止补造；S24 为预载释放，不进入完整拉伸 VFM。Linear H 符号冲突须在解释 Y/H 前核实。

## 9. 自建 VFM 主路径；MatchID 历史审计

当前主流程使用 `VFM自建/`。对已确认的双轴十字试样，旋转方向映射为机器 X→DIC `Eyy`、机器 Y→DIC `Exx`；中心 ROI 使用厚度 1 mm，外围整体 3 mm 单独记录，外围机器力按用户确认作为 ROI 边界合力。该映射尚未由 S19–S22 单轴装夹独立确认，当前单轴输出仅为方向条件诊断。MatchID 文件、`.vfm` 格式、Boundary/Forces 映射和 GUI 试算保留为历史审计证据，不作为自建计算依赖。即使 MatchID VFM 不可用，也继续由自建流程导出内外虚功和参数候选。

- 阶段 1：当前固定工作假设 `ν=0.375`，由加载初期内外虚功计算条件 E；阶段 F E–ν 剖面表明 ν 尚未被独立识别。
- 阶段 2：固定条件 E 和 ν，使用平面应力/等效塑性应变约化得到 Y/H 候选；不是 MatchID 内部 J2 求解的复刻。
- 模型比较：Linear、通用 Ludwik、通用 Swift、通用 Voce I、通用 Voce II；通用公式不等同于 MatchID 界面同名模型。
- 当前阶段 A–F：双轴完整 Job ROI 主结果、DIC subset 内缩域独立敏感性、固定窗口/严格留出、单轴 Polygon 诊断、S19 准入与 E–ν 剖面均已记录；四组等双轴和四组单轴仍为 `REVIEW_REQUIRED`。阶段 F 未识别出稳定 ν；S17 阶段 2 点数不足，S22 在当前条件映射下阶段 1 为非正模量，S23 断裂处无力，S24 为预载释放。
- 当前下一道门槛：获取真实双轴 ROI 与中心 1 mm 厚度边界证据及 ν 的独立约束；单轴正式识别前逐试样确认机器轴—DIC 轴映射，再补齐单轴几何/外功证据。完成后才重跑正式参数候选与跨试验验证。

复现入口：`tools/run_pa12_self_vfm.py`；配置：`configs/pa12_self_vfm.json`；E–ν 审计：`tools/audit_pa12_self_vfm_nu_profile.py`；结果总表：`Agents/PA12实验数据处理/VFM自建/汇总/PA12自建VFM结果.csv`。四组仍是复核结果；不能绕过数据、几何、面积、ν 可辨识性和稳定性门槛直接写成正式材料参数。

## 8. 可复现命令

```powershell
python -m unittest discover -s tests -v
python tools/run_pa12_batch.py --config configs/pa12_rotated_batch.json
python tools/matchid_prepare.py --config configs/pa12_rotated_batch.json
python tools/check_pa12_environment.py --config configs/pa12_rotated_batch.json --output-root D:\2026.9.21_finally
python tools/audit_matchid_dic.py --config configs/pa12_rotated_batch.json
python tools/audit_pa12_outputs.py --config configs/pa12_rotated_batch.json
python tools/audit_pa12_vfm_boundary.py --config configs/pa12_vfm_boundary.json
python -m compileall -q tools tests
```

检查器只读构建当前使用批次配置作为入口；writer 会覆盖两份检查结果。此前用户要求检查产物由其并行生成，因此在获得新的明确授权前不要运行 `write_current_check()` 或 CLI writer。
