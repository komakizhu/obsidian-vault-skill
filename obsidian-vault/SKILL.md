---
name: Obsidian 库
description: |
  管理和分析用户的本地 Obsidian 库，同时保留库的 PM3 规则、链接、元数据、矛盾以及用户审核边界。当用户提到 Obsidian、他们的库、笔记、知识库、个人知识管理、MOC、PARA、PM3，或要求搜索、查询、阅读、总结、整理、导入、创建、更新或管理笔记时使用。支持中文口语化触发（如“根据我的笔记”、“管理我的知识库”等）以及对应的英文请求。
---

# Obsidian 库

For the reusable pattern behind this Chinese-trigger setup, see [Chinese trigger method](../references/chinese-trigger-method.md).

This skill connects your coding agent to your local Obsidian vault. It implements **Andrej Karpathy's LLM-Wiki** incremental compilation, **Google's Open Knowledge Format (OKF) v0.1** metadata standards, and a **Socratic cognitive friction** workflow to preserve ideological tensions and prevent cognitive outsourcing.

## Definition Note Generator

When the user asks to define a professional term, generate a batch of definition notes, or connect a term to existing notes, load and follow [Definition Notes](./references/definition-notes.md). Treat requests such as “给我生成 SKU 的定义笔记”“放到 xxx 文件夹”“和其他笔记联结起来” as this workflow, even when the user does not mention a sub-skill. This workflow is also independently available as `/obsidian-definition-notes`.

The generator may create or update a terminology MOC/navigation note when direct links are sparse or the requested set contains multiple related terms. It must detect the vault and read `AGENTS.md` first, show a proposed file list and link plan, and wait for confirmation before writing. Existing notes are never overwritten silently.

## Vault Location & Detection

The vault location is dynamically detected and cached on the machine. Always query the path before performing operations by executing the detection script:
```bash
python3 /path/to/obsidian-vault/scripts/detect_vault.py --get
```

### Auto-Detection & Memory
- **Automatic Search**: The script parses Obsidian's native config (`obsidian.json`) or searches common folders (`~/Documents`, `~/Desktop`, `~/`) to find vaults.
- **Save/Remember Path**: If the user provides a path, save and remember it by running:
  ```bash
  python3 /path/to/obsidian-vault/scripts/detect_vault.py --set "/path/to/your/vault"
  ```
  This permanently saves it to `~/.config/obsidian-vault/path.txt`.

## The Workflow Contract

### 1. Read the Local Rules First
Once the vault path is determined (referred to as `<vault_path>`), you **MUST** locate and read `<vault_path>/AGENTS.md` to load the vault-specific PM3 conventions (PARA directories, lightweight MOCs, 333 tagging rule, metadata and state rules).

### 2. Ingest Workflow (Socratic Friction & OKF Standard)
When the user drops a new source or clippings file and asks you to process it:
1.  **Search**: Use the `grep_search` tool inside `<vault_path>/` to find potentially related notes, overlapping concepts, or MOCs.
2.  **Draft Meta**: Draft the frontmatter using the vault's `AGENTS.md` schema first. The generic OKF fields below are fallback guidance only and must not override local rules:
    ```yaml
    ---
    type: Concept / Article / Project / MOC / Area
    title: Note Title
    description: 1-sentence summary of the note
    resource: https://... (original URL or source link)
    tags: [para-tag, theme-tag]
    timestamp: YYYY-MM-DDTHH:MM:SSZ
    # Custom keys required by AGENTS.md:
    creator: AI Assistant
    status: seed / growing / fruit
    created: YYYY-MM-DDTHH:MM
    updated: YYYY-MM-DDTHH:MM
    ---
    ```
3.  **Identify Tension Points**: Compare the source with existing notes. Define **at least 2 conceptual tensions or contradictions** between the new source and your existing notes.
4.  **Dialogue Check**: Present the summary, the proposed note title/path, and the tension points to the user. **Wait for user confirmation before writing the file.**
5.  **Write and Log**: Once approved:
    - Write the markdown file to its target PM3/PARA folder.
    - Append an operation log entry to `<vault_path>/LLM Wiki Log.md`.

### 3. Query Workflow
When answering questions against the vault:
1.  Look at current MOCs (Maps of Content) and index notes first to locate candidate pages.
2.  Search using `grep_search` on the vault path.
3.  Synthesize a comprehensive answer containing relative links to relevant notes. If you find conflicting notes, **preserve and highlight the conflict** rather than merging them.

### 4. Lint Workflow (Health Check)
Periodically inspect the vault:
-   Find orphan notes (no incoming links) and missing cross-references.
-   Identify conflicting claims or updates that have superseded older notes.
-   Compile a **Tension Report** for the user rather than modifying notes automatically.
