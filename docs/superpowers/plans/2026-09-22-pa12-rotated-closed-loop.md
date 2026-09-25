# PA12 旋转照片闭环处理实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在不修改原始 JPG、DAT、XLS 的前提下，以 `vertical_all_45°/PAPER` 旋转序列为唯一最终图像来源，确定力文件映射，生成正拉伸力照片同步表、X/Y VFM CSV、概览、检查图和 GPT/MatchID 交接文档。

**Architecture:** 保留现有 `tools/pa12_sync.py` 的力事件检测、零点校正和插值逻辑；将旋转序列和状态导出映射写入版本化 JSON 配置。帧选择以旋转目录中同时存在 JPG 与 DAT 的帧为主索引，使用原始帧号建立照片时间轴，不使用 `CHECK` 图片，不把缺 DAT 的旋转 JPG 静默当作 DIC/VFM 帧。批量报告区分正式 VFM、诊断结果和未完成映射。

**Tech Stack:** Python 3.12、pandas、numpy、matplotlib、Pillow、openpyxl、MatchID 2D 19.2.2.0。

---

### Task 1: 固化旋转目录与力文件映射

**Files:**
- Create: `configs/pa12_rotated_batch.json`
- Create: `Agents/PA12实验数据处理/处理记录/旋转序列—力文件映射.csv`
- Test: `tests/test_pa12_sync.py`

- [ ] **Step 1: 读取 `vertical_all_45°/PAPER` 的十个序列，记录 JPG/DAT 数量、帧号范围、`Job.m2inp` 标尺和对应原始序列帧数。**
- [ ] **Step 2: 用序列标签、原始帧数、原始目录时间和状态导出时间确定映射；双候选 `xy-04-1` 按图像目录采集时间与状态导出结束时间一致性选择一个文件，并把选择依据写入映射表。**
- [ ] **Step 3: 在配置中显式写出十个 `experiment_id`、旋转 `image_folder`、力文件、速度口径、通道、正力符号和发布许可；禁止批处理通过文件名重新猜测映射。**
- [ ] **Step 4: 测试映射配置中每个实验路径存在，且每个正式入口目录为 `vertical_all_45°/PAPER` 子目录而非 `CHECK`。**

### Task 2: 让帧选择尊重旋转目录的实际 JPG/DAT 配对

**Files:**
- Modify: `tools/pa12_sync.py`
- Test: `tests/test_pa12_sync.py`

- [ ] **Step 1: 先写失败测试：给出稀疏配对帧 `[0, 8, 16]`，要求选择结果只包含这些帧且时间单调；给出缺 DAT 的末帧，要求正式 VFM 被阻断。**
- [ ] **Step 2: 修改有效区间选择：在力加载起点和断裂点对应的相机帧窗口内，从已配对帧集合中过滤，不再构造不存在的连续帧号。**
- [ ] **Step 3: 使用配对帧原始编号建立照片时间轴；连续帧用设置频率，稀疏帧保留帧号间隔，照片时间仍只作为 X/Y 同步插值的共同轴。**
- [ ] **Step 4: 将报告中的图像来源、DAT 配对数、缺 DAT 数和帧号间隔写清楚；不通过删除或补造 DAT 凑数量。**

### Task 3: 重新生成旋转照片结果

**Files:**
- Modify: `tools/run_pa12_batch.py`
- Create/overwrite only generated outputs under: `Agents/PA12实验数据处理/`

- [ ] **Step 1: 使用 `configs/pa12_rotated_batch.json` 执行批量处理。**
- [ ] **Step 2: 对每个实验生成精简照片—力表、单列无表头 X/Y VFM CSV、中文概览和检查图。**
- [ ] **Step 3: 正式 VFM 门禁必须同时通过：旋转 JPG/DAT 配对、照片/X/Y 行数相等、无 NaN、时间严格递增、首行归零、全部力值 `>0`（允许仅首行 0）、有效区间无缺号、事件终点已确定。**
- [ ] **Step 4: 对不能满足条件的实验只生成诊断与具体缺口，不生成正式 VFM CSV。**

### Task 4: GPT/MatchID 交接文档

**Files:**
- Create: `Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md`
- Modify: `wiki/PA12照片力同步与VFM生成.md`
- Modify: `wiki/PA12双轴拉伸项目_第一阶段盘点.md`
- Modify: `index.md`
- Modify: `log.md`

- [ ] **Step 1: 写明用户意图：后续把旋转照片/DAT、同步 X/Y 力、几何和标定接入 MatchID VFM，并继续补齐单位、边界力和材料参数短板。**
- [ ] **Step 2: 分别列出正式完成、仅诊断和未完成实验，写出每个结果路径与阻塞原因。**
- [ ] **Step 3: 写明 `Press`、等双轴通道平均、正力公式、速度口径、旋转目录约束、标定值和 DAT 格式。**
- [ ] **Step 4: 写出下一次 GPT 的可执行顺序：先审检查图，再确认单位/标定/边界力，最后进入 MatchID VFM，不重新选择原始图像。**

### Task 5: 验证与交付

**Files:**
- No raw-file edits.

- [ ] **Step 1: 运行 `python -m unittest discover -s tests -v`。**
- [ ] **Step 2: 运行旋转批处理并检查清单状态、正式 CSV 行数、正力条件和路径前缀。**
- [ ] **Step 3: 读取汇总 CSV/XLSX，检查中文列、行数、无空值和照片数量与 X/Y 数量。**
- [ ] **Step 4: 用 Pillow 打开全部检查图，并抽查正式实验图中的加载起点、峰值、掉载点、照片采样点和最终区间。**
- [ ] **Step 5: 比较原始 JPG/DAT/XLS 的大小和修改时间，确认本次没有修改原始文件。**
