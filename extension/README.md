# Prompt Orchestrator

A VS Code extension that orchestrates AI agent workflows using structured prompts from `.github/prompts/`.

## Features

- **Discover Prompts**: Automatically loads prompt templates from `.github/prompts/` directory
- **Execute Commands**: Run prompts on files via Command Palette or sidebar
- **Chat Integration**: Send prompts to GitHub Copilot Chat or Language Model API
- **Sidebar View**: Browse and execute available prompts from the Explorer
- **Context-Aware**: Automatically includes file content as context

## Installation & Usage

### Development Setup

1. **Navigate to extension directory:**
   ```bash
   cd extension
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Compile and run:**
   Press `F5` in VS Code to launch Extension Development Host

### Configure Prompts Directory

The extension looks for prompts in `.github/prompts/` by default. You can change this in Settings:
```json
{
  "promptOrchestrator.promptsDirectory": ".github/prompts"
}
```

### Available Commands

Open Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`):

- **Prompt Orchestrator: Refresh Prompts** - Reload prompt templates
- **Prompt Orchestrator: Execute Prompt on File** - Choose prompt and file
- **Prompt Orchestrator: Review Article** - Run article-review prompt
- **Prompt Orchestrator: Refactor Code** - Run refactoring prompt
- **Prompt Orchestrator: Generate Tests** - Run test-generation prompt
- **Prompt Orchestrator: Generate Documentation** - Run documentation prompt
- **Prompt Orchestrator: Debug Code** - Run debugging prompt

### Execution Methods

When executing a prompt, choose:
1. **Send to Chat (Copilot)** - Opens in Chat panel with prompt ready to paste
2. **Execute with Language Model** - Directly calls GPT-4o and shows results
3. **Copy to Clipboard** - Copies formatted prompt for manual use

## Prompt Template Format

Create `.prompt.md` files in `.github/prompts/`:

```markdown
---
agent: agent
---
Act as an expert [role].

Your task is to [description].

[Instructions...]
```

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

## Project Structure

```
extension/
├── src/
│   ├── extension.ts          # Main extension entry point
│   ├── promptManager.ts      # Prompt discovery and loading
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

## Extension Settings

- `promptOrchestrator.promptsDirectory`: Directory containing prompt files
- `promptOrchestrator.autoRefresh`: Auto-refresh prompts on file changes

---

Built for BASH Consultants
