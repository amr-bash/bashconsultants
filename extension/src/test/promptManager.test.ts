import * as assert from 'assert';
import * as path from 'path';
import { PromptManager, PromptTemplate } from '../promptManager';

suite('PromptManager Test Suite', () => {
    const workspaceRoot = path.resolve(__dirname, '../../..');
    const promptManager = new PromptManager(workspaceRoot, '.github/prompts');

    suiteSetup(async () => {
        // Load prompts before running tests
        await promptManager.loadPrompts();
    });

    test('should load prompts from .github/prompts directory', async () => {
        const prompts = promptManager.getAllPrompts();
        assert.ok(prompts.length > 0, 'Should have loaded at least one prompt');
        console.log(`Loaded ${prompts.length} prompts`);
    });

    test('should find docs prompt', () => {
        const docsPrompt = promptManager.getPrompt('docs');
        assert.ok(docsPrompt, 'Should find docs prompt');
        assert.strictEqual(docsPrompt?.name, 'docs');
        console.log('Docs prompt found:', docsPrompt?.name);
    });

    test('should find documentation prompt', () => {
        const docPrompt = promptManager.getPrompt('documentation');
        assert.ok(docPrompt, 'Should find documentation prompt');
        console.log('Documentation prompt found:', docPrompt?.name);
    });

    test('docs prompt should have frontmatter with agent', () => {
        const docsPrompt = promptManager.getPrompt('docs');
        assert.ok(docsPrompt?.frontmatter, 'Should have frontmatter');
        assert.ok(docsPrompt?.frontmatter?.agent, 'Should have agent in frontmatter');
        console.log('Agent:', docsPrompt?.frontmatter?.agent);
    });

    test('docs prompt content should contain documentation instructions', () => {
        const docsPrompt = promptManager.getPrompt('docs');
        assert.ok(docsPrompt?.content, 'Should have content');
        assert.ok(
            docsPrompt?.content.includes('Technical Writer') || 
            docsPrompt?.content.includes('Documentation'),
            'Content should mention documentation'
        );
        console.log('Content preview:', docsPrompt?.content.substring(0, 100) + '...');
    });

    test('should list all available prompts', () => {
        const prompts = promptManager.getAllPrompts();
        const promptNames = prompts.map(p => p.name);
        console.log('Available prompts:', promptNames.join(', '));
        
        // Check for expected prompts
        const expectedPrompts = ['code-refactoring', 'test-generation', 'debugging'];
        for (const expected of expectedPrompts) {
            assert.ok(
                promptNames.includes(expected),
                `Should have ${expected} prompt`
            );
        }
    });
});
