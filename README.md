# Obsidian Vault Skill for AI Coding Agents (LLM-Wiki + OKF + Socratic Friction)

[简体中文](README.zh-CN.md)

An integration skill and rules kit for agentic coding assistants (including **Claude Code**, **Gemini/Antigravity**, **Cursor**, **Windsurf**, and **GitHub Copilot**). 

It combines **Andrej Karpathy's LLM-Wiki** concept, **Google's Open Knowledge Format (OKF) v0.1** standard, and a **Socratic cognitive friction** loop designed to keep the user in the cognitive driver's seat and protect the vault against automated over-simplification.

---

## Key Features

- **Portability (Google OKF v0.1)**: Formats all note frontmatter metadata into standard fields (`type`, `title`, `description`, `resource`, `tags`, `timestamp`) making your knowledge base interoperable across different AI agents.
- **Socratic Interaction & Tension Preservation**: Prevents the agent from auto-merging opposing views or overwriting subjective insights. Forces the agent to explicitly report conceptual contradictions and obtain permission before making writes.
- **PM3 Knowledge-Base Model**: The repository's named organizational model, combining PARA's Projects/Areas/Resources/Archives layout, lightweight MOCs, and the user's 333 principle for directory, tag, and metadata discipline.
- **Dynamic Vault Path Caching**: Auto-detects local vaults via `obsidian.json` (macOS, Windows, Linux) or directory scanning, caching the path to a standard configuration file (`~/.config/obsidian-vault/path.txt`).
- **Definition Notes Sub-skill**: Generates batches of professional-term notes, searches the vault for related concepts, creates reliable Wikilinks, and proposes a lightweight terminology MOC when direct connections are insufficient.

### PM3

**PM3** is the name of the knowledge-base model this skill is designed to preserve: **PARA + MOC + 333**. PARA provides the four top-level areas, MOCs provide lightweight navigation, and the 333 principle constrains folder depth, tag depth, and metadata growth. The agent must read the vault's `AGENTS.md` and follow the user's concrete PM3 rules rather than substituting a generic PARA implementation.

---

## Repository Layout

```
obsidian-vault-skill/
├── .gitignore
├── README.md                # This setup guide
├── AGENTS.md                # [Template] Vault rules to copy into your Obsidian vault root
├── references/
│   └── definition-notes.md   # Shared workflow and frontmatter rules for definition notes
├── obsidian-vault/
    ├── SKILL.md             # Skill instructions loaded by agents
    └── scripts/
        └── detect_vault.py  # Python script managing path discovery & caching
└── obsidian-definition-notes/
    └── SKILL.md              # Independently callable definition-notes sub-skill
```

## Definition Notes Sub-skill

The repository includes an independently callable `obsidian-definition-notes` sub-skill for building a connected glossary inside an existing vault.

### What it does

- Expands a request such as “关于 SKU 生成一批定义笔记” into a focused cluster of related terms.
- Searches existing notes, aliases, MOCs, parent concepts, examples, and possible conflicts before drafting.
- Produces definition notes with a consistent structure: one-sentence definition, purpose, core elements, examples, confusing neighbors, related notes, and unresolved questions.
- Creates Wikilinks only when the relationship is supported by the vault context, labeling relationships such as `related`, `depends on`, `contrasts with`, or `example of`.
- Suggests a terminology MOC only when it improves navigation and does not duplicate an existing MOC.
- Shows the proposed files, definitions, links, MOC, and ambiguities before writing. It waits for explicit confirmation and never silently overwrites an existing note.

### How to invoke it

Use the skill's directory name as the explicit command where the agent supports slash commands:

```text
/obsidian-definition-notes 关于 SKU 生成一批定义笔记，放到 333 Resources 兴趣资源，并和已有笔记建立链接。
```

It can also be invoked implicitly by requests mentioning definition notes, professional terms, glossaries, terminology maps, or connecting newly generated concepts to existing Obsidian notes. The parent `obsidian-vault` skill routes these requests to the same workflow.

### Frontmatter priority

The vault's local `AGENTS.md` is authoritative. For vaults using the included template, `Topic` and `Subject` are YAML data fields; they must not be duplicated as `Topic/...` or `Subject/...` tags. Tags should remain limited to approved PARA, keyword, or explicitly requested namespaces.

Example:

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

### Rollback and auditability

