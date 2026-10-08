# ChatGPT Work: installation and distribution

[中文说明](#zh-cn)

## Copy one instruction

Use the code block's top-right copy button, then paste the instruction into your agent conversation:

**Full research workflow: all 27 skills**

```text
Read and follow https://github.com/Boom5426/Nature-Paper-Skills/blob/main/INSTALL.md to install all 27 Nature Paper Skills for this environment, using the all profile, and verify the result.
If the page cannot be read, use an available GitHub tool or git clone to retrieve the main branch and read INSTALL.md from the repository root; do not substitute search snippets for the file.
```

**Manuscript writing and review: 19 skills**

```text
Read and follow https://github.com/Boom5426/Nature-Paper-Skills/blob/main/INSTALL.md to install the recommended 19 Nature Paper Skills for this environment, and verify the result.
If the page cannot be read, use an available GitHub tool or git clone to retrieve the main branch and read INSTALL.md from the repository root; do not substitute search snippets for the file.
```

The agent handles source retrieval, selects the available installation flow and
checks the result. You do not need to explicitly invoke a creator, run Python,
generate an archive or upload files. [INSTALL.md](../INSTALL.md) provides the
agent procedure and checks registration capabilities before installation. Its
URL must resolve to this published file; local edits alone do not change GitHub.

**Status: automatic ChatGPT Work web installation is unverified.** The agent
must first check that this account exposes a supported save/register flow. If
it does not, the agent reports the missing capability. Writing a local skill
directory in a web task does not establish availability in a new conversation.

[OpenAI Docs](https://learn.chatgpt.com/docs/build-skills) documents standalone
skills for desktop/CLI/IDE and plugin-bundled skills on the web. [Workspace
controls](https://learn.chatgpt.com/docs/enterprise/skills) separate account
registration from filesystem installation. A creator may be used internally
when available and suitable; seeing `skill-creator` alone does not confirm a
workspace registration capability.

A reliable distribution route is a published plugin or a workspace-imported
marketplace. The maintainer or workspace administrator handles the setup below.
Users receive the resulting listing, rather than source-building instructions.
Live account installation and new-chat invocation still need verification.

## Maintainer: prepare distribution materials

From the repository, with Python 3.9+:

```bash
python3 scripts/build_chatgpt_plugin.py --output-dir dist/chatgpt-work/v0.1.0-recommended
```

Use `python` instead of `python3` on Windows when appropriate. This builder uses
the standard library, needs no Bash and refuses an existing output directory.
Use a new output directory for each build; add `--version 0.1.1` for a new release.
Add `--figure` for 21 specialists, or `--set all` for all 27.

| Output | Purpose |
|---|---|
| `nature-paper-workflow-0.1.0-recommended.zip` | Single-entry skill source, retaining 19 specialists under `resources/`; use only with a supported creation/registration flow |
| `SKILL-CREATOR-PROMPT.txt` | Optional source-based creation request; not an automatic installer |
| `skills/nature-paper-workflow/` | Complete single-entry directory for publication |
| `nature-paper-skills-0.1.0-recommended.zip` | Skills-only plugin package for publication |
| `.agents/plugins/marketplace.json` and `plugins/nature-paper-skills/` | GitHub workspace import tree |

The builder does not save, register or publish anything to a web account. It
preserves skill resources, licensing and hashes. Individual scripts retain
their original tool and dependency requirements.

### Publish for ordinary users

Upload the **plugin ZIP** to the [plugin publishing dashboard](https://platform.openai.com/plugins),
complete validation and publishing, then provide the actual listing. The
single-entry skill source ZIP is not a plugin submission package. See
[OpenAI Docs: plugin submission](https://developers.openai.com/plugins/deploy/submission).

### Workspace administrator: import from GitHub

Publish the generated marketplace tree first. Generated `dist/chatgpt-work/`
files are Git-ignored; the builder does not commit or publish them.

If the published marketplace root is `dist/chatgpt-work/v0.1.0-recommended`:

1. Open **Admin → Plugins → Add → Import marketplace**.
2. Set **Source** to `https://github.com/Boom5426/Nature-Paper-Skills`.
3. Set **Path** to `dist/chatgpt-work/v0.1.0-recommended`, the marketplace root.
4. Select the branch/tag/commit containing that directory.
5. Review import results and configure plugin availability for the intended roles.
6. Members install **Nature Paper Skills** and select it in a new Work chat.

Use the actual source, path and ref if the generated tree is hosted elsewhere.
The directory must contain the published marketplace and plugin files. Follow
[OpenAI Docs: GitHub import](https://learn.chatgpt.com/docs/enterprise/plugin-management).

### Optional source-based creator trial

If a supported creator can save/register repository resources, it can use the
single-entry `nature-paper-workflow` directory or source ZIP. Preserve the root
`SKILL.md`, `references/` and all `resources/<name>/` folders. No particular
creator is required by this repository, and archive attachment alone is not a
documented automatic importer.

A GitHub folder link requires the complete generated directory to be published.
The root repository is a skill collection; the built-in Codex `skill-installer`
requires individual `--path` values. Other collection installers can discover
the categorized tree: Vercel's `skills@1.7.1 add ... --list` found all 27 skills.
That local discovery result does not test ChatGPT Work account registration.
See [Vercel's installer](https://github.com/vercel-labs/skills#skill-discovery).

## Verification

Local checks cover profile selection, package layout, resources, licensing,
metadata, hashes and existing-output preservation. A supported save/register
flow must return a real skill/plugin identifier or listing before installation
can be reported. Finding and invoking it in a new chat verifies reuse. No live
ChatGPT Work account registration or invocation test has been completed.

Use your own passage and evidence, or the [first-run example](../examples/first-run/README.md),
when testing the installed workflow.

<a name="zh-cn"></a>

## 中文说明

点击下方代码块右上角的复制按钮，再粘贴到代理对话中：

**完整科研流程：全部 27 个技能**

```text
读取并执行 https://github.com/Boom5426/Nature-Paper-Skills/blob/main/INSTALL.md，为当前环境安装 Nature Paper Skills 全部 27 个技能（all 完整集），并验证结果。
若页面读取失败，请使用可用的 GitHub 工具或 git clone 获取 main 分支源码，再读取根目录 INSTALL.md；不要用搜索摘要代替原文。
```

**论文写作与审稿：19 个技能**

```text
读取并执行 https://github.com/Boom5426/Nature-Paper-Skills/blob/main/INSTALL.md，为当前环境安装 Nature Paper Skills 推荐的 19 个技能，并验证结果。
若页面读取失败，请使用可用的 GitHub 工具或 git clone 获取 main 分支源码，再读取根目录 INSTALL.md；不要用搜索摘要代替原文。
```

无需指定 `@skill-creator`、执行 Python、制作或上传 ZIP。代理自行取得资源，
检查当前环境支持的安装路径，再执行与验证。[INSTALL.md](../INSTALL.md) 提供
代理流程，先核对账号注册能力。链接必须对应已发布文件，本地修改不会更新 GitHub。

**网页版自动安装尚未验证。** 账号需要有受支持的保存／注册流程；如果当前代理
没有这项能力，应直接说明缺少什么。下载了仓库、打包成功或写入网页任务内的
技能目录，都不能证明新会话能调用。看得到 `skill-creator` 也不等于已具备账号
注册能力；creator 可作为代理内部选用的工具，无需用户预先点选。

可靠分发由维护者或工作区管理员完成：

- **面向普通用户：** 维护者生成插件包，完成官方发布，然后提供真实的插件安装入口。
- **工作区内使用：** 管理员导入已发布的 GitHub marketplace，再设置成员可用性。

上方打包、发布与导入步骤属于维护者／管理员操作。它们不应成为普通用户复制
安装指令后还要完成的前置任务。

**已验证：** 本地安装器、包结构、技能集、完整资源、许可、哈希及防覆盖行为。
**待验证：** 网页账号注册、实际安装和新会话调用。
