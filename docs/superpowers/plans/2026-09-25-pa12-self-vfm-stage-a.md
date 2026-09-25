# PA12 自建 VFM 阶段 A Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在现有 PA12 自建 VFM 中加入可审计的 ROI 逐点三角形积分，并用同一输入同时输出逐点积分与现有均值基线结果。

**Architecture:** 保留 `tools/pa12_self_vfm.py` 的材料拟合函数和现有批处理入口，在其中增加纯计算的点场积分函数；`tools/run_pa12_self_vfm.py` 读取合并 CSV 的逐点场，先做参考帧场对齐，再把积分系数送入现有阶段 1/2 拟合。输出同时记录积分方法、有效点/三角形、积分面积和与矩形面积的差异，均值法只作为回归基线，不替换正式结果。

**Tech Stack:** Python 3、NumPy、Matplotlib `tri.Triangulation`、现有 unittest/pytest、JSON/CSV/Markdown。

---

## 文件边界

- Modify: `tools/pa12_self_vfm.py` — 增加逐点平面应力虚功系数计算，不改现有拟合公式。
- Modify: `tools/run_pa12_self_vfm.py` — 读取逐点 CSV、对齐参考场、选择 ROI 三角形、写入逐点积分诊断和阶段结果。
- Modify: `configs/pa12_self_vfm.json` — 将正式积分规则写成配置，同时保留均值基线开关。
- Modify: `tests/test_pa12_self_vfm.py` — 添加解析几何、积分面积、基线对齐和面积差异门槛测试。
- Modify: `Agents/PA12实验数据处理/VFM自建/README.md` — 记录阶段 A 的正式计算规则和输出字段。
- Create: `Agents/PA12实验数据处理/VFM自建/汇总/PA12自建VFM阶段A记录.md` — 只记录运行证据、结论、限制和下一步，不写最终材料参数。
- Modify: `index.md` — 收录阶段 A 记录和正式自建 VFM 入口。
- Modify: `log.md` — 追加一次阶段 A 实验/重算日志。

不修改：`raw/`、MatchID 历史审计文件、并行维护的 `tools/pa12_vfm_check.py`、`tests/test_pa12_vfm_check.py`、`configs/pa12_vfm_boundary.json`。

### Task 1: 定义逐点积分接口并写失败测试

**Files:**
- Modify: `tests/test_pa12_self_vfm.py`
- Modify: `tools/pa12_self_vfm.py`

- [ ] **Step 1: 写三角形积分的失败测试**

在 `tests/test_pa12_self_vfm.py` 增加测试数据：矩形 `(0,0)、(2,0)、(2,1)、(0,1)`，用两个三角形覆盖，令 `exx=0.01、eyy=0.02` 为常数，`nu=0.25、t=1、Lx=2、Ly=1`。测试新函数返回积分面积 `2.0 mm²`，并满足：

```python
expected_x = 1.0 / (1.0 - 0.25**2) * (0.01 + 0.25 * 0.02)
expected_y = 2.0 / (1.0 - 0.25**2) * (0.02 + 0.25 * 0.01)
```

系数允许 `1e-12` 数值误差，且有效三角形数为 2。

- [ ] **Step 2: 写 ROI 外点不参与积分的失败测试**

增加一个包含矩形外点的点场，传入 `roi_bounds=(0.0, 2.0, 0.0, 1.0)`；测试输出的积分面积仍为 `2.0`，外点不影响系数，且诊断中记录被排除点数。

- [ ] **Step 3: 运行测试确认接口尚不存在**

运行：`python -m pytest tests/test_pa12_self_vfm.py -q`

预期：新增测试因导入的积分函数尚不存在而失败；若旧测试也失败，先记录失败名称，不修改无关代码。

### Task 2: 实现逐点平面应力虚功积分

**Files:**
- Modify: `tools/pa12_self_vfm.py`
- Test: `tests/test_pa12_self_vfm.py`

- [ ] **Step 1: 定义最小函数接口**

增加：

```python
def integrate_plane_stress_virtual_work_coefficients(
    *,
    points: Sequence[dict[str, float]],
    nu: float,
    thickness_mm: float,
    length_x_mm: float,
    length_y_mm: float,
    roi_bounds: tuple[float, float, float, float],
) -> dict[str, float | int]:
    """Integrate unit-modulus X/Y virtual-work coefficients over valid ROI triangles."""
```

