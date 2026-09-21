# Karpathy LLM Wiki gist

来源：https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

## 摘要

Andrej Karpathy 提出一种 LLM 维护的个人知识库模式。它不同于传统 RAG：不是每次查询时从原始资料中重新检索和拼接答案，而是让 LLM 持续维护一个结构化、互相链接、可追溯的 Markdown wiki。

核心思想：

- 原始资料是不可变的事实来源。
- LLM 把资料编译成持久 wiki，并在新资料进入时更新相关页面。
- schema 规定目录结构、页面约定和维护流程，让 LLM 像维护代码库一样维护知识库。
- `index.md` 提供内容目录，`log.md` 提供时间线。
- 人负责选择资料、提出问题和审核方向，LLM 负责总结、交叉引用、更新和记账。

## 对本仓库的采用方式

本仓库采用最小三层架构：

1. `raw/`：原始资料。
2. `wiki/`：编译后的知识页。
3. `AGENTS.md` 与 `schema/`：维护协议。

为了兼容 Obsidian 和 GitHub Pages，本仓库优先使用标准 Markdown 链接。

