---
name: Obsidian 定义笔记
description: |
  在本地 Obsidian 库中批量生成专业术语定义笔记，并自动搜索已有笔记建立可靠的双向链接、关系标注和术语导航 MOC。当用户要求解释术语、生成一批定义笔记、放入指定文件夹、连接已有笔记，或制作术语地图时使用。调用命令：/obsidian-definition-notes。
---

# Obsidian 定义笔记

这是一个可独立调用的 Obsidian 子 skill。完整工作规范见 [Definition Notes](../obsidian-vault/references/definition-notes.md)，本文件负责触发和路由。

本子 skill 必须遵守 vault 的 PM3（PARA + MOC + 333）模式：先读取 `AGENTS.md`，沿用既有 PARA 目录和 MOC，遵守 333 的目录、标签与元数据约束，不用通用知识库模板替代用户规则。

## 执行流程

1. 读取并执行 `/Users/mac/.codex/skills/obsidian-vault/SKILL.md` 的 vault 检测流程。
2. 运行 vault 检测脚本，读取 `<vault_path>/AGENTS.md`，再搜索目标术语、别名、上下位概念、例子和现有 MOC。
3. 根据上下文提出一组定义笔记；“一批”没有数量时，生成一个适度的相关术语簇，不擅自无限扩展。
4. 为每个术语规划目标路径、文件名、定义、关系类型和已有笔记链接。
5. 如果直接链接太少或术语较多，规划一个术语导航图/MOC；MOC 只负责发现，不代替真实语义关系。
6. 写入前展示文件清单、定义摘要、链接计划、MOC 方案、歧义和冲突，并等待用户明确确认。
7. 用户确认后才创建文件；不得静默覆盖已有笔记。严格使用 vault `AGENTS.md` 的 frontmatter schema，并记录 `LLM Wiki Log.md`。
8. 完成后报告创建文件、建立的链接、未解决的关系和跳过的覆盖操作。

## 输出要求

定义笔记至少包含：一句话定义、解决的问题、核心要素、例子、容易混淆的术语、相关笔记和待确认项。无法可靠判断的内容必须标为“待确认”。`Topic`、`Subject` 等字段必须写入 YAML；不得把它们重复写成 `Topic/...` 或 `Subject/...` 标签。

## 示例

用户：`/obsidian-definition-notes 关于 SKU 生成一批定义笔记，放到业务概念文件夹，并和其他笔记联结。`

先搜索 SKU、SPU、商品、变体、条码、库存等相关词，再给出待确认的笔记和 MOC 方案；确认后写入。
