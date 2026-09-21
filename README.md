# 终极大脑 Wiki

这是一个从零搭建的中文 LLM Wiki / 第二大脑仓库。它把原始资料、编译后的知识页和维护协议分开，让 Obsidian 作为阅读与导航环境，让 LLM 作为维护者持续更新知识结构。

当前仓库就是 Obsidian 连接的 Second Brain 文件夹。后续建设都在这里继续进行。

## 在线入口

GitHub Pages 启用后，入口页为 `index.md` 渲染出的站点首页。

## 结构

```text
.
├── AGENTS.md          # LLM 维护协议
├── index.md           # 内容索引与首页
├── log.md             # 追加式工作日志
├── raw/               # 原始资料，不可变
├── wiki/              # 编译后的知识页
└── schema/            # 模板与处理规范
```

## 使用方式

1. 把新资料放入 `raw/`。
2. 让 LLM 按 `AGENTS.md` 的 ingest 流程处理。
3. 在 Obsidian 中阅读 `index.md`、`log.md` 和 `wiki/` 页面。
4. 周期性运行 lint，检查矛盾、孤页、缺失来源和长期未验证问题。

## Obsidian 配置

本仓库已包含基础 `.obsidian` 配置：

- 新笔记默认进入 `wiki/`。
- 附件默认进入 `raw/assets/`。
- 模板目录为 `schema/obsidian-templates/`。
- 使用标准 Markdown 链接，兼容 GitHub Pages。
