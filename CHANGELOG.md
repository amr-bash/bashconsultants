# Change Log

All notable changes to the BASH Consultants repository will be documented in this file.

Check [Keep a Changelog](http://keepachangelog.com/) for recommendations on how to structure this file.

## [1.1.0] - 2026-01-24

### Changed
- **Navigation Data Structure** (`_data/navigation/`): Updated to zer0-mistakes theme v0.17+ format
  - Migrated from `sublinks` to `children` property for nested navigation items
  - Added Bootstrap Icons (`bi-*` prefix) to all navigation items
  - Added consistent Home links to sidebar navigation files
  - Added trailing slashes to all URLs for consistency

### Added
- **New Navigation Files** (`_data/navigation/`)
  - `home.yml` - Homepage quick navigation with icons
  - `services.yml` - Services sidebar navigation
  - `README.md` - Navigation schema documentation with migration guide

### Fixed
- Fixed HTML entity `&amp;` in about.yml to proper `&` character
- Fixed inconsistent URL trailing slashes across navigation files

## [1.0.0] - 2026-01-24

### Added
- **Prompt Orchestrator VS Code Extension** (`extension/`): New VS Code extension for orchestrating AI agent workflows using structured prompts
  - Discovers and loads prompt templates from `.github/prompts/` directory
  - Execute prompts via Command Palette or sidebar tree view
  - Integration with VS Code Chat API and Language Model API
  - Commands: refreshPrompts, executePrompt, review, refactor, test, docs, debug
  - Configuration settings for prompts directory and auto-refresh
  
- **Prompt Engineering Toolkit** (`.github/prompts/`)
  - `docs.prompt.md` - Technical documentation generation
  - Additional prompts for requirements analysis, system design, code implementation, test generation, code refactoring, and debugging

- **Automation Scripts** (`scripts/`)
  - `routine-maintenance.sh` - Prepare prompt workflows for VS Code Chat
  - `demo-docs-generation.js` - Demonstrate documentation prompt generation
  - `test-docs-prompt.js` - Standalone test script for prompt loading
  - `vscode-integration.sh` - VS Code CLI integration helper

- **Blog Posts** (`pages/_posts/`)
  - "Prompts: The New Command Line" - Exploring the paradigm shift in development
  - "From Prompts to Pipelines: Agentic Workflows in VS Code" - Extension design and agentic workflows

### Changed
- **Repository Structure**: Reorganized to separate Jekyll website from VS Code extension
  - Jekyll site configs remain at root level
  - Extension code moved to dedicated `extension/` directory
  - Updated `.gitignore` for new structure
  
- **VS Code Workspace Configuration** (`.vscode/`)
  - Updated `launch.json` for Jekyll-focused development
  - Updated `tasks.json` for Jekyll build tasks
  - Updated `settings.json` for Liquid/Jekyll file associations
  - Updated `extensions.json` with Jekyll-relevant recommendations

- **Root `package.json`**: Clean Jekyll-only build configuration for Azure Static Web Apps

- **README.md**: Added Tools and Resources section documenting prompt engineering toolkit

### Removed
- Extension files from root directory (moved to `extension/`)
  - `tsconfig.json`, `esbuild.js`, `eslint.config.mjs` (now in `extension/`)
  - `src/`, `out/`, `dist/` directories (now in `extension/`)
  - `.vscode-test.mjs`, `.vscodeignore`, `vsc-extension-quickstart.md`, `EXTENSION-README.md`