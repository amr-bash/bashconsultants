# Navigation Data Schema Documentation

This directory contains YAML navigation data files used by the sidebar and navbar components. All files follow a standardized schema compatible with the **zer0-mistakes theme v0.17+**.

## Schema Definition

Each navigation item can have the following properties:

```yaml
- title: string        # Required - Display text
  url: string          # Optional - Link URL (relative to site root)
  icon: string         # Optional - Bootstrap Icons class (e.g., "bi-folder", "bi-house")
  description: string  # Optional - Tooltip or description text
  expanded: boolean    # Optional - Default expanded state (default: false)
  children: array      # Optional - Nested navigation items (max 2 levels deep)
```

### Property Details

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `title` | string | Yes | Display text for the navigation item |
| `url` | string | No | Link URL (relative to site root) |
| `icon` | string | No | Bootstrap Icons class with `bi-` prefix |
| `description` | string | No | Tooltip or additional description |
| `expanded` | boolean | No | Whether children are expanded by default |
| `children` | array | No | Nested navigation items (max 2 levels) |

## Navigation Modes

The sidebar supports three navigation modes set via `page.sidebar.nav`:

1. **auto** - Auto-generates from collection documents
2. **tree** - Uses YAML data from this directory (specify file name)
3. **categories** - Groups by Jekyll categories

## Available Files

| File | Purpose | Description |
|------|---------|-------------|
| `main.yml` | Primary site navigation | Navbar dropdowns and main menu |
| `docs.yml` | Documentation section | Sidebar for /docs/ pages |
| `about.yml` | About section | Sidebar for /about/ pages |
| `home.yml` | Homepage quick links | Icon-based quick navigation |
| `posts.yml` | Blog categories | Category navigation for posts |
| `services.yml` | Services section | Sidebar for /services/ pages |

## Example Usage

### In Page Front Matter

```yaml
---
title: My Documentation Page
sidebar:
  nav: docs  # Uses _data/navigation/docs.yml
---
```

### Navigation File Example

```yaml
# _data/navigation/docs.yml
- title: Getting Started
  url: /docs/getting-started/
  icon: bi-rocket-takeoff
  expanded: true
  children:
    - title: Installation
      url: /docs/installation/
      icon: bi-download
    - title: Configuration
      url: /docs/configuration/
      icon: bi-gear
- title: API Reference
  url: /docs/api/
  icon: bi-code-slash
```

## Bootstrap Icons Reference

Common icons used in navigation:

| Icon | Class | Purpose |
|------|-------|---------|
| 🏠 | `bi-house` | Home links |
| 📖 | `bi-book` | Documentation |
| 📝 | `bi-journal-text` | Blog/Posts |
| ⚙️ | `bi-gear` | Settings/Config |
| 💼 | `bi-briefcase` | Services/Business |
| 📊 | `bi-bar-chart-line` | Analytics/Data |
| 💻 | `bi-code-slash` | Code/Development |
| ☁️ | `bi-cloud` | Cloud services |
| ℹ️ | `bi-info-circle` | About/Info |
| ✉️ | `bi-envelope` | Contact |

Browse all icons at: https://icons.getbootstrap.com/

## Migration from Legacy Format

If migrating from older navigation files:

| Old Property | New Property |
|--------------|--------------|
| `sublinks` | `children` |
| `icon: globe` | `icon: bi-globe` |
| `icon: home` | `icon: bi-house` |
| `icon: cash` | `icon: bi-currency-dollar` |

All icons now require the `bi-` prefix for Bootstrap Icons compatibility.
