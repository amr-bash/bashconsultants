import * as assert from 'assert';
import * as path from 'path';
import { PromptManager } from '../promptManager';

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
    });

    test('should resolve the docs alias to the documentation prompt', () => {
        const docsPrompt = promptManager.getPrompt('docs');
        assert.ok(docsPrompt, 'Should resolve the "docs" alias');
        assert.strictEqual(docsPrompt?.name, 'documentation');
    });

    test('should find documentation prompt', () => {
        const docPrompt = promptManager.getPrompt('documentation');
        assert.ok(docPrompt, 'Should find documentation prompt');
    });

    test('should resolve every shortcut alias to its canonical prompt', () => {
        // Mirrors the canonical mapping in scripts/routine-maintenance.sh
        const aliases: Record<string, string> = {
            review: 'article-review',
            refactor: 'code-refactoring',
            test: 'test-generation',
            docs: 'documentation',
            debug: 'debugging'
        };
        for (const [alias, canonical] of Object.entries(aliases)) {
            const prompt = promptManager.getPrompt(alias);
            assert.ok(prompt, `Alias "${alias}" should resolve to a prompt`);
            assert.strictEqual(
                prompt?.name,
                canonical,
                `Alias "${alias}" should resolve to "${canonical}"`
            );
        }
    });

    test('documentation prompt should have canonical frontmatter', () => {
        const docsPrompt = promptManager.getPrompt('docs');
        assert.ok(docsPrompt?.frontmatter, 'Should have frontmatter');
        assert.strictEqual(
            docsPrompt?.frontmatter?.mode,
            'agent',
            'Should have mode: agent per .github/FRONTMATTER.md'
        );
        assert.ok(
            typeof docsPrompt?.frontmatter?.description === 'string' &&
                docsPrompt.frontmatter.description.length > 0,
            'Should have a non-empty description'
        );
    });

    test('docs prompt content should contain documentation instructions', () => {
        const docsPrompt = promptManager.getPrompt('docs');
        assert.ok(docsPrompt?.content, 'Should have content');
        assert.ok(
            docsPrompt?.content.includes('Technical Writer') ||
            docsPrompt?.content.includes('Documentation'),
            'Content should mention documentation'
        );
        assert.ok(
            !docsPrompt?.content.startsWith('---'),
            'Frontmatter should be stripped from content'
        );
    });

    test('should list all available prompts', () => {
        const prompts = promptManager.getAllPrompts();
        const promptNames = prompts.map(p => p.name);

        // Check for expected prompts
        const expectedPrompts = ['code-refactoring', 'test-generation', 'debugging'];
        for (const expected of expectedPrompts) {
            assert.ok(
                promptNames.includes(expected),
                `Should have ${expected} prompt`
            );
        }
    });

    test('should return an empty list for a missing prompts directory', async () => {
        const missing = new PromptManager(workspaceRoot, 'does/not/exist');
        const prompts = await missing.loadPrompts();
        assert.deepStrictEqual(prompts, [], 'Missing directory should yield no prompts, not throw');
    });
});
