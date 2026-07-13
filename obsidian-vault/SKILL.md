---
name: obsidian-vault
description: Manage and reason over the user's local Obsidian vault while preserving the vault's rules, links, metadata, contradictions, and user approval boundaries. Use this skill whenever the user mentions Obsidian, their vault, notes, knowledge base, personal knowledge management, MOCs, PARA, or asks to search, query, read, summarize, organize, ingest, create, update, or manage notes. Trigger for Chinese requests such as "根据我的笔记", "根据我的知识库", "根据我的 Obsidian 库", "查一下我的笔记", "从我的知识库里找", "把这篇文章整理进 Obsidian", "写入我的笔记", "管理我的知识库", "我的笔记里有没有", "在我的笔记中搜索", "根据我的 ob", "根据我的 obsidian", or similar natural wording, even when the user does not explicitly say "vault" or "skill". Also trigger for equivalent English requests such as "according to my notes", "search my vault", or "add this to my Obsidian".
---

# Obsidian Vault Integration (LLM-Wiki + OKF + Socratic Friction)

For the reusable pattern behind this Chinese-trigger setup, see [Chinese trigger method](../references/chinese-trigger-method.md).

This skill connects your coding agent to your local Obsidian vault. It implements **Andrej Karpathy's LLM-Wiki** incremental compilation, **Google's Open Knowledge Format (OKF) v0.1** metadata standards, and a **Socratic cognitive friction** workflow to preserve ideological tensions and prevent cognitive outsourcing.

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
Once the vault path is determined (referred to as `<vault_path>`), you **MUST** locate and read `<vault_path>/AGENTS.md` to load the vault-specific conventions (e.g. PARA directories, 333 tagging rule, state rules).

### 2. Ingest Workflow (Socratic Friction & OKF Standard)
When the user drops a new source or clippings file and asks you to process it:
1.  **Search**: Use the `grep_search` tool inside `<vault_path>/` to find potentially related notes, overlapping concepts, or MOCs.
2.  **Draft OKF Meta**: Draft the frontmatter using Google OKF v0.1 fields:
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
    - Write the markdown file to its target PARA folder.
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
