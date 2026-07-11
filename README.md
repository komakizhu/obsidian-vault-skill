# Obsidian Vault Skill for AI Coding Agents

An integration skill for Gemini/Antigravity and other agentic coding assistants that automatically redirects operations to your local Obsidian vault when trigger phrases (like "according to my notes" or "根据我的ob") are used.

## Features

- **Dynamic Auto-Detection**: Finds your active Obsidian vault automatically by parsing `obsidian.json` (macOS, Windows, Linux) or scanning common user directories (`~/Documents`, `~/Desktop`).
- **Memory/Persistence**: Once a vault path is detected or manually specified, it is cached locally and remembered for all future operations.
- **Global Integration**: Integrates via agent customizations (Skills & Rules) so it automatically works across all projects and conversations.

## Structure

```
obsidian-vault-skill/
├── .gitignore
├── README.md
└── obsidian-vault/
    ├── SKILL.md                 # Skill instructions loaded by agents
    └── scripts/
        └── detect_vault.py      # Python script managing path discovery & caching
```

---

## Installation

### Step 1: Copy the Skill
Copy the `obsidian-vault` directory to your agent's global customizations root. For Gemini/Antigravity, this is typically:
- **macOS/Linux**: `~/.gemini/config/skills/obsidian-vault/`
- **Windows**: `%USERPROFILE%\.gemini\config\skills\obsidian-vault\`

Make sure the script is executable:
```bash
chmod +x ~/.gemini/config/skills/obsidian-vault/scripts/detect_vault.py
```

### Step 2: Configure Global Rules
Add the redirection rule to the global `AGENTS.md` file in the customizations root (e.g. `~/.gemini/config/AGENTS.md`). If the file doesn't exist, create it:

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
   - Once the vault path is determined, read the local rules file at `<vault_path>/AGENTS.md`.
   - Adhere strictly to the rules specified there.
```

---

## Usage

### Auto-Detection
The first time you invoke the agent with "根据我的ob", it will run the detection utility. If you have Obsidian installed and a vault open, it will locate it instantly.

### Manual Setup
If you want to manually bind a specific vault, run:
```bash
python3 ~/.gemini/config/skills/obsidian-vault/scripts/detect_vault.py --set "/path/to/your/obsidian/vault"
```
The script saves this path to `~/.gemini/config/obsidian_vault_path.txt` and uses it as the active vault.
