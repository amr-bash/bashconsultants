#!/usr/bin/env node
/**
 * Demo: Generate Documentation for a File
 * 
 * This script demonstrates how the Prompt Orchestrator generates
 * documentation prompts for a given file.
 */

const path = require('path');
const fs = require('fs/promises');

async function loadDocsPrompt() {
    const promptPath = path.resolve(__dirname, '..', '.github/prompts/docs.prompt.md');
    const content = await fs.readFile(promptPath, 'utf-8');
    
    // Parse frontmatter
    const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
    if (match) {
        return match[2].trim();
    }
    return content;
}

async function formatPromptForFile(promptContent, filePath) {
    const absolutePath = path.resolve(__dirname, '..', filePath);
    const fileContent = await fs.readFile(absolutePath, 'utf-8');
    const fileName = path.basename(filePath);
    
    return `${promptContent}

Context/Input:
File: ${fileName}

\`\`\`typescript
${fileContent}
\`\`\``;
}

async function main() {
    console.log('\n📚 Prompt Orchestrator - Docs Generation Demo\n');
    console.log('='.repeat(70));
    
    // File to generate docs for
    const targetFile = process.argv[2] || 'src/promptManager.ts';
    
    console.log(`\n📄 Target File: ${targetFile}\n`);
    
    try {
        // Load the docs prompt
        const docsPrompt = await loadDocsPrompt();
        
        // Format with target file
        const formattedPrompt = await formatPromptForFile(docsPrompt, targetFile);
        
        console.log('='.repeat(70));
        console.log('📝 GENERATED PROMPT (ready for VS Code Chat):');
        console.log('='.repeat(70));
        console.log(formattedPrompt);
        console.log('\n' + '='.repeat(70));
        
        // Save to file for easy copying
        const outputPath = path.resolve(__dirname, '../.generated-prompt.md');
        await fs.writeFile(outputPath, formattedPrompt);
        console.log(`\n✅ Prompt saved to: .generated-prompt.md`);
        console.log('\n💡 Usage:');
        console.log('   1. Open VS Code Chat (Cmd+Shift+I)');
        console.log('   2. Paste the generated prompt above');
        console.log('   3. Or copy from .generated-prompt.md');
        
    } catch (error) {
        console.error(`\n❌ Error: ${error.message}`);
        process.exit(1);
    }
}

main();
