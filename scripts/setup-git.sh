#!/usr/bin/env bash
# Interactive Git setup helper (single script)
# - Interactive when run with no args
# - Supports non-interactive flags for automation
# - Dry-run by default; use --apply to actually make changes

set -euo pipefail

SCRIPT_NAME=$(basename "$0")
DRY_RUN=1
NAME=""
EMAIL=""
EDITOR=""
USE_GH=0
DO_SSH=0

usage(){
  cat <<EOF
Usage: $SCRIPT_NAME [--apply] [--name "Your Name"] [--email "you@example.com"] [--editor "code --wait"] [--gh] [--ssh]
  --apply    : actually apply changes (default: dry-run)
  --name     : git user.name
  --email    : git user.email
  --editor   : core.editor
  --gh       : use GitHub CLI where available (run gh auth setup-git)
  --ssh      : generate SSH key and upload via gh (if gh used)
  --help     : show this message
Run without options to enter interactive mode.
EOF
}

# parse args (non-interactive)
if [[ $# -gt 0 ]]; then
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --apply) DRY_RUN=0; shift;;
      --name) NAME="$2"; shift 2;;
      --email) EMAIL="$2"; shift 2;;
      --editor) EDITOR="$2"; shift 2;;
      --gh) USE_GH=1; shift;;
      --ssh) DO_SSH=1; shift;;
      --help) usage; exit 0;;
      *) echo "Unknown arg: $1"; usage; exit 1;;
    esac
  done
else
  # Interactive prompts
  read -r -p "Git user.name (leave blank to skip): " NAME
  read -r -p "Git user.email (leave blank to skip): " EMAIL
  read -r -p "Preferred editor (default: code --wait): " EDITOR
  if [[ -z "$EDITOR" ]]; then EDITOR="code --wait"; fi
  if command -v gh >/dev/null 2>&1; then
    read -r -p "Use GitHub CLI for credential setup and SSH upload? (y/N): " ghans
    case "$ghans" in
      [Yy]*) USE_GH=1;;
      *) USE_GH=0;;
    esac
  fi
  read -r -p "Generate SSH key and upload to GitHub? (y/N): " sshans
  case "$sshans" in
    [Yy]*) DO_SSH=1;;
    *) DO_SSH=0;;
  esac
  read -r -p "Apply changes now? (y/N): " applyans
  case "$applyans" in
    [Yy]*) DRY_RUN=0;;
    *) DRY_RUN=1;;
  esac
fi

if ! command -v git >/dev/null 2>&1; then
  echo "git not found. Install git first." >&2
  exit 2
fi

echo "Git version: $(git --version)"

if [[ $USE_GH -eq 1 ]]; then
  if ! command -v gh >/dev/null 2>&1; then
    echo "gh not found; continuing without gh." >&2
    USE_GH=0
  else
    echo "gh version: $(gh --version | head -n1)"
  fi
fi

# get existing values if not provided
NAME=${NAME:-$(git config --global --get user.name || true)}
EMAIL=${EMAIL:-$(git config --global --get user.email || true)}
EDITOR=${EDITOR:-$(git config --global --get core.editor || echo "code --wait")}

echo
echo "Planned changes:"
echo "  user.name  = ${NAME:-<not set>}"
echo "  user.email = ${EMAIL:-<not set>}"
echo "  core.editor= ${EDITOR}"
if [[ $USE_GH -eq 1 ]]; then
  echo "  use gh to setup credentials"
fi
if [[ $DO_SSH -eq 1 ]]; then
  echo "  generate SSH key and upload to GitHub (if gh available)"
fi

apply_cmd(){
  local cmd="$*"
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "DRY-RUN: $cmd"
    return 0
  else
    echo "+ $cmd"
    eval "$cmd"
  fi
}

# Apply git configuration
if [[ -n "$NAME" ]]; then
  apply_cmd "git config --global user.name \"${NAME}\""
fi
if [[ -n "$EMAIL" ]]; then
  apply_cmd "git config --global user.email \"${EMAIL}\""
fi
apply_cmd "git config --global core.editor \"${EDITOR}\""
apply_cmd "git config --global init.defaultBranch main"
apply_cmd "git config --global color.ui auto"
apply_cmd "git config --global alias.st status"
apply_cmd "git config --global alias.co checkout"
apply_cmd "git config --global alias.br branch"
apply_cmd "git config --global alias.cm commit"
apply_cmd "git config --global alias.lg 'log --oneline --graph --decorate --all'"

if [[ $USE_GH -eq 1 ]]; then
  apply_cmd gh auth setup-git
else
  # on macOS, prefer osxkeychain
  if [[ "$OSTYPE" == "darwin"* ]]; then
    apply_cmd git config --global credential.helper osxkeychain
  fi
fi

if [[ $DO_SSH -eq 1 ]]; then
  KEY_PATH="$HOME/.ssh/id_ed25519"
  if [[ -f "$KEY_PATH" ]]; then
    echo "Found existing key at $KEY_PATH"
  else
    apply_cmd "ssh-keygen -t ed25519 -C \"${EMAIL}\" -f \"$KEY_PATH\" -N \"\""
  fi
  apply_cmd "eval \"\$(ssh-agent -s)\""
  if apply_cmd "ssh-add --apple-use-keychain \"$KEY_PATH\""; then
    :
  else
    apply_cmd "ssh-add \"$KEY_PATH\""
  fi
  if [[ $USE_GH -eq 1 ]]; then
    apply_cmd "gh ssh-key add \"$KEY_PATH.pub\" --title \"$(hostname)-$(date +%F)\""
  else
    echo "Public key at $KEY_PATH.pub — add it to your git host manually."
  fi
  apply_cmd "echo 'Test: ssh -T git@github.com'"
fi

echo
if [[ $DRY_RUN -eq 1 ]]; then
  echo "Dry-run complete. Re-run with --apply or choose Apply when prompted to make changes." 
else
  echo "Done. Current global git config:"
  git config --global --list
fi
