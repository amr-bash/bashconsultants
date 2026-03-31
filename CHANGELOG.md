# Change Log

All notable changes to the BASH Consultants repository will be documented in this file.

Check [Keep a Changelog](http://keepachangelog.com/) for recommendations on how to structure this file.

## [1.3.0] - 2026-03-31

### Changed
- **Theme Upgrade**: Updated zer0-mistakes theme from v0.18.0 to v0.21.6
  - `Gemfile`: Updated `jekyll-theme-zer0` from `~> 0.18.0` to `~> 0.21.2` (latest on RubyGems)
  - `Gemfile.azure`: Added version pin `~> 0.21.2`
  - `_config.yml`: Pinned `remote_theme` to `bamr87/zer0-mistakes@v0.21.6`

- **Layout Standardization**: Aligned post and section layouts with theme v0.20.3+ conventions
  - Changed default post layout from `journals` to `article` in `_config.yml` defaults
  - Updated 9 posts with explicit `layout: journals` or `layout: blog` to `layout: article`
  - Updated 6 category/index pages to use `layout: default` (theme's `section` layout uses `/news/` URLs)
  - Renamed category pages with date prefixes for proper Jekyll `_posts` processing

- **New Features Enabled**:
  - Added `search.json` for GitHub Pages compatible search (theme v0.20.2 feature)
  - Added `mermaid` diagram configuration for client-side rendering
  - Added `jekyll-include-cache` plugin for improved build performance
  - Updated vendor exclusion paths to support `assets/vendor/` publishing

- **Configuration Updates**:
  - Updated Bootstrap version reference from 5.2.0 to 5.3.3 in `powered_by`
  - Updated version references in `_data/README.md` and `_data/navigation/README.md` to v0.21+
  - Synced `pages/_about/site/_config.yml` with main config changes

### Fixed
- **404 Page**: Fixed broken `/blog` navigation link to use correct `/posts` path
- **Navigation**: Removed broken links to non-existent pages (`/docs/`, `/about/org/`, `/about/portfolio/`)
- **Navigation**: Fixed `/home/` links to `/` across navigation data files
- **Blog Index**: Fixed hardcoded post URLs using slug format to use date-based format
- **Category Pages**: Added missing `permalink` to muses category page

## [1.2.0] - 2026-01-24

### Changed
- **Development Port Standardization**: Updated all development ports from 4002 to 4042 for consistency
  - `Dockerfile`: Changed EXPOSE and CMD to use port 4042
  - `docker-compose.yml`: Updated port mapping to 4042:4042
  - `.vscode/tasks.json`: Updated Jekyll local serve port to 4042
  - `.vscode/launch.json`: Updated all debug configuration URLs to localhost:4042

- **VS Code Development Environment**: Complete overhaul of development configurations
  - `.vscode/launch.json`: Added 6 new debug configurations:
    - 🐳 Debug BASH Consultants (Docker) - Primary Docker debugging
    - 🔗 Attach to Running Jekyll (Docker) - Attach to running container
    - 🔄 Docker Rebuild & Debug - Force rebuild with debugging
    - 🖥️ Debug BASH Consultants (Local) - Local development debugging
    - 📱 Mobile Debug (Docker) - Mobile responsive testing
    - 🎯 Performance Debug (Docker) - Performance profiling
  - `.vscode/tasks.json`: Added 12 comprehensive tasks:
    - Docker operations (up, stop, down, rebuild, logs)
    - Jekyll serve/build (Docker and Local)
    - Maintenance tasks (clean up, update dependencies)

- **Theme Version**: Updated jekyll-theme-zer0 to v0.18.0
  - `Gemfile`: Updated gem version constraint to `~> 0.18.0`
  - `_config.yml`: Simplified remote_theme to `bamr87/zer0-mistakes` (uses latest)

- **Gemfile Cleanup**: Simplified dependencies
  - Removed redundant jekyll_plugins group (already included in github-pages gem)
  - Removed pinned versions for ffi and webrick (use latest compatible)
  - Removed commonmarker pin (resolved upstream)

### Added
- **`.gitignore`**: Added `logs/` directory for debug trace logs

### Fixed
- **Dockerfile**: Added newline at end of file

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