#!/usr/bin/env bash
# ==============================================================================
# Zer0-Mistakes Theme: Admin Settings Setup Script
# ==============================================================================
#
# Creates the admin/settings pages for any site using the zer0-mistakes theme.
# All infrastructure (layouts, includes, JS, CSS, SVGs) ships with the theme —
# this script only creates the content pages that reference them.
#
# Usage:
#   ./scripts/setup-admin-settings.sh [--force] [--dry-run]
#
# Options:
#   --force     Overwrite existing settings pages
#   --dry-run   Show what would be created without making changes
#
# Prerequisites:
#   - Site must use zer0-mistakes theme (remote_theme or gem)
#   - pages/_about/settings/ directory structure
# ==============================================================================

set -euo pipefail

# ── Configuration ─────────────────────────────────────────────────────────────

SETTINGS_DIR="pages/_about/settings"
TODAY=$(date +%Y-%m-%dT00:00:00.000Z)
FORCE=false
DRY_RUN=false

# ── Color output helpers ──────────────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1"; }

# ── Parse arguments ───────────────────────────────────────────────────────────

while [[ $# -gt 0 ]]; do
  case $1 in
    --force)   FORCE=true;   shift ;;
    --dry-run) DRY_RUN=true; shift ;;
    -h|--help)
      echo "Usage: $0 [--force] [--dry-run]"
      echo ""
      echo "Creates admin/settings content pages for zer0-mistakes theme."
      echo "  --force     Overwrite existing files"
      echo "  --dry-run   Preview changes without writing files"
      exit 0
      ;;
    *) log_error "Unknown option: $1"; exit 1 ;;
  esac
done

# ── Validation ────────────────────────────────────────────────────────────────

if [[ ! -f "_config.yml" ]]; then
  log_error "No _config.yml found. Run this script from the site root directory."
  exit 1
fi

# Check theme connection
if ! grep -qE 'remote_theme.*zer0-mistakes|theme.*jekyll-theme-zer0' _config.yml _config_dev.yml 2>/dev/null; then
  log_warn "Could not detect zer0-mistakes theme in config files. Proceeding anyway."
fi

# ── File creation helper ──────────────────────────────────────────────────────

create_page() {
  local filepath="$1"
  local content="$2"
  local description="$3"

  if [[ -f "$filepath" ]] && [[ "$FORCE" != "true" ]]; then
    log_warn "Skipping $filepath (exists; use --force to overwrite)"
    return 0
  fi

  if [[ "$DRY_RUN" == "true" ]]; then
    log_info "[DRY RUN] Would create: $filepath — $description"
    return 0
  fi

  mkdir -p "$(dirname "$filepath")"
  echo "$content" > "$filepath"
  log_success "Created $filepath — $description"
}

# ── Generate admin settings pages ─────────────────────────────────────────────

log_info "Setting up zer0-mistakes admin settings pages..."
log_info "Target directory: $SETTINGS_DIR"
echo ""

# 1. Theme Customizer
create_page "$SETTINGS_DIR/theme.md" "---
title: Theme Customizer
layout: admin
icon: bi-palette
permalink: /about/settings/theme/
excerpt: Preview theme skins, generate palettes, customize CSS variables, and export YAML configuration.
lastmod: $TODAY
---

<!-- chroma.js — color manipulation library (BSD-3, 36 KB min) -->
<script src=\"https://cdn.jsdelivr.net/npm/chroma-js@2.4.2/chroma.min.js\"></script>

