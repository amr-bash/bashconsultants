# Prompt Orchestrator

A VS Code extension that orchestrates AI agent workflows using structured prompts from `.github/prompts/`.

## Features

- **Discover prompts**: automatically loads prompt templates from the `.github/prompts/` directory
- **Execute commands**: run prompts on files via the Command Palette or the sidebar
- **Chat integration**: send prompts to GitHub Copilot Chat or the VS Code Language Model API
- **Sidebar view**: browse and execute available prompts from the Explorer
- **Context-aware**: automatically includes file content as context

## Installation and usage

### Development setup

1. **Navigate to the extension directory:**
   ```bash
   cd extension
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Compile and run:**
   Press `F5` in VS Code to launch the Extension Development Host

### Configure the prompts directory

The extension looks for prompts in `.github/prompts/` by default. You can change this in Settings:
```json
{
  "promptOrchestrator.promptsDirectory": ".github/prompts"
}
```

### Available commands

Open the Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`):

| Command | What it runs |
| --- | --- |
| **Prompt Orchestrator: Refresh Prompts** | Reloads prompt templates from disk |
| **Prompt Orchestrator: Execute Prompt on File** | Pick any prompt from the library, then a file |
| **Prompt Orchestrator: Review Article** | `article-review.prompt.md` |
| **Prompt Orchestrator: Refactor Code** | `code-refactoring.prompt.md` |
| **Prompt Orchestrator: Generate Tests** | `test-generation.prompt.md` |
| **Prompt Orchestrator: Generate Documentation** | `documentation.prompt.md` |
| **Prompt Orchestrator: Debug Code** | `debugging.prompt.md` |

The shortcut commands use short aliases (`review`, `refactor`, `test`, `docs`, `debug`) that the extension resolves to the canonical prompt filenames above — the same mapping used by `scripts/routine-maintenance.sh` at the repository root.

### Execution methods

When executing a prompt, choose:
1. **Send to Chat (Copilot)** — copies the formatted prompt to the clipboard and opens the Chat panel for you to paste into
2. **Execute with Language Model** — sends the prompt through the VS Code Language Model API (currently Copilot's GPT-4o) and opens the response in a new editor; falls back to the clipboard method when no model is available
3. **Copy to Clipboard** — copies the formatted prompt for manual use

## Prompt template format

Create `.prompt.md` files in `.github/prompts/`. Frontmatter follows the canonical schema in `.github/FRONTMATTER.md`:

```markdown
---
mode: agent
description: "One-line summary shown in the prompt picker (<= 160 chars)"
date: 2026-05-18T12:00:00.000Z
lastmod: 2026-05-18T12:00:00.000Z
---
Act as an expert [role].

Your task is to [description].

[Instructions...]
```

Files with malformed frontmatter are skipped gracefully and logged to the **Prompt Orchestrator** output channel — they never break activation.

## Development

```bash
# Navigate to extension directory
cd extension

# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Watch mode
npm run watch

# Run tests
npm test

# Package extension
npm run package
```

## Project structure

```
extension/
├── src/
│   ├── extension.ts          # Main extension entry point
│   ├── promptManager.ts      # Prompt discovery, parsing, and alias resolution
│   ├── promptExplorer.ts     # Sidebar tree view provider
│   ├── chatIntegration.ts    # VS Code Chat API integration
│   └── test/
│       ├── extension.test.ts
│       └── promptManager.test.ts
├── .vscode/
│   ├── launch.json           # Debug configurations
│   ├── tasks.json            # Build tasks
│   └── extensions.json       # Recommended extensions
├── package.json              # Extension manifest
├── tsconfig.json             # TypeScript configuration
├── esbuild.js                # Build configuration
├── eslint.config.mjs         # Linting rules
└── .vscodeignore             # Files to exclude from package
```

## Requirements

- VS Code 1.96.0 or higher
- GitHub Copilot (optional, for chat integration)

## Extension settings

- `promptOrchestrator.promptsDirectory`: directory containing prompt files
- `promptOrchestrator.autoRefresh`: auto-refresh prompts on file changes

## Roadmap

Planned work, in rough priority order:

- **Pipeline chaining** — run multi-step workflows (for example refactor → test → docs) as a single command, mirroring `full-maintenance` in `scripts/routine-maintenance.sh`
- **`@bash` chat participant** — a native Copilot Chat participant so prompts can be invoked inline (`@bash /review`) without leaving the Chat panel
- **Model-agnostic execution** — select any model exposed by `vscode.lm` instead of assuming Copilot's GPT-4o
- **MCP server exposure** — publish the prompt library through a Model Context Protocol (MCP) server so tools beyond VS Code can consume the same prompts

---

Built for BASH Consulting
