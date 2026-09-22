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
