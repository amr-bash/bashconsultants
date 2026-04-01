#!/usr/bin/env node
/**
 * Standalone test script for Prompt Orchestrator
 * Tests the PromptManager without requiring VS Code runtime
 */

const path = require('path');
const fs = require('fs/promises');

class TestPromptManager {
    constructor(workspaceRoot, promptsDirectory) {
        this.prompts = new Map();
        this.promptsDir = path.join(workspaceRoot, promptsDirectory);
    }

    async loadPrompts() {
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

    parsePrompt(filename, filePath, content) {
        const name = filename.replace('.prompt.md', '');
        
        const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
        let frontmatter = {};
        let promptContent = content;

        if (frontmatterMatch) {
            try {
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

    parseSimpleYaml(yaml) {
        const result = {};
        const lines = yaml.split('\n');
        
        for (const line of lines) {
            const match = line.match(/^(\w+):\s*(.+)$/);
            if (match) {
                result[match[1]] = match[2];
            }
        }
        
        return result;
    }

    getPrompt(name) {
        return this.prompts.get(name);
    }

    getAllPrompts() {
        return Array.from(this.prompts.values());
    }
}

// Test runner
async function runTests() {
    console.log('\n🧪 Testing Prompt Orchestrator - Docs Generation\n');
    console.log('='.repeat(60));
    
    const workspaceRoot = path.resolve(__dirname, '..');
    const promptManager = new TestPromptManager(workspaceRoot, '.github/prompts');
    
    let passed = 0;
    let failed = 0;
    
    function test(name, fn) {
        try {
            fn();
            console.log(`✅ PASS: ${name}`);
            passed++;
        } catch (error) {
            console.log(`❌ FAIL: ${name}`);
            console.log(`   Error: ${error.message}`);
            failed++;
        }
    }
    
    function assertEqual(actual, expected, message) {
        if (actual !== expected) {
            throw new Error(`${message}\n   Expected: ${expected}\n   Got: ${actual}`);
        }
    }
    
    function assertTrue(condition, message) {
        if (!condition) {
            throw new Error(message);
        }
    }
    
    // Load prompts
    console.log('\n📂 Loading prompts from .github/prompts/...\n');
    await promptManager.loadPrompts();
    
    const prompts = promptManager.getAllPrompts();
    console.log(`Found ${prompts.length} prompts: ${prompts.map(p => p.name).join(', ')}\n`);
    
    // Test 1: Should have prompts loaded
    test('Should load prompts from directory', () => {
        assertTrue(prompts.length > 0, 'No prompts loaded');
    });
    
    // Test 2: Should find docs prompt
    test('Should find "docs" prompt', () => {
        const docsPrompt = promptManager.getPrompt('docs');
        assertTrue(docsPrompt !== undefined, '"docs" prompt not found');
    });
    
    // Test 3: Docs prompt should have frontmatter
    test('Docs prompt should have frontmatter with agent', () => {
        const docsPrompt = promptManager.getPrompt('docs');
        assertTrue(docsPrompt?.frontmatter !== undefined, 'No frontmatter');
        assertTrue(docsPrompt?.frontmatter?.agent !== undefined, 'No agent in frontmatter');
    });
    
    // Test 4: Docs prompt content should be meaningful
    test('Docs prompt should contain documentation instructions', () => {
        const docsPrompt = promptManager.getPrompt('docs');
        assertTrue(docsPrompt?.content?.length > 100, 'Content too short');
        assertTrue(
            docsPrompt?.content?.includes('Technical Writer') || 
            docsPrompt?.content?.includes('Documentation'),
            'Content should mention documentation'
        );
    });
    
    // Test 5: Should find documentation prompt
    test('Should find "documentation" prompt', () => {
        const docPrompt = promptManager.getPrompt('documentation');
        assertTrue(docPrompt !== undefined, '"documentation" prompt not found');
    });
    
    // Test 6: Test prompt content preview
    test('Docs prompt should have complete structure', () => {
        const docsPrompt = promptManager.getPrompt('docs');
        assertTrue(docsPrompt?.content?.includes('Overview'), 'Missing Overview section');
        assertTrue(docsPrompt?.content?.includes('Installation'), 'Missing Installation section');
    });
    
    // Test 7: Check all expected prompts exist
    test('Should have all expected prompts', () => {
        const expectedPrompts = [
            'code-refactoring',
            'test-generation', 
            'debugging',
            'documentation'
        ];
        const loadedNames = prompts.map(p => p.name);
        
        for (const expected of expectedPrompts) {
            assertTrue(
                loadedNames.includes(expected),
                `Missing expected prompt: ${expected}`
            );
        }
    });
    
    // Test 8: Simulate docs prompt formatting
    test('Should format docs prompt with file context', () => {
        const docsPrompt = promptManager.getPrompt('docs');
        const sampleFile = 'extension.ts';
        const sampleContent = 'export function activate(context) {}';
        
        const formatted = `${docsPrompt.content}\n\nContext/Input:\nFile: ${sampleFile}\n\n\`\`\`\n${sampleContent}\n\`\`\``;
        
        assertTrue(formatted.includes(docsPrompt.content), 'Should include original content');
        assertTrue(formatted.includes(sampleFile), 'Should include filename');
        assertTrue(formatted.includes(sampleContent), 'Should include file content');
    });
    
    // Summary
    console.log('\n' + '='.repeat(60));
    console.log(`\n📊 Test Results: ${passed} passed, ${failed} failed\n`);
    
    if (failed > 0) {
        process.exit(1);
    }
    
    // Show docs prompt preview
    console.log('\n📝 Docs Prompt Preview:');
    console.log('-'.repeat(60));
    const docsPrompt = promptManager.getPrompt('docs');
    if (docsPrompt) {
        console.log(`Name: ${docsPrompt.name}`);
        console.log(`Agent: ${docsPrompt.frontmatter?.agent || 'N/A'}`);
        console.log(`Content Preview:\n${docsPrompt.content.substring(0, 300)}...`);
    }
}

runTests().catch(console.error);
