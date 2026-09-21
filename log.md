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
