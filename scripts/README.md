# Git setup helper

This repository includes a small, safe helper to set up your global Git configuration.

Files added:
- `.gitconfig.example` — template you can copy or inspect.
- `scripts/setup-git.sh` — a script that shows the commands it would run (dry-run) and can apply them with `--apply`.

Quick usage:

Dry-run (shows what would be changed):

```bash
bash scripts/setup-git.sh --name "Your Name" --email you@example.com
```

Apply changes:

```bash
bash scripts/setup-git.sh --apply --name "Your Name" --email you@example.com
```

Notes:
- The script defaults to `core.editor = code --wait` if you have VS Code installed.
- It sets `credential.helper=osxkeychain` (macOS recommended).
- It will not automatically generate SSH keys; instructions are included in the script output.

Using the GitHub CLI (recommended)

- If you have `gh` installed and authenticated (`gh auth login`), this repo includes a simpler `gh`-backed helper: `scripts/setup-git-gh.sh`.
- `scripts/setup-git-gh.sh` uses `gh auth setup-git` to wire Git to your GitHub credentials and can upload an SSH key with `gh ssh-key add`.

Dry-run (gh script):

```bash
bash scripts/setup-git-gh.sh --name "Your Name" --email you@example.com
```

Apply (gh script):

```bash
bash scripts/setup-git-gh.sh --apply --name "Your Name" --email you@example.com --ssh
```

Notes:
- `scripts/setup-git-gh.sh` defaults to dry-run. Use `--apply` to actually change your global config.
- When you run with `--ssh` the script will generate an `ed25519` key (if missing), add it to the ssh-agent, and upload the public key to GitHub using `gh ssh-key add`.

If you'd like, I can make the `gh` script interactive (prompting for missing values), or replace the original `scripts/setup-git.sh` entirely. Tell me which option you prefer.
