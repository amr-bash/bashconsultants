# Change Log

All notable changes to the BASH Consultants repository will be documented in this file.

Check [Keep a Changelog](http://keepachangelog.com/) for recommendations on how to structure this file.

## [Unreleased]

Platform transformation: activated the site's dormant AI capabilities, wired the dead conversion paths, added CI quality gates, and expanded the content and services catalog.

### Added
- **Native Claude context framework** — turned the repo's AI tooling into a first-class Claude Code framework and made the repository its own reference implementation of the governed-AI model the site sells. Added a root `CLAUDE.md` (the canonical Claude entry point, routing into the existing `AGENTS.md`/instructions/prompts plus the operating rules) and `.claude/README.md` (the map of the layer). Codified the brand as a single source of truth (`.github/instructions/brand.instructions.md` — name/etymology, mission, voice, doctrine, colors, logo). Added four **skills** (`.claude/skills/{content-editorial,toolkit-doc,wikilinks,brand}`), two **subagents** (`.claude/agents/{jekyll-build-validator,brand-guardian}`), and three **commands** (`.claude/commands/{lint-content,new-toolkit-doc,brand-check}`) — the agents the practice describes at `/ai-operations/` now exist as files. Documented the whole pattern on-site as a partner-track guide, `pages/_toolkit/claude-context-framework.md` (`/tools/partners/claude-context-framework/`), with a mermaid architecture diagram.
- **The BASH toolkit collection** — turned the single `/tools/` page into a two-track docs/training library (`toolkit` collection under `pages/_toolkit/`, served at `/tools/business/…` and `/tools/partners/…`). The **business track** is 10 plain-English DIY guides for SMB owners (IT foundations, adopting AI, cloud migration, outgrowing QuickBooks, faster close, dashboards, integrations, IT roadmap, security baseline, backups); the **partner track** is 10 advanced technical references for consultants (engagement method, deterministic-first doctrine, AI-native practice, production AI/RAG, cloud landing zones, ERP architecture, record-to-report, modern data stack, integration architecture, security architecture), several with mermaid architecture diagrams. Data-driven hub + track landings, a `toolkit` sidebar nav, and a "Toolkit" top-nav dropdown; the old internal-tooling content moved into the partner-track "Running an AI-native consulting practice" doc. Cross-linked with Obsidian wiki-links; every doc cites a verified-live primary source.
- **Two new service pages** — `pages/_services/ai.md` (`/services/ai/`) and `pages/_services/managed-it.md` (`/services/managed-it/`), completing the eight-service catalog; the flagship AI offering previously existed only as a hub section with the landing card mis-linked to `/services/dev/`.
- **Case studies collection** — `pages/_case_studies/` (six anonymized engagement snapshots + index), registered in `_config.yml`, surfaced in the landing proof band.
- **`/tools/` and `/ai-operations/`** — root pages presenting the firm's own AI toolchain (prompt playbook, VS Code orchestrator, image pipeline, governance stack) as client-relevant proof, with `_data/playbook.yml` auto-generated from the prompt/instruction files by `scripts/generate_playbook_data.py`.
- **Four pillar posts** (2026-07-06) — an SMB AI acceptable-use policy, cyber-insurance renewal questions, MCP for the back office, and the AI audit trail for finance; plus the promoted `bashos` post from `drafts/`.
- **AI chat proxy** — `api/` Azure Functions app implementing the theme's chat-proxy contract (server-held Anthropic key, model pinned server-side, per-IP rate limiting keyed on the trusted proxy hop, body-size and token caps); `staticwebapp.config.json` pins the managed-functions runtime to Node 20.
- **CI and automation** — `.github/workflows/build-validate.yml` (builds both production stacks + content lint on every push/PR), `site-health.yml` (nightly), and `content-gardener.yml` (weekly draft PRs); `scripts/content_lint.py` mechanically enforces the editorial contract.
- **AI-search layer** — `/llms.txt`, site-wide + per-type JSON-LD (Article/Service) in `_includes/structured-data.html`, and a wired `/search/` page over `search.json`.
- **`_data/taxonomy.yml`**, `docs/preview-images.md`, `docs/automation.md`, and `.devcontainer/` — codified the section voice profiles, preview-image and automation runbooks, and a container dev environment.

### Changed
- **Founder page redesigned** (`/about/amr/`) — added a designed profile hero (avatar, identity, social links, consultation call-to-action), a stat band mixing career numbers with live GitHub stats for `@bamr87` (30 repos, 19 stars, 17 followers, coding in public since 2015), a row of open-source project cards (it-journey, zer0-mistakes — the theme this site runs on — bamr87.github.io, aieo), and technical-skills and strengths as badge groups; the full CV detail is preserved. The GitHub stats are deterministic-first: real static values render without JavaScript and a small client-side script only ever *updates* them from the GitHub API, never blanks them. Accent color uses the UI blue per the brand palette — the `brand-guardian` agent caught an initial use of logo-teal as the UI accent, which the brand SSOT forbids.
- **Registered the Claude layer and standardized the brand name** — `AGENTS.md` and `.github/copilot-instructions.md` now point to `CLAUDE.md`, the brand SSOT, and the `.claude/` primitives; the file-scoped instruction map routes brand-bearing files to `brand.instructions.md`. Aligned the `BASH` expansion to the canonical **Bourne Again Solutions Hero** (the form that actually spells the acronym) in `llms.txt`, matching `README.md`.
- **Landing page** rebuilt as data-driven sections (`_layouts/landing.html` + `index.md` frontmatter + `_data/entity/*.yml`): hero, eight service cards, six industry pain-point cards, process, an "AI-augmented practice" section, proof band, and FAQ; removed the Thrasymachus epigraph.
- **Hero particle background fixed** — the `#particles-js` element was a Bootstrap `.container` (capped at 1140px, centered), so the particle canvas rendered as a bounded box; it now fills the hero edge-to-edge with the content layered above.
- **Obsidian wiki-links** — internal cross-references across service, post, and case-study pages now use pipeless `[[Page Title]]` wiki-links (Obsidian-native, vault-portable), resolved to real links by the theme's client-side resolver over `wiki-index.json`. Pipeless is required: the server-side plugin can't run under GitHub Pages safe mode, and kramdown mangles the `|` of aliased wiki-links into broken tables. Root-page and CTA links (`/tools/`, `/ai-operations/`, `/contact/`) stay markdown.
- **`powered_by` refreshed** — corrected to the real toolchain (Ruby 3.3, Jekyll 3.10, zer0-mistakes 1.26.0, Bootstrap 5.3.3, Claude, OpenAI gpt-image, Python 3.13, Docker, GitHub Pages/Actions, Azure Static Web Apps); dropped the removed Algolia and the stale HTML/CSS/JS/jQuery filler.
- **Conversion forms wired** — the contact and newsletter forms now POST to config-driven endpoints (`site.forms.*`) with graceful `mailto:` fallbacks; previously both had no handler.
- **Theme pinned** — `remote_theme` pinned to `bamr87/zer0-mistakes@v1.26.0` and `Gemfile.azure` raised to the matching `~> 1.26.0` (with `jekyll-include-cache`); a registered `aqua` skin replaces the invalid `dark` value; `theme_color` hex values quoted so they stop parsing as null.
- **Editorial debt burn-down** — sentence-cased service-page titles, removed unbacked "robust/seamless/scalable", stripped trailing periods from service descriptions, retitled the ERP section off its self-labeling name, and realigned `article-review.prompt.md` and the reviewer agent to the house rules they enforce.
- **`content_statistics_generator.rb`** made Jekyll-3/4 compatible (Azure stack was crashing on `Theme#root_dir`).

### Removed
- **Stale artifacts** — the drifted `scripts/lib/preview_generator.py`, clipboard-era `scripts/{vscode-integration.sh,demo-docs-generation.js,test-docs-prompt.js}`, the broken `Rakefile`, and the stale Algolia config block; rewrote the root `README.md` from stale marketing copy (wrong `bash-365.com` contact, 3-of-8 services) into a repo-facing developer doc.

## [1.5.0] - 2026-06-21

### Added
- **`pages/_posts/muses/2025-01-24-bash-consulting-breaking.md`** — New satirical press-release post ("If a press release about ethical capitalism wrote itself") covering ESG accounting for Denver SMBs; includes a straight practical section on what's buildable on QuickBooks today.
- **`.github/prompts/article-write.prompt.md`** — New `/article-write` agent prompt for drafting new bashconsultants.com posts end-to-end.

### Changed
- **`pages/_posts/muses/2025-08-12-innovation-paradox.md`** — Frontmatter updated (author, description, keywords, lastmod, tags normalized); content rewritten for voice and SMB focus.
- **`pages/_posts/tech/2025-08-12-ai-integration-reality.md`** — Frontmatter updated; content rewritten with honest SMB-first framing on AI implementation.
- **`pages/_posts/tech/2025-11-19-prompts-are-the-new-command-line.md`** — Frontmatter normalized (author, lastmod, categories/tags as YAML lists); content already updated to SMB voice.
- **Site-wide content review** — Rewrote `about.md`, `contact.md`, and all service pages (`pages/_services/{cloud,erp,data,dev,fintech,strat}.md`) to comply with `content-style.instructions.md`: removed banned marketing phrases, switched to sentence-case headings and the 8-section service-page structure, defined acronyms on first use, and added inline images with descriptive alt text.
- **`pages/_services/index.md`** — Rebuilt as a card-based hub linking to all six real service pages (it previously listed generic categories that did not match the site's actual services).
- **`_data/entity/info.yml`** — Cleaned banned phrases from the About / Founder / Mission copy that feeds the landing page.
- **Blog posts** — Added a next-step call-to-action to posts that lacked one; normalized `preview:` paths to the `/assets/images/previews/` convention; bumped `lastmod` on edited posts.
- **All 11 blog posts (`pages/_posts/{corp,erp,muses,tech}/*.md`)** — Full editorial pass aligning every post to `content-style.instructions.md` and `posts.instructions.md`: heavy rewrite to the business-outcome-first voice, acronyms defined on first use, banned marketing phrases removed, sentence-case headings, and a single next-step CTA plus one outbound primary-source link in every post. Tightened titles to sentence case ≤ 60 chars and `description` to 120–155 chars.
- **Creative voice — show, don't announce** — Removed raw genre/device labels ("satire", "parody", "reality show", "Broadway-style musical number", "exposé") from reader-facing text so each post *enacts* its device (the press release, the show conceit, the song, the Frankenstein metaphor) instead of narrating it.
- **`pages/_posts/tech/2025-08-12-ai-integration-reality.md`** — Published the post (was `draft: true` with duplicated `author`/`description` keys); kept the stronger "AI for small business: what the pilots don't tell you" version and rewrote the body as an SMB-first AI-adoption guide.
- **Post frontmatter normalized site-wide** — `author: "Amr Abdel-Motaleb"` everywhere (replacing "BASH Consulting Team" / "bamr87"); lowercase `categories`; flow-style `tags` / `keywords` lists; duplicate keys removed; `lastmod` set to 2026-06-21.
- **Preview images** — Regenerated 9 AI preview banners (`gpt-image-2`, retro pixel-art) to match the rewritten titles and content; standardized all post `preview:` paths to the `/images/previews/<slug>.png` short form (auto-normalized by the theme).

### Removed
- **`pages/_posts/tech/2025-01-24-bash-consulting-breaking.md`** — Deleted from `tech/`; replaced by the muses rewrite above.
- **Invented case studies and unverifiable metrics** — Removed fabricated results ("40% cost reduction", "99.9% uptime", "300% revenue increase", "30+ ERP projects", "over 15 years") and overreaching capability claims (e.g., AI/ML clinical decision support, fraud detection) from the service pages, per the "never invent customer wins" rule.

### Fixed
- **Broken images** — Renamed `assets/images/red-rocks.JPG` → `red-rocks.jpg` so the lowercase reference resolves on case-sensitive production builds; repointed the missing `office-594119.png` `og_image` to `office.jpg` in `_config.yml` and `pages/_about/site/_config.yml`; repointed the missing `bamr-avatar.png` avatar to `Amr-Headshot_v2.jpg`.
- **Contact-info consistency** — Standardized all customer pages to `bashconsultants.com` / `info@bashconsultants.com` / `(720) 352-4641`; replaced the stale `bash-365.com` details on `about.md` and `contact.md`; fixed the `contact-email: info@consultants.com` typo in `_config.yml` that broke the landing page's "Email Now" button.

---

### Added
- **`.github/instructions/`** — Six file-scoped instruction files for AI agents:
  - `content-style.instructions.md` (applyTo `pages/**`, `index.md`, `about.md`, `contact.md`) — shared editorial voice, audience profile (Denver SMBs 5–200 employees), target-industry table, banned phrases, SEO + accessibility rules
  - `posts.instructions.md` (applyTo `pages/_posts/**/*.md`) — blog post structure + subfolder routing (corp/erp/muses/tech)
  - `services.instructions.md` (applyTo `pages/_services/**/*.md`) — service-page conversion structure + industry-fit naming
  - `jekyll-theme.instructions.md` (applyTo theme override paths) — local override rules for the remote theme
  - `extension.instructions.md` (applyTo `extension/**`) — VS Code Prompt Orchestrator dev rules
  - `prompts.instructions.md` (applyTo `.github/{prompts,instructions}/**`) — schema + slash-hard body style
- **AGENTS.md** — Cross-tool entry point for AI coding agents (Copilot, Codex, Cursor, Aider, Claude Code). Points to canonical guidance.
- **`.github/prompts/commit-publish.prompt.md`** — Standard commit + push + deploy workflow for the direct-to-main publishing model.
- **Canonical frontmatter reference** — `.github/FRONTMATTER.md` documents the required schema for `.prompt.md` and `.instructions.md` files.

### Changed
- **`.github/copilot-instructions.md`** — Rewritten to reflect the actual dual-purpose repo (Jekyll site + `extension/` sub-project). Previous content described only the extension and was stale.
- **`.github/prompts/` frontmatter normalized** — All `.prompt.md` files updated to canonical `mode: agent` + `description` + `date` + `lastmod` schema. Body content already concise (≤100 lines per file); no further compression needed.

### Removed
- **`.github/prompts/docs.prompt.md`** — superseded by `documentation.prompt.md`.

## [1.4.0] - 2026-04-06

### Changed
- **Theme Upgrade**: Updated zer0-mistakes theme from v0.21.6 to v0.22.10
  - `Gemfile.azure`: Updated `jekyll-theme-zer0` from `~> 0.21.2` to `~> 0.22.10`
  - `pages/_about/site/_config.yml`: Updated `remote_theme` pin from `v0.21.6` to `v0.22.10`
  - `_data/README.md` and `_data/navigation/README.md`: Updated version references to v0.22+
  - Notable theme changes since v0.21.6:
    - Admin layout and configuration dashboards (v0.22.10)
    - Cross-platform installation compatibility fixes (v0.22.8)
    - Hero layout and scroll animation stabilization (v0.22.3)
    - Various documentation and CI improvements

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
  - Synced `pages/_about/site/_config.yml` remote_theme pin and post layout default

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