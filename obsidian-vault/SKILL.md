---
name: obsidian-vault
description: Use when the user says "根据我的笔记", "根据我的ob", "根据我的obsidian", "根据ob", "根据笔记", "根据我的知识库", "根据我的Obsidian库", or mentions searching, querying, reading, creating, or managing notes in their Obsidian vault.
---

# Obsidian Vault

## Vault location

The vault location is dynamically detected and cached on the machine. Always query the path before performing operations by executing:
```bash
python3 ~/.gemini/config/skills/obsidian-vault/scripts/detect_vault.py --get
```

### Auto-Detection & Memory
- **Automatic Search**: The script parses Obsidian's native config (`obsidian.json`) or searches common folders (`~/Documents`, `~/Desktop`, `~/`) to find vaults.
- **Save/Remember Path**: If the user provides a path, save and remember it by running:
  ```bash
  python3 ~/.gemini/config/skills/obsidian-vault/scripts/detect_vault.py --set "/path/to/your/vault"
  ```
  This permanently saves it to `~/.gemini/config/obsidian_vault_path.txt`.

## Vault Structure & Rules

The vault follows the PARA + MOC framework.
A dedicated rules file is located at `[vault_path]/AGENTS.md`.
**Crucial**: You must read and adhere to `[vault_path]/AGENTS.md` for any modifications or reads in this vault.

The top-level directories are:
- `000 Projects 短期目标` (Active projects, essay, lyrics, video scripts)
- `222 Areas 长期目标` (Long-term interests, thoughts, critical studies)
- `333 Resources 兴趣资源` (Reference materials, clippings, external info)
- `444 Archives` (Completed or archived notes)

## Workflows

### Search for notes

Search the vault using the grep_search tool on the vault path returned by the script:
```bash
# Search by filename
find "<vault_path>/" -name "*.md" | grep -i "keyword"

# Search by content
grep -rl "keyword" "<vault_path>/" --include="*.md"
```

Or search using standard codebase tools directly scoped to the vault path.

### Create or Modify notes

1. Always explain proposed changes before writing (files, reasons, status updates).
2. Check if a relevant MOC (Map of Content) already exists and suggest updating it.
3. Log all major edits in `LLM Wiki Log.md` in the vault.
4. Respect philosophy and creative materials (do not sanitize or make them too objective).
