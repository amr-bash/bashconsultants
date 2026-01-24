import * as vscode from 'vscode';

export class ChatIntegration {
    
    async sendToChat(promptText: string): Promise<void> {
        try {
            // Method 1: Use vscode.editorChat.start command
            await vscode.commands.executeCommand('vscode.editorChat.start');
            
            // Copy to clipboard as fallback
            await vscode.env.clipboard.writeText(promptText);
            
            vscode.window.showInformationMessage(
                'Prompt copied to clipboard. Paste into Chat panel.',
                'Open Chat'
            ).then(selection => {
                if (selection === 'Open Chat') {
                    vscode.commands.executeCommand('workbench.action.chat.open');
                }
            });
        } catch (error) {
            console.error('Error sending to chat:', error);
            
            // Fallback: just copy to clipboard
            await vscode.env.clipboard.writeText(promptText);
            vscode.window.showInformationMessage('Prompt copied to clipboard. Paste into your Chat panel.');
        }
    }

    async sendToLanguageModel(promptText: string): Promise<string | undefined> {
        try {
            // Select a chat model (GPT-4o preferred)
            const models = await vscode.lm.selectChatModels({
                vendor: 'copilot',
                family: 'gpt-4o',
            });

            if (models.length === 0) {
                vscode.window.showWarningMessage('No language models available. Using clipboard fallback.');
                await this.sendToChat(promptText);
                return undefined;
            }

            const model = models[0];
            
            // Create chat messages
            const messages = [
                vscode.LanguageModelChatMessage.User(promptText)
            ];

            // Send request
            const cancellationToken = new vscode.CancellationTokenSource().token;
            const response = await model.sendRequest(messages, {}, cancellationToken);

            // Collect response
            let fullResponse = '';
            for await (const fragment of response.text) {
                fullResponse += fragment;
            }

            return fullResponse;
        } catch (error) {
            console.error('Error with language model:', error);
            // Fallback to clipboard method
            await this.sendToChat(promptText);
            return undefined;
        }
    }

    async executePromptWithModel(promptText: string, showInEditor: boolean = true): Promise<void> {
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'Processing prompt...',
            cancellable: true
        }, async (progress, token) => {
            const response = await this.sendToLanguageModel(promptText);
            
            if (response && showInEditor) {
                // Create a new document with the response
                const doc = await vscode.workspace.openTextDocument({
                    content: response,
                    language: 'markdown'
                });
                await vscode.window.showTextDocument(doc);
            }
        });
    }
}
