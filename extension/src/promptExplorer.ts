import * as vscode from 'vscode';
import { PromptManager, PromptTemplate } from './promptManager';

export class PromptExplorerProvider implements vscode.TreeDataProvider<PromptItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<PromptItem | undefined | null | void> = new vscode.EventEmitter<PromptItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<PromptItem | undefined | null | void> = this._onDidChangeTreeData.event;

    constructor(private promptManager: PromptManager) {}

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: PromptItem): vscode.TreeItem {
        return element;
    }

    async getChildren(element?: PromptItem): Promise<PromptItem[]> {
        if (!element) {
            const prompts = await this.promptManager.loadPrompts();
            return prompts.map(p => new PromptItem(
                this.formatPromptName(p.name),
                p.name,
                vscode.TreeItemCollapsibleState.None,
                {
                    command: 'prompt-orchestrator.executePrompt',
                    title: 'Execute Prompt',
                    arguments: [p.name]
                }
            ));
        }
        return [];
    }

    private formatPromptName(name: string): string {
        return name
            .split('-')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }
}

export class PromptItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly promptName: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly command?: vscode.Command
    ) {
        super(label, collapsibleState);
        this.tooltip = `Execute ${label} prompt`;
        this.iconPath = new vscode.ThemeIcon('symbol-event');
    }
}
