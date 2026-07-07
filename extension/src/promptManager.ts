import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs/promises';
import * as yaml from 'js-yaml';

/**
 * Shortcut aliases -> canonical prompt filenames (without `.prompt.md`).
 * Mirrors the canonical mapping in `scripts/routine-maintenance.sh`.
 */
const PROMPT_ALIASES: Record<string, string> = {
    review: 'article-review',
    refactor: 'code-refactoring',
    test: 'test-generation',
    docs: 'documentation',
    debug: 'debugging'
};

/**
 * Canonical `.prompt.md` frontmatter per `.github/FRONTMATTER.md`:
 * `mode`, `description`, optional `tools`, `date`, `lastmod`.
 */
export interface PromptFrontmatter {
    mode?: string;
    description?: string;
    tools?: string[];
    date?: string | Date;
    lastmod?: string | Date;
    [key: string]: unknown;
}

export interface PromptTemplate {
    name: string;
    filePath: string;
    content: string;
    frontmatter?: PromptFrontmatter;
}

export class PromptManager {
    private prompts: Map<string, PromptTemplate> = new Map();
    private promptsDir: string;

    constructor(
        private workspaceRoot: string,
        promptsDirectory: string,
        private output?: vscode.OutputChannel
    ) {
        this.promptsDir = path.join(workspaceRoot, promptsDirectory);
    }

    async loadPrompts(): Promise<PromptTemplate[]> {
        this.prompts.clear();

        let files: string[];
        try {
            files = await fs.readdir(this.promptsDir);
        } catch (error) {
            this.log(`Could not read prompts directory "${this.promptsDir}": ${error}`);
            return [];
        }

        const promptFiles = files.filter(f => f.endsWith('.prompt.md'));

        for (const file of promptFiles) {
            const filePath = path.join(this.promptsDir, file);
            try {
                const content = await fs.readFile(filePath, 'utf-8');
                const prompt = this.parsePrompt(file, filePath, content);
                this.prompts.set(prompt.name, prompt);
            } catch (error) {
                // Skip unreadable files; never throw during activation.
                this.log(`Skipping unreadable prompt file "${file}": ${error}`);
            }
        }

        return Array.from(this.prompts.values());
    }

    private parsePrompt(filename: string, filePath: string, content: string): PromptTemplate {
        const name = filename.replace('.prompt.md', '');

        // Extract frontmatter delimited by `---` lines.
        const frontmatterMatch = content.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/);
        let frontmatter: PromptFrontmatter = {};
        let promptContent = content;

        if (frontmatterMatch) {
            promptContent = frontmatterMatch[2];
            try {
                const parsed = yaml.load(frontmatterMatch[1]);
                if (parsed && typeof parsed === 'object' && !Array.isArray(parsed)) {
                    frontmatter = parsed as PromptFrontmatter;
                }
            } catch (error) {
                // Malformed frontmatter: keep the body, log, and continue.
                this.log(`Malformed frontmatter in "${filename}": ${error}`);
            }
        }

        return {
            name,
            filePath,
            content: promptContent.trim(),
            frontmatter
        };
    }

    getPrompt(name: string): PromptTemplate | undefined {
        const direct = this.prompts.get(name);
        if (direct) {
            return direct;
        }
        const alias = PROMPT_ALIASES[name];
        return alias ? this.prompts.get(alias) : undefined;
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

    private log(message: string): void {
        this.output?.appendLine(`[PromptManager] ${message}`);
    }
}
