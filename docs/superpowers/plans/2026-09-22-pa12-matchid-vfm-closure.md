# PA12 MatchID VFM 闭环实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在保留现有同步力值结果的前提下，完成 DAT 全场质量审计、MatchID 标准 CSV 合并入口、环境报告和 GPT 可继续执行的 VFM 交接。

**Architecture:** 新增一个小型 `matchid_dic.py` 负责流式 DAT 审计和声明式导出表解析；`matchid_prepare.py` 复用它写入逐帧质量；`merge_matchid_exports.py` 只处理已明确列名/单位的 Results Viewer CSV。环境检查与最终状态文档只读取配置和生成结果，不改原始资料。

**Tech Stack:** Python 3.12、csv、gzip、zlib、pandas、现有 PA12 配置与 Obsidian Vault。

---

### Task 1: DAT 质量审计

**Files:**
- Create: `tools/matchid_dic.py`
- Modify: `tools/matchid_prepare.py`
- Create: `tools/audit_matchid_dic.py`
- Test: `tests/test_matchid_dic.py`

- [x] **Step 1: 写失败测试**：验证流式审计能区分 `<53>` 为 0 的 DAT、含有 `<53>` 的 DAT，以及字段映射缺失时拒绝解析。
- [x] **Step 2: 运行单测确认失败原因是缺少新接口，而不是测试输入错误。**
- [x] **Step 3: 实现最小流式 DAT 审计和声明式 CSV 字段解析。**
- [x] **Step 4: 让 `matchid_prepare.py` 写入逐帧 DAT 质量和汇总审计文件。**
- [x] **Step 5: 运行单测确认新行为通过。**

### Task 2: MatchID 导出合并

**Files:**
- Create: `tools/merge_matchid_exports.py`
- Modify: `configs/pa12_rotated_batch.json`
- Test: `tests/test_matchid_dic.py`

- [x] **Step 1: 写失败测试**：给定一帧标准导出 CSV 和帧—力索引，要求输出 DIC 点表附带同一帧时间和 X/Y 力；缺列、NaN 或单位未声明时失败。
- [x] **Step 2: 运行测试确认失败。**
- [x] **Step 3: 实现逐帧合并、点数记录和索引输出；不改源导出 CSV。**
- [x] **Step 4: 添加示例配置段，明确列名、单位和导出根目录的约定。**
- [x] **Step 5: 运行测试确认通过。**

### Task 3: 环境与状态交接

**Files:**
- Create: `tools/check_pa12_environment.py`
- Modify: `Agents/PA12实验数据处理/处理记录/PA12_GPT交接文档.md`
- Modify: `Agents/PA12实验数据处理/MatchID_VFM准备/PA12_MatchID_VFM准备说明.md`
- Create: `Agents/PA12实验数据处理/MatchID_VFM准备/PA12_环境检查.md`
- Create: `Agents/PA12实验数据处理/MatchID_VFM准备/PA12_环境检查.json`
- Create: `Agents/PA12实验数据处理/MatchID_VFM准备/PA12_MatchID_VFM闭环状态.md`
- Create: `Agents/PA12实验数据处理/MatchID_VFM准备/PA12_MatchID_VFM闭环状态.json`

- [x] **Step 1: 写失败测试**：环境报告必须把 MatchID 不可调用与 Python 依赖可用分开，不把缺失专有软件写成 Python 依赖失败。
- [x] **Step 2: 运行测试确认失败。**
- [x] **Step 3: 实现环境检查并生成中文报告。**
- [x] **Step 4: 重新生成 MatchID 准备包与最终 GPT 交接文档，准确列出已完成、阻塞和下一步。**
- [x] **Step 5: 运行全量测试、批处理、MatchID 准备和审计。**

### Task 4: 交付验证

**Files:**
- No raw-file edits.

- [x] **Step 1: 运行 `python -m unittest discover -s tests -v`，失败时只修复本计划引入的问题。**
- [x] **Step 2: 运行 DAT 审计，确认 S22 无 `<53>` 帧出现在报告中，S15 `000285.jpg` 的 DAT 状态不是因 Job 清单缺失而被误判。**
- [x] **Step 3: 运行批处理、MatchID 准备和总审计，确认力值 CSV 行数契约不变。**
- [x] **Step 4: 检查原始 JPG/DAT/XLS/Job 的修改时间没有被本次流程写入；由于没有任务开始前基线，文档保留该证明限制。**
- [x] **Step 5: 更新 `index.md` 与 `log.md`，留下后续 GPT 能直接执行的入口。**
