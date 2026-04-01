<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project: Prompt Orchestrator VS Code Extension

This workspace contains a VS Code extension for BASH Consultants that orchestrates AI agent workflows using structured prompts.

### Extension Overview
- **Name**: Prompt Orchestrator
- **Purpose**: Enable developers to run AI-assisted workflows using prompt files from `.github/prompts/`
- **Key Features**:
  - Discover and load prompt templates
  - Execute prompts via VS Code commands
  - Integrate with VS Code Chat API
  - Support workflow pipelines
  - Sidebar view for browsing prompts

### Development Guidelines
- Use TypeScript for all source code
- Follow VS Code extension best practices
- Implement proper error handling
- Use VS Code API for file system, commands, and chat integration
- Support YAML frontmatter in prompt markdown files

### Project Structure
```
prompt-orchestrator/
├── src/
│   ├── extension.ts          # Main extension entry point
│   ├── promptManager.ts      # Prompt discovery and loading
│   ├── commandProvider.ts    # Command registration
│   ├── chatIntegration.ts    # VS Code Chat API integration
│   ├── workflowEngine.ts     # Workflow execution
│   └── views/
│       └── promptExplorer.ts # Sidebar tree view
├── package.json              # Extension manifest
└── tsconfig.json             # TypeScript configuration
```

### Key VS Code APIs to Use
- `vscode.workspace.fs` - File system access
- `vscode.commands.registerCommand` - Command registration
- `vscode.chat.*` - Chat integration
- `vscode.window.createTreeView` - Sidebar views
- `vscode.workspace.getConfiguration` - Extension settings

---
**Status**: Setting up VS Code extension project structure
