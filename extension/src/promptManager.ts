import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs/promises';

export interface PromptTemplate {
    name: string;
    filePath: string;
    content: string;
    frontmatter?: {
        agent?: string;
        [key: string]: any;
    };
}

export class PromptManager {
    private prompts: Map<string, PromptTemplate> = new Map();
    private promptsDir: string;

    constructor(private workspaceRoot: string, promptsDirectory: string) {
        this.promptsDir = path.join(workspaceRoot, promptsDirectory);
    }

    async loadPrompts(): Promise<PromptTemplate[]> {
        this.prompts.clear();

        try {
            const files = await fs.readdir(this.promptsDir);
            const promptFiles = files.filter(f => f.endsWith('.prompt.md'));

            for (const file of promptFiles) {
                const filePath = path.join(this.promptsDir, file);
                const content = await fs.readFile(filePath, 'utf-8');
                
                const prompt = this.parsePrompt(file, filePath, content);
                this.prompts.set(prompt.name, prompt);
            }

            return Array.from(this.prompts.values());
        } catch (error) {
            console.error('Error loading prompts:', error);
            return [];
        }
    }

    private parsePrompt(filename: string, filePath: string, content: string): PromptTemplate {
        const name = filename.replace('.prompt.md', '');
        
        // Extract frontmatter
        const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
        let frontmatter = {};
        let promptContent = content;

        if (frontmatterMatch) {
            try {
                // Simple YAML parsing for frontmatter
                const yamlContent = frontmatterMatch[1];
                frontmatter = this.parseSimpleYaml(yamlContent);
                promptContent = frontmatterMatch[2];
            } catch (error) {
                console.error('Error parsing frontmatter:', error);
            }
        }

        return {
            name,
            filePath,
            content: promptContent.trim(),
            frontmatter
        };
    }

    private parseSimpleYaml(yaml: string): any {
        const result: any = {};
        const lines = yaml.split('\n');
        
        for (const line of lines) {
            const match = line.match(/^(\w+):\s*(.+)$/);
            if (match) {
                result[match[1]] = match[2];
            }
        }
        
        return result;
    }

    getPrompt(name: string): PromptTemplate | undefined {
        return this.prompts.get(name);
    }

    getAllPrompts(): PromptTemplate[] {
        return Array.from(this.prompts.values());
    }

    async formatPromptWithContext(prompt: PromptTemplate, fileUri: vscode.Uri): Promise<string> {
        try {
            const fileContent = await vscode.workspace.fs.readFile(fileUri);
            const text = Buffer.from(fileContent).toString('utf-8');
            const fileName = path.basename(fileUri.fsPath);

            return `${prompt.content}\n\nContext/Input:\nFile: ${fileName}\n\n\`\`\`\n${text}\n\`\`\``;
        } catch (error) {
            vscode.window.showErrorMessage(`Error reading file: ${error}`);
            return prompt.content;
        }
    }
}
