---
name: obsidian-vault
description: Use when the user says "根据我的笔记", "根据我的ob", "根据我的obsidian", "根据ob", "根据笔记", "根据我的知识库", "根据我的Obsidian库", or mentions searching, querying, reading, creating, or managing notes in their Obsidian vault.
---

# Obsidian Vault Integration (LLM-Wiki + OKF + Socratic Friction)

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