<!-- Mode + Skin bar -->
<div class=\"d-flex flex-wrap align-items-center gap-3 mb-4 p-3 bg-body-tertiary rounded-3 border\">
  <div class=\"d-flex align-items-center gap-2\">
    <i class=\"bi bi-moon-stars\"></i>
    <span class=\"fw-semibold small\">Mode:</span>
    {% include components/halfmoon.html %}
  </div>
  <div class=\"vr d-none d-sm-block\"></div>
  <div class=\"d-flex align-items-center gap-2 flex-grow-1\">
    <i class=\"bi bi-palette2\"></i>
    <span class=\"fw-semibold small\">Skin:</span>
    {% assign skins_list = \"air,aqua,contrast,dark,dirt,neon,mint,plum,sunrise\" | split: \",\" %}
    {% assign active_skin = site.theme_skin | default: \"dark\" %}
    <div class=\"d-flex flex-wrap gap-1\" id=\"quickSkinBar\">
      {% for s in skins_list %}
      <button class=\"btn btn-sm {% if s == active_skin %}btn-primary{% else %}btn-outline-secondary{% endif %}\" data-quick-skin=\"{{ s }}\" title=\"{{ s | capitalize }}\">{{ s | capitalize }}</button>
      {% endfor %}
    </div>
  </div>
</div>

<ul class=\"nav nav-tabs\" id=\"themeTabs\" role=\"tablist\">
  <li class=\"nav-item\" role=\"presentation\"><button class=\"nav-link active\" id=\"tab-skins\" data-bs-toggle=\"tab\" data-bs-target=\"#pane-skins\" type=\"button\" role=\"tab\"><i class=\"bi bi-brush me-1\"></i>Skins</button></li>
  <li class=\"nav-item\" role=\"presentation\"><button class=\"nav-link\" id=\"tab-skin-editor\" data-bs-toggle=\"tab\" data-bs-target=\"#pane-skin-editor\" type=\"button\" role=\"tab\"><i class=\"bi bi-pencil-square me-1\"></i>Skin Editor</button></li>
  <li class=\"nav-item\" role=\"presentation\"><button class=\"nav-link\" id=\"tab-palette\" data-bs-toggle=\"tab\" data-bs-target=\"#pane-palette\" type=\"button\" role=\"tab\"><i class=\"bi bi-rainbow me-1\"></i>Palette Generator</button></li>
  <li class=\"nav-item\" role=\"presentation\"><button class=\"nav-link\" id=\"tab-live\" data-bs-toggle=\"tab\" data-bs-target=\"#pane-live\" type=\"button\" role=\"tab\"><i class=\"bi bi-sliders me-1\"></i>Live Preview</button></li>
  <li class=\"nav-item\" role=\"presentation\"><button class=\"nav-link\" id=\"tab-colors\" data-bs-toggle=\"tab\" data-bs-target=\"#pane-colors\" type=\"button\" role=\"tab\"><i class=\"bi bi-palette2 me-1\"></i>Color Editor</button></li>
  <li class=\"nav-item\" role=\"presentation\"><button class=\"nav-link\" id=\"tab-export\" data-bs-toggle=\"tab\" data-bs-target=\"#pane-export\" type=\"button\" role=\"tab\"><i class=\"bi bi-download me-1\"></i>Export</button></li>
</ul>

<div class=\"tab-content pt-4\" id=\"themeTabContent\">
  <div class=\"tab-pane fade show active\" id=\"pane-skins\" role=\"tabpanel\">{% include components/theme-customizer.html %}</div>
  <div class=\"tab-pane fade\" id=\"pane-skin-editor\" role=\"tabpanel\">{% include components/skin-editor-tab.html %}</div>
  <div class=\"tab-pane fade\" id=\"pane-palette\" role=\"tabpanel\">{% include components/palette-tab.html %}</div>
  <div class=\"tab-pane fade\" id=\"pane-live\" role=\"tabpanel\">{% include components/live-preview-tab.html %}</div>
  <div class=\"tab-pane fade\" id=\"pane-colors\" role=\"tabpanel\">{% include components/color-editor-tab.html %}</div>
  <div class=\"tab-pane fade\" id=\"pane-export\" role=\"tabpanel\">{% include components/export-tab.html %}</div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function () {
  if (typeof zer0Bg === 'undefined') return;
  document.querySelectorAll('#quickSkinBar [data-quick-skin]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      zer0Bg.setSkin(this.dataset.quickSkin);
      document.querySelectorAll('#quickSkinBar [data-quick-skin]').forEach(function (b) { b.classList.replace('btn-primary', 'btn-outline-secondary'); });
      this.classList.replace('btn-outline-secondary', 'btn-primary');
    });
  });
});
</script>
<script src=\"{{ '/assets/js/theme-customizer.js' | relative_url }}\" defer></script>
<script src=\"{{ '/assets/js/palette-generator.js' | relative_url }}\" defer></script>
<script src=\"{{ '/assets/js/skin-editor.js' | relative_url }}\" defer></script>" "Theme Customizer — skins, palette generator, skin editor, live preview, color editor, export"

