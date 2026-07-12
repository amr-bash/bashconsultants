<!-- Workspace-specific instructions for GitHub Copilot.
     See https://code.visualstudio.com/docs/copilot/copilot-customization -->

# BASH Consultants — Copilot Instructions

## Repository Overview

Dual-purpose repository:

1. **Jekyll site** (root) — Marketing & content site for bashconsultants.com (Denver IT consulting). Uses the `jekyll-theme-zer0` remote theme. Deployed to GitHub Pages on push to `main`. CNAME: `bash-365.com`.
2. **VS Code extension** (`extension/`) — "Prompt Orchestrator" — runs AI workflows from `.github/prompts/`. TypeScript, bundled with esbuild.

Treat each sub-project independently; do not mix Jekyll and extension concerns in a single commit.

## Tech Stack

| Sub-project | Stack |
|---|---|
| Jekyll site | Ruby 3.x, Jekyll, `jekyll-theme-zer0` (remote theme), Bootstrap 5, Docker-first dev (`docker-compose up`) |
| Extension | TypeScript, VS Code Extension API, esbuild, ESLint |

## Project Structure

```
bashconsultants/
├── _config.yml, _config_dev.yml, _config.azure.yml   # Jekyll configs (dev overrides + Azure)
├── Gemfile, Gemfile.azure                            # Ruby deps
├── docker-compose.yml, Dockerfile                    # Local Jekyll dev
├── _data/, _includes/, _layouts/, _plugins/          # Jekyll theme overrides
├── pages/
│   ├── _posts/           # Blog posts (collection)
│   ├── _services/        # Service offerings
│   ├── _quests/          # Gamified learning (mirrors it-journey pattern)
│   ├── _docs/, _notes/, _quickstart/, _about/
├── assets/               # Static assets
├── scripts/              # Automation
├── extension/            # VS Code "Prompt Orchestrator" extension (self-contained)
└── .github/
    ├── FRONTMATTER.md            # Canonical .prompt.md / .instructions.md schema
    ├── copilot-instructions.md   # This file
    ├── prompts/                  # Reusable agent prompts (.prompt.md)
    └── workflows/                # GitHub Actions
```

## Essential Commands

```bash
# Jekyll site
docker-compose up                              # Start dev server (recommended)
docker-compose exec jekyll bundle exec jekyll build --config '_config.yml,_config_dev.yml'
docker-compose down

# Extension
cd extension && npm install && npm run compile
cd extension && npm run lint
cd extension && npm run watch                  # esbuild watch mode
```

## Frontmatter Standards

All `.prompt.md` and `.instructions.md` files under `.github/` must follow the canonical schema in `.github/FRONTMATTER.md`:

- `.prompt.md` → `mode: agent` + `description` + `date` + `lastmod`
- `.instructions.md` → `applyTo` + `description` + `date` + `lastmod`

Jekyll content under `pages/` follows standard Jekyll frontmatter: `title`, `description`, `date`, `categories`, `tags`, `layout`.

## Workflow Conventions

- **Direct-to-main**: No PR gate; commit and push to `main` triggers GitHub Pages deploy. Use `/commit-publish` prompt for the full review→validate→commit→push pipeline.
- **Conventional commits**: `<type>(<scope>): <subject>` where type ∈ `feat fix docs refactor chore ci` and scope ∈ `posts pages services config extension prompts docs`.
- **CHANGELOG**: Maintain `[Unreleased]` section at top of `CHANGELOG.md`.
- **Never commit**: `_site/`, `node_modules/`, `vendor/`, `Gemfile.lock` if `.gitignore`'d.

## Editorial Voice (for content under `pages/`)

- Audience: SMB owners and operators evaluating IT consulting.
- Tone: Professional, plain-language, ROI-focused; avoid jargon without definition.
- Always tie technical content back to business outcomes.
- **Identity is governed by a single source of truth:** `.github/instructions/brand.instructions.md` (name, mission, voice, doctrine, colors, logo). Read it before brand or positioning work.

## Hard Rules

- Don't restructure the Jekyll theme — it's a remote theme; override via `_includes/`, `_layouts/`, `_sass/` locally.
- Don't bump theme version in `Gemfile` without testing the build.
- Don't refactor `extension/` source unless explicitly asked.
- Don't generate or guess external URLs.

---

**Related:** `AGENTS.md` (cross-tool entry point) · `CLAUDE.md` (Claude Code entry point) · `.github/instructions/brand.instructions.md` (brand SSOT) · `.github/FRONTMATTER.md` · `.github/prompts/commit-publish.prompt.md` · `.github/instructions/` (file-scoped rules) · `.claude/README.md` (Claude-native layer)