The sub-skill writes only after confirmation, records important operations in `LLM Wiki Log.md`, and should create backups before correcting existing notes. Newly created notes can be rolled back by deleting the explicitly reported files; existing notes are not modified unless the user approves that change.

---

## Installation & Setup

### Step 1: Initialize Your Vault Rules
1. Copy the **`AGENTS.md` template file** from the root of this repository.
2. Paste it directly into the **root directory of your Obsidian vault** (e.g., inside your actual vault folder on your machine).
3. (Optional) Open the copied `AGENTS.md` in Obsidian and customize the `creator` and other default frontmatter settings.

### Step 2: Deploy the Detection Script
1. Place the `detect_vault.py` script somewhere convenient on your machine (e.g. `~/.config/obsidian-vault/scripts/detect_vault.py`).
2. Make it executable:
   ```bash
   chmod +x ~/.config/obsidian-vault/scripts/detect_vault.py
   ```

---

## Step 3: Configure Your Agent

### 1. Claude Code
Add the redirection instructions to your global or local `CLAUDE.md` (e.g. `~/.config/claude/CLAUDE.md` or the `CLAUDE.md` in your project root):
```markdown
## Obsidian Vault Redirection

Whenever the user mentions their notes, Obsidian, or trigger phrases like "根据我的笔记" / "根据我的ob", follow these instructions:
1. Run `python3 ~/.config/obsidian-vault/scripts/detect_vault.py --get` to retrieve the active vault path.
2. Scope your operations and searches to that directory. If no vault is found, prompt the user for the path and save it with `python3 ~/.config/obsidian-vault/scripts/detect_vault.py --set "<path>"`.
3. Read the vault's local rules file at `<vault_path>/AGENTS.md` and follow them strictly.
```

### 2. Cursor / Windsurf
Put the custom instructions in your `.cursorrules` or `.windsurfrules` file:
```text
Obsidian Vault Redirection:
- When matching keywords like "according to my notes" or "根据我的ob":
  1. Execute `python3 ~/.config/obsidian-vault/scripts/detect_vault.py --get` to retrieve the active vault path.
  2. Scope your search and operations to that path.
  3. Load and strictly adhere to `<vault_path>/AGENTS.md` for writing/reading rules.
```

### 3. Gemini / Antigravity
Copy the `obsidian-vault` directory to your agent's global customizations root (usually `~/.gemini/config/skills/obsidian-vault/`), and add the redirection rule to `~/.gemini/config/AGENTS.md`.

### 4. OpenAI Codex
Install the `obsidian-vault/` directory under Codex's skills directory (for example, `~/.codex/skills/obsidian-vault/`). Codex will discover the skill from its `SKILL.md` metadata and `agents/openai.yaml` UI configuration, where it is displayed as `笔记`. In the skill picker, invoke it as the notes/Obsidian skill; depending on the Codex build, the explicit command may appear as `/笔记` or `$obsidian-vault`. Requests such as `根据我的笔记查一下……` and `把这篇文章整理进我的 Obsidian 知识库` can also invoke it implicitly. If you also use project-level rules, add the following redirection instructions to the workspace `AGENTS.md`:
```markdown
## Obsidian Vault Redirection

Whenever the user mentions their notes, Obsidian, or trigger phrases like "根据我的笔记" / "根据我的ob", follow these instructions:
1. Run `python3 ~/.config/obsidian-vault/scripts/detect_vault.py --get` to retrieve the active vault path.
2. Scope your operations and searches to that directory. If no vault is found, prompt the user for the path and save it with `python3 ~/.config/obsidian-vault/scripts/detect_vault.py --set "<path>"`.
3. Read the vault's local rules file at `<vault_path>/AGENTS.md` and follow them strictly.
```

---

## How It Works in Practice

### Ingesting a Note with Cognitive Friction
1. When you say: *"根据我的ob，把这篇文章整理进去"* (According to my ob, file this article).
2. The agent reads the source, drafts the metadata in OKF format, and compares it with your current vault.
3. Instead of writing silently, the agent outputs:
   - A summary of the key takeaways.
   - **Tension Points**: e.g., *"This article claims X, which conflicts with your note [[Note Title]] which asserts Y."*
4. The agent **stops and waits** for you to confirm whether you want to reconcile it, explicitly document the tension in a `# Tension` section, or dismiss the new source.
5. Once confirmed, it writes the note and appends to `<vault_path>/LLM Wiki Log.md` to keep a clean audit trail.
