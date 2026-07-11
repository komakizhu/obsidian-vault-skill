# Obsidian Vault Skill for AI Coding Agents (LLM-Wiki + OKF + Socratic Friction)

An integration skill and rules kit for Gemini/Antigravity and other agentic coding assistants. It combines **Andrej Karpathy's LLM-Wiki** concept, **Google's Open Knowledge Format (OKF) v0.1** standard, and a **Socratic cognitive friction** loop designed to keep the user in the cognitive driver's seat and protect the vault against automated over-simplification.

## Features

- **Portability (Google OKF v0.1)**: Formats all note frontmatter metadata into standard fields (`type`, `title`, `description`, `resource`, `tags`, `timestamp`) making your knowledge base interoperable across different AI agents.
- **Socratic Interaction & Tension Preservation**: Prevents the agent from auto-merging opposing views or overwriting subjective insights. Forces the agent to explicitly report conceptual contradictions and obtain permission before making writes.
- **Structure-Enforcing Rules (PARA + MOC)**: Rules for managing Projects, Areas, Resources, and Archives directories, and lightweight Maps of Content.
- **Dynamic Vault Path Caching**: Auto-detects local vaults via `obsidian.json` or directory scanning and remembers the path to avoid hardcoding.

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

### Step 2: Deploy the Agent Skill
Copy the `obsidian-vault` directory to your agent's global customizations root. For Gemini/Antigravity, this is typically:
- **macOS/Linux**: `~/.gemini/config/skills/obsidian-vault/`
- **Windows**: `%USERPROFILE%\.gemini\config\skills\obsidian-vault\`

Make the detection script executable:
```bash
chmod +x ~/.gemini/config/skills/obsidian-vault/scripts/detect_vault.py
```

### Step 3: Configure Global Redirection Rules
Add the following rule to your global agent configurations at `~/.gemini/config/AGENTS.md` (create the file if it does not exist) so all agents automatically redirect to the vault on trigger words:

```markdown
# Global Agent Rules

## Obsidian Vault Integration & Redirection

Whenever the user mentions their notes, Obsidian, or uses trigger phrases like:
- "根据我的笔记" (According to my notes)
- "根据我的ob" (According to my ob)
- "根据我的obsidian" (According to my obsidian)
- "根据ob" (According to ob)
- "根据笔记" (According to notes)
- "根据我的知识库" (According to my knowledge base)
- "根据我的Obsidian库" (According to my Obsidian vault)
- or any similar variations,

**ALL AGENTS MUST AUTOMATICALLY FOLLOW THESE INSTRUCTIONS:**

1. **Dynamic Path Detection & Redirection**:
   - Immediately run the following script to get the active Obsidian vault directory path:
     `python3 ~/.gemini/config/skills/obsidian-vault/scripts/detect_vault.py --get`
   - Scope all your operations, searches, and context retrieval to the directory returned by the script.
   - If the script fails or returns that no vault was detected, ask the user to provide their vault path, and save it by executing:
     `python3 ~/.gemini/config/skills/obsidian-vault/scripts/detect_vault.py --set "<user_provided_path>"`
     This path will be permanently remembered and returned by future `--get` queries.

2. **Follow Local Vault Rules**:
   - Once the vault path is determined, read the local rules file at `<vault_path>/AGENTS.md` (which you copied in Step 1).
   - Adhere strictly to the rules specified there (PARA folder boundaries, Socratic friction, OKF schema, tension logging).
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
