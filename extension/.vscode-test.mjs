import { defineConfig } from '@vscode/test-cli';
import * as os from 'os';
import * as path from 'path';

// Keep the user-data-dir short: VS Code creates a Unix domain socket inside
// it, and macOS rejects socket paths longer than 103 characters. Deeply
// nested checkouts (e.g. git worktrees) exceed that with the default
// .vscode-test/user-data location.
const userDataDir = path.join(os.tmpdir(), 'vscode-test-prompt-orchestrator');

export default defineConfig({
  files: 'out/test/**/*.test.js',
  launchArgs: ['--user-data-dir', userDataDir],
});
