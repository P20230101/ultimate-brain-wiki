# 终极大脑 Wiki

这是一个面向工程试验和数据处理的中文第二大脑。它不是资料仓库本身，而是一个持续编译的知识系统：原始资料进入 `raw/`，LLM 把它们加工成 `wiki/` 中可复用、可追溯、可迭代的知识页。

## 快速入口

- [维护协议](AGENTS.md)
- [论文写作框架](AGENTS/论文写作框架.md)
- [科研工具环境](AGENTS/科研工具环境.md)
- [技能分类与调用协议](AGENTS/技能分类与调用协议.md)
- [工作日志](log.md)
- [原始资料说明](raw/README.md)
- [Wiki 总览](wiki/README.md)
- [Schema 说明](schema/README.md)

## Obsidian 工作台

- 默认首页：打开本文件 `index.md`。
- 默认新笔记位置：`wiki/`。
- 默认附件位置：`raw/assets/`。
- 模板目录：`schema/obsidian-templates/`。
- 每日记录目录：`wiki/daily/`。
- 书签入口：`index.md`、`log.md`、`wiki/`、`raw/`、`schema/`。
- 推荐流程：资料先进入 `raw/`，再用模板编译到 `wiki/`，最后追加 `log.md`。

## 核心架构

| 层级 | 路径 | 作用 | 当前状态 |
| --- | --- | --- | --- |
| Raw sources | `raw/` | 保存不可变原始资料、附件、数据和剪藏 | 已初始化 |
| The wiki | `wiki/` | 保存 LLM 编译后的主题页、概念页、方法页和综合分析 | 已初始化 |
| The schema | `AGENTS.md`, `schema/` | 规定命名、页面字段、ingest/query/lint 流程 | 已初始化 |

## Wiki 页面

### 长期框架

- [论文写作框架](AGENTS/论文写作框架.md)：论文润色、Discussion 写作和论文结构化总结协议。
- [科研工具环境](AGENTS/科研工具环境.md)：MinerU 论文解析和 Semantic Scholar 文献检索配置。
- [技能分类与调用协议](AGENTS/技能分类与调用协议.md)：所有 skill 的分类、路由和执行顺序。
- [PA12 双轴试样仿真与实验全流程](AGENTS/PA12双轴试样仿真与实验全流程.md)：当前 SLS PA12 双轴试样课题的执行协议。

### 总览

- [终极大脑总览](wiki/终极大脑总览.md)：项目目标、边界和工作方式。

### 概念

- [LLM Wiki 模式](wiki/concepts/LLM-Wiki模式.md)：Raw sources、The wiki、The schema 的关系。
- [编译式知识管理](wiki/concepts/编译式知识管理.md)：为什么不是每次查询都从原始资料重新推理。

### 方法

- [资料摄取流程](wiki/methods/资料摄取流程.md)：新资料进入 wiki 的最小处理流程。
- [Wiki 健康检查](wiki/methods/Wiki健康检查.md)：周期性检查矛盾、孤页和缺失证据。

### 文献

- [检索增强生成：面向知识密集型自然语言处理任务](wiki/literature/rag-2020-knowledge-intensive-nlp.md)：以一篇新论文验证“官方来源 → Raw source → MinerU → 中文 Wiki”的完整流程。
- [PA12 双轴中心区均匀性筛选](wiki/methods/PA12双轴中心区均匀性筛选.md)：用 Abaqus、DIC 和 VFM 比较中心区均匀性的力学方法页。
- [PA12 流程验证报告](AGENTS/PA12双轴试样仿真/验证/2026-09-22_流程验证报告.md)：五个 STEP 前处理、Abaqus smoke solve 和 ODB 指标提取的证据。

## 原始资料

- [Karpathy LLM Wiki gist](raw/karpathy-llm-wiki.md)：本仓库的初始参考资料。
- [RAG 论文 PDF](raw/papers/lewis2020-rag-knowledge-intensive-nlp-v4.pdf)：Lewis 等，arXiv:2005.11401v4。
- [RAG 原始文献登记卡](raw/papers/lewis2020-rag-knowledge-intensive-nlp-v4.md)：来源、哈希、解析范围和定位记录。
- [PA12 数据源登记](raw/datasets/PA12数据源登记.md)：外部实验、DIC、MatchID、VFM 与 STEP 数据的来源和边界。

## 当前成功标准

- 新资料可以被放入 `raw/` 并按流程编译到 `wiki/`。
- 任何新会话都能通过 `AGENTS.md` 理解维护规则。
- `index.md` 能作为 Obsidian 和 GitHub Pages 的首页。
- `log.md` 能追踪每次资料处理、查询和健康检查。
- 新论文可由 MinerU 解析并编译为带 locator 引用的中文文献页。
- PA12 原始数据可被定位到，五个已核实厚度模型可进入 Abaqus 输入文件生成和中心区均匀性后处理流程。