点记录只使用 `x、y、exx、eyy`。先筛选四边界内且字段有限的点；用 `matplotlib.tri.Triangulation` 对剩余点三角剖分；屏蔽三角形重心落在 ROI 外的三角形；每个三角形用面积乘三个顶点场值的平均值积分。对每个有效三角形分别积分 `exx + nu*eyy` 和 `eyy + nu*exx`，再乘 `t/(1-nu²)` 与对应虚场长度倒数。

返回至少包含：`coefficient_x`、`coefficient_y`、`integrated_area_mm2`、`valid_point_count`、`excluded_point_count`、`valid_triangle_count`、`rectangle_area_mm2`、`area_ratio`。不在函数内吞掉非法输入；沿用现有正值和泊松比约束。

- [ ] **Step 2: 运行新增单元测试**

运行：`python -m pytest tests/test_pa12_self_vfm.py -q`

预期：逐点积分测试通过，旧有拟合测试保持通过。

- [ ] **Step 3: 提交核心计算变更**

```bash
git add tools/pa12_self_vfm.py tests/test_pa12_self_vfm.py
git commit -m "feat: add pointwise PA12 VFM integration"
```

### Task 3: 接入逐点场读取和参考帧对齐

**Files:**
- Modify: `tools/run_pa12_self_vfm.py`
- Modify: `tests/test_pa12_self_vfm.py`

- [ ] **Step 1: 写参考场对齐测试**

增加小型基线与当前帧：两者点顺序相同、坐标相同；断言逐点应变等于当前值减基线值。再增加坐标不一致测试，断言函数明确抛出 `ValueError`，因为坐标错配会改变虚功而不能静默按行相减。

- [ ] **Step 2: 实现逐点 CSV 读取和对齐**

在 `tools/run_pa12_self_vfm.py` 增加内部读取函数，读取 `x、y、exx、eyy、exy` 和 `point_count`；把第一张有效照片作为参考场；后续帧按 CSV 行对应并比较 `x、y`，生成扣除参考场后的点记录。保留现有均值读取函数用于基线结果和兼容已有报告。

- [ ] **Step 3: 运行读取/对齐测试**

运行：`python -m pytest tests/test_pa12_self_vfm.py -q`

预期：对齐测试通过，且现有纯函数测试不受影响。

### Task 4: 把逐点积分接入实验计算并保留基线对照

**Files:**
- Modify: `tools/run_pa12_self_vfm.py`
- Modify: `configs/pa12_self_vfm.json`
- Modify: `tests/test_pa12_self_vfm.py`

- [ ] **Step 1: 写结果字段测试**

对一个合成矩形实验记录调用现有 `process_experiment` 所使用的帧计算路径，断言每帧同时有：

```text
integration_method = pointwise_triangle
pointwise_coefficient_x/y
baseline_coefficient_x/y
integrated_area_mm2
area_ratio
valid_triangle_count
```

并断言阶段 1 使用逐点系数，基线只用于报告比较。

- [ ] **Step 2: 增加配置项**

在 `configs/pa12_self_vfm.json` 的 `virtual_fields` 下增加：

```json
"integration_method": "pointwise_triangle",
"baseline_method": "mean_strain_rectangle",
"minimum_area_ratio": 0.95
```

`minimum_area_ratio` 只用于报告门槛：低于该值时状态为 `REVIEW_REQUIRED`，不得静默用矩形面积补足积分面积。

- [ ] **Step 3: 替换阶段 1/2 的正式系数来源**

在 `process_experiment` 中对每个帧读取逐点场，使用 `integrate_plane_stress_virtual_work_coefficients` 生成正式 `coefficient_x/y`；现有 `plane_stress_virtual_work_coefficients` 只生成 `baseline_coefficient_x/y`。阶段 1 的 `fit_elastic_modulus` 只接收正式逐点系数。阶段 2 的边界应力计算仍使用已确认的机器力、中心厚度和边界长度，不改变材料模型公式。

- [ ] **Step 4: 扩展逐帧 CSV 和 JSON 输出**

