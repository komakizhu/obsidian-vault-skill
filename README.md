# Obsidian Vault Skill for AI Coding Agents (LLM-Wiki + OKF + Socratic Friction)

An integration skill and rules kit for agentic coding assistants (including **Claude Code**, **Gemini/Antigravity**, **Cursor**, **Windsurf**, and **GitHub Copilot**). 

It combines **Andrej Karpathy's LLM-Wiki** concept, **Google's Open Knowledge Format (OKF) v0.1** standard, and a **Socratic cognitive friction** loop designed to keep the user in the cognitive driver's seat and protect the vault against automated over-simplification.

---

## Key Features

- **Portability (Google OKF v0.1)**: Formats all note frontmatter metadata into standard fields (`type`, `title`, `description`, `resource`, `tags`, `timestamp`) making your knowledge base interoperable across different AI agents.
- **Socratic Interaction & Tension Preservation**: Prevents the agent from auto-merging opposing views or overwriting subjective insights. Forces the agent to explicitly report conceptual contradictions and obtain permission before making writes.
- **Structure-Enforcing Rules (PARA + MOC)**: Rules for managing Projects, Areas, Resources, and Archives directories, and lightweight Maps of Content.
- **Dynamic Vault Path Caching**: Auto-detects local vaults via `obsidian.json` (macOS, Windows, Linux) or directory scanning, caching the path to a standard configuration file (`~/.config/obsidian-vault/path.txt`).

---

## Repository Layout

```
obsidian-vault-skill/
├── .gitignore
├── README.md                # This setup guide
├── AGENTS.md                # [Template] Vault rules to copy into your Obsidian vault root
└── obsidian-vault/
    ├── SKILL.md             # Skill instructions loaded by agents
    └── scripts/
        └── detect_vault.py  # Python script managing path discovery & caching
```

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
Codex natively loads rules from the global customizations root (`~/.gemini/config/AGENTS.md`) or the workspace root `AGENTS.md`. Add the following redirection instructions to the rules file:
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
