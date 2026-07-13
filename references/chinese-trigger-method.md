# 中文触发改造方法

这份方法用于把一个已有 skill 改成“中文也容易被 agent 调用”的形态。目标不是单纯翻译，而是提高触发率、减少误判、让入口更像自然口语。

## 适用目标

适合以下情况：

- skill 本来只在英文语境下容易被触发。
- 用户会用中文说同一件事，但不会主动说 skill 名称。
- 你希望 agent 在“隐式调用”阶段更愿意选中这个 skill。

## 核心原则

1. 把“什么时候用”写进 description，而不是只写功能简介。
2. description 要比你直觉里更具体、更 pushy，明确列出中文口语表达。
3. 让中文别名覆盖真实用户会说的话，不要只写直译词。
4. 保留英文等价说法，避免把原有触发面缩窄。
5. 如果运行环境支持 UI 入口展示，就同步补 `agents/openai.yaml`，否则只改 `SKILL.md` 往往不够。

## 推荐改法

### 1. 扩写 frontmatter `description`

把 description 改成三段信息合一：

- skill 做什么。
- 什么时候应该触发。
- 用户可能怎么说这件事，尤其是中文自然表达。

推荐写法：

```yaml
description: Do X for Y. Use this skill whenever the user mentions A, B, or C, including Chinese phrases such as “...”, “...”, or “...”, even if they do not mention the skill name explicitly.
```

### 2. 加中文例子，不要只放泛化词

优先写真实口语，而不是抽象名词。

好的例子：

- “根据我的笔记”
- “从我的知识库里找”
- “把这篇文章整理进 Obsidian”
- “在我的笔记中搜索”

不够好的例子：

- “与笔记相关”
- “处理知识管理”
- “进行内容整理”

### 3. 把隐式触发写死

如果这个 skill 在中文里应该经常被调用，就直接写明：

- 用户没有说 skill 名字也要触发。
- 用户说的是功能描述，不是术语，也要触发。
- 用户用中英混写时也要触发。

这一步对 agent 很关键，因为它会把“我不确定要不要调用”变成“应该调用”。

### 4. 同步 UI 入口名

如果系统会显示 skill 卡片或菜单入口，补一个 `agents/openai.yaml`：

- `display_name`：中文可读的入口名。
- `short_description`：一句话说明能力。
- `default_prompt`：真正调用时塞给模型的默认提示。
- `policy.allow_implicit_invocation: true`：允许隐式触发。

注意：

- `display_name` 负责展示，不等于所有系统里的硬性别名机制。
- 真正能不能用 `/xxx` 调出，取决于宿主的 UI 规则，不要只靠文件名猜。

### 5. 保持原 skill 的功能边界

中文触发改造只改“入口”和“触发判断”，不要顺手把业务规则改散。

要保留的东西：

- 原有工作流
- 约束条件
- 文件路径规则
- 安全边界
- 输出格式

## 可复用模板

你可以直接把下面这段当成别的 skill 的 description 骨架：

```text
<skill does X>. Use this skill whenever the user asks for X, Y, or Z, including Chinese phrases such as “...”, “...”, “...”, even if they do not mention the skill name explicitly. Also trigger for equivalent English requests.
```

如果要更激进一点，可以补：

```text
Treat natural Chinese descriptions of the same task as trigger-worthy, even when they are informal, abbreviated, or mixed with English.
```

## 迁移检查清单

- [ ] description 写了功能 + 触发场景 + 中文例子
- [ ] 中文例子覆盖真实口语
- [ ] 保留英文等价表达
- [ ] `agents/openai.yaml` 已同步
- [ ] `allow_implicit_invocation` 已开启
- [ ] 没有把触发条件写得过窄
- [ ] 没有把显示名误当成唯一入口机制

