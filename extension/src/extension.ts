import * as vscode from 'vscode';
import { PromptManager } from './promptManager';
import { PromptExplorerProvider } from './promptExplorer';
import { ChatIntegration } from './chatIntegration';

export function activate(context: vscode.ExtensionContext) {
	console.log('Prompt Orchestrator is now active');

	// Get workspace root
	const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
	if (!workspaceFolder) {
		vscode.window.showWarningMessage('Prompt Orchestrator requires an open workspace');
		return;
	}

	// Get configuration
	const config = vscode.workspace.getConfiguration('promptOrchestrator');
	const promptsDirectory = config.get<string>('promptsDirectory', '.github/prompts');

	// Initialize managers
	const promptManager = new PromptManager(workspaceFolder.uri.fsPath, promptsDirectory);
	const chatIntegration = new ChatIntegration();
	const promptExplorer = new PromptExplorerProvider(promptManager);

	// Register tree view
	const treeView = vscode.window.createTreeView('promptOrchestratorExplorer', {
		treeDataProvider: promptExplorer
	});

	// Register commands
	context.subscriptions.push(
		vscode.commands.registerCommand('prompt-orchestrator.refreshPrompts', async () => {
			await promptManager.loadPrompts();
			promptExplorer.refresh();
			vscode.window.showInformationMessage('Prompts refreshed');
		})
	);

	context.subscriptions.push(
		vscode.commands.registerCommand('prompt-orchestrator.executePrompt', async (promptName?: string) => {
			// If no prompt name provided, show quick pick
			if (!promptName) {
				const prompts = promptManager.getAllPrompts();
				if (prompts.length === 0) {
					await promptManager.loadPrompts();
				}
				
				const items = promptManager.getAllPrompts().map(p => ({
					label: p.name,
					description: p.frontmatter?.agent || ''
				}));

				const selected = await vscode.window.showQuickPick(items, {
					placeHolder: 'Select a prompt to execute'
				});

				if (!selected) {
					return;
				}
				promptName = selected.label;
			}

			const prompt = promptManager.getPrompt(promptName);
			if (!prompt) {
				vscode.window.showErrorMessage(`Prompt "${promptName}" not found`);
				return;
			}

			// Get active editor or ask user to select file
			const editor = vscode.window.activeTextEditor;
			let fileUri: vscode.Uri | undefined;

			if (editor) {
				fileUri = editor.document.uri;
			} else {
				const files = await vscode.window.showOpenDialog({
					canSelectFiles: true,
					canSelectMany: false,
					openLabel: 'Select file for prompt context'
				});
				fileUri = files?.[0];
			}

			if (!fileUri) {
				vscode.window.showWarningMessage('No file selected');
				return;
			}

			// Format prompt with context
			const formattedPrompt = await promptManager.formatPromptWithContext(prompt, fileUri);

			// Ask user for execution method
			const method = await vscode.window.showQuickPick([
				{ label: 'Send to Chat (Copilot)', value: 'chat' },
				{ label: 'Execute with Language Model', value: 'model' },
				{ label: 'Copy to Clipboard', value: 'clipboard' }
			], {
				placeHolder: 'How do you want to execute this prompt?'
			});

			if (!method) {
				return;
			}

			switch (method.value) {
				case 'chat':
					await chatIntegration.sendToChat(formattedPrompt);
					break;
				case 'model':
					await chatIntegration.executePromptWithModel(formattedPrompt);
					break;
				case 'clipboard':
					await vscode.env.clipboard.writeText(formattedPrompt);
					vscode.window.showInformationMessage('Prompt copied to clipboard');
					break;
			}
		})
	);

	// Register specific prompt commands
	const promptCommands = ['review', 'refactor', 'test', 'docs', 'debug'];
	for (const cmd of promptCommands) {
		context.subscriptions.push(
			vscode.commands.registerCommand(`prompt-orchestrator.${cmd}`, async () => {
				await vscode.commands.executeCommand('prompt-orchestrator.executePrompt', cmd);
			})
		);
	}

	// Auto-load prompts on activation
	promptManager.loadPrompts().then(() => {
		promptExplorer.refresh();
	});

	context.subscriptions.push(treeView);
}

export function deactivate() {}
