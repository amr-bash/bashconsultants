# Preview image pipeline

How the AI-generated banner images for posts and section pages work, and the rules that keep frontmatter, filenames, and the generator in sync.

## The facts

| Item | Value |
|---|---|
| Generator | `scripts/features/generate-preview-images` (wrapper: `scripts/generate-preview-images.sh`) |
| Jekyll integration | `_plugins/preview_image_generator.rb` (Liquid tags, path normalization, missing-preview detection) |
| Provider / model | OpenAI `gpt-image-2` (configured in the `preview_images` block of `_config.yml`; DALL-E 3 is retired on this account) |
| Size / quality | `1536x1024` landscape, `high` |
| Style | Retro pixel art, 8-bit video game aesthetic — the `style` and `style_modifiers` keys in `_config.yml` are the single source of truth for the look |
| Output directory | `assets/images/previews/` |
| API key | `OPENAI_API_KEY`, loaded from `.env` at the repo root (never committed) |
| Cost | Roughly $0.15–0.20 per image at current pricing — cheap for one post, real money for a `--force` run across the whole site |

## Filename rule

The image filename is derived from the post's `title:`, not its file path:

1. Lowercase the title.
2. Replace every run of non-alphanumeric characters with a single `-`.
3. Strip leading and trailing `-`.
4. Truncate to 50 characters (a trailing `-` left by truncation is kept).

Example: `"bashos: the new command-line operating system"` → `bashos-the-new-command-line-operating-system.png`.

Because the filename comes from the title, **changing a title orphans its image**. Regenerate previews only after titles are final, and if you retitle a published piece, regenerate (or rename) its preview in the same change.

## Frontmatter path rule

Use the short form in frontmatter:

```yaml
preview: /images/previews/<slug>.png
```

The build auto-prefixes `/assets` (the `assets_prefix` / `auto_prefix` keys in `_config.yml`), so `/images/previews/foo.png` resolves to `assets/images/previews/foo.png`. Do not write `/assets/images/previews/...` in frontmatter — both work at render time, but the short form is the house convention and what the generator writes back.

## Running the generator

```bash
# See what's missing without spending anything
./scripts/generate-preview-images.sh --dry-run
./scripts/generate-preview-images.sh --list-missing

# Generate for everything that lacks a preview
./scripts/generate-preview-images.sh --collection posts

# Regenerate one post's image after a title change
./scripts/generate-preview-images.sh --force --file pages/_posts/tech/2026-07-06-my-post.md
```

`--force` regenerates even when an image already exists — pair it with `--file` for a single post rather than running it site-wide.

## House rule: the final review pass

The last polish pass over any content batch is always run by the strongest available model at the top level (currently Opus-class) — not delegated to a subagent. That pass confirms titles are final *before* previews are generated, and checks that no reader-facing text names a piece's creative device. Order of operations: write → review → finalize titles → generate previews.
