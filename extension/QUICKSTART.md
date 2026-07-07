# Prompt Orchestrator quickstart

Get the extension running against this repository's prompt library in about five minutes.

## 1. Install and build

```bash
cd extension
npm install
npm run compile
```

## 2. Launch the Extension Development Host

1. Open the `extension/` folder (or the repository root) in VS Code.
2. Press `F5`. A new VS Code window opens with the extension loaded.
3. In that window, open the repository root as your workspace — the extension reads prompts from `.github/prompts/` relative to the first workspace folder.

## 3. Run a command

Open the Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`) and type `Prompt Orchestrator`. Available commands:

| Command | Prompt file it runs |
| --- | --- |
| Refresh Prompts | (reloads the library) |
| Execute Prompt on File | any prompt you pick |
| Review Article | `article-review.prompt.md` |
| Refactor Code | `code-refactoring.prompt.md` |
| Generate Tests | `test-generation.prompt.md` |
| Generate Documentation | `documentation.prompt.md` |
| Debug Code | `debugging.prompt.md` |

Each command uses the active editor's file as context (or asks you to pick a file), then offers three execution methods: send to Copilot Chat, execute with the Language Model API, or copy to the clipboard.

You can also run prompts from the **Prompt Orchestrator** view in the Explorer sidebar — click any entry to execute it.

## 4. See what the extension is doing

Diagnostics go to the **Prompt Orchestrator** output channel (View → Output, then pick "Prompt Orchestrator" from the dropdown). Skipped or malformed prompt files are logged there.

## 5. Run the tests

```bash
cd extension
npm test
```

The test runner (`@vscode/test-cli`) downloads a VS Code build on first run, compiles the tests to `out/`, and executes `src/test/*.test.ts` against the real prompt library in `.github/prompts/`.

## 6. Make changes

- Edit code in `src/`, then relaunch (`F5`) or reload the development window (`Cmd+R` / `Ctrl+R`).
- `npm run watch` keeps esbuild and the TypeScript checker running as you edit.
- Before committing: `npm run lint` and `npm run compile` must pass, and any new command must be declared in both `package.json` (`contributes.commands`) and `src/extension.ts`.

## Troubleshooting

- **"Prompt not found"** — run **Refresh Prompts**, then check the output channel; the prompt file may have malformed frontmatter or a name that doesn't match. Shortcut names resolve via the alias map in `src/promptManager.ts` (`docs` → `documentation`, etc.).
- **Empty sidebar** — confirm the workspace folder contains `.github/prompts/*.prompt.md`, or point `promptOrchestrator.promptsDirectory` at the right folder in Settings.
- **No language model available** — the Language Model execution method needs GitHub Copilot; without it, the extension falls back to copying the prompt to your clipboard.
