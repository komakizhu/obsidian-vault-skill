# Obsidian Vault Skill：面向 AI Coding Agent 的 Obsidian 知识库技能

[English](README.md)

用于让 Claude Code、Gemini、Cursor、Windsurf、GitHub Copilot 和 OpenAI Codex 等 AI Coding Agent 管理本地 Obsidian 知识库，同时遵守知识库自身的规则、链接、元数据和人工确认边界。

本项目融合了 Andrej Karpathy 的 LLM-Wiki 思路、Google Open Knowledge Format（OKF）以及 Socratic cognitive friction 工作流，避免 AI 静默覆盖笔记、强行合并矛盾观点或把个人材料过度百科化。

## 核心能力

- **Obsidian 库管理**：搜索、查询、整理、创建和更新本地笔记。
- **PARA + MOC 结构**：遵守 Projects、Areas、Resources、Archives 目录和轻量 MOC 规则。
- **人工确认机制**：写入前展示文件清单、链接方案、冲突和待确认项。
- **动态 Vault 检测**：通过 `obsidian.json` 或常见目录自动发现 vault，并缓存路径。
- **定义笔记子 skill**：批量生成专业术语定义笔记，搜索已有概念并建立可靠双链。

## 仓库结构

```text
obsidian-vault-skill/
├── README.md
├── README.zh-CN.md
├── AGENTS.md                         # 可复制到 Obsidian vault 根目录的规则模板
├── references/
│   └── definition-notes.md           # 定义笔记的共享工作规范
├── obsidian-vault/
│   ├── SKILL.md                      # 主 Obsidian skill
│   └── scripts/detect_vault.py       # Vault 检测和路径缓存脚本
└── obsidian-definition-notes/
    └── SKILL.md                      # 可独立调用的定义笔记子 skill
```

## 定义笔记子 skill

`obsidian-definition-notes` 用于在现有 Obsidian 库中建立互相连接的术语词典。

### 它会做什么

- 将“关于 SKU 生成一批定义笔记”扩展为适度的相关术语簇。
- 搜索已有笔记、别名、MOC、上下位概念、例子和可能的冲突。
- 生成包含以下部分的定义笔记：一句话定义、解决的问题、核心要素、例子、容易混淆的术语、相关笔记和待确认项。
- 只有在关系有库内依据时才建立 Wikilink，并标注 `related`、`depends on`、`contrasts with`、`example of` 等关系。
- 只有在能改善导航且不会重复现有 MOC 时，才建议建立术语 MOC。
- 写入前展示文件、定义、链接、MOC 和歧义，等待用户明确确认；不会静默覆盖已有笔记。

### 调用方式

在支持 slash command 的 Agent 中使用：

```text
/obsidian-definition-notes 关于 SKU 生成一批定义笔记，放到 333 Resources 兴趣资源，并和已有笔记建立链接。
```

也可以直接用自然语言触发，例如：

```text
帮我把这组专业术语做成定义笔记，并连接到已有的 Obsidian 笔记。
```

主 `obsidian-vault` skill 也会自动把这类请求路由到定义笔记流程。

### YAML 字段规则

你的 vault 中的 `AGENTS.md` 优先级最高。对于使用本项目规则模板的 vault：

- `Topic` 和 `Subject` 是 YAML 数据字段；
- 不得把它们重复写成 `Topic/...` 或 `Subject/...` 标签；
- `tags` 只使用已批准的 PARA、keyword 或用户明确要求的命名空间。

示例：

```yaml
---
author: Komaki Zhu
type: Concept
Topic: 商品与库存管理
Subject: 商品与库存管理
status: seed
tags:
  - Resource/概念
  - keyword/SKU
aliases:
created: 2026-07-15T00:00
updated: 2026-07-15T00:00
---
```

### 回退和审计

子 skill 只在用户确认后写入，重要操作记录在 `LLM Wiki Log.md`。修正已有笔记前应先创建备份；新建笔记可以通过删除明确报告的文件回退，已有笔记不会在未经批准时被修改。

## 安装和配置

### 1. 配置 Vault 规则

将仓库根目录的 `AGENTS.md` 复制到你的 Obsidian vault 根目录，并根据个人目录、标签和 frontmatter 规则进行调整。

### 2. 安装主 skill

将 `obsidian-vault/` 安装到 Agent 的 skill 目录。例如 Codex：

```bash
cp -R obsidian-vault ~/.codex/skills/obsidian-vault
```

### 3. 安装定义笔记子 skill

```bash
cp -R obsidian-definition-notes ~/.codex/skills/obsidian-definition-notes
cp -R references ~/.codex/skills/references
```

安装后重启或刷新 Agent，使新的 skill 出现在 skill picker 中。

### 4. Vault 检测

```bash
python3 ~/.codex/skills/obsidian-vault/scripts/detect_vault.py --get
```

如果需要手动设置：

```bash
python3 ~/.codex/skills/obsidian-vault/scripts/detect_vault.py --set "/path/to/your/vault"
```

## 相关文档

- [English README](README.md)
- [主 Obsidian skill](obsidian-vault/SKILL.md)
- [定义笔记子 skill](obsidian-definition-notes/SKILL.md)
- [定义笔记工作规范](references/definition-notes.md)
