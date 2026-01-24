#!/bin/bash

# VS Code CLI Integration Script
# This script attempts to interact with VS Code's AI capabilities through available APIs

set -e

WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROMPTS_DIR=".github/prompts"

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

usage() {
    echo "Usage: $0 [command] [file] [options]"
    echo ""
    echo "Commands:"
    echo "  auto-review [file]       - Open file in VS Code and trigger chat with prompt"
    echo "  vscode-prompt [file]     - Open VS Code with prompt in clipboard"
    echo "  api-submit [file]        - Submit via VS Code API (experimental)"
    echo ""
    echo "Options:"
    echo "  --wait                   - Wait for VS Code to process"
    echo "  --output [file]          - Save response to file"
}

# Function to open VS Code with file and copy prompt to clipboard
cmd_vscode_prompt() {
    local file="$1"
    
    echo -e "${BLUE}Opening $file in VS Code with prompt ready...${NC}"
    
    # Generate the prompt
    local prompt_output=$("$WORKSPACE_ROOT/scripts/routine-maintenance.sh" review "$file" --chat)
    
    # Copy to clipboard
    echo "$prompt_output" | pbcopy
    echo -e "${GREEN}✓ Prompt copied to clipboard${NC}"
    
    # Open file in VS Code
    code "$file"
    
    echo -e "${YELLOW}Next steps:${NC}"
    echo "1. In VS Code, open Chat (Cmd+Shift+I or Cmd+I)"
    echo "2. Paste the prompt (Cmd+V)"
    echo "3. Press Enter to submit"
}

# Function to use VS Code CLI to open chat
cmd_auto_review() {
    local file="$1"
    
    echo -e "${BLUE}Attempting to open VS Code Chat...${NC}"
    
    # Generate the prompt
    local prompt_output=$("$WORKSPACE_ROOT/scripts/routine-maintenance.sh" review "$file" --chat)
    
    # Copy to clipboard
    echo "$prompt_output" | pbcopy
    
    # Open the file in VS Code
    code "$file"
    
    # Try to open chat panel using VS Code CLI (this may not work with all extensions)
    # GitHub Copilot Chat command ID: github.copilot.interactiveEditor.explain
    code --wait "$file" 2>/dev/null || true
    
    echo -e "${GREEN}✓ File opened in VS Code${NC}"
    echo -e "${YELLOW}Prompt is in your clipboard - paste it into the Chat panel${NC}"
}

# Function to attempt API submission (experimental)
cmd_api_submit() {
    local file="$1"
    
    echo -e "${BLUE}Experimental: Attempting API submission...${NC}"
    
    # Check if GitHub Copilot CLI is available
    if command -v github-copilot &> /dev/null; then
        local prompt_output=$("$WORKSPACE_ROOT/scripts/routine-maintenance.sh" review "$file" --chat)
        echo "$prompt_output" | github-copilot
    else
        echo -e "${YELLOW}GitHub Copilot CLI not found${NC}"
        echo "You can install it with: npm install -g @githubnext/github-copilot-cli"
        echo ""
        echo -e "${BLUE}Alternative: Using VS Code API...${NC}"
        
        # Generate prompt and save to temp file
        local prompt_output=$("$WORKSPACE_ROOT/scripts/routine-maintenance.sh" review "$file" --chat)
        local temp_file="/tmp/vscode_prompt_$$.txt"
        echo "$prompt_output" > "$temp_file"
        
        echo -e "${GREEN}✓ Prompt saved to $temp_file${NC}"
        echo -e "${YELLOW}You can process this prompt through VS Code extensions${NC}"
    fi
}

# Main
main() {
    if [[ $# -lt 1 ]]; then
        usage
        exit 1
    fi
    
    local command="$1"
    shift
    
    case "$command" in
        vscode-prompt)
            [[ $# -lt 1 ]] && { echo "Error: vscode-prompt requires a file argument"; exit 1; }
            cmd_vscode_prompt "$1"
            ;;
        auto-review)
            [[ $# -lt 1 ]] && { echo "Error: auto-review requires a file argument"; exit 1; }
            cmd_auto_review "$1"
            ;;
        api-submit)
            [[ $# -lt 1 ]] && { echo "Error: api-submit requires a file argument"; exit 1; }
            cmd_api_submit "$1"
            ;;
        *)
            echo "Error: Unknown command '$command'"
            usage
            exit 1
            ;;
    esac
}

main "$@"
