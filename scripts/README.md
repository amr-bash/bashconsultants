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
# Routine Maintenance Script

This script automates the preparation of prompt workflows for VS Code Chat extensions, enabling you to run structured AI-assisted maintenance tasks on your codebase.

## Setup

1. Make the script executable:
   ```bash
   chmod +x scripts/routine-maintenance.sh
   ```

2. Ensure your prompt files are in `.github/prompts/` directory

## Usage

### Basic Commands

```bash
# Refactor a specific file
./scripts/routine-maintenance.sh refactor src/main.js

# Generate tests for a file
./scripts/routine-maintenance.sh test src/component.js

# Create documentation for a file or folder
./scripts/routine-maintenance.sh docs src/ --chat

# Debug a problematic file
./scripts/routine-maintenance.sh debug src/buggy.js

# Run full maintenance workflow (refactor → test → docs)
./scripts/routine-maintenance.sh full-maintenance src/feature.js
```

### Advanced Workflows

```bash
# Feature development workflow (analyze → design → implement → test → docs)
./scripts/routine-maintenance.sh workflow feature notes/new-feature.md

# Maintenance workflow
./scripts/routine-maintenance.sh workflow maintenance src/legacy.js

# Debug workflow
./scripts/routine-maintenance.sh workflow debug src/error.js
```

### Options

- `--chat`: Format output for direct paste into VS Code Chat
- `--copy`: Copy output to clipboard (macOS only)
- `--verbose`: Show detailed output information

## Integration with VS Code Chat

### Method 1: Manual (Most Reliable)
1. Run the script with your desired command and `--chat --copy` flags
2. Open VS Code Chat (Cmd+Shift+I or Cmd+I)
3. Paste (Cmd+V) - the prompt is already in your clipboard
4. The AI will process the prompt and provide the requested output
5. Apply the suggestions back to your codebase

```bash
./scripts/routine-maintenance.sh review pages/_posts/my-article.md --chat --copy
# Then paste into VS Code Chat
```

### Method 2: Semi-Automated (VS Code Integration)
Use the `vscode-integration.sh` script for streamlined workflows:

```bash
# Opens file in VS Code with prompt in clipboard
./scripts/vscode-integration.sh vscode-prompt pages/_posts/my-article.md

# Attempts to open VS Code Chat automatically
./scripts/vscode-integration.sh auto-review pages/_posts/my-article.md
```

**Note:** VS Code Chat extensions don't expose a direct CLI API, so full automation requires manual paste step.

## Example Workflow

```bash
# Prepare refactoring prompt for a component
./scripts/routine-maintenance.sh refactor src/MyComponent.js --chat --copy

# In VS Code Chat, paste the output and get refactoring suggestions
# Apply the changes, then run tests
./scripts/routine-maintenance.sh test src/MyComponent.js --chat --copy
```

## Available Prompts

The script uses these prompt files from `.github/prompts/`:

- `code-refactoring.prompt.md` - Code quality improvements
- `test-generation.prompt.md` - Automated test creation
- `documentation.prompt.md` - Documentation generation
- `debugging.prompt.md` - Issue diagnosis and fixes
- `requirements-analysis.prompt.md` - Requirements extraction
- `system-design.prompt.md` - Architecture design
- `code-implementation.prompt.md` - Code writing
- `prompt-engineering.prompt.md` - Prompt creation

## Customization

You can extend the script by:

1. Adding new prompt files to `.github/prompts/`
2. Creating new workflow types in the `cmd_workflow()` function
3. Modifying the output formatting in `format_for_chat()`

## Safety Features

- File existence validation
- Large file truncation (shows first 100 lines for files >100KB)
- Error handling for missing prompts
- Safe file content reading

This script transforms your prompt engineering into an executable, repeatable process for maintaining high-quality codebases.

## Advanced: Programmatic API Access

While VS Code Chat extensions (GitHub Copilot, etc.) don't expose a direct CLI API, here are alternatives for background automation:

### Option 1: GitHub Copilot CLI (Separate Tool)
```bash
npm install -g @githubnext/github-copilot-cli
# Use with your prompts
gh copilot suggest "your prompt here"
```

### Option 2: OpenAI API / Azure OpenAI (Direct)
Create a script that calls the AI model API directly:
```bash
# Example using curl with OpenAI API
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "your prompt"}]
  }'
```

### Option 3: VS Code Extension Development
Build a custom VS Code extension that:
1. Reads your `.github/prompts/` files
2. Provides commands to trigger workflows
3. Integrates with Chat API programmatically

See the article "Agentic Prompt Workflows in VS Code" for conceptual design.
