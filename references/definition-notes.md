# Definition Notes

Use this workflow for batches of professional-term definition notes.

## Inputs

Extract:

- terms and desired count (expand the term into a useful cluster when the user says “一批”);
- target folder, preserving the vault's naming and PARA conventions;
- intended audience and domain, if supplied;
- whether the user wants only notes, or also a navigation/MOC note.

If a term is ambiguous, list the candidate meanings and choose the one best supported by nearby vault notes; flag the choice in the proposal.

## Research and relationship discovery

1. Detect the vault and read `<vault_path>/AGENTS.md` before inspecting or writing anything.
2. Search existing notes for each term, aliases, abbreviations, parent concepts, examples, metrics, and likely related notes. Prefer existing MOCs and indexes as entry points.
3. Do not invent links merely because two terms sound similar. Classify each proposed link as `related`, `depends on`, `contrasts with`, `example of`, or `used by`.
4. If there are too few reliable direct connections, create a terminology MOC with a table of terms, one-line meanings, and links. A MOC is a fallback for discoverability, not evidence of a semantic relationship.

## Note template

Each definition note must use the vault's `AGENTS.md` frontmatter. The vault-local schema has priority over this skill and over the generic OKF example in the parent skill. For this vault, use:

```yaml
---
author: Komaki Zhu
cover:
source:
type: Concept
Topic: <broad topic>
Subject: <subject>
status: seed
tags:
  - Resource/概念
  - keyword/<term>
aliases:
created: <YYYY-MM-DDTHH:MM>
updated: <YYYY-MM-DDTHH:MM>
---
```

`Topic` and `Subject` are YAML data fields, not automatic tags. Never copy them into `tags` as `Topic/...` or `Subject/...`. Use `tags` only for the vault's approved PARA, keyword, or other explicitly requested tag namespaces. Do not invent a new domain tag when the same information already belongs in `Topic` or `Subject`.

Then write:

```markdown
# <Term>

## 一句话定义
<plain-language definition>

## 它解决什么问题
<purpose and boundary>

## 核心要素
- ...

## 例子
<concrete domain example>

## 容易混淆
- <nearby term>: <distinction>

## 相关笔记
- [[...]] — <relationship label>

## 待确认
- <uncertain claim, source, or unresolved distinction>
```

Keep uncertainty explicit. If no reliable source or existing note supports a claim, mark it as `待确认` rather than presenting it as fact.

## Proposal and write gate

Before creating files, show:

1. the target folder and exact filenames;
2. the terms and one-line definitions;
3. the existing notes each new note will link to;
4. the proposed MOC, if any, and why it is needed;
5. possible ambiguities, conflicts, and notes that would be updated.

Wait for explicit confirmation. After confirmation, create the notes, update only approved existing notes, and append the operation to `LLM Wiki Log.md`. Report created files, links made, unresolved items, and any skipped overwrite.

## Example routing

For “关于 SKU 生成一批定义笔记放在业务概念中，并和其他笔记联结起来”, search for `SKU`, `库存`, `商品`, `变体`, `SPU`, `条码`, and existing MOCs; propose a cluster such as SKU, SPU, variant, barcode, and inventory unit only when the vault context supports it. Create a “业务概念—商品标识 MOC” only if it improves navigation.
