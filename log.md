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
