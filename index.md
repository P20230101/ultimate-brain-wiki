# 终极大脑 Wiki

这是一个面向工程试验和数据处理的中文第二大脑。它不是资料仓库本身，而是一个持续编译的知识系统：原始资料进入 `raw/`，LLM 把它们加工成 `wiki/` 中可复用、可追溯、可迭代的知识页。

## 快速入口

- [维护协议](AGENTS.md)
- [工作日志](log.md)
- [原始资料说明](raw/README.md)
- [Wiki 总览](wiki/README.md)
- [Schema 说明](schema/README.md)

## 核心架构

| 层级 | 路径 | 作用 | 当前状态 |
| --- | --- | --- | --- |
| Raw sources | `raw/` | 保存不可变原始资料、附件、数据和剪藏 | 已初始化 |
| The wiki | `wiki/` | 保存 LLM 编译后的主题页、概念页、方法页和综合分析 | 已初始化 |
| The schema | `AGENTS.md`, `schema/` | 规定命名、页面字段、ingest/query/lint 流程 | 已初始化 |

## Wiki 页面

### 总览

- [终极大脑总览](wiki/终极大脑总览.md)：项目目标、边界和工作方式。

### 概念

- [LLM Wiki 模式](wiki/concepts/LLM-Wiki模式.md)：Raw sources、The wiki、The schema 的关系。
- [编译式知识管理](wiki/concepts/编译式知识管理.md)：为什么不是每次查询都从原始资料重新推理。

### 方法

- [资料摄取流程](wiki/methods/资料摄取流程.md)：新资料进入 wiki 的最小处理流程。
- [Wiki 健康检查](wiki/methods/Wiki健康检查.md)：周期性检查矛盾、孤页和缺失证据。

## 原始资料

- [Karpathy LLM Wiki gist](raw/karpathy-llm-wiki.md)：本仓库的初始参考资料。

## 当前成功标准

- 新资料可以被放入 `raw/` 并按流程编译到 `wiki/`。
- 任何新会话都能通过 `AGENTS.md` 理解维护规则。
- `index.md` 能作为 Obsidian 和 GitHub Pages 的首页。
- `log.md` 能追踪每次资料处理、查询和健康检查。