# 2. Configuration Utility
create_page "$SETTINGS_DIR/config.md" "---
title: Configuration Utility
layout: admin
icon: bi-gear
excerpt: View, manage, and update your Jekyll theme configuration from one place.
lastmod: $TODAY
config-dir: pages/_about/settings
config-file: _config.yml
permalink: /about/config/
sidebar: false
---

{% include components/config-viewer.html %}

<script src=\"{{ '/assets/js/config-utility.js' | relative_url }}\" defer></script>" "Configuration Viewer — browse and export site config"

# 3. Navigation Editor
create_page "$SETTINGS_DIR/navigation.md" "---
title: Navigation Editor
layout: admin
icon: bi-signpost-2
permalink: /about/settings/navigation/
excerpt: View and export navigation menu structures.
lastmod: $TODAY
---

{% include components/nav-editor.html %}

<script src=\"{{ '/assets/js/nav-editor.js' | relative_url }}\" defer></script>" "Navigation Editor — view and export nav menus"

# 4. Collection Manager
create_page "$SETTINGS_DIR/collections.md" "---
title: Collection Manager
layout: admin
icon: bi-collection
permalink: /about/settings/collections/
excerpt: Overview of all Jekyll collections, their configuration, and content counts.
lastmod: $TODAY
---

{% include components/collection-manager.html %}" "Collection Manager — collections overview"

# 5. Analytics Dashboard
create_page "$SETTINGS_DIR/analytics.md" "---
title: Analytics Dashboard
layout: admin
icon: bi-graph-up
permalink: /about/settings/analytics/
excerpt: PostHog analytics configuration, privacy compliance, and tracking status.
lastmod: $TODAY
---

{% include components/analytics-dashboard.html %}" "Analytics Dashboard — PostHog and tracking settings"

# 6. Environment & Build
create_page "$SETTINGS_DIR/environment.md" "---
title: Environment & Build Info
layout: admin
icon: bi-hdd-network
permalink: /about/settings/environment/
excerpt: Jekyll environment, build details, Ruby version, theme info, and plugin list.
lastmod: $TODAY
---

{% include components/env-dashboard.html %}" "Environment & Build — Jekyll, Ruby, and build info"

# ── Copy _config.yml for Raw YAML display ─────────────────────────────────────

if [[ -f "_config.yml" ]]; then
  if [[ "$DRY_RUN" == "true" ]]; then
    log_info "[DRY RUN] Would copy _config.yml → $SETTINGS_DIR/_config.yml"
  else
    cp _config.yml "$SETTINGS_DIR/_config.yml"
    log_success "Copied _config.yml → $SETTINGS_DIR/_config.yml (for Raw YAML tab)"
  fi
fi

# ── Summary ───────────────────────────────────────────────────────────────────

echo ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "Admin settings setup complete!"
echo ""
log_info "Pages created in: $SETTINGS_DIR/"
log_info "  • /about/settings/theme/        — Theme Customizer"
log_info "  • /about/config/                — Configuration Utility"
log_info "  • /about/settings/navigation/   — Navigation Editor"
log_info "  • /about/settings/collections/  — Collection Manager"
log_info "  • /about/settings/analytics/    — Analytics Dashboard"
log_info "  • /about/settings/environment/  — Environment & Build"
echo ""
log_info "All UI components, JS, CSS, and SVG assets are provided by the theme."
log_info "No additional dependencies required."
echo ""
log_info "Next steps:"
log_info "  1. Verify theme_skin is set in _config.yml (e.g., theme_skin: \"dark\")"
log_info "  2. Rebuild: docker-compose up  (or bundle exec jekyll serve)"
log_info "  3. Visit: http://localhost:PORT/about/settings/theme/"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