在现有内外虚功 CSV 增加逐点积分方法、积分面积、面积比、有效点数、有效三角形数、逐点系数、均值基线系数和系数相对差异；在实验 JSON 的几何/质量段记录同样的门槛状态。Markdown 汇总只写结论和限制，不堆中间点数据。

- [ ] **Step 5: 运行单个实验闭环**

运行：`python tools/run_pa12_self_vfm.py --batch-config configs/pa12_rotated_batch.json --self-config configs/pa12_self_vfm.json`

预期：现有双轴实验仍生成结果；每个实验的结果 JSON 明确记录 `pointwise_triangle`，面积不足的实验被标为复核而不是被补足。若当前入口参数不同，以 `python tools/run_pa12_self_vfm.py --help` 的实际参数为准并在日志记录命令。

### Task 5: 更新自建 VFM 文档与 Obsidian 证据

**Files:**
- Modify: `Agents/PA12实验数据处理/VFM自建/README.md`
- Create: `Agents/PA12实验数据处理/VFM自建/汇总/PA12自建VFM阶段A记录.md`
- Modify: `index.md`
- Modify: `log.md`

- [ ] **Step 1: 更新 README 的正式规则**

明确：正式结果使用 ROI 内逐点三角形积分；矩形均值法只作为回归基线；中心厚度为 1 mm；外部机器力直接作为边界合力；不重建牵引分布；面积比低于配置门槛时人工复核。

- [ ] **Step 2: 写阶段 A 记录**

记录实际运行日期、代码提交、输入实验数量、每个实验的有效帧/点/三角形、面积比范围、逐点与基线差异、阶段 1/2 状态、不能得出的结论和下一步。候选参数必须标记为候选，不写成最终材料参数。

- [ ] **Step 3: 更新索引和追加日志**

在 `index.md` 增加阶段 A 记录和自建 VFM 正式入口；在 `log.md` 追加 `experiment` 或 `refactor` 条目，链接到代码、配置和阶段记录。

- [ ] **Step 4: 运行文档路径检查**

运行：`git diff --check`

预期：无空白错误；所有新增页面均可从 `index.md` 链接到达。

### Task 6: 阶段 A 验证与交付

**Files:**
- Test: `tests/test_pa12_self_vfm.py`
- Test: 全量现有测试

- [ ] **Step 1: 验证失败类型和下一步**

运行前记录：本次检查用于发现逐点积分是否破坏现有拟合、输出字段是否缺失、以及文档链接是否不可达；若失败，先修正对应阶段 A 文件，不进入单轴识别。

- [ ] **Step 2: 运行目标测试和全量测试**

```bash
python -m pytest tests/test_pa12_self_vfm.py -q
python -m pytest -q
python -m compileall -q tools tests
git diff --check
```

预期：目标测试和全量测试通过，编译无错误，差异检查无输出。

- [ ] **Step 3: 检查结果审计字段**

读取一个双轴结果 JSON 和对应 CSV，确认正式方法为 `pointwise_triangle`、基线方法单独记录、厚度为 `1.0`、机器 X/Y 映射可见、面积比和门槛状态可追溯。若任一字段缺失，修复输出后重新运行该实验和目标测试。

- [ ] **Step 4: 提交阶段 A 变更**

```bash
git add tools/pa12_self_vfm.py tools/run_pa12_self_vfm.py configs/pa12_self_vfm.json tests/test_pa12_self_vfm.py Agents/PA12实验数据处理/VFM自建/README.md Agents/PA12实验数据处理/VFM自建/汇总/PA12自建VFM阶段A记录.md index.md log.md
git commit -m "feat: stabilize pointwise PA12 self VFM workflow"
```

提交前只纳入本计划列出的文件，不纳入 MatchID 检查/配置文件和其他并行变更。

## 计划自审

- 设计要求覆盖：自建 VFM 正式路径、逐点积分、基线回归、厚度/力规则、门槛、诊断输出、Obsidian 留证和不补造数据。
- 未覆盖内容：单轴几何补证、双轴跨速度参数验证、FEM 代理模型；这些是后续独立阶段，不属于本阶段 A 的成功标准。
- 无函数占位符：新增函数签名、输入字段、输出字段和计算规则已在 Task 2/3/4 中定义。
- 测试闭环：先写三角积分/对齐/输出字段测试，再实现，再运行目标测试、全量测试、编译和差异检查。
